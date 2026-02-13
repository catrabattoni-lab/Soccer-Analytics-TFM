# ⚽ Soccer Analytics - Multi-Team Platform

**Dashboard interactivo de análisis deportivo con IA para fútbol universitario**

Plataforma desarrollada como parte del Trabajo de Fin de Máster (TFM) en IA Aplicada al Deporte - UCAM

---

## 🎯 Descripción del Proyecto

Sistema de análisis multi-equipo que procesa datos de partidos de soccer universitario de la Orange Empire Conference, generando insights automáticos mediante inteligencia artificial para validar la hipótesis de **Academic Periodization**: el impacto de la carga académica en el rendimiento deportivo.

---

## 🚀 Características Principales

### 📊 **Análisis Multi-Equipo**
- Dashboard interactivo con 4 equipos simultáneos
- 435 partidos analizados (5 temporadas: 2021-2026)
- Filtros dinámicos por equipo y temporada
- 4 gráficos principales con bandas de rendimiento

### 📈 **Métricas Avanzadas**
- **Opponent Quality Impact**: Win rate según calidad del rival
- **Academic Rank Correlation**: Correlación ranking académico vs rendimiento
- **Consistency Score**: Análisis de variabilidad de goles
- **Home Advantage Index**: Ventaja local cuantificada

### 🤖 **Análisis con IA (GPT-4)**
- **Análisis Comparativo**: Resumen automático de equipos
- **Validación Academic Periodization**: Validación estadística de hipótesis TFM
- **Recomendaciones Estratégicas**: Consejos personalizados por equipo

### 🔍 **Web Scraping Automatizado**
- Extracción automática de datos desde 3C2A Sports
- Procesamiento y limpieza de datos
- Detección inteligente de meses y temporadas

---

## 🏗️ Estructura del Proyecto

```
Soccer_Analytics_Streamlit/
├── Home.py                          # Página principal
├── pages/
│   ├── 1_📊_Scraping.py            # Extracción de datos
│   ├── 2_📈_Analysis.py            # Análisis individual
│   ├── 3_📄_Reports.py             # Generación de reportes
│   └── 4_📊_Multi_Team_Analysis.py # Dashboard multi-equipo + IA
├── data/
│   ├── matches_raw.csv             # Datos crudos
│   └── multi_team_data_complete.csv # Datos procesados (435 partidos)
├── utils/                          # Utilidades y funciones auxiliares
├── .streamlit/                     # Configuración de Streamlit
├── .env                            # Variables de entorno (API keys)
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Este archivo
```

---

## 🛠️ Instalación

### **Requisitos Previos**
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Cuenta de OpenAI con API Key

### **Paso 1: Clonar o descargar el proyecto**
```bash
# Si tienes el ZIP, descomprímelo
# Si tienes Git:
git clone [URL_DEL_REPOSITORIO]
cd Soccer_Analytics_Streamlit
```

### **Paso 2: Instalar dependencias**
```bash
py -m pip install -r requirements.txt
```

### **Paso 3: Configurar API Key de OpenAI**

1. Crea un archivo `.env` en la raíz del proyecto
2. Agrega tu API Key:
```
OPENAI_API_KEY=sk-proj-tu-api-key-aqui
```

3. **IMPORTANTE**: Usa OpenAI versión 0.28.1 (ya incluida en requirements.txt)

### **Paso 4: Verificar instalación**
```bash
py -m pip show openai
# Debería mostrar: Version: 0.28.1
```

---

## 🚀 Uso de la Aplicación

