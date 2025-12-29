# Zepp Health Analysis - Instrucciones para Agentes IA

## Perfil del Usuario

**Datos personales:**
- **Fecha de nacimiento:** 1971-02-20 *(calcular edad dinámica: edad actual = año actual - 1971)*
- **Ubicación:** Buenos Aires, Argentina
- **Profesión:** Desarrollador web y estudiante de Ciencias de Datos
- **Estado fitness:** Retomando actividad física tras ~2 años de inactividad

**Objetivos:**
1. Mejorar salud general, calidad de sueño y reducir estrés
2. Desarrollar fuerza y condición física de forma progresiva y segura
3. Construir proyecto real de Data Science para portfolio profesional

---

## Suplementación y Criterios de Salud

**Suplementación actual (NO debatir salvo nueva evidencia):**
- Multivitamínico Centrum +50
- Omega-3
- Whey Protein + Creatina monohidratada (XBody 2 lbs + 300g)
- **NO magnesio por ahora** → Reevaluar tras 3-4 semanas de entrenamiento

**Criterios clave:**
- Creatina: monohidratada, 3-5g diarios, todos los días
- Proteína: apoyo nutricional, NO reemplaza comidas
- Evitar marketing confuso (combos falsos, "energía instantánea")
- **Prioridad absoluta:** entrenamiento progresivo → sueño → hidratación → suplementos

**❌ NO sugerir:**
- Cambios en suplementación (ya decidido)
- Productos con marketing sin evidencia
- Sobre-suplementación

---

## Arquitectura del Proyecto

### Data Flow
```
Zepp App (exportación manual) 
  ↓
data/raw/ (CSV/ZIP)
  ↓
src/data_loader.py (carga + limpieza)
  ↓
src/metrics.py (cálculo métricas)
  ↓
notebooks/ (análisis exploratorio)
  ↓
reports/ (visualizaciones + insights)
```

### Estructura de Directorios
```
zepp-health-analysis/
├── data/
│   ├── raw/              # CSVs exportados desde Zepp (NO versionados)
│   └── processed/        # Datos limpios con fechas parseadas
├── notebooks/            # Entry point: 01_exploracion_inicial.ipynb
├── src/                  # Librería reutilizable (NO ejecutar directamente)
│   ├── __init__.py
│   ├── data_loader.py    # Carga robusta, detección automática
│   └── metrics.py        # Rolling avg, tendencias, correlaciones
├── reports/              # Gráficos generados
├── requirements.txt
└── AGENTS.md            # Este archivo
```

---

## Datos y Dispositivos

**Fuente única:** App Zepp (reloj Amazfit)  
**Google Fit descartado** para evitar duplicados

**Método de ingesta:**
- ❌ NO hay API oficial de Zepp
- ❌ NO auto-sincronización
- ✅ Exportación manual: CSV/ZIP desde Perfil → Configuración → Exportar datos

**Variables clave:**
- Sueño: duración total, sueño profundo, despertares
- Frecuencia cardíaca: en reposo, promedio diario
- HRV (variabilidad FC): si disponible en export
- Pasos diarios
- Entrenamientos registrados

---

## Convenciones de Código

### 1. Carga de Datos (SIEMPRE usar src/data_loader.py)

```python
from src import load_csv, parse_dates, get_date_range

# Carga con encoding robusto (utf-8 → latin-1 fallback)
df = load_csv('data/raw/sleep.csv')

# Auto-detección y parsing de fechas
df = parse_dates(df)  # Busca: date, fecha, time, timestamp

# Verificar rango temporal
min_date, max_date, days = get_date_range(df)
```

**Nunca hardcodear:**
- Nombres de columnas de fecha (usar `detect_date_column()`)
- Encodings (dejarlo en load_csv)

### 2. Cálculo de Métricas (src/metrics.py)

```python
from src import rolling_average, weekly_summary, sleep_quality_score

# Promedios móviles: default 7 días para tendencias cortas
df['sleep_7d'] = rolling_average(df, 'sleep_hours', window=7)
df['sleep_30d'] = rolling_average(df, 'sleep_hours', window=30)

# Resumen semanal con .dt.to_period('W')
weekly = weekly_summary(df, date_col='date', metrics=['sleep_hours', 'steps'])

# Score custom de sueño: 0-100 (40% duración + 40% profundo + 20% continuidad)
df['quality'] = df.apply(
    lambda x: sleep_quality_score(
        x['total_hours'], x['deep_hours'], x['awakenings']
    ), axis=1
)
```

