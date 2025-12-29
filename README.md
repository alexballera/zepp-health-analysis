# Zepp Health Analysis

Proyecto de Ciencia de Datos para análisis de datos de salud y actividad física exportados desde **Zepp** (Amazfit).

## 🎯 Objetivos

**Personales:**
- Mejorar salud general, calidad de sueño y reducir estrés
- Desarrollar fuerza y condición física de forma progresiva (retomando tras 2 años de inactividad)
- Tomar decisiones basadas en datos objetivos

**Profesionales:**
- Proyecto real de Data Science para portfolio
- Aplicar pipeline completo: ingesta → limpieza → análisis → visualización → insights
- Código mantenible y defendible en contexto profesional

---

## � Preguntas Analíticas

Este proyecto aborda interrogantes medibles mediante análisis longitudinal:

**Sueño y recuperación:**
- ¿Existe correlación entre volumen de actividad física (pasos, entrenamientos) y calidad de sueño con rezago temporal (0-2 días)?
- ¿Qué porcentaje de varianza en duración de sueño profundo se explica por carga de entrenamiento?
- ¿Se observan patrones cíclicos (semanales) en métricas de sueño?

**Actividad y rendimiento:**
- ¿El inicio de entrenamiento estructurado (ene-feb 2025) correlaciona con cambios en FC en reposo?
- ¿Existe relación entre días consecutivos de baja actividad y deterioro de métricas de sueño?

**Longitudinal:**
- ¿Se detectan puntos de cambio (changepoints) en series temporales asociados a intervenciones (inicio entrenamiento, suplementación)?
- ¿Qué métricas muestran mayor estabilidad/variabilidad intra-sujeto?

Estas preguntas guían el análisis exploratorio y la selección de features para modelado futuro.

---

## 📊 Datos

**Fuente:** App Zepp (reloj Amazfit)  
**Método:** Exportación manual (CSV/ZIP)  
**Variables clave:**
- Sueño (duración, profundo, despertares)
- Frecuencia cardíaca (reposo, promedio)
- HRV (si disponible)
- Pasos y actividad diaria
- Entrenamientos

### 📐 Nota Metodológica

**Enfoque:** Este proyecto implementa un **análisis longitudinal N=1** (single-subject design), válido para:
- Decisiones personalizadas basadas en datos propios (no generalizables a población)
- Detección de patrones individuales y relaciones causales dentro-sujeto
- Evaluación de intervenciones (entrenamiento, suplementación) con mediciones repetidas

**Limitaciones reconocidas:**
- Sin grupo control (comparaciones pre/post y análisis de series temporales compensan)
- Confounders no medidos (dieta, estrés laboral) pueden afectar interpretación
- Variabilidad de dispositivo wearable (precisión de sueño profundo en Amazfit)

**Valor profesional:**  
Muestra habilidades de análisis exploratorio, ingeniería de features, visualización y pensamiento crítico sobre limitaciones, aplicables a proyectos de mayor escala.

---

## 🗂️ Estructura del proyecto

```
zepp-health-analysis/
├── data/
│   ├── raw/              # CSVs exportados desde Zepp (NO versionados)
│   └── processed/        # Datos limpios y transformados
├── notebooks/            # Jupyter notebooks para análisis exploratorio
│   └── 01_exploracion_inicial.ipynb
├── src/                  # Scripts reutilizables
│   ├── __init__.py
│   ├── data_loader.py    # Carga y limpieza de datos
│   └── metrics.py        # Cálculo de métricas y análisis
├── reports/              # Gráficos, dashboards, insights
├── requirements.txt      # Dependencias Python
├── .gitignore
└── README.md
```

---

## 🚀 Setup

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd zepp-health-analysis
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Exportar datos desde Zepp
1. Abrir app Zepp
2. Ir a Perfil → Configuración → Exportar datos
3. Guardar archivos CSV en `data/raw/`

### 5. Ejecutar análisis
```bash
jupyter notebook notebooks/01_exploracion_inicial.ipynb
```

---

## 📈 Métricas y Metodología Analítica

**Feature engineering:**
- **Promedios móviles (rolling means):** Ventanas de 7, 14 y 30 días para suavizar series temporales y detectar tendencias de corto/medio plazo
- **Rezagos (lags):** Variables con desplazamiento temporal (1-3 días) para modelar efectos diferidos de actividad sobre sueño
- **Score compuesto de calidad de sueño:** Métrica custom (0-100) ponderando duración (40%), sueño profundo (40%) y continuidad (20%)

