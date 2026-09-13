from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from utils import basic_clean


@dataclass
class PipelineResult:
    ocean: Optional[pd.DataFrame] = None
    fisheries: Optional[pd.DataFrame] = None
    biodiversity: Optional[pd.DataFrame] = None


def run_pipeline(ocean: Optional[pd.DataFrame], fisheries: Optional[pd.DataFrame], biodiversity: Optional[pd.DataFrame]) -> PipelineResult:
    """Simple, no-infra pipeline. Extend with your real transformations."""
    res = PipelineResult()
    if ocean is not None:
        res.ocean = basic_clean(ocean)
    if fisheries is not None:
        res.fisheries = basic_clean(fisheries)
    if biodiversity is not None:
        res.biodiversity = basic_clean(biodiversity)
    return res


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
