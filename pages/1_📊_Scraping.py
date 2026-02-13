"""
============================================
PÁGINA - WEB SCRAPING
============================================
Extracción de datos de 3C2A Sports
"""

import streamlit as st
import pandas as pd
from utils.scraper_3c2a import Scraper3C2A, get_irvine_matches, get_conference_standings

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Web Scraping - Soccer Analytics",
    page_icon="🕷️",
    layout="wide"
)

# Verificar autenticación
if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] != True:
    st.error("⚠️ Por favor inicia sesión primero")
    st.page_link("Home.py", label="Ir a Inicio de Sesión", icon="🔐")
    st.stop()

# ============================================
# TÍTULO
# ============================================
st.title("🕷️ Web Scraping - 3C2A Sports")
st.markdown("Extrae datos en tiempo real de equipos, calendario y estadísticas")
st.markdown("---")

# ============================================
# CONTROLES DE SCRAPING
# ============================================

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ⚙️ Configuración de Scraping")
    
    scraping_type = st.radio(
        "Tipo de datos a extraer:",
        options=[
            "📅 Calendario de partidos (Irvine Valley)",
            "🏆 Clasificación Orange Empire Conference",
            "⚽ Análisis de partido individual (Box Score)"
        ],
        index=0
    )

with col2:
    st.markdown("### 📊 Estado")
    st.info("""
    **Fuente:** 3C2A Sports
    
    **Equipos disponibles:**
    - Irvine Valley
    - Fullerton
    - Santa Ana
    - Cypress
    """)

st.markdown("---")

# ============================================
# EJECUTAR SCRAPING
# ============================================

