# The "Sugar Trap" Market Gap Analysis

## A. The Executive Summary

An analysis of 109,624 cleaned Open Food Facts products across five major snack categories reveals a clear "Blue Ocean" opportunity in the **Bars** category. Despite consumer expectations that bars are a health-forward, protein-driven product, only **5.6%** of Bar products currently combine high protein (≥10g/100g) with low sugar (<5g/100g) — the widest gap of any category analyzed, ahead of Chips & Savory Snacks (6.4%), Cookies & Biscuits (8.7%), and Cereal & Granola (19.5%). A deeper investigation into ingredient drivers found that soy — while the most commonly cited ingredient in high-protein products (1,992 mentions vs. 471 for whey and 313 for peanut) — does **not** actually correlate with higher average protein content, suggesting the market is under-leveraging deliberate protein fortification in favor of soy as a general-purpose additive. We recommend Helix's client target a Bar-format product engineered specifically around a genuinely high-protein, low-sugar nutritional profile, rather than relying on soy inclusion alone as a health signal.

## B. Project Links

- **Notebook:** https://colab.research.google.com/drive/1uvoiWnd2vuMaUa40oXHaYoJclxwauX6m?usp=sharing
- **Dashboard:** https://the-market-gap-analysis-d2rg3as7rkw5cwhsbidbdj.streamlit.app
- **Presentation:** https://docs.google.com/presentation/d/1eJxGRqd6bVfRlzM0h87LgZOnWfcdwNwr/edit?usp=sharing&ouid=114702118757669919978&rtpof=true&sd=true

## C. Technical Explanation

**Data Cleaning:** We loaded a 500,000-row subset of the Open Food Facts CSV export (tab-separated), keeping only the columns needed for analysis. Rows missing `product_name`, `sugars_100g`, or `proteins_100g` were dropped, and any nutrient value outside the biologically valid 0–100g-per-100g range was filtered out. This reduced the working dataset from 500,000 to 109,624 usable rows.

Products were bucketed into five high-level categories (Cookies & Biscuits, Chips & Savory Snacks, Bars, Cereal & Granola, Candy & Confectionery) via keyword matching against the `categories_tags` field — the comma-separated string is explicitly parsed into a list of individual tags before matching. All unmatched products are grouped as "Other" and excluded from the core nutrient-matrix analysis to avoid noise.

**Candidate's Choice:** After identifying soy as the most frequently mentioned ingredient in high-protein products, we ran a direct comparison of soy-containing vs. non-soy products across the full cleaned dataset. This revealed that soy-containing products do *not* have higher average protein (7.95g vs. 8.33g/100g) and actually trend slightly higher in sugar (14.39g vs. 12.62g/100g) than non-soy products. We added this analysis because it directly challenges an assumption a client might otherwise make from the ingredient-frequency data alone — that "soy" on a label signals a protein-forward product — and instead shows soy's prevalence (particularly in Bars at 50% and Cookies & Biscuits at 48%) more likely reflects its use as a common additive (e.g. soy lecithin, soybean oil) rather than intentional fortification. This reframes the R&D recommendation: differentiation should focus on actual nutrient content, not the presence of any specific protein-associated ingredient.

**Why these thresholds?** We used ≥10g protein and <5g sugar per 100g as the "healthy" bar — a reasonable floor/ceiling for a product to credibly market itself as high-protein and low-sugar. These thresholds are not fixed: the dashboard's sidebar sliders let you redefine them and see the recommended category update live, so the analysis is stress-testable rather than a single fixed claim.

## D. How to Reproduce This Analysis

**View the results (no setup required):**
- Open the notebook link above (read-only, runs entirely in Google Colab)
- Open the dashboard link above (live, interactive, no installation needed)

**Run it yourself:**
1. Open the notebook in [Google Colab](https://colab.research.google.com) via the link above, or upload the `.ipynb` file from this repo
2. Run all cells top to bottom (**Runtime → Run all**) — the notebook downloads its own data via `wget`, so no manual file setup is needed
3. To run the dashboard locally instead of viewing the deployed version:
   ```bash
   git clone https://github.com/Cutelyn19/The-Market-Gap-Analysis.git
   cd The-Market-Gap-Analysis
   pip install -r requirements.txt
   streamlit run app.py
   ```
   The dashboard expects `cleaned_snacks.csv` in the same folder (already included in this repo).

**Data source:** [Open Food Facts](https://world.openfoodfacts.org/data) (CSV export, tab-separated). We use a 500,000-row subset rather than the full 3GB+ dataset, filtered down to 109,624 rows after cleaning.

## E. Next Steps

With more time or data, we would extend this analysis with:
- **Predictive recipe modeling** — suggest candidate formulations for R&D based on patterns in existing high-protein, low-sugar products
- **Real-time price data** — pair nutrient gaps with price-per-100g to confirm commercial viability, not just nutritional under-service
- **Geographic breakdown** — Open Food Facts includes country-level data; regional taste and regulatory differences could refine launch strategy
- **Brand-level competitive analysis** — identify which specific brands already occupy the "healthy Bars" niche
- **Ingredient cost modeling** — estimate whether the target nutrient profile is achievable within a realistic COGS budget

---
