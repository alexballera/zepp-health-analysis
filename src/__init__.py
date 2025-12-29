"""
Paquete para análisis de datos de salud Zepp.
"""

from .data_loader import (
    load_csv,
    detect_date_column,
    parse_dates,
    remove_duplicates,
    handle_missing,
    get_date_range
)

from .metrics import (
    rolling_average,
    calculate_trend,
    weekly_summary,
    detect_anomalies,
    sleep_quality_score
)

__version__ = '0.1.0'