### 3. Logging con Emojis

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"✓ Cargado: {filepath.name} ({df.shape[0]} filas)")
logger.warning(f"⚠ Encoding utf-8 falló, usando latin-1")
logger.error(f"✗ Archivo no encontrado: {filepath}")
```

### 4. Estilo Bilingüe

**Español (contexto local):**
- Comentarios en notebooks
- Log messages
- Nombres de variables exploratorias
- Paths descriptivos: `data/procesado/`

**Inglés (código profesional):**
- Nombres de funciones: `load_csv()`, `rolling_average()`
- Docstrings
- Variable names en src/
- Commits

---

## Workflow de Desarrollo

### Setup Inicial
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Ejecutar Análisis
```bash
# Colocar CSVs en data/raw/
jupyter notebook notebooks/01_exploracion_inicial.ipynb
```

### Agregar Nueva Métrica
1. Implementar en `src/metrics.py` con docstring completo
2. Exportar en `src/__init__.py`
3. Probar en notebook
4. Refactorizar si es reutilizable

---

## Patrones Específicos del Proyecto

### Prioridad de Métricas (orden de análisis)
1. **Sueño:** duración, % profundo, despertares
2. **FC en reposo:** tendencia semanal/mensual
3. **HRV:** disponibilidad en exports, correlación con estrés
4. **Actividad:** pasos, correlación con calidad sueño
5. **Entrenamientos:** impacto en métricas de recuperación

### Análisis Típicos
- Promedios 7/30 días (rolling windows)
- Tendencias: regresión lineal/polinómica
- Correlaciones: sueño ↔ estrés, actividad ↔ FC reposo
- Anomalías: IQR, Z-score
- Resúmenes semanales: `.dt.to_period('W')`

### Testing & Validación
❌ **NO hay suite de tests formal**  
✅ **Validación mediante:**
- Ejecución de notebooks con datos reales
- Inspección visual de plots
- Logs de calidad: nulls, duplicados, rangos

Cuando agregues lógica compleja en src/, incluir ejemplos en docstrings.

---

## Common Pitfalls

| Problema | Causa | Solución |
|----------|-------|----------|
| UnicodeDecodeError | Exports Zepp usan latin-1 | `load_csv()` hace fallback automático |
| Fechas como strings | Columnas no convertidas | Usar `parse_dates()` siempre |
| Duplicados | Zepp app exporta duplicados | Llamar `remove_duplicates()` |
| Nombres hardcodeados | Exports varían según versión Zepp | `detect_date_column()` auto-detecta |
| Timezone confusion | Zepp asume local | Asumir UTC-3 (Buenos Aires) |

---

## Stack Tecnológico

**Core:**
- Python 3.11+
- pandas >= 2.0 (manipulación)
- numpy >= 1.24 (cálculos)

**Visualización:**
- matplotlib >= 3.7
- seaborn >= 0.12
- plotly >= 5.14 (interactivo opcional)

**Análisis:**
- scipy >= 1.10 (stats)
- jupyter, notebook (interactivo)

**No incluido aún (agregar si necesario):**
- scikit-learn (ML avanzado)
- statsmodels (modelos estadísticos)

---

## Decisiones de Diseño (Razonamiento)

**¿Por qué exportación manual y no API?**
- Zepp no tiene API oficial
- Reverse engineering posible pero frágil
- Datos sensibles de salud → control total del usuario

**¿Por qué src/ como librería y no scripts?**
- Reutilización en múltiples notebooks
- Testing más fácil si se agrega en futuro
- Portfolio: muestra arquitectura modular

**¿Por qué NO ML desde el inicio?**
- Baseline EDA primero (conocer los datos)
- Evitar over-engineering
- ML solo si surge necesidad real (predicción, clasificación)

**¿Por qué bilingüe (ES/EN)?**
- Usuario hispanohablante (contexto natural)
- Portfolio internacional (código en inglés)
- Mejores prácticas: código en inglés, docs en idioma de usuario

---

## Próximos Pasos (Estado Actual: 2025-12-29)

**Completado:**
- ✅ Estructura de proyecto
- ✅ Funciones base en src/
- ✅ Notebook exploratorio placeholder
- ✅ Dependencias instaladas

**Pendiente:**
1. Usuario exportará primeros CSVs desde Zepp → `data/raw/`
2. Ejecutar `01_exploracion_inicial.ipynb` para inspeccionar estructura real
3. Adaptar `detect_date_column()` según nombres reales de columnas
4. Definir métricas baseline (promedio últimos 7/30 días)
5. Dashboard semanal: comparar semanas pre/post entrenamiento
6. Correlaciones: inicio entrenamiento (fin dic 2025) → cambios en sueño/HRV

---

## Para Todos los Agentes IA

**Al trabajar en este proyecto:**
1. **Siempre leer este archivo primero** antes de hacer cambios
2. **No asumir acceso automático** a Zepp/Google Fit
3. **No proponer soluciones sin justificar** su necesidad con datos
4. **Mantener código defendible** (entrevistas, portfolio)
5. **Distinguir claramente:**
   - Datos observados
   - Inferencias
   - Recomendaciones
6. **Evitar:**
   - Sugerir APIs inexistentes
   - Recomendar suplementos
   - ML antes de EDA completo
   - Hardcodear columnas/paths

**Principio rector:**  
Decisiones basadas en evidencia, código simple y mantenible, no sobre-ingeniería.
