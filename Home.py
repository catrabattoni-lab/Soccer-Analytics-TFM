"""
============================================
SOCCER ANALYTICS STREAMLIT - TFM
Multi-Team Soccer Performance Analysis
============================================

Aplicación principal con sistema de login
"""

import streamlit as st
import streamlit_authenticator as stauth
from utils.config import APP_TITLE, APP_VERSION, validate_config
import yaml
from yaml.loader import SafeLoader

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Soccer Analytics - TFM",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# VALIDAR CONFIGURACIÓN
# ============================================
if not validate_config():
    st.error("⚠️ Por favor configura el archivo .env con tu OPENAI_API_KEY")
    st.info("Copia .env.example a .env y agrega tu API key de OpenAI")
    st.stop()

# ============================================
# SISTEMA DE LOGIN SIMPLE
# ============================================

# Inicializar session state para autenticación
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None

# Si no está autenticado, mostrar login
if st.session_state['authentication_status'] != True:
    st.title("⚽ Soccer Analytics Platform")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.subheader("🔐 Iniciar Sesión")
        st.info("**Usuario:** admin | **Contraseña:** admin123")
        
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Iniciar Sesión")
            
            if submit:
                # Login simple (en producción usar hashing)
                if username == "admin" and password == "admin123":
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username
                    st.session_state['name'] = "Admin User"
                    st.rerun()
                elif username == "claudio" and password == "ivc2024":
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username
                    st.session_state['name'] = "Claudio Catrambone"
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
    
    st.markdown("---")
    st.caption("Soccer Analytics Platform | TFM - Master en IA Aplicada al Deporte")
    st.stop()

# ============================================
# USUARIO AUTENTICADO - MOSTRAR APP
# ============================================

# Sidebar con logout
with st.sidebar:
    st.title("⚽ Soccer Analytics")
    st.markdown(f"**{st.session_state['name']}**")
    st.markdown("---")
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state['authentication_status'] = None
        st.session_state['username'] = None
        st.session_state['name'] = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Navegación")
    st.page_link("Home.py", label="🏠 Inicio", icon="🏠")
    st.page_link("pages/1_📊_Scraping.py", label="Web Scraping", icon="🕷️")
    st.page_link("pages/2_📈_Analysis.py", label="Análisis IA", icon="🤖")
    st.page_link("pages/3_📄_Reports.py", label="Reportes PDF", icon="📄")
    
    st.markdown("---")
    st.caption(f"Versión {APP_VERSION}")

# ============================================
# PÁGINA DE INICIO
# ============================================

st.title(f"{APP_TITLE}")
st.markdown("### Sistema inteligente de análisis deportivo multi-equipo")
st.markdown("---")

# Descripción
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 🎯 Bienvenido
    
    Dashboard profesional que combina **web scraping**, **visualizaciones avanzadas**, 
    **IA generativa** y **machine learning** para análisis deportivo de múltiples equipos.
    
    ### ✨ Proyecto TFM - Master en IA Aplicada al Deporte
    
    Este proyecto analiza el rendimiento de **4 equipos** de la Orange Empire Conference:
    - **Irvine Valley College** (110 partidos)
    - **Fullerton College** (123 partidos)
    - **Santa Ana College** (117 partidos)
    - **Cypress College** (113 partidos)
    
    **Total:** 463 partidos analizados | Temporadas 2021-2026
    """)

with col2:
    st.info("""
    **📊 Stack Tecnológico**
    
    - Python 3.10+
    - Streamlit
    - BeautifulSoup
    - OpenAI GPT-4
    - Plotly
    - Scikit-learn
    - ReportLab
    """)

st.markdown("---")

# Características principales
st.markdown("## 🚀 Características Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 🕷️ Web Scraping
    Extracción automática de datos desde 3C2A Sports:
    - Calendarios de partidos
    - Box Scores completos
    - Estadísticas de equipo
    - Clasificación de conferencia
    """)

with col2:
    st.markdown("""
    ### 📊 Visualizaciones
    Gráficos interactivos avanzados:
    - Radar Charts multi-equipo
    - Heat Maps de rendimiento
    - Análisis comparativos
    - Timeline de evolución
    """)

with col3:
    st.markdown("""
    ### 🤖 IA Generativa
    Análisis inteligente con OpenAI:
    - Resúmenes de partidos
    - Fortalezas y debilidades
    - Recomendaciones tácticas
    - Reportes de temporada
    """)

with col4:
    st.markdown("""
    ### 🎯 Machine Learning
    Modelos predictivos:
    - Regresión multi-variable
    - Feature engineering avanzado
    - Validación académica
    - Análisis de periodización
    """)

st.markdown("---")

# Flujo de trabajo
st.markdown("## 📋 Flujo de Trabajo")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 1️⃣ Extracción de Datos
    Ve a **🕷️ Web Scraping** para:
    - Extraer calendario de partidos
    - Obtener estadísticas de equipos
    - Descargar Box Scores
    - Ver clasificación de conferencia
    """)

with col2:
    st.markdown("""
    ### 2️⃣ Análisis con IA
    Ve a **🤖 Análisis IA** para:
    - Visualizar datos con gráficos
    - Generar análisis con OpenAI
    - Comparar equipos
    - Explorar tendencias
    """)

with col3:
    st.markdown("""
    ### 3️⃣ Generar Reportes
    Ve a **📄 Reportes PDF** para:
    - Crear reportes profesionales
    - Exportar datos a CSV
    - Guardar análisis
    - Compartir resultados
    """)

st.markdown("---")

# Investigación
st.markdown("## 🔬 Hipótesis de Investigación")

st.markdown("""
### Academic Periodization Effect

Este proyecto investiga la relación entre rendimiento académico y deportivo:

**Hipótesis principal:** 
> Los equipos con mejor ranking académico (como IVC, #1 en California) experimentan 
> decline en rendimiento deportivo durante períodos de exámenes (Noviembre, Diciembre).

**Metodología:**
- Análisis de 463 partidos de 4 equipos
- Feature engineering: `opponent_quality`, `team_academic_rank`, `month`
- Modelo de regresión multi-variable
- Validación estadística con R² mejorado (target: 0.25-0.35)

**Resultados esperados:**
- Correlación inversa entre ranking académico y rendimiento deportivo
- Decline mensual específico en equipos académicamente top
- Mejora del modelo de R² = -0.41 → R² = 0.25+
""")

st.markdown("---")

# Footer
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **👨‍💻 Desarrollado por:**
    
    Claudio Catrambone  
    Irvine Valley College
    """)

with col2:
    st.markdown("""
    **🎓 Programa:**
    
    Master en IA Aplicada al Deporte  
    UCAM - Universidad Católica de Murcia
    """)

with col3:
    st.markdown("""
    **📅 Proyecto:**
    
    TFM - Trabajo Final de Master  
    Febrero 2026
    """)

st.markdown("---")
st.caption("Soccer Analytics Platform | Powered by Streamlit + OpenAI | Version 2.0.0")
