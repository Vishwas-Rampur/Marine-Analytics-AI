from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import pandas as pd


@dataclass
class LoadedData:
    ocean: Optional[pd.DataFrame] = None
    fisheries: Optional[pd.DataFrame] = None
    biodiversity: Optional[pd.DataFrame] = None


def _read_df(file_bytes: bytes, name: str) -> pd.DataFrame:
    lower = name.lower()
    if lower.endswith(".csv"):
        return pd.read_csv(io.BytesIO(file_bytes))
    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return pd.read_excel(io.BytesIO(file_bytes))
    if lower.endswith(".parquet"):
        return pd.read_parquet(io.BytesIO(file_bytes))
    raise ValueError(f"Unsupported file type for: {name}. Use CSV, XLSX, or Parquet.")


def load_from_zip(uploaded_zip_bytes: bytes) -> Tuple[LoadedData, Dict[str, pd.DataFrame]]:
    """Load multiple data files from a single ZIP upload.

    Convention (recommended):
      - filenames containing 'ocean' -> ocean dataset
      - filenames containing 'fisher' -> fisheries dataset
      - filenames containing 'biodiv' or 'molecular' -> biodiversity dataset

    If names don't match, you can still use the returned 'all_files' dict.
    """
    loaded = LoadedData()
    all_files: Dict[str, pd.DataFrame] = {}

    with zipfile.ZipFile(io.BytesIO(uploaded_zip_bytes), "r") as z:
        names = [n for n in z.namelist() if not n.endswith("/")]

        if not names:
            raise ValueError("ZIP is empty. Please upload a ZIP containing your dataset files (CSV/XLSX/Parquet).")

        for n in names:
            data = z.read(n)
            try:
                df = _read_df(data, n)
            except Exception:
                continue
            all_files[n] = df

            low = n.lower()
            if loaded.ocean is None and "ocean" in low:
                loaded.ocean = df
            elif loaded.fisheries is None and ("fisher" in low or "fishery" in low):
                loaded.fisheries = df
            elif loaded.biodiversity is None and ("biodiv" in low or "molecular" in low or "biodiversity" in low):
                loaded.biodiversity = df

    return loaded, all_files


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.dropna(axis=1, how="all")
    out.columns = [str(c).strip() for c in out.columns]
    return out


def summarize(df: pd.DataFrame) -> dict:
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "columns": list(map(str, df.columns[:50])),
    }
