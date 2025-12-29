"""
Funciones para análisis de métricas de salud.

Incluye:
- Promedios móviles (rolling averages)
- Cálculo de tendencias
- Correlaciones entre variables
- Detección de anomalías simples
"""

import pandas as pd
import numpy as np
from typing import Optional


def rolling_average(
    df: pd.DataFrame,
    column: str,
    window: int = 7,
    min_periods: Optional[int] = None
) -> pd.Series:
    """
    Calcula promedio móvil de una columna.
    
    Args:
        df: DataFrame con los datos
        column: Nombre de la columna a promediar
        window: Tamaño de la ventana (default: 7 días)
        min_periods: Mínimo de períodos para calcular (default: window)
        
    Returns:
        Serie con promedio móvil
    """
    if min_periods is None:
        min_periods = window
    
    return df[column].rolling(window=window, min_periods=min_periods).mean()


def calculate_trend(
    df: pd.DataFrame,
    column: str,
    method: str = 'linear'
) -> pd.Series:
    """
    Calcula tendencia de una serie temporal.
    
    Args:
        df: DataFrame con los datos
        column: Nombre de la columna
        method: 'linear' o 'polynomial'
        
    Returns:
        Serie con valores de tendencia
    """
    x = np.arange(len(df))
    y = df[column].values
    
    # Remover NaNs
    mask = ~np.isnan(y)
    x_clean = x[mask]
    y_clean = y[mask]
    
    if len(x_clean) < 2:
        return pd.Series([np.nan] * len(df), index=df.index)
    
    if method == 'linear':
        z = np.polyfit(x_clean, y_clean, 1)
        p = np.poly1d(z)
        trend = p(x)
    else:
        # Polynomial de grado 2
        z = np.polyfit(x_clean, y_clean, 2)
        p = np.poly1d(z)
        trend = p(x)
    
    return pd.Series(trend, index=df.index)


def weekly_summary(
    df: pd.DataFrame,
    date_col: str,
    metrics: list[str],
    agg_funcs: Optional[dict] = None
) -> pd.DataFrame:
    """
    Genera resumen semanal de métricas.
    
    Args:
        df: DataFrame con los datos
        date_col: Nombre de la columna de fecha
        metrics: Lista de columnas a agregar
        agg_funcs: Diccionario {métrica: función} (default: mean)
        
    Returns:
        DataFrame con resumen semanal
    """
    df = df.copy()
    
    # Asegurar que date_col es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])
    
    # Crear columna de semana
    df['week'] = df[date_col].dt.to_period('W')
    
    # Funciones de agregación por defecto
    if agg_funcs is None:
        agg_funcs = {metric: 'mean' for metric in metrics}
    
    # Agregar por semana
    summary = df.groupby('week')[metrics].agg(agg_funcs).reset_index()
    summary['week'] = summary['week'].astype(str)
    
    return summary


def detect_anomalies(
    series: pd.Series,
    method: str = 'iqr',
    threshold: float = 1.5
) -> pd.Series:
    """
    Detecta valores anómalos en una serie.
    
    Args:
        series: Serie a analizar
        method: 'iqr' o 'zscore'
        threshold: Umbral para detección (IQR multiplier o Z-score)
        
    Returns:
        Serie booleana (True = anomalía)
    """
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - threshold * IQR
        upper = Q3 + threshold * IQR
        return (series < lower) | (series > upper)
    
    elif method == 'zscore':
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > threshold
    
    else:
        raise ValueError(f"Método desconocido: {method}")


def sleep_quality_score(
    total_sleep: float,
    deep_sleep: float,
    awakenings: int,
    target_sleep: float = 7.5
) -> float:
    """
    Calcula un score simple de calidad de sueño.
    
    Args:
        total_sleep: Horas totales de sueño
        deep_sleep: Horas de sueño profundo
        awakenings: Número de despertares
        target_sleep: Objetivo de horas de sueño
        
    Returns:
        Score 0-100
    """
    # Componente de duración (40 puntos)
    duration_score = min(40, (total_sleep / target_sleep) * 40)
    
    # Componente de sueño profundo (40 puntos)
    # Ideal: ~20-25% del total
    deep_ratio = deep_sleep / total_sleep if total_sleep > 0 else 0
    deep_score = min(40, (deep_ratio / 0.25) * 40)
    
    # Componente de continuidad (20 puntos)
    continuity_score = max(0, 20 - (awakenings * 2))
    
    return duration_score + deep_score + continuity_score
