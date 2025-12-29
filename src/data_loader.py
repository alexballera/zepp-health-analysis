"""
Utilidades para cargar y limpiar datos exportados desde Zepp.

Funciones:
- load_csv: Carga CSV con manejo robusto de encoding y formatos
- detect_date_column: Identifica columna de fecha automáticamente
- parse_dates: Convierte columnas de fecha a datetime
- remove_duplicates: Elimina registros duplicados
- handle_missing: Estrategias para valores faltantes
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv(
    filepath: Union[str, Path],
    encoding: str = 'utf-8',
    **kwargs
) -> pd.DataFrame:
    """
    Carga archivo CSV con manejo de errores común.
    
    Args:
        filepath: Ruta al archivo CSV
        encoding: Codificación del archivo (default: utf-8)
        **kwargs: Argumentos adicionales para pd.read_csv
        
    Returns:
        DataFrame con los datos cargados
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    
    try:
        df = pd.read_csv(filepath, encoding=encoding, **kwargs)
        logger.info(f"✓ Cargado: {filepath.name} ({df.shape[0]} filas, {df.shape[1]} columnas)")
        return df
    except UnicodeDecodeError:
        # Reintentar con encoding alternativo
        logger.warning(f"Error de encoding con {encoding}, intentando latin-1")
        df = pd.read_csv(filepath, encoding='latin-1', **kwargs)
        logger.info(f"✓ Cargado: {filepath.name} ({df.shape[0]} filas, {df.shape[1]} columnas)")
        return df
    except Exception as e:
        logger.error(f"Error al cargar {filepath.name}: {e}")
        raise


def detect_date_column(df: pd.DataFrame) -> Optional[str]:
    """
    Detecta automáticamente la columna de fecha en el DataFrame.
    
    Args:
        df: DataFrame a inspeccionar
        
    Returns:
        Nombre de la columna de fecha, o None si no se encuentra
    """
    date_keywords = ['date', 'fecha', 'time', 'timestamp', 'datetime', 'day']
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in date_keywords):
            return col
    
    return None


def parse_dates(
    df: pd.DataFrame,
    date_col: Optional[str] = None,
    format: Optional[str] = None
) -> pd.DataFrame:
    """
    Convierte columnas de fecha a datetime.
    
    Args:
        df: DataFrame a procesar
        date_col: Nombre de la columna de fecha (si None, se detecta automáticamente)
        format: Formato de fecha (si None, se infiere)
        
    Returns:
        DataFrame con columna de fecha convertida
    """
    df = df.copy()
    
    if date_col is None:
        date_col = detect_date_column(df)
        if date_col is None:
            logger.warning("No se encontró columna de fecha")
            return df
    
    try:
        df[date_col] = pd.to_datetime(df[date_col], format=format)
        logger.info(f"✓ Columna '{date_col}' convertida a datetime")
    except Exception as e:
        logger.error(f"Error al convertir '{date_col}': {e}")
    
    return df


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[List[str]] = None,
    keep: str = 'first'
) -> pd.DataFrame:
    """
    Elimina filas duplicadas.
    
    Args:
        df: DataFrame a procesar
        subset: Columnas para detectar duplicados (si None, usa todas)
        keep: 'first', 'last', o False
        
    Returns:
        DataFrame sin duplicados
    """
    initial_rows = len(df)
    df = df.drop_duplicates(subset=subset, keep=keep)
    removed = initial_rows - len(df)
    
    if removed > 0:
        logger.info(f"✓ Eliminados {removed} duplicados")
    
    return df


def handle_missing(
    df: pd.DataFrame,
    strategy: str = 'info',
    threshold: float = 0.5
) -> pd.DataFrame:
    """
    Maneja valores faltantes.
    
    Args:
        df: DataFrame a procesar
        strategy: 'info' (solo reporta), 'drop' (elimina), 'fill' (rellena)
        threshold: Para 'drop', % mínimo de datos no-nulos requerido
        
    Returns:
        DataFrame procesado
    """
    df = df.copy()
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    if missing.sum() > 0:
        logger.info("Valores faltantes detectados:")
        for col in missing[missing > 0].index:
            logger.info(f"  - {col}: {missing[col]} ({missing_pct[col]:.1f}%)")
        
        if strategy == 'drop':
            df = df.dropna(thresh=int(len(df.columns) * threshold))
            logger.info(f"✓ Eliminadas filas con >{(1-threshold)*100:.0f}% valores faltantes")
        elif strategy == 'fill':
            # Estrategia simple: forward fill para series temporales
            df = df.fillna(method='ffill').fillna(method='bfill')
            logger.info("✓ Valores faltantes rellenados (ffill + bfill)")
    else:
        logger.info("✓ No hay valores faltantes")
    
    return df


def get_date_range(df: pd.DataFrame, date_col: Optional[str] = None) -> tuple:
    """
    Obtiene el rango de fechas en el DataFrame.
    
    Args:
        df: DataFrame a analizar
        date_col: Nombre de la columna de fecha
        
    Returns:
        Tupla (fecha_min, fecha_max, días_únicos)
    """
    if date_col is None:
        date_col = detect_date_column(df)
    
    if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        unique_days = df[date_col].dt.date.nunique()
        return min_date, max_date, unique_days
    
    return None, None, 0