**Análisis de tendencias:**
- Regresión lineal (OLS) para estimar pendientes en períodos de interés
- Regresión polinómica (grado 2) para capturar patrones no lineales
- Detección de cambios estructurales (changepoint detection) con métodos de segmentación

**Correlaciones:**
- Pearson para relaciones lineales (sueño ↔ pasos)
- Spearman para relaciones monotónicas no lineales
- Cross-correlation con rezagos para identificar desfases temporales óptimos

**Detección de anomalías:**
- Método IQR (Q1 - 1.5×IQR, Q3 + 1.5×IQR) para outliers robustos
- Z-score (|z| > 3) para identificar valores extremos en distribuciones normales
- Validación visual mediante box plots y series temporales anotadas

**Agregaciones temporales:**
- Resúmenes semanales (`.dt.to_period('W')`) para comparar períodos
- Estadísticos: media, mediana, percentiles (25, 75), coeficiente de variación

---

## 🧪 Stack Tecnológico

**Core (manipulación y análisis):**
- **pandas ≥2.0:** Manipulación eficiente de series temporales con `.dt` accessor
- **numpy ≥1.24:** Operaciones vectorizadas y cálculo numérico
- **scipy ≥1.10:** Tests estadísticos (correlaciones, detección de outliers)

**Visualización:**
- **matplotlib ≥3.7:** Plots estáticos de alta calidad (series temporales, scatter plots)
- **seaborn ≥0.12:** Visualizaciones estadísticas (heatmaps de correlación, distribuciones)
- **plotly ≥5.14:** Gráficos interactivos para exploración (opcional, según necesidad)

**Entorno:**
- **jupyter, notebook:** Análisis interactivo y narrativa reproducible
- **python-dateutil:** Parsing robusto de timestamps Zepp

**No incluido (agregar si necesario):**
- **scikit-learn:** Feature scaling, clustering, modelos predictivos
- **statsmodels:** ARIMA, tests de estacionariedad, modelos de series temporales
- **ruptures:** Detección automática de changepoints

---

## 📝 Contexto personal

- **Edad:** 55 años
- **Ubicación:** Buenos Aires
- **Perfil:** Desarrollador web + estudiante de Ciencias de Datos
- **Suplementación actual:**
  - Multivitamínico Centrum +50
  - Omega-3
  - Whey Protein + Creatina monohidratada (XBody)
  
**Principios:**
- Priorizar entrenamiento progresivo, sueño e hidratación
- Evitar sobre-suplementación y marketing confuso
- Decisiones basadas en evidencia, no en modas

---

## 📌 Roadmap Analítico

**Fase 1: EDA y limpieza** ✅ En progreso
- [x] Setup del proyecto y estructura de carpetas
- [x] Carga inicial de CSVs con validación de encoding
- [ ] Análisis de calidad de datos (missings, outliers, rangos válidos)
- [ ] Estadísticas descriptivas por variable
- [ ] Visualización de distribuciones y series temporales

**Fase 2: Feature engineering**
- [ ] Construcción de rolling averages (7/14/30d)
- [ ] Cálculo de score de calidad de sueño
- [ ] Creación de features de rezago (lags 1-3d)
- [ ] Agregaciones semanales y mensuales

**Fase 3: Análisis de correlaciones**
- [ ] Matriz de correlación Pearson/Spearman
- [ ] Cross-correlation con rezagos variables
- [ ] Identificación de relaciones significativas
- [ ] Visualización de scatter plots con tendencias

**Fase 4: Análisis de intervenciones**
- [ ] Comparación pre/post inicio de entrenamiento (ene 2025)
- [ ] Detección de changepoints en series clave
- [ ] Análisis de impacto en ventanas de 2-4 semanas

**Fase 5: Modelado (opcional)**
- [ ] Predicción de calidad de sueño con regresión (baseline)
- [ ] Clustering de días según perfil de actividad/sueño
- [ ] Análisis de series temporales (ARIMA, Prophet)

**Fase 6: Reporting**
- [ ] Dashboard interactivo con métricas principales
- [ ] Documento de insights y recomendaciones accionables
- [ ] Preparación para presentación en portfolio

---

## 📄 Licencia

[Elegir licencia: MIT, GPL, etc.]

---

**Última actualización:** 2025-12-29
Mis datos personales de salud y entrenamiento
