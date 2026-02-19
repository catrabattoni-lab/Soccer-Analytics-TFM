"""
============================================
PÁGINA - ANÁLISIS CON IA
============================================
Visualizaciones y análisis con OpenAI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.openai_helper import OpenAIHelper
from utils.visualizations import AdvancedVisualizations

st.set_page_config(
    page_title="Análisis IA - Soccer Analytics",
    page_icon="📈",
    layout="wide"
)

# Verificar autenticación
if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] != True:
    st.error("⚠️ Por favor inicia sesión primero")
    st.page_link("Home.py", label="Ir a Inicio de Sesión", icon="🔐")
    st.stop()

st.title("📈 Análisis y Visualizaciones")
st.markdown("Explora datos con gráficos interactivos y análisis con IA")
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Visualizaciones", "🤖 Análisis con IA"])

# ============================================
# TAB 1: VISUALIZACIONES
# ============================================
with tab1:
    st.markdown("### 📊 Visualizaciones Interactivas")
    
    # Verificar que hay datos
    if 'scraped_matches' not in st.session_state:
        st.warning("⚠️ Primero extrae datos en la página de Web Scraping")
    else:
        df = st.session_state['scraped_matches']
        
        # Distribución de resultados
        st.markdown("#### 🎯 Distribución de Resultados")
        
        results_count = df['resultado'].value_counts()
        
        fig = px.pie(
            values=results_count.values,
            names=results_count.index,
            title="Distribución de Resultados - Irvine Valley",
            color_discrete_map={'W': '#18BC9C', 'L': '#E74C3C', 'D': '#F39C12', 'TBD': '#95A5A6'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Resultados por mes
        st.markdown("#### 📅 Resultados por Mes")
        
        if 'mes' in df.columns:
            fig2 = px.histogram(
                df,
                x='mes',
                color='resultado',
                title="Distribución de Resultados por Mes",
                barmode='group',
                color_discrete_map={'W': '#18BC9C', 'L': '#E74C3C', 'D': '#F39C12'}
            )
            
            st.plotly_chart(fig2, use_container_width=True)

# ============================================
# TAB 2: ANÁLISIS CON IA
# ============================================
with tab2:
    st.markdown("### 🤖 Análisis con Inteligencia Artificial")
    
    analysis_type = st.selectbox(
        "Tipo de análisis:",
        options=[
            "📝 Resumen de temporada",
            "💪 Fortalezas y debilidades",
            "🎯 Recomendaciones tácticas"
        ]
    )
    
    if st.button("🚀 Generar Análisis IA", type="primary"):
        
        # Verificar que hay datos
        if 'match_analysis' not in st.session_state:
            st.warning("⚠️ Primero analiza un partido en la página de Web Scraping")
        else:
            with st.spinner("🤖 Generando análisis con OpenAI..."):
                try:
                    helper = OpenAIHelper()
                    analysis_data = st.session_state['match_analysis']
                    
                    if "Fortalezas y debilidades" in analysis_type:
                        # Preparar datos para análisis
                        team_stats = {
                            'goles_favor': analysis_data['total_goles_irvine'],
                            'goles_contra': analysis_data['total_goles_oponente'],
                            'tarjetas': analysis_data['total_tarjetas_irvine']
                        }
                        
                        result = helper.analyze_strengths_weaknesses(team_stats)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 💪 Fortalezas")
                            for item in result.get('fortalezas', []):
                                st.success(f"✅ {item}")
                        
                        with col2:
                            st.markdown("#### ⚠️ Debilidades")
                            for item in result.get('debilidades', []):
                                st.warning(f"⚠️ {item}")
                        
                        st.markdown("#### 🎯 Recomendaciones")
                        for item in result.get('recomendaciones', []):
                            st.info(f"💡 {item}")
                    
                    else:
                        st.info("Este tipo de análisis estará disponible próximamente")
                    
                except Exception as e:
                    st.error(f"❌ Error al generar análisis: {str(e)}")

