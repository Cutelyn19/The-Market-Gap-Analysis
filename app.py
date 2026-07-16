import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="The Sugar Trap: Market Gap Analysis", layout="wide")

# =========================================================
# Data loading
# Expects 'cleaned_snacks.csv' in the same repo, exported from
# the notebook via: clean.to_csv('cleaned_snacks.csv', index=False)
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_snacks.csv")

df = load_data()
df = df[df["primary_category"] != "Other"]  # exclude uncategorized products from analysis

st.title("The 'Sugar Trap': Snack Market Gap Analysis")
st.caption("Prepared for Helix CPG Partners — identifying under-served healthy snacking categories")

# =========================================================
# Sidebar: filters + actionable thresholds
# =========================================================
st.sidebar.header("Filters")
categories = sorted(df["primary_category"].dropna().unique())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

sugar_max = st.sidebar.slider("Max sugar shown (g/100g)", 0, 100, 100)
protein_min = st.sidebar.slider("Min protein shown (g/100g)", 0, 50, 0)

st.sidebar.divider()
st.sidebar.subheader("Opportunity thresholds")
st.sidebar.caption("Drag to redefine what counts as 'healthy' — the insight below updates live.")
protein_threshold = st.sidebar.slider("High protein \u2265 (g/100g)", 1, 30, 10)
sugar_threshold = st.sidebar.slider("Low sugar < (g/100g)", 1, 30, 5)

filtered = df[
    df["primary_category"].isin(selected_categories)
    & (df["sugars_100g"] <= sugar_max)
    & (df["proteins_100g"] >= protein_min)
]

st.sidebar.metric("Products shown", f"{len(filtered):,}")

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    "Download filtered data (CSV)", data=csv_bytes,
    file_name="filtered_snacks.csv", mime="text/csv"
)

tab_overview, tab_matrix, tab_opportunity, tab_ingredients, tab_next = st.tabs(
    ["Overview", "Nutrient Matrix", "Category Opportunity", "Ingredient Deep Dive", "Next Steps"]
)

# =========================================================
# Tab: Overview — the business story, told up front
# =========================================================
with tab_overview:
    st.subheader("The Business Story")
    st.markdown(
        """
        Our client — a global snack manufacturer — wants to launch a **Healthy Snacking** line but
        suspects the shelf is oversaturated with sugary treats. This dashboard answers one question:

        > **"Where is the Blue Ocean in the snack aisle?"** — a product category where consumer demand
        > for health (high protein, low sugar) is currently under-served by the market.

        We analyzed **109,624 cleaned products** from Open Food Facts across five snack categories, then
        measured what share of each category actually delivers on a genuinely healthy nutrient profile.
        """
    )

    st.subheader("Why These Thresholds?")
    st.markdown(
        """
        The default opportunity thresholds — **\u226510g protein** and **<5g sugar** per 100g — reflect a
        reasonable, defensible bar for a product to credibly market itself as "high protein" and
        "low sugar" under common food-labeling conventions. These aren't fixed: use the sliders in the
        sidebar to test tighter or looser definitions and see whether the recommended category changes.
        """
    )

    st.subheader("Why This Matters: Soy \u2260 Protein")
    st.info(
        "**Our core discovery:** Soy is the most common ingredient in high-protein products "
        "(1,992 mentions vs. 471 for whey and 313 for peanut) — but soy-containing products do "
        "**not** actually have higher average protein than non-soy products (7.95g vs. 8.33g/100g), "
        "and trend slightly *higher* in sugar. Soy's prevalence reflects common additive use "
        "(lecithin, oil), not deliberate fortification. See the **Ingredient Deep Dive** tab for the full analysis."
    )

    st.subheader("How We Handled Data Quality")
    st.markdown(
        """
        Open Food Facts is crowdsourced, so missing and erroneous values are common. We dropped rows
        missing `product_name`, `sugars_100g`, or `proteins_100g`, and filtered out biologically
        impossible values (anything outside 0–100g per 100g of product). This reduced our working
        dataset from 500,000 raw rows to 109,624 usable rows.
        """
    )

