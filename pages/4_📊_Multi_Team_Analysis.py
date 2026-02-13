"""
============================================
PÁGINA - ANÁLISIS MULTI-TEAM
============================================
Análisis comparativo de 4 equipos con IA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
import json

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Multi-Team Analysis - Soccer Analytics",
    page_icon="📊",
    layout="wide"
)

# Verificar autenticación
if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] != True:
    st.error("⚠️ Por favor inicia sesión primero")
    st.page_link("Home.py", label="Ir a Inicio de Sesión", icon="🔐")
    st.stop()

# ============================================
# CARGAR DATOS
# ============================================
@st.cache_data
def load_multi_team_data():
    """Carga el CSV con datos de múltiples equipos"""
    csv_path = Path(__file__).parent.parent / "data" / "multi_team_data_complete.csv"
    
    if not csv_path.exists():
        return None
    
    df = pd.read_csv(csv_path)
    return df

# ============================================
# TÍTULO
# ============================================
st.title("📊 Análisis Multi-Team Comparativo")
st.markdown("Análisis avanzado de 4 equipos de la Orange Empire Conference")
st.markdown("---")

# Cargar datos
df = load_multi_team_data()

if df is None:
    st.error("❌ No se encontró el archivo de datos. Por favor, sube el CSV primero.")
    st.info("📁 El archivo debe estar en: `data/multi_team_data_complete.csv`")
    st.stop()

# ============================================
# INFORMACIÓN DEL DATASET
# ============================================
with st.expander("ℹ️ Información del Dataset", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Partidos", len(df))
    
    with col2:
        st.metric("Equipos", df['equipo'].nunique())
    
    with col3:
        st.metric("Temporadas", df['temporada'].nunique())
    
    with col4:
        st.metric("Meses", df['mes'].nunique())
    
    st.markdown("**Equipos disponibles:**")
    for team in sorted(df['equipo'].unique()):
        team_games = len(df[df['equipo'] == team])
        team_rank = df[df['equipo'] == team]['team_academic_rank'].iloc[0]
        st.markdown(f"- **{team}**: {team_games} partidos | Academic Rank: #{team_rank}")

st.markdown("---")

# ============================================
# CONTROLES INTERACTIVOS
# ============================================
st.markdown("## 🎛️ Controles de Análisis")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### Selección de Equipos y Temporadas")
    
    # Selector de equipos
    all_teams = sorted(df['equipo'].unique())
    
    col1, col2 = st.columns(2)
    
    with col1:
        select_all_teams = st.checkbox("Seleccionar todos los equipos", value=True)
        
        if select_all_teams:
            selected_teams = all_teams
        else:
            selected_teams = st.multiselect(
                "Equipos a comparar:",
                options=all_teams,
                default=[all_teams[0]] if all_teams else []
            )
    
    with col2:
        # Selector de temporadas
        all_seasons = sorted(df['temporada'].unique())
        
        select_all_seasons = st.checkbox("Todas las temporadas", value=True)
        
        if select_all_seasons:
            selected_seasons = all_seasons
        else:
            selected_seasons = st.multiselect(
                "Temporadas:",
                options=all_seasons,
                default=all_seasons
            )

with col_right:
    st.markdown("### Opciones de Visualización")
    
    show_home_away = st.checkbox("Separar Local/Visitante", value=False)
    show_monthly = st.checkbox("Análisis Mensual", value=True)
    show_academic = st.checkbox("Correlación Académica", value=True)

# Botón de actualizar
st.markdown("---")
if st.button("🔄 Actualizar Análisis", type="primary", use_container_width=True):
    st.rerun()

# ============================================
# FILTRAR DATOS
# ============================================
if not selected_teams:
    st.warning("⚠️ Por favor selecciona al menos un equipo")
    st.stop()

if not selected_seasons:
    st.warning("⚠️ Por favor selecciona al menos una temporada")
    st.stop()

# Aplicar filtros
df_filtered = df[
    (df['equipo'].isin(selected_teams)) &
    (df['temporada'].isin(selected_seasons))
].copy()

st.success(f"✅ Analizando {len(df_filtered)} partidos de {len(selected_teams)} equipo(s) en {len(selected_seasons)} temporada(s)")

# ============================================
# GUARDAR EN SESSION STATE
# ============================================
st.session_state['multi_team_data'] = df_filtered
st.session_state['selected_teams'] = selected_teams
st.session_state['selected_seasons'] = selected_seasons
st.session_state['show_home_away'] = show_home_away
st.session_state['show_monthly'] = show_monthly
st.session_state['show_academic'] = show_academic

st.markdown("---")

# ============================================
# RESUMEN RÁPIDO CON RECUADROS Y COLORES
# ============================================
st.markdown("## 📈 Resumen Rápido")

# Función para determinar color según academic rank
def get_academic_rank_color(rank):
    if rank == 1:
        return "#d4edda", "#155724"  # Verde claro, texto verde oscuro
    elif rank <= 41:
        return "#fff3cd", "#856404"  # Amarillo claro, texto amarillo oscuro
    else:
        return "#f8d7da", "#721c24"  # Rojo claro, texto rojo oscuro

cols = st.columns(len(selected_teams))

for i, team in enumerate(selected_teams):
    team_data = df_filtered[df_filtered['equipo'] == team]
    
    wins = len(team_data[team_data['resultado_code'] == 'W'])
    losses = len(team_data[team_data['resultado_code'] == 'L'])
    ties = len(team_data[team_data['resultado_code'] == 'T'])
    total = len(team_data)
    
    win_pct = (wins / total * 100) if total > 0 else 0
    
    # Academic rank y color
    academic_rank = team_data['team_academic_rank'].iloc[0]
    bg_color, text_color = get_academic_rank_color(academic_rank)
    
    with cols[i]:
        # Crear container con borde para cada equipo
        with st.container():
            st.markdown(f"""
                <div style='
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #e0e0e0;
                    background-color: #f8f9fa;
                    margin-bottom: 10px;
                '>
                    <h3 style='margin-top: 0; color: #1f77b4;'>{team}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Partidos", total)
                st.metric("Victorias", wins, delta=f"{win_pct:.1f}%")
            
            with col2:
                st.metric("Derrotas", losses)
                st.metric("Empates", ties)
            
            # Academic rank con color según posición
            st.markdown(f"""
                <div style='
                    padding: 10px;
                    border-radius: 5px;
                    background-color: {bg_color};
                    color: {text_color};
                    text-align: center;
                    font-weight: bold;
                    margin-top: 10px;
                '>
                    🎓 Academic Rank: #{academic_rank}
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# GRÁFICOS DINÁMICOS
# ============================================
st.markdown("## 📊 Visualizaciones Dinámicas")

# Tabs para diferentes análisis
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Win Rate Timeline",
    "🏠 Home vs Away",
    "⚽ Goals Analysis",
    "📅 Monthly Performance"
])

# ============================================
# TAB 1: WIN RATE TIMELINE
# ============================================
with tab1:
    st.markdown("### 📈 Win Rate por Temporada")
    st.markdown("Evolución del porcentaje de victorias a lo largo de las temporadas")
    
    # Calcular win rate por equipo y temporada
    win_rate_data = []
    
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        for season in selected_seasons:
            season_data = team_data[team_data['temporada'] == season]
            
            if len(season_data) > 0:
                wins = len(season_data[season_data['resultado_code'] == 'W'])
                total = len(season_data)
                win_pct = (wins / total * 100) if total > 0 else 0
                
                win_rate_data.append({
                    'Equipo': team,
                    'Temporada': season,
                    'Win %': win_pct,
                    'Victorias': wins,
                    'Total': total
                })
    
    if win_rate_data:
        df_win_rate = pd.DataFrame(win_rate_data)
        
        # Crear gráfico de líneas
        fig_winrate = px.line(
            df_win_rate,
            x='Temporada',
            y='Win %',
            color='Equipo',
            markers=True,
            title='Evolución de Win Rate por Temporada',
            labels={'Win %': 'Win Rate (%)', 'Temporada': 'Temporada'},
            hover_data=['Victorias', 'Total']
        )
        
        # Agregar bandas de color de fondo para zonas de rendimiento
        # Zona ROJA (Necesita mejorar): 0-45%
        fig_winrate.add_hrect(
            y0=0, y1=45,
            fillcolor="red", opacity=0.15,
            layer="below", line_width=0,
            annotation_text="Necesita Mejorar", 
            annotation_position="left",
            annotation=dict(font_size=10, font_color="darkred")
        )
        
        # Zona AMARILLA (Regular): 45-55%
        fig_winrate.add_hrect(
            y0=45, y1=55,
            fillcolor="yellow", opacity=0.15,
            layer="below", line_width=0,
            annotation_text="Regular", 
            annotation_position="left",
            annotation=dict(font_size=10, font_color="orange")
        )
        
        # Zona VERDE (Exitoso): 55-100%
        fig_winrate.add_hrect(
            y0=55, y1=100,
            fillcolor="green", opacity=0.15,
            layer="below", line_width=0,
            annotation_text="Exitoso", 
            annotation_position="left",
            annotation=dict(font_size=10, font_color="darkgreen")
        )
        
        fig_winrate.update_traces(mode='lines+markers', line=dict(width=3), marker=dict(size=10))
        fig_winrate.update_layout(
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            yaxis=dict(range=[0, 85])  # Ajustado para que quepa Fullerton (~77%)
        )
        
        st.plotly_chart(fig_winrate, use_container_width=True)
        
        # Mostrar tabla de datos
        with st.expander("📋 Ver datos detallados"):
            st.dataframe(
                df_win_rate.pivot(index='Temporada', columns='Equipo', values='Win %').round(1),
                use_container_width=True
            )
    else:
        st.warning("No hay suficientes datos para generar el gráfico")

# ============================================
# TAB 2: HOME VS AWAY
# ============================================
with tab2:
    st.markdown("### 🏠 Rendimiento Local vs Visitante")
    st.markdown("Comparación de win rate cuando juegan en casa vs fuera")
    
    # Calcular win rate por equipo y venue
    home_away_data = []
    
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        # Local (home_advantage = 1)
        home_data = team_data[team_data['home_advantage'] == 1]
        home_wins = len(home_data[home_data['resultado_code'] == 'W'])
        home_total = len(home_data)
        home_win_pct = (home_wins / home_total * 100) if home_total > 0 else 0
        
        # Visitante (home_advantage = 0)
        away_data = team_data[team_data['home_advantage'] == 0]
        away_wins = len(away_data[away_data['resultado_code'] == 'W'])
        away_total = len(away_data)
        away_win_pct = (away_wins / away_total * 100) if away_total > 0 else 0
        
        home_away_data.append({
            'Equipo': team,
            'Tipo': 'Local',
            'Win %': home_win_pct,
            'Victorias': home_wins,
            'Total': home_total
        })
        
        home_away_data.append({
            'Equipo': team,
            'Tipo': 'Visitante',
            'Win %': away_win_pct,
            'Victorias': away_wins,
            'Total': away_total
        })
    
    if home_away_data:
        df_home_away = pd.DataFrame(home_away_data)
        
        # Crear gráfico de barras agrupadas
        fig_home_away = px.bar(
            df_home_away,
            x='Equipo',
            y='Win %',
            color='Tipo',
            barmode='group',
            title='Win Rate: Local vs Visitante',
            labels={'Win %': 'Win Rate (%)', 'Equipo': 'Equipo'},
            hover_data=['Victorias', 'Total'],
            color_discrete_map={'Local': '#2ecc71', 'Visitante': '#e74c3c'},
            text='Win %'  # Agregar valores en las barras
        )
        
        # Formatear texto en las barras (sin decimales)
        fig_home_away.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        
        # Agregar bandas de color de fondo (mismos rangos que Tab 1)
        fig_home_away.add_hrect(
            y0=0, y1=40,
            fillcolor="red", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_home_away.add_hrect(
            y0=40, y1=60,
            fillcolor="yellow", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_home_away.add_hrect(
            y0=60, y1=100,
            fillcolor="green", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_home_away.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            yaxis=dict(range=[0, 75])
        )
        
        st.plotly_chart(fig_home_away, use_container_width=True)
        
        # Análisis de home advantage
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏠 Home Advantage Index")
            for team in selected_teams:
                team_df = df_home_away[df_home_away['Equipo'] == team]
                home_pct = team_df[team_df['Tipo'] == 'Local']['Win %'].values[0]
                away_pct = team_df[team_df['Tipo'] == 'Visitante']['Win %'].values[0]
                advantage = home_pct - away_pct
                
                color = "green" if advantage > 0 else "red"
                st.markdown(f"**{team}:** :{'green' if advantage > 0 else 'red'}[{advantage:+.1f}%]")
        
        with col2:
            with st.expander("📋 Ver datos detallados"):
                st.dataframe(df_home_away, use_container_width=True)
    else:
        st.warning("No hay suficientes datos para generar el gráfico")

# ============================================
# TAB 3: GOALS ANALYSIS
# ============================================
with tab3:
    st.markdown("### ⚽ Análisis de Goles")
    st.markdown("Goles a favor y en contra por equipo")
    
    # Calcular goles totales por equipo
    goals_data = []
    
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        total_goals_for = team_data['goals_for'].sum()
        total_goals_against = team_data['goals_against'].sum()
        games = len(team_data)
        avg_goals_for = total_goals_for / games if games > 0 else 0
        avg_goals_against = total_goals_against / games if games > 0 else 0
        
        goals_data.append({
            'Equipo': team,
            'Tipo': 'Goles a Favor',
            'Promedio': avg_goals_for,
            'Total': total_goals_for
        })
        
        goals_data.append({
            'Equipo': team,
            'Tipo': 'Goles en Contra',
            'Promedio': avg_goals_against,
            'Total': total_goals_against
        })
    
    if goals_data:
        df_goals = pd.DataFrame(goals_data)
        
        # Gráfico de barras agrupadas
        fig_goals = px.bar(
            df_goals,
            x='Equipo',
            y='Promedio',
            color='Tipo',
            barmode='group',
            title='Promedio de Goles por Partido',
            labels={'Promedio': 'Goles por Partido', 'Equipo': 'Equipo'},
            hover_data=['Total'],
            color_discrete_map={'Goles a Favor': '#3498db', 'Goles en Contra': '#e74c3c'},
            text='Promedio'  # Agregar valores en las barras
        )
        
        # Formatear texto en las barras (1 decimal para goles)
        fig_goals.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        
        # Agregar bandas de color de fondo (basadas en goles por partido)
        fig_goals.add_hrect(
            y0=0, y1=1.0,
            fillcolor="red", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_goals.add_hrect(
            y0=1.0, y1=2.0,
            fillcolor="yellow", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_goals.add_hrect(
            y0=2.0, y1=5.0,
            fillcolor="green", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_goals.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            yaxis=dict(range=[0, 4])
        )
        
        st.plotly_chart(fig_goals, use_container_width=True)
        
        # Métricas adicionales
        st.markdown("#### ⚽ Métricas Ofensivas y Defensivas")
        
        cols = st.columns(len(selected_teams))
        
        for i, team in enumerate(selected_teams):
            team_df = df_goals[df_goals['Equipo'] == team]
            goals_for = team_df[team_df['Tipo'] == 'Goles a Favor']['Promedio'].values[0]
            goals_against = team_df[team_df['Tipo'] == 'Goles en Contra']['Promedio'].values[0]
            goal_diff = goals_for - goals_against
            
            with cols[i]:
                st.markdown(f"**{team}**")
                st.metric("⚽ Goles/Partido", f"{goals_for:.2f}")
                st.metric("🛡️ Recibidos/Partido", f"{goals_against:.2f}")
                st.metric("📊 Diferencia", f"{goal_diff:+.2f}", 
                         delta=f"{'Positiva' if goal_diff > 0 else 'Negativa'}")
    else:
        st.warning("No hay suficientes datos para generar el gráfico")

# ============================================
# TAB 4: MONTHLY PERFORMANCE
# ============================================
with tab4:
    st.markdown("### 📅 Rendimiento Mensual - Academic Periodization")
    st.markdown("Análisis de rendimiento por mes para detectar efectos de periodos académicos")
    
    # Calcular win rate por mes
    monthly_data = []
    
    # Orden de meses (SOLO temporada de soccer: Ago-Dic)
    month_order = ['August', 'September', 'October', 'November', 'December']
    
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        for month in month_order:
            month_data = team_data[team_data['mes'] == month]
            
            if len(month_data) > 0:
                wins = len(month_data[month_data['resultado_code'] == 'W'])
                total = len(month_data)
                win_pct = (wins / total * 100) if total > 0 else 0
                
                monthly_data.append({
                    'Equipo': team,
                    'Mes': month,
                    'Win %': win_pct,
                    'Partidos': total
                })
    
    if monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        
        # Crear gráfico de líneas
        fig_monthly = px.line(
            df_monthly,
            x='Mes',
            y='Win %',
            color='Equipo',
            markers=True,
            title='Rendimiento Mensual - Detección de Academic Periodization',
            labels={'Win %': 'Win Rate (%)', 'Mes': 'Mes'},
            hover_data=['Partidos'],
            category_orders={'Mes': month_order}
        )
        
        # Agregar bandas de color de fondo (mismos rangos que Tab 1)
        fig_monthly.add_hrect(
            y0=0, y1=40,
            fillcolor="red", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_monthly.add_hrect(
            y0=40, y1=60,
            fillcolor="yellow", opacity=0.15,
            layer="below", line_width=0
        )
        
        fig_monthly.add_hrect(
            y0=60, y1=100,
            fillcolor="green", opacity=0.15,
            layer="below", line_width=0
        )
        
        # Agregar zona sombreada para periodos de exámenes (Oct final - Nov)
        fig_monthly.add_vrect(
            x0=2.5, x1=3.5,  # Final de October - November
            fillcolor="orange", opacity=0.2,
            layer="above", line_width=2,
            line_dash="dash", line_color="red",
            annotation_text="📚 Periodo de Exámenes", 
            annotation_position="top left",
            annotation=dict(font_size=12, font_color="darkred")
        )
        
        fig_monthly.update_traces(mode='lines+markers', line=dict(width=3), marker=dict(size=10))
        fig_monthly.update_layout(
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            yaxis=dict(range=[0, 75])
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Análisis de caída en Noviembre/Diciembre
        st.markdown("#### 🎓 Análisis de Academic Periodization")
        
        st.info("""
        **Hipótesis:** Los equipos con mejor ranking académico experimentan decline en 
        rendimiento durante periodos de exámenes (Noviembre, Diciembre).
        """)
        
        # Calcular decline por equipo
        decline_data = []
        
        for team in selected_teams:
            team_monthly = df_monthly[df_monthly['Equipo'] == team]
            
            # Octubre (antes)
            oct_data = team_monthly[team_monthly['Mes'] == 'October']
            oct_win = oct_data['Win %'].values[0] if len(oct_data) > 0 else 0
            
            # Noviembre (durante)
            nov_data = team_monthly[team_monthly['Mes'] == 'November']
            nov_win = nov_data['Win %'].values[0] if len(nov_data) > 0 else 0
            
            # Calcular decline
            decline = oct_win - nov_win
            
            # Academic rank
            academic_rank = df_filtered[df_filtered['equipo'] == team]['team_academic_rank'].iloc[0]
            
            decline_data.append({
                'Equipo': team,
                'Academic Rank': academic_rank,
                'Octubre Win%': oct_win,
                'Noviembre Win%': nov_win,
                'Decline': decline
            })
        
        df_decline = pd.DataFrame(decline_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Decline en Noviembre:**")
            for _, row in df_decline.iterrows():
                color = "red" if row['Decline'] > 0 else "green"
                st.markdown(
                    f"**{row['Equipo']}** (Rank #{row['Academic Rank']}): "
                    f":{color}[{row['Decline']:+.1f}%]"
                )
        
        with col2:
            with st.expander("📋 Ver datos detallados"):
                st.dataframe(df_decline, use_container_width=True)
    else:
        st.warning("No hay suficientes datos para generar el gráfico")

st.markdown("---")

# ============================================
# MÉTRICAS AVANZADAS
# ============================================
st.markdown("## 🎯 Métricas Avanzadas")
st.markdown("Análisis profundo de patrones y correlaciones")

# ============================================
# MÉTRICA 1: OPPONENT QUALITY IMPACT
# ============================================
with st.expander("📊 Opponent Quality Impact", expanded=False):
    st.markdown("### Impacto de la Calidad del Rival")
    
    # Calcular win rate por rangos de opponent quality
    df_filtered['opp_quality_range'] = pd.cut(
        df_filtered['opponent_quality'], 
        bins=[0, 0.4, 0.5, 1.0], 
        labels=['Débil (<0.4)', 'Medio (0.4-0.5)', 'Fuerte (>0.5)']
    )
    
    quality_impact = []
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        for quality_range in ['Débil (<0.4)', 'Medio (0.4-0.5)', 'Fuerte (>0.5)']:
            range_data = team_data[team_data['opp_quality_range'] == quality_range]
            
            if len(range_data) > 0:
                wins = len(range_data[range_data['resultado_code'] == 'W'])
                total = len(range_data)
                win_pct = (wins / total * 100) if total > 0 else 0
                
                quality_impact.append({
                    'Equipo': team,
                    'Rival': quality_range,
                    'Win %': win_pct,
                    'Partidos': total
                })
    
    if quality_impact:
        df_quality = pd.DataFrame(quality_impact)
        
        fig_quality = px.bar(
            df_quality,
            x='Rival',
            y='Win %',
            color='Equipo',
            barmode='group',
            title='Win Rate según Calidad del Rival',
            hover_data=['Partidos'],
            text='Win %'  # Agregar valores en las barras
        )
        
        # Formatear texto en las barras (sin decimales)
        fig_quality.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        
        fig_quality.update_layout(height=400)
        st.plotly_chart(fig_quality, use_container_width=True)
        
        st.markdown("**Interpretación:** Equipos con mejor performance contra rivales fuertes son más competitivos.")

# ============================================
# MÉTRICA 2: ACADEMIC RANK CORRELATION
# ============================================
with st.expander("🎓 Academic Rank vs Performance", expanded=False):
    st.markdown("### Correlación entre Ranking Académico y Rendimiento Deportivo")
    
    # Calcular win% promedio por equipo
    academic_perf = []
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        wins = len(team_data[team_data['resultado_code'] == 'W'])
        total = len(team_data)
        win_pct = (wins / total * 100) if total > 0 else 0
        
        academic_rank = team_data['team_academic_rank'].iloc[0]
        
        academic_perf.append({
            'Equipo': team,
            'Academic Rank': academic_rank,
            'Win %': win_pct,
            'Partidos': total
        })
    
    df_academic = pd.DataFrame(academic_perf)
    
    # Scatter plot
    fig_academic = px.scatter(
        df_academic,
        x='Academic Rank',
        y='Win %',
        text='Equipo',
        size='Partidos',
        title='Ranking Académico vs Rendimiento Deportivo',
        hover_data=['Partidos']
    )
    
    # Agregar bandas de color de fondo (horizontal - Win%)
    fig_academic.add_hrect(
        y0=0, y1=40,
        fillcolor="red", opacity=0.1,
        layer="below", line_width=0
    )
    
    fig_academic.add_hrect(
        y0=40, y1=60,
        fillcolor="yellow", opacity=0.1,
        layer="below", line_width=0
    )
    
    fig_academic.add_hrect(
        y0=60, y1=100,
        fillcolor="green", opacity=0.1,
        layer="below", line_width=0
    )
    
    # Ajustar posición del texto y layout
    fig_academic.update_traces(textposition='top center', textfont=dict(size=10))
    fig_academic.update_layout(
        height=450,
        yaxis=dict(range=[35, 60]),  # Rango ajustado para que Fullerton quepa
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_academic, use_container_width=True)
    
    # Análisis de correlación
    correlation = df_academic['Academic Rank'].corr(df_academic['Win %'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Correlación", f"{correlation:.3f}")
        if correlation < -0.3:
            st.success("✅ Correlación negativa: Mejor académico → Menor rendimiento deportivo")
        elif correlation > 0.3:
            st.info("📈 Correlación positiva: Mejor académico → Mejor rendimiento deportivo")
        else:
            st.warning("➡️ Sin correlación significativa")
    
    with col2:
        st.markdown("**Hipótesis TFM:**")
        st.markdown("Los equipos con mejor ranking académico (IVC #1) experimentan más presión académica, afectando rendimiento deportivo.")

# ============================================
# MÉTRICA 3: CONSISTENCY SCORE
# ============================================
with st.expander("📉 Consistency Score", expanded=False):
    st.markdown("### Consistencia de Rendimiento por Equipo")
    
    consistency_data = []
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        # Calcular desviación estándar de goles
        goals_std = team_data['goals_for'].std()
        goals_mean = team_data['goals_for'].mean()
        
        # Coefficient of variation (CV)
        cv = (goals_std / goals_mean * 100) if goals_mean > 0 else 0
        
        consistency_data.append({
            'Equipo': team,
            'Goles Promedio': goals_mean,
            'Desviación Estándar': goals_std,
            'Coef. Variación (%)': cv
        })
    
    df_consistency = pd.DataFrame(consistency_data)
    
    # Gráfico de barras
    fig_consistency = px.bar(
        df_consistency,
        x='Equipo',
        y='Coef. Variación (%)',
        title='Consistencia de Goles (menor = más consistente)',
        color='Coef. Variación (%)',
        color_continuous_scale='RdYlGn_r',
        text='Coef. Variación (%)'  # Agregar valores en las barras
    )
    
    # Formatear texto en las barras (sin decimales)
    fig_consistency.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    
    fig_consistency.update_layout(
        height=400,
        yaxis=dict(range=[0, 75])  # Ajustado para que los valores quepan arriba
    )
    st.plotly_chart(fig_consistency, use_container_width=True)
    
    # Tabla de datos
    st.dataframe(df_consistency.style.format({
        'Goles Promedio': '{:.2f}',
        'Desviación Estándar': '{:.2f}',
        'Coef. Variación (%)': '{:.1f}'
    }), use_container_width=True)
    
    st.markdown("**Interpretación:** Coeficiente de variación bajo indica equipo predecible y consistente.")

# ============================================
# MÉTRICA 4: HOME ADVANTAGE INDEX DETALLADO
# ============================================
with st.expander("🏠 Home Advantage Index Detallado", expanded=False):
    st.markdown("### Ventaja de Jugar en Casa por Equipo")
    
    home_adv_data = []
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        
        # Local
        home_games = team_data[team_data['home_advantage'] == 1]
        home_wins = len(home_games[home_games['resultado_code'] == 'W'])
        home_total = len(home_games)
        home_win_pct = (home_wins / home_total * 100) if home_total > 0 else 0
        
        # Visitante
        away_games = team_data[team_data['home_advantage'] == 0]
        away_wins = len(away_games[away_games['resultado_code'] == 'W'])
        away_total = len(away_games)
        away_win_pct = (away_wins / away_total * 100) if away_total > 0 else 0
        
        # Index
        ha_index = home_win_pct - away_win_pct
        
        home_adv_data.append({
            'Equipo': team,
            'Local Win%': home_win_pct,
            'Visitante Win%': away_win_pct,
            'Home Advantage Index': ha_index,
            'Partidos Local': home_total,
            'Partidos Visitante': away_total
        })
    
    df_home_adv = pd.DataFrame(home_adv_data)
    
    # Redondear Home Advantage Index para visualización limpia
    df_home_adv['Home Advantage Index'] = df_home_adv['Home Advantage Index'].round(0)
    
    # Gráfico de índice
    fig_ha_index = px.bar(
        df_home_adv,
        x='Equipo',
        y='Home Advantage Index',
        title='Home Advantage Index (diferencia Local - Visitante)',
        color='Home Advantage Index',
        color_continuous_scale='RdYlGn',
        text='Home Advantage Index'  # Agregar valores en las barras
    )
    
    # Formatear texto en las barras (con signo +/-)
    fig_ha_index.update_traces(texttemplate='%{text:+.0f}%', textposition='outside')
    
    fig_ha_index.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_ha_index.update_layout(
        height=400,
        yaxis=dict(range=[-10, 20])  # Ajustado para que valores negativos y positivos quepan
    )
    st.plotly_chart(fig_ha_index, use_container_width=True)
    
    # Tabla detallada
    st.dataframe(df_home_adv.style.format({
        'Local Win%': '{:.1f}%',
        'Visitante Win%': '{:.1f}%',
        'Home Advantage Index': '{:+.1f}%'
    }).background_gradient(subset=['Home Advantage Index'], cmap='RdYlGn', vmin=-30, vmax=30),
    use_container_width=True)
    
    st.markdown("**Interpretación:** Índice positivo indica fuerte ventaja local. Índice negativo sugiere problemas en casa.")

# ============================================
# ANÁLISIS CON IA (OPENAI)
# ============================================
st.markdown("---")
st.markdown("## 🤖 Análisis con Inteligencia Artificial")
st.markdown("Insights generados automáticamente usando OpenAI")

# Verificar API Key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ No se encontró OPENAI_API_KEY. Configúrala en el archivo .env para habilitar análisis con IA.")
else:
    # ============================================
    # PREPARAR CONTEXTO PARA IA
    # ============================================
    
    # Resumen de datos para IA
    ai_context = {
        'equipos': selected_teams,
        'temporadas': selected_seasons,
        'total_partidos': len(df_filtered),
        'resumen_equipos': []
    }
    
    for team in selected_teams:
        team_data = df_filtered[df_filtered['equipo'] == team]
        wins = len(team_data[team_data['resultado_code'] == 'W'])
        losses = len(team_data[team_data['resultado_code'] == 'L'])
        ties = len(team_data[team_data['resultado_code'] == 'T'])
        total = len(team_data)
        win_pct = (wins / total * 100) if total > 0 else 0
        
        academic_rank = int(team_data['team_academic_rank'].iloc[0])  # Convertir a int nativo
        
        ai_context['resumen_equipos'].append({
            'nombre': team,
            'academic_rank': academic_rank,
            'partidos': int(total),  # Convertir a int nativo
            'victorias': int(wins),  # Convertir a int nativo
            'derrotas': int(losses),  # Convertir a int nativo
            'empates': int(ties),  # Convertir a int nativo
            'win_percentage': float(win_pct)  # Convertir a float nativo
        })
    
    # ============================================
    # ANÁLISIS 1: COMPARATIVE ANALYSIS
    # ============================================
    with st.expander("📊 Análisis Comparativo de Equipos", expanded=True):
        st.markdown("### Análisis Generado por IA")
        
        if st.button("🔄 Generar Análisis Comparativo", key="btn_comparative"):
            with st.spinner("Analizando datos..."):
                try:
                    import openai
                    
                    openai.api_key = api_key
                    
                    prompt = f"""Eres un analista deportivo experto en fútbol universitario. Analiza los siguientes equipos de la Orange Empire Conference:

Datos:
{json.dumps(ai_context, indent=2)}

Proporciona un análisis comparativo breve (máximo 200 palabras) que incluya:
1. Identificar el equipo con mejor rendimiento general
2. Comparar rendimiento académico vs deportivo
3. Identificar tendencias o patrones destacables
4. Dar 2 insights clave

Responde en español de forma profesional y concisa."""

                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Eres un analista deportivo experto en soccer universitario."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=400,
                        temperature=0.7
                    )
                    
                    analysis = response.choices[0].message['content']
                    st.markdown(analysis)
                    
                except Exception as e:
                    st.error(f"Error al generar análisis: {str(e)}")
    
    # ============================================
    # ANÁLISIS 2: ACADEMIC PERIODIZATION INSIGHTS
    # ============================================
    with st.expander("🎓 Validación de Academic Periodization", expanded=False):
        st.markdown("### Análisis de Hipótesis TFM")
        
        if st.button("🔄 Validar Hipótesis con IA", key="btn_academic"):
            with st.spinner("Analizando academic periodization..."):
                try:
                    # Calcular datos mensuales para IA
                    monthly_data = []
                    for team in selected_teams:
                        team_data = df_filtered[df_filtered['equipo'] == team]
                        academic_rank = int(team_data['team_academic_rank'].iloc[0])  # Convertir a int nativo
                        
                        for month in ['October', 'November', 'December']:
                            month_games = team_data[team_data['mes'] == month]
                            if len(month_games) > 0:
                                wins = len(month_games[month_games['resultado_code'] == 'W'])
                                total = len(month_games)
                                win_pct = (wins / total * 100) if total > 0 else 0
                                
                                monthly_data.append({
                                    'equipo': team,
                                    'academic_rank': academic_rank,
                                    'mes': month,
                                    'win_percentage': float(win_pct)  # Convertir a float nativo
                                })
                    
                    import openai
                    
                    openai.api_key = api_key
                    
                    prompt = f"""Eres un investigador académico experto en rendimiento deportivo estudiantil. 

Hipótesis: "Los equipos con mejor ranking académico experimentan decline en rendimiento durante periodos de exámenes (Noviembre-Diciembre)"

Datos mensuales:
{json.dumps(monthly_data, indent=2)}

Analiza:
1. ¿Hay evidencia de decline en Octubre→Noviembre→Diciembre?
2. ¿Los equipos con mejor ranking académico (menor número) muestran más decline?
3. ¿La hipótesis es válida o refutada?
4. ¿Qué factores adicionales podrían influir?

Responde en español de forma académica pero clara (máximo 250 palabras)."""

                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Eres un investigador académico en ciencias del deporte."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=450,
                        temperature=0.7
                    )
                    
                    analysis = response.choices[0].message['content']
                    st.markdown(analysis)
                    
                except Exception as e:
                    st.error(f"Error al validar hipótesis: {str(e)}")
    
    # ============================================
    # ANÁLISIS 3: STRATEGIC RECOMMENDATIONS
    # ============================================
    with st.expander("💡 Recomendaciones Estratégicas", expanded=False):
        st.markdown("### Consejos para Coaches")
        
        if st.button("🔄 Generar Recomendaciones", key="btn_recommendations"):
            with st.spinner("Generando recomendaciones estratégicas..."):
                try:
                    import openai
                    
                    openai.api_key = api_key
                    
                    prompt = f"""Eres un coach experimentado de fútbol universitario. Basándote en estos datos:

{json.dumps(ai_context, indent=2)}

Proporciona 3-4 recomendaciones estratégicas específicas para cada equipo, considerando:
- Su rendimiento actual
- Su ranking académico
- Fortalezas y debilidades observadas

Formato:
**[Nombre del Equipo]**
- Recomendación 1
- Recomendación 2

Máximo 250 palabras. Responde en español."""

                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Eres un coach experimentado de soccer universitario."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=450,
                        temperature=0.8
                    )
                    
                    recommendations = response.choices[0].message['content']
                    st.markdown(recommendations)
                    
                except Exception as e:
                    st.error(f"Error al generar recomendaciones: {str(e)}")

st.markdown("---")

st.markdown("---")
st.caption("Multi-Team Soccer Analytics | Powered by Streamlit + OpenAI")