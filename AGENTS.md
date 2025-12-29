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

**Enfoque de la actividad física:**
- La actividad física es principalmente una **herramienta de gestión del estrés**
- El análisis debe priorizar métricas de recuperación y estrés sobre métricas puramente estéticas
- Foco en sostenibilidad y progresión segura, no en optimización extrema

**Preguntas analíticas clave:**
- Correlación actividad física → calidad sueño (con rezagos 0-2 días)
- Impacto de entrenamiento estructurado en FC en reposo
- Detección de changepoints asociados a intervenciones
- Variabilidad intra-sujeto en métricas clave
- Patrones cíclicos (semanales) en sueño y actividad

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

# Promedios móviles: ventanas 7/14/30d para tendencias corto/medio plazo
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

**Métodos estadísticos disponibles:**
- Correlación: Pearson (lineal), Spearman (monotónica), cross-correlation con lags
- Tendencias: OLS (lineal), polinomial grado 2, changepoint detection
- Anomalías: IQR (robusto), Z-score (|z|>3)
- Agregaciones: media, mediana, percentiles, coeficiente de variación

### 3. Logging con Emojis

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"✓ Cargado: {filepath.name} ({df.shape[0]} filas)")
logger.warning(f"⚠ Encoding utf-8 falló, usando latin-1")
logger.error(f"✗ Archivo no encontrado: {filepath}")
```

### 4. Preferencias de Idioma

**Respuestas del agente:**
- SIEMPRE en **español latino neutro** (sin regionalismos, sin acentos específicos de país)
- Comunicación técnica clara y profesional
- Explicaciones y discusiones conceptuales en español

**Código y archivos (SIEMPRE en inglés):**
- Filesystem: nombres de carpetas y archivos en inglés (`data/raw/`, no `data/crudo/`)
- Funciones, métodos, clases: inglés (`load_csv()`, `rolling_average()`)
- Variables: inglés en src/, inglés también en notebooks para consistencia
- Comentarios en código: inglés
- Docstrings: inglés
- Commits: inglés

**Excepción (español permitido):**
- Markdown en notebooks para narrativa y explicaciones al usuario
- Mensajes de log cuando van dirigidos al usuario final
- Variables temporales en exploración rápida (pero preferir inglés)

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

## Principios de Análisis

### Nota Metodológica
**Enfoque N=1 (single-subject design):**
- Análisis longitudinal para decisiones personalizadas, no generalizables a población
- Válido para detectar patrones individuales y evaluar intervenciones con mediciones repetidas
- **Limitaciones reconocidas:** sin grupo control, confounders no medidos (dieta, estrés laboral), variabilidad de wearable
- **Valor profesional:** Demuestra rigor metodológico, pensamiento crítico sobre limitaciones, aplicable a proyectos escalables

### Análisis Útil vs. Estético
- ✅ **Útil (priorizar):** Correlaciones sueño-estrés, tendencias de recuperación, impacto de entrenamientos en métricas de salud
- ❌ **Estético (evitar):** Dashboards complejos sin insight accionable, métricas vanity sin contexto de decisión
- **Criterio de validación:** ¿Este análisis informa una decisión concreta o cambio de comportamiento? Si no → descartar o simplificar

### Enfoque Longitudinal
- **Priorizar análisis de series temporales:** tendencias, cambios post-intervención, evolución semanal/mensual
- **Comparaciones clave:** pre/post inicio de entrenamiento, semanas con buen vs. mal sueño, impacto de cambios en rutina
- **Ingestión incremental:** diseñar scripts que soporten agregar nuevos CSVs sin rehacer análisis completo
- **Ventanas de análisis:** últimos 7 días (tendencia corta), últimos 30 días (tendencia media), histórico completo (baseline)

### Visión de Largo Plazo
- Estructura modular para agregar métricas futuras sin refactorizar código base
- Documentar decisiones de diseño en código (comentarios) y en notebooks (markdown)
- Evitar soluciones one-off, pensar en reutilización y escalabilidad ligera
- Priorizar reproducibilidad: alguien debe poder clonar el repo y reproducir análisis

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

### Protocolo de Trabajo

**CRÍTICO - Antes de programar:**
1. **NO escribir código sin instrucción explícita del usuario**
2. Si hay ambigüedad en la solicitud, proponer opciones y esperar confirmación
3. Para cambios arquitecturales (nuevas carpetas, módulos, dependencias), justificar primero y obtener aprobación
4. Mostrar plan de acción antes de implementar tareas complejas

**Al trabajar en este proyecto:**
1. **Siempre leer este archivo primero** antes de hacer cambios
2. **Responder SIEMPRE en español latino neutro** (ver sección Preferencias de Idioma)
3. **No asumir acceso automático** a Zepp/Google Fit (exportación manual únicamente)
4. **No proponer soluciones sin justificar** su necesidad con datos o razonamiento técnico
5. **Mantener código defendible** para contexto de entrevistas y portfolio profesional
6. **Distinguir claramente en respuestas:**
   - Datos observados (hechos)
   - Inferencias (interpretaciones)
   - Recomendaciones (acciones sugeridas)
7. **Mantener trazabilidad:** comentarios claros, commits descriptivos, documentar decisiones no obvias

**Evitar absolutamente:**
- Sugerir APIs inexistentes o soluciones de auto-sincronización sin confirmación
- Recomendar suplementos (decisiones ya tomadas por el usuario)
- Proponer ML/modelos complejos antes de completar EDA baseline
- Hardcodear nombres de columnas o paths (usar detección automática)
- Análisis estético sin valor accionable
- Sobre-ingeniería (KISS: Keep It Simple, Stupid)

**Principio rector:**  
Decisiones basadas en evidencia, código simple y mantenible, análisis accionable, no sobre-ingeniería.
