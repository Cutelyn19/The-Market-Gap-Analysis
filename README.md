# The "Sugar Trap" Market Gap Analysis

## A. The Executive Summary

An analysis of 109,624 cleaned Open Food Facts products across five major snack categories reveals a clear "Blue Ocean" opportunity in the **Bars** category. Despite consumer expectations that bars are a health-forward, protein-driven product, only **5.6%** of Bar products currently combine high protein (≥10g/100g) with low sugar (<5g/100g) — the widest gap of any category analyzed, ahead of Chips & Savory Snacks (6.4%), Cookies & Biscuits (8.7%), and Cereal & Granola (19.5%). A deeper investigation into ingredient drivers found that soy — while the most commonly cited ingredient in high-protein products (1,992 mentions vs. 471 for whey and 313 for peanut) — does **not** actually correlate with higher average protein content, suggesting the market is under-leveraging deliberate protein fortification in favor of soy as a general-purpose additive. We recommend Helix's client target a Bar-format product engineered specifically around a genuinely high-protein, low-sugar nutritional profile, rather than relying on soy inclusion alone as a health signal.

## B. Project Links

- **Notebook:** [insert your Colab share link here — confirm "Anyone with the link can view" is enabled]
- **Dashboard:** https://the-market-gap-analysis-d2rg3as7rkw5cwhsbidbdj.streamlit.app
- **Presentation:** [insert your slide deck link here] (Optional video walkthrough: [insert YouTube link if applicable])

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

# Project Brief: The "Sugar Trap" Market Gap Analysis

**Client:** Helix CPG Partners (Strategic Food & Beverage Consultancy)
**Deliverable:** Interactive Dashboard, Code Notebook & Insight Presentation

---

## 1. Business Context
**Helix CPG Partners** advises major food manufacturers on new product development. Our newest client, a global snack manufacturer, wants to launch a "Healthy Snacking" line. They believe the market is oversaturated with sugary treats, but they lack the data to prove where the specific gaps are.

They have hired us to answer one question: **"Where is the 'Blue Ocean' in the snack aisle?"**

Specifically, they are looking for product categories that are currently under-served—areas where consumer demand for health (e.g., High Protein, High Fiber) is not being met by current product offerings (which are mostly High Sugar, High Fat).

## 2. The Data
You will use the **Open Food Facts** dataset, a free, open, and massive database of food products from around the world.

* **Source:** [Open Food Facts Data](https://world.openfoodfacts.org/data)
* **Format:** CSV (Comma Separated Values)
* **Warning:** The full dataset is massive (over 3GB). You are **not** expected to process the entire file. You should filter the data early or work with a manageable subset (e.g., the first 500,000 rows or specific categories).

## 3. Tooling Requirements
You have the flexibility to choose your development environment:

* **Option A (Recommended):** Use a cloud-hosted notebook like **Google Colab**, or **Deepnote**, etc.
* **Option B:** Use a local **Jupyter Notebook** or **VS Code**.
    * *Condition:* If you choose this, you must ensure your code is reproducible. Do not reference local file paths (e.g., `C:/Downloads/...`). Assume the dataset is in the same folder as your notebook.
* **Dashboarding:** The final output must be a **publicly accessible link** (e.g., Tableau Public, Google Looker Studio, Streamlit Cloud, or PowerBI Web).

---

## 4. User Stories & Acceptance Criteria

### Story 1: Data Ingestion & "The Clean Up"
**As a** Strategy Director,
**I want** a clean dataset that removes products with erroneous nutritional information,
**So that** my analysis is not skewed by bad data entry.

* **Acceptance Criteria:**
    * Handle missing values: Decide what to do with rows that have `null` or empty `sugars_100g`, `proteins_100g`, or `product_name`.
    * Handle outliers: Filter out biologically impossible values.
    * **Deliverable:** A cleaned Pandas DataFrame or SQL table export.

### Story 2: The Category Wrangler
**As a** Product Manager,
**I want** to group products into readable high-level categories,
**So that** I don't have to look at 10,000 unique, messy tags like `en:chocolate-chip-cookies-with-nuts`.

* **Acceptance Criteria:**
    * The `categories_tags` column is a comma-separated string (e.g., `en:snacks, en:sweet-snacks, en:biscuits`). You must parse this string.
    * Create a logic to assign a "Primary Category" to each product based on keywords.
    * Create at least 5 distinct high-level buckets.

### Story 3: The "Nutrient Matrix" Visualization
**As a** Marketing Lead,
**I want** to see a Scatter Plot comparing Sugar (X-axis) vs. Protein (Y-axis) for different categories,
**So that** I can visually spot where the products are clustered.

* **Acceptance Criteria:**
    * Create a dashboard (PowerBI, Tableau, Streamlit, or Python-based charts) displaying this relationship.
    * Allow the user to filter the chart by the "High Level Categories" you created in Story 2.
    * **Key Visual:** Identify the "Empty Quadrant" (e.g., High Protein + Low Sugar).

### Story 4: The Recommendation
**As a** Client,
**I want** a clear text recommendation on what product we should build,
**So that** I can take this to the R&D team.

* **Acceptance Criteria:**
    * On the dashboard, include a "Key Insight" box.
    * Complete this sentence: *"Based on the data, the biggest market opportunity is in [Category Name], specifically targeting products with [X]g of protein and less than [Y]g of sugar."*

---

## 5. Bonus User Story: The "Hidden Gem"
**As a** Health Conscious Consumer,
**I want** to know which specific ingredients are driving the high protein content in the "good" products,
**So that** I can replicate this in our new recipe.

* **Acceptance Criteria:**
    * Analyze the `ingredients_text` column for products in your "High Protein" cluster.
    * Extract and list the Top 3 most common protein sources (e.g., "Whey", "Peanuts", "Soy").

---

## 6. The "Candidate's Choice" Challenge
**As a** Creative Analyst,
**I want** to add one additional feature or analysis to this project that I believe provides massive value,
**So that** I can show off my business acumen.

* **Instructions:**
    * Add one more chart, filter, or metric that wasn't asked for.
    * Explain **why** you added it.
    * **There is no wrong answer, but you must justify your choice.**

---

## 7. Submission Guidelines
Please edit this `README.md` file in your forked repository to include the following three sections at the top:

### A. The Executive Summary
* A 3-5 sentence summary of your findings.

### B. Project Links
* **Link to Notebook:** (e.g., Google Colab, etc.). *Ensure sharing permissions are set to "Anyone with the link can view".*
* **Link to Dashboard:** (e.g., Tableau Public / Power BI Web, etc.).
* **Link to Presentation:** A link to a short slide deck (PDF, PPT) AND (Optional) a 2-minute video walkthrough (YouTube) explaining your results.

### C. Technical Explanation
* Briefly explain how you handled the "Data Cleaning".
* Explain your "Candidate's Choice" addition.

**Important Note on Code Submission:**
* Upload your `.ipynb` notebook file to the repo.
* **Crucial:** Also upload an **HTML or PDF export** of your notebook so we can see your charts even if GitHub fails to render the notebook code.
* Once you are ready, please fill out the [Official Submission Form Here](https://forms.office.com/e/heitZ9PP7y) with your links
