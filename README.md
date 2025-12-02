# Data Analyst (Sales Insights)

A compact project that showcases how I explore a messy sales file, engineer metrics, and surface business-ready insights for Daxwell. The dataset is synthetic but modeled after a mid-market distributor with multiple channels and regions.

## What this shows
- Cleans and enriches transactional data (pricing, discounts, margin)
- Builds quick visuals to explain channel and category performance
- Produces a concise, stakeholder-friendly summary

## File structure
- `data/daxwell_sales.csv` — synthetic 240-row sales dataset with regions, channels, discounts, and costs
- `src/analyze.py` — main analysis script that builds metrics, charts, and a summary
- `reports/summary.md` — generated one-page readout with key metrics and figure links
- `reports/figures/` — saved charts
- `requirements.txt` — minimal Python dependencies

## How to run
```bash
python -m venv .venv
.venv\Scripts\activate            # use source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python src/analyze.py             # prints and writes summary + figures
```

## Data dictionary (key fields)
- `order_date` — transactional date
- `region` / `city` — territory identifiers
- `channel` — Retail, Wholesale, or Ecommerce
- `customer_segment` — Consumer, Small Business, Enterprise
- `product_category` / `product` — category and SKU name
- `units_sold`, `unit_price`, `unit_cost`, `discount_rate`
- `revenue`, `cost`, `gross_margin`, `margin_rate` (engineered in `analyze.py`)

## Notes for the reviewer
- Top-line margin holds at ~39% with Ecommerce leading revenue; Packaging is the strongest category.
- The code is intentionally short and readable to mirror day-one ramp-up work: load, profile, visualize, communicate.
- Extend by adding forecasting, cohorting by segment, or anomaly checks on discounting.
