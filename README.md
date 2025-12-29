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

## 📊 Datos

**Fuente:** App Zepp (reloj Amazfit)  
**Método:** Exportación manual (CSV/ZIP)  
**Variables clave:**
- Sueño (duración, profundo, despertares)
- Frecuencia cardíaca (reposo, promedio)
- HRV (si disponible)
- Pasos y actividad diaria
- Entrenamientos

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

## 📈 Métricas clave

- **Promedios móviles** (7 y 30 días)
- **Tendencias** (regresión lineal/polinómica)
- **Correlaciones**: sueño ↔ estrés, actividad ↔ FC en reposo
- **Score de calidad de sueño** (custom)
- **Detección de anomalías** (IQR, Z-score)

---

## 🧪 Stack tecnológico

- **Python 3.11+**
- **pandas, numpy**: manipulación de datos
- **matplotlib, seaborn, plotly**: visualización
- **jupyter**: análisis interactivo
- **scipy**: estadística

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

## 📌 Próximos pasos

1. ✅ Setup inicial del proyecto
2. ⏳ Cargar primer dataset de Zepp
3. ⏳ Análisis exploratorio y limpieza
4. ⏳ Definir métricas baseline
5. ⏳ Dashboard semanal de progreso
6. ⏳ Análisis de correlaciones (sueño/estrés/entrenamiento)

---

## 📄 Licencia

[Elegir licencia: MIT, GPL, etc.]

---

**Última actualización:** 2025-12-29
Mis datos personales de salud y entrenamiento