if st.button("🚀 Iniciar Scraping", type="primary", use_container_width=True):
    
    # Calendario de partidos
    if "Calendario de partidos" in scraping_type:
        with st.spinner("🔍 Extrayendo calendario de Irvine Valley..."):
            try:
                df_matches = get_irvine_matches()
                
                if not df_matches.empty:
                    st.success(f"✅ Se extrajeron {len(df_matches)} partidos exitosamente")
                    
                    # Guardar en session state
                    st.session_state['scraped_matches'] = df_matches
                    
                    # Mostrar resultados
                    st.markdown("### 📅 Calendario de Partidos - Irvine Valley")
                    
                    # Métricas rápidas
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        total_games = len(df_matches)
                        st.metric("Total de Partidos", total_games)
                    
                    with col2:
                        wins = len(df_matches[df_matches['resultado'] == 'W'])
                        st.metric("Victorias", wins, delta=f"{wins/total_games*100:.1f}%")
                    
                    with col3:
                        losses = len(df_matches[df_matches['resultado'] == 'L'])
                        st.metric("Derrotas", losses, delta=f"-{losses/total_games*100:.1f}%")
                    
                    with col4:
                        ties = len(df_matches[df_matches['resultado'] == 'D'])
                        st.metric("Empates", ties)
                    
                    st.markdown("---")
                    
                    # Tabla de partidos
                    st.dataframe(
                        df_matches,
                        use_container_width=True,
                        height=400
                    )
                    
                    # Botón de descarga
                    csv = df_matches.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name="irvine_valley_matches.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.warning("⚠️ No se encontraron partidos")
                    
            except Exception as e:
                st.error(f"❌ Error al extraer datos: {str(e)}")
    
    # Clasificación de conferencia
    elif "Clasificación" in scraping_type:
        with st.spinner("🔍 Extrayendo clasificación de Orange Empire Conference..."):
            try:
                df_standings = get_conference_standings()
                
                if not df_standings.empty:
                    st.success(f"✅ Se extrajeron {len(df_standings)} equipos exitosamente")
                    
                    # Guardar en session state
                    st.session_state['scraped_standings'] = df_standings
                    
                    # Mostrar resultados
                    st.markdown("### 🏆 Clasificación - Orange Empire Conference")
                    
                    # Métricas de los top 3
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🥇 1er Lugar")
                        first = df_standings.iloc[0]
                        st.markdown(f"**{first['equipo']}**")
                        st.markdown(f"Record: {first['victorias']}-{first['derrotas']}-{first['empates']}")
                        st.markdown(f"PCT: {first['porcentaje']}")
                    
                    with col2:
                        st.markdown("#### 🥈 2do Lugar")
                        second = df_standings.iloc[1]
                        st.markdown(f"**{second['equipo']}**")
                        st.markdown(f"Record: {second['victorias']}-{second['derrotas']}-{second['empates']}")
                        st.markdown(f"PCT: {second['porcentaje']}")
                    
                    with col3:
                        st.markdown("#### 🥉 3er Lugar")
                        third = df_standings.iloc[2]
                        st.markdown(f"**{third['equipo']}**")
                        st.markdown(f"Record: {third['victorias']}-{third['derrotas']}-{third['empates']}")
                        st.markdown(f"PCT: {third['porcentaje']}")
                    
                    st.markdown("---")
                    
                    # Tabla completa
                    st.dataframe(
                        df_standings,
                        use_container_width=True,
                        height=400
                    )
                    
                    # Botón de descarga
                    csv = df_standings.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name="orange_empire_standings.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.warning("⚠️ No se encontró la clasificación")
                    
            except Exception as e:
                st.error(f"❌ Error al extraer datos: {str(e)}")
    
    # Análisis de partido individual
    elif "Análisis de partido" in scraping_type:
        st.markdown("### ⚽ Análisis de Partido Individual")
        
        # Primero necesita haber extraído el calendario
        if 'scraped_matches' not in st.session_state:
            st.warning("⚠️ Primero extrae el calendario de partidos")
        else:
            df_matches = st.session_state['scraped_matches']
            
            # Filtrar solo partidos con Box Score
            matches_with_box = df_matches[df_matches['box_score_url'].notna()]
            
            if matches_with_box.empty:
                st.warning("⚠️ No hay partidos con Box Score disponible")
            else:
                # Selector de partido
                match_options = matches_with_box.apply(
                    lambda x: f"{x['fecha']} vs {x['oponente']} ({x['resultado']} {x['marcador']})",
                    axis=1
                ).tolist()
                
                selected_match = st.selectbox(
                    "Selecciona un partido:",
                    options=match_options,
                    index=0
                )
                
                if st.button("📊 Analizar Partido", type="primary"):
                    idx = match_options.index(selected_match)
                    match_row = matches_with_box.iloc[idx]
                    
                    box_score_url = match_row['box_score_url']
                    opponent = match_row['oponente']
                    
                    with st.spinner(f"🔍 Analizando partido vs {opponent}..."):
                        try:
                            scraper = Scraper3C2A()
                            analysis = scraper.analyze_match(box_score_url, opponent)
                            
                            if analysis:
                                st.success("✅ Análisis completado")
                                
                                # Guardar en session state
                                st.session_state['match_analysis'] = analysis
                                
                                # Mostrar resultados
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("#### ⚽ Goles")
                                    st.metric("Irvine Valley", analysis['total_goles_irvine'])
                                    for gol in analysis['goles_irvine']:
                                        st.markdown(f"- {gol['play']} ({gol['tiempo']})")
                                
                                with col2:
                                    st.markdown(f"#### ⚽ Goles {opponent}")
                                    st.metric(opponent, analysis['total_goles_oponente'])
                                    for gol in analysis['goles_oponente']:
                                        st.markdown(f"- {gol['play']} ({gol['tiempo']})")
                                
                                st.markdown("---")
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("#### 🟨 Tarjetas Irvine")
                                    st.metric("Total", analysis['total_tarjetas_irvine'])
                                    for card in analysis['tarjetas_irvine']:
                                        st.markdown(f"- {card['tipo_tarjeta']}: {card['jugador']} ({card['tiempo']})")
                                
                                with col2:
                                    st.markdown(f"#### 🟨 Tarjetas {opponent}")
                                    st.metric("Total", analysis['total_tarjetas_oponente'])
                                    for card in analysis['tarjetas_oponente']:
                                        st.markdown(f"- {card['tipo_tarjeta']}: {card['jugador']} ({card['tiempo']})")
                            
                        except Exception as e:
                            st.error(f"❌ Error al analizar partido: {str(e)}")

# ============================================
# DATOS GUARDADOS
# ============================================
st.markdown("---")
st.markdown("### 💾 Datos en Sesión")

col1, col2, col3 = st.columns(3)

with col1:
    if 'scraped_matches' in st.session_state:
        st.success(f"✅ Calendario: {len(st.session_state['scraped_matches'])} partidos")
    else:
        st.info("❌ No hay calendario cargado")

with col2:
    if 'scraped_standings' in st.session_state:
        st.success(f"✅ Clasificación: {len(st.session_state['scraped_standings'])} equipos")
    else:
        st.info("❌ No hay clasificación cargada")

with col3:
    if 'match_analysis' in st.session_state:
        st.success("✅ Análisis de partido disponible")
    else:
        st.info("❌ No hay análisis de partido")

st.markdown("---")
st.caption("Los datos se mantienen en la sesión actual | Se perderán al cerrar la app")