# =========================================================
# Tab: Nutrient Matrix — Story 3 (scatter + labeled empty quadrant)
# =========================================================
with tab_matrix:
    st.subheader("Nutrient Matrix: Sugar vs Protein")
    fig = px.scatter(
        filtered,
        x="sugars_100g",
        y="proteins_100g",
        color="primary_category",
        opacity=0.5,
        hover_name="product_name",
        labels={
            "sugars_100g": "Sugar (g per 100g)",
            "proteins_100g": "Protein (g per 100g)",
            "primary_category": "Category",
        },
        height=550,
    )
    fig.add_vline(x=sugar_threshold, line_dash="dash", line_color="gray")
    fig.add_hline(y=protein_threshold, line_dash="dash", line_color="gray")

    # Explicit "Empty Quadrant" label directly on the chart (Story 3 key visual requirement)
    fig.add_annotation(
        x=sugar_threshold / 2,
        y=min(95, filtered["proteins_100g"].max() if len(filtered) else 95),
        text="Empty Quadrant<br>(High Protein, Low Sugar)",
        showarrow=False,
        font=dict(size=12, color="gray"),
        align="center",
        bgcolor="rgba(255,255,255,0.7)",
    )

    st.plotly_chart(fig, width="stretch")
    st.caption(
        f"Dashed lines and the annotated box mark the current opportunity thresholds: "
        f"\u2265{protein_threshold}g protein and <{sugar_threshold}g sugar per 100g. "
        "Adjust them in the sidebar to explore different definitions of the gap."
    )

# =========================================================
# Tab: Category Opportunity — Story 4 (Key Insight box, live-computed)
# =========================================================
with tab_opportunity:
    st.subheader("Which category has the biggest gap?")

    opp = df[df["primary_category"].isin(selected_categories)].assign(
        meets_threshold=(df["proteins_100g"] >= protein_threshold)
        & (df["sugars_100g"] < sugar_threshold)
    )
    summary = (
        opp.groupby("primary_category")["meets_threshold"]
        .agg(share="mean", count="size")
        .reset_index()
        .sort_values("share")
    )
    summary["share_pct"] = (summary["share"] * 100).round(1)

    bar_fig = px.bar(
        summary,
        x="primary_category",
        y="share_pct",
        text="share_pct",
        labels={"primary_category": "Category", "share_pct": "% meeting threshold"},
        height=420,
    )
    bar_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(bar_fig, width="stretch")

    top = summary.iloc[0]
    st.subheader("Key Insight")
    st.info(
        f"Based on the data, the biggest market opportunity is in "
        f"**{top['primary_category']}**, specifically targeting products with "
        f"**{protein_threshold}g** of protein and less than **{sugar_threshold}g** of sugar. "
        f"Only **{top['share_pct']}%** of {top['primary_category']} products "
        f"(out of {int(top['count']):,} total) currently meet this bar — the widest gap "
        f"of any category shown."
    )
    st.caption(
        "This updates automatically as you move the threshold sliders in the sidebar — "
        "try tightening or loosening the definition of 'healthy' to see if the recommended "
        "category changes."
    )

# =========================================================
# Tab: Ingredient Deep Dive — Bonus + Candidate's Choice
# =========================================================
with tab_ingredients:
    st.subheader("Hidden Gem: Top Protein Sources in High-Protein Products")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            """
            | Source | Mentions |
            |---|---|
            | Soy | 1,992 |
            | Whey | 471 |
            | Peanut | 313 |
            """
        )
    with col2:
        st.caption(
            "Soy appears far more often than any other protein source in ingredient lists "
            "for high-protein products — but the comparison below complicates that story."
        )

    st.subheader("Candidate's Choice: Does Soy Actually Drive Protein Content?")
    st.markdown(
        """
        A closer look complicates the "soy = protein" assumption above:

        | Metric | Soy-containing products | Non-soy products |
        |---|---|---|
        | Avg. protein (g/100g) | 7.95 | 8.33 |
        | Avg. sugar (g/100g) | 14.39 | 12.62 |

        Soy-containing products do **not** have higher average protein than non-soy products —
        and trend slightly *higher* in sugar. Soy is most common in **Bars (50%)** and
        **Cookies & Biscuits (48%)**, suggesting its prevalence reflects common additives
        (soy lecithin, soybean oil) rather than deliberate protein fortification.

        **Why this matters for R&D:** simply listing "soy" is not a protein-differentiator.
        The real opportunity lies in products that combine genuinely high protein with low sugar,
        regardless of the specific protein source used.
        """
    )

# =========================================================
# Tab: Next Steps
# =========================================================
with tab_next:
    st.subheader("What We'd Add With More Time or Data")
    st.markdown(
        """
        - **Predictive recipe modeling** — use the nutrient/ingredient patterns of existing
          high-protein, low-sugar products to suggest candidate formulations for R&D to test.
        - **Real-time price data** — pair nutrient gaps with price-per-100g to find opportunities
          that are not just under-served but also commercially viable at a competitive price point.
        - **Geographic breakdown** — Open Food Facts includes country-level data; regional taste
          and regulatory differences could refine where to launch first.
        - **Brand-level competitive analysis** — identify which specific brands already occupy the
          "healthy Bars" niche, to size up direct competition rather than just the category gap.
        - **Ingredient cost modeling** — estimate whether hitting the target protein/sugar profile
          is achievable within a realistic COGS budget for a mass-market snack.
        """
    )

st.divider()
st.caption("Data source: Open Food Facts (openfoodfacts.org)")