### **Ejecutar la aplicación**
```bash
streamlit run Home.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### **Páginas Disponibles**

#### **1. 📊 Scraping**
- Extrae datos automáticamente desde 3C2A Sports
- Procesa y limpia la información
- Genera archivos CSV con los datos

#### **2. 📈 Analysis**
- Análisis individual por equipo
- Estadísticas detalladas
- Gráficos de rendimiento

#### **3. 📄 Reports**
- Genera reportes en PDF
- Exportación de datos
- Resúmenes ejecutivos

#### **4. 📊 Multi-Team Analysis** ⭐ **(PÁGINA PRINCIPAL)**

**Controles Dinámicos:**
- Selecciona equipos (1-4 simultáneos)
- Filtra por temporadas (2021-2026)
- Visualización en tiempo real

**Gráficos Principales:**
1. **Win Rate Timeline**: Evolución por temporada con bandas de rendimiento
2. **Home vs Away**: Comparación local vs visitante
3. **Goals Analysis**: Promedio de goles a favor y en contra
4. **Monthly Performance**: Rendimiento por mes con zona de exámenes

**Métricas Avanzadas:**
- Impacto de calidad del rival
- Correlación académica vs deportiva
- Consistencia de rendimiento
- Índice de ventaja local

**Análisis con IA:**
1. **Generar Análisis Comparativo** → Resumen automático de equipos
2. **Validar Hipótesis con IA** → Validación de academic periodization
3. **Generar Recomendaciones** → Consejos estratégicos por equipo

---

## 📊 Datos Incluidos

### **Equipos Analizados**
- **Irvine Valley College (IVC)** - Academic Rank: #1
- **Fullerton College** - Academic Rank: #41  
- **Cypress College** - Academic Rank: #77
- **Santa Ana College** - Academic Rank: #71

### **Temporadas**
- 2021-2022 (75 partidos)
- 2022-2023 (99 partidos)
- 2023-2024 (104 partidos)
- 2024-2025 (83 partidos)
- 2025-2026 (74 partidos)

**Total: 435 partidos analizados**

### **Meses de Temporada**
- August (33 partidos)
- September (125 partidos)
- October (149 partidos)
- November (96 partidos)
- December (32 partidos)

---

## 🎓 Contexto Académico - TFM

### **Hipótesis de Investigación**
> "Los equipos con mejor ranking académico experimentan decline en rendimiento deportivo durante periodos de exámenes (Noviembre-Diciembre)"

### **Metodología**
1. Recopilación de datos de 4 equipos (5 temporadas)
2. Integración de rankings académicos
3. Análisis estadístico de patrones mensuales
4. Validación mediante IA (GPT-4)

### **Resultados Clave**
- **IVC (#1 académico)**: Decline evidente Oct→Nov→Dec
- **Fullerton (#41)**: Colapso dramático en Diciembre
- **Correlación detectada**: Equipos académicos top muestran mayor variabilidad

---

## 🔧 Configuración Avanzada

### **Variables de Entorno (.env)**
```bash
# OpenAI API Key (obligatorio para análisis IA)
OPENAI_API_KEY=sk-proj-tu-key-aqui

# Configuración de Streamlit (opcional)
DEBUG=False
PORT=8501
```

### **Personalización de Streamlit**
Edita `.streamlit/config.toml` para cambiar:
- Tema de colores
- Puerto de ejecución
- Opciones de caché

---

## 🐛 Solución de Problemas

### **Error: "ModuleNotFoundError: No module named 'openai'"**
```bash
py -m pip install openai==0.28.1
```

### **Error: "No se encontró OPENAI_API_KEY"**
1. Verifica que el archivo `.env` existe en la raíz
2. Verifica que contiene: `OPENAI_API_KEY=tu-key`
3. Reinicia Streamlit

### **Error de versión de OpenAI**
```bash
# Desinstalar versión incorrecta
py -m pip uninstall openai

# Instalar versión correcta
py -m pip install openai==0.28.1
```

### **Gráficos no se actualizan**
```bash
# Limpiar caché de Streamlit
streamlit cache clear

# Reiniciar aplicación
streamlit run Home.py
```

---

## 📦 Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje principal
- **Streamlit 1.31.0**: Framework de dashboards interactivos
- **Pandas 2.2.3**: Procesamiento de datos
- **Plotly 5.24.1**: Visualizaciones interactivas
- **OpenAI 0.28.1**: Análisis con GPT-4
- **BeautifulSoup4 4.12.3**: Web scraping
- **ReportLab 4.2.5**: Generación de PDFs

---

## 👤 Autor

**Claudio Catrambone**
- Coach de Soccer - Irvine Valley College
- Estudiante de Máster en IA Aplicada al Deporte - UCAM
- Especialización: Sport Analytics y Academic Periodization

---

## 📄 Licencia

Este proyecto fue desarrollado como parte de un Trabajo de Fin de Máster (TFM) con fines académicos.

---

## 🙏 Agradecimientos

- **Orange Empire Conference**: Por los datos deportivos
- **3C2A Sports**: Plataforma de estadísticas
- **OpenAI**: API de GPT-4 para análisis inteligente
- **UCAM**: Universidad Católica de Murcia - Programa de Máster

---

## 📞 Contacto

Para consultas sobre el proyecto:
- Email: [tu-email@ejemplo.com]
- LinkedIn: [tu-perfil]
- GitHub: [tu-github]

---

**Multi-Team Soccer Analytics | Powered by Streamlit + OpenAI**

*Última actualización: Febrero 2026*
