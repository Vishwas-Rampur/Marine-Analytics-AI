# AI-Driven Unified Data Platform (Capstone-style)

Simplified version:
- ✅ Streamlit frontend (`main.py`)
- ✅ Upload your datasets as **one ZIP**
- ✅ No Docker / Postgres / Kafka
- ✅ Repo ships with **no datasets**

## Run locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

## ZIP upload format

Upload **one ZIP** containing your datasets (CSV / XLSX / Parquet).

Recommended naming:
- `*ocean*` -> Oceanographic data
- `*fisher*` -> Fisheries data
- `*biodiv*` or `*molecular*` -> Biodiversity data

If your filenames don't match, the app still shows all tables under **All Files**.
