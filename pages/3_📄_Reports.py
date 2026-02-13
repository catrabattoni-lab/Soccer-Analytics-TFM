"""
============================================
PÁGINA - REPORTES PDF
============================================
Generación de reportes profesionales
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.pdf_generator import PDFReportGenerator

st.set_page_config(
    page_title="Reportes - Soccer Analytics",
    page_icon="📄",
    layout="wide"
)

# Verificar autenticación
if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] != True:
    st.error("⚠️ Por favor inicia sesión primero")
    st.page_link("Home.py", label="Ir a Inicio de Sesión", icon="🔐")
    st.stop()

st.title("📄 Generación de Reportes")
st.markdown("Crea reportes profesionales en PDF y exporta datos a CSV")
st.markdown("---")

# ============================================
# CONFIGURACIÓN DEL REPORTE
# ============================================

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ⚙️ Configuración del Reporte")
    
    report_type = st.selectbox(
        "Tipo de reporte:",
        options=[
            "📊 Reporte completo de temporada",
            "⚽ Análisis de partido individual",
            "🏆 Clasificación de conferencia"
        ]
    )
    
    include_ia = st.checkbox("Incluir análisis con IA", value=True)
    include_graphs = st.checkbox("Incluir gráficos", value=True)

with col2:
    st.markdown("### 💾 Opciones de Exportación")
    
    st.info("""
    **Formatos disponibles:**
    - 📄 PDF (profesional)
    - 📊 CSV (datos crudos)
    """)

st.markdown("---")

# ============================================
# GENERAR REPORTE PDF
# ============================================

if st.button("📄 Generar Reporte PDF", type="primary", use_container_width=True):
    
    # Verificar que hay datos
    if 'match_analysis' not in st.session_state:
        st.warning("⚠️ Primero extrae y analiza datos en las páginas anteriores")
    else:
        with st.spinner("📝 Generando reporte PDF..."):
            try:
                # Preparar datos para PDF
                stored_data = st.session_state['match_analysis']
                
                # Agregar información adicional si existe
                if 'scraped_matches' in st.session_state:
                    df_matches = st.session_state['scraped_matches']
                    
                    # Calcular estadísticas agregadas
                    total_goals = len(df_matches[df_matches['resultado'] == 'W']) * 2  # Estimado
                    total_cards = len(df_matches) * 0.5  # Estimado
                    
                    stored_data['total_goals'] = int(total_goals)
                    stored_data['total_cards'] = int(total_cards)
                    
                    # Preparar datos de jugadores
                    players_dict = {}
                    
                    for roster_team, players in stored_data.get('rosters', {}).items():
                        if 'Irvine Valley' in roster_team:
                            for player in players:
                                nombre = player.get('nombre', 'Unknown')
                                players_dict[nombre] = {
                                    'goles': int(player.get('g', 0)),
                                    'asistencias': int(player.get('a', 0)),
                                    'tiros': int(player.get('sh', 0)),
                                    'amarillas': 0,
                                    'rojas': 0
                                }
                    
                    stored_data['players'] = players_dict
                
                # Generar PDF
                pdf_gen = PDFReportGenerator(
                    filename=f"reporte_irvine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
                
                output_path = pdf_gen.generate_full_report(stored_data)
                
                # Leer el PDF generado
                with open(output_path, 'rb') as f:
                    pdf_data = f.read()
                
                st.success("✅ Reporte PDF generado exitosamente")
                
                # Botón de descarga
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf_data,
                    file_name=f"reporte_irvine_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.info(f"📁 Archivo guardado en: `{output_path}`")
                
            except Exception as e:
                st.error(f"❌ Error al generar PDF: {str(e)}")
                st.exception(e)

st.markdown("---")

# ============================================
# EXPORTAR CSV
# ============================================

st.markdown("### 📊 Exportar Datos a CSV")

if st.button("📥 Descargar Datos CSV", use_container_width=True):
    
    if 'scraped_matches' not in st.session_state:
        st.warning("⚠️ No hay datos disponibles para exportar")
    else:
        df = st.session_state['scraped_matches']
        
        # Convertir a CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Descargar CSV - Calendario de Partidos",
            data=csv_data,
            file_name=f"irvine_matches_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.success(f"✅ Listo para descargar ({len(df)} filas)")

# ============================================
# VISTA PREVIA
# ============================================

st.markdown("---")
st.markdown("### 👁️ Vista Previa de Datos")

if 'scraped_matches' in st.session_state:
    df = st.session_state['scraped_matches']
    
    st.dataframe(df, use_container_width=True, height=300)
    
    st.caption(f"Total de registros: {len(df)}")
else:
    st.info("No hay datos cargados para previsualizar")

st.markdown("---")
st.caption("Los reportes se guardan en la carpeta 'outputs/' | Los datos CSV se descargan directamente")
