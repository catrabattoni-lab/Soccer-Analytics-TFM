"""
============================================
VISUALIZACIONES AVANZADAS
============================================

Módulo para crear gráficos interactivos con Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from .config import PLOTLY_CONFIG, PLOTLY_TEMPLATE, COLORS

class AdvancedVisualizations:
    """
    Clase para crear visualizaciones avanzadas
    """
    
    def __init__(self):
        self.config = PLOTLY_CONFIG
        self.template = PLOTLY_TEMPLATE
        self.colors = COLORS
    
    def create_radar_chart(self, team_name, stats_dict):
        """
        Crea un gráfico de radar para visualizar estadísticas de equipo
        
        Args:
            team_name (str): Nombre del equipo
            stats_dict (dict): Diccionario con estadísticas
                               Ej: {'Ataque': 85, 'Defensa': 70, ...}
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        categories = list(stats_dict.keys())
        values = list(stats_dict.values())
        
        # Cerrar el polígono
        categories_closed = categories + [categories[0]]
        values_closed = values + [values[0]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            name=team_name,
            line_color=self.colors['primary'],
            fillcolor=self.colors['secondary'],
            opacity=0.6
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title=f"Análisis de Rendimiento: {team_name}",
            template=self.template,
            height=500
        )
        
        return fig
    
    def create_heatmap(self, data_matrix, x_labels, y_labels, title="Heat Map"):
        """
        Crea un mapa de calor
        
        Args:
            data_matrix (list or np.array): Matriz de datos
            x_labels (list): Etiquetas del eje X
            y_labels (list): Etiquetas del eje Y
            title (str): Título del gráfico
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        fig = go.Figure(data=go.Heatmap(
            z=data_matrix,
            x=x_labels,
            y=y_labels,
            colorscale='RdYlGn',
            text=data_matrix,
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Valor")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="",
            yaxis_title="",
            template=self.template,
            height=500
        )
        
        return fig
    
    def create_comparison_bar(self, team1_name, team1_stats, team2_name, team2_stats):
        """
        Crea un gráfico de barras comparativo entre dos equipos
        
        Args:
            team1_name (str): Nombre del equipo 1
            team1_stats (dict): Estadísticas del equipo 1
            team2_name (str): Nombre del equipo 2
            team2_stats (dict): Estadísticas del equipo 2
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        categories = list(team1_stats.keys())
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name=team1_name,
            x=categories,
            y=list(team1_stats.values()),
            marker_color=self.colors['primary']
        ))
        
        fig.add_trace(go.Bar(
            name=team2_name,
            x=categories,
            y=list(team2_stats.values()),
            marker_color=self.colors['secondary']
        ))
        
        fig.update_layout(
            title=f"Comparación: {team1_name} vs {team2_name}",
            barmode='group',
            xaxis_title="Categoría",
            yaxis_title="Valor",
            template=self.template,
            height=500
        )
        
        return fig
    
    def create_timeline_chart(self, df, x_col, y_col, title="Evolución"):
        """
        Crea un gráfico de línea temporal
        
        Args:
            df (pd.DataFrame): DataFrame con datos
            x_col (str): Nombre de columna para eje X (fechas)
            y_col (str): Nombre de columna para eje Y
            title (str): Título del gráfico
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title,
            markers=True,
            template=self.template
        )
        
        fig.update_traces(
            line_color=self.colors['primary'],
            line_width=3
        )
        
        fig.update_layout(
            xaxis_title="Fecha",
            yaxis_title=y_col,
            height=400
        )
        
        return fig
    
    def create_scatter_plot(self, df, x_col, y_col, color_col=None, title="Scatter Plot"):
        """
        Crea un gráfico de dispersión
        
        Args:
            df (pd.DataFrame): DataFrame con datos
            x_col (str): Columna para eje X
            y_col (str): Columna para eje Y
            color_col (str): Columna para color (opcional)
            title (str): Título del gráfico
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            template=self.template,
            size_max=15
        )
        
        fig.update_traces(marker=dict(size=12))
        
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=500
        )
        
        return fig
    
    def create_pie_chart(self, labels, values, title="Distribución"):
        """
        Crea un gráfico de pastel
        
        Args:
            labels (list): Etiquetas
            values (list): Valores
            title (str): Título del gráfico
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3
        )])
        
        fig.update_layout(
            title=title,
            template=self.template,
            height=400
        )
        
        return fig
    
    def create_box_plot(self, df, y_col, x_col=None, title="Distribución de Datos"):
        """
        Crea un gráfico de caja (box plot)
        
        Args:
            df (pd.DataFrame): DataFrame con datos
            y_col (str): Columna para valores
            x_col (str): Columna para categorías (opcional)
            title (str): Título del gráfico
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        fig = px.box(
            df,
            x=x_col,
            y=y_col,
            title=title,
            template=self.template
        )
        
        fig.update_layout(
            xaxis_title=x_col if x_col else "",
            yaxis_title=y_col,
            height=500
        )
        
        return fig
    
    def create_multi_radar(self, teams_stats):
        """
        Crea un gráfico de radar para comparar múltiples equipos
        
        Args:
            teams_stats (dict): Diccionario con equipos y sus stats
                                Ej: {'Team A': {'Ataque': 85, ...}, 'Team B': {...}}
            
        Returns:
            go.Figure: Gráfico de Plotly
        """
        fig = go.Figure()
        
        # Obtener categorías (asumiendo que todos tienen las mismas)
        first_team = list(teams_stats.keys())[0]
        categories = list(teams_stats[first_team].keys())
        categories_closed = categories + [categories[0]]
        
        # Colores para cada equipo
        colors = [self.colors['primary'], self.colors['secondary'], 
                  self.colors['info'], self.colors['warning']]
        
        for idx, (team_name, stats) in enumerate(teams_stats.items()):
            values = list(stats.values())
            values_closed = values + [values[0]]
            
            color = colors[idx % len(colors)]
            
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                name=team_name,
                line_color=color,
                opacity=0.6
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title="Comparación Multi-Equipo",
            template=self.template,
            height=600
        )
        
        return fig


# ============================================
# FUNCIONES DE AYUDA
# ============================================

def create_radar(team_name, stats):
    """Función auxiliar para crear radar chart"""
    viz = AdvancedVisualizations()
    return viz.create_radar_chart(team_name, stats)


def create_heatmap(data, x_labels, y_labels, title="Heat Map"):
    """Función auxiliar para crear heat map"""
    viz = AdvancedVisualizations()
    return viz.create_heatmap(data, x_labels, y_labels, title)


def create_comparison(team1_name, team1_stats, team2_name, team2_stats):
    """Función auxiliar para crear comparación"""
    viz = AdvancedVisualizations()
    return viz.create_comparison_bar(team1_name, team1_stats, team2_name, team2_stats)


# ============================================
# TESTING
# ============================================
if __name__ == "__main__":
    print("Testing Visualizations...")
    
    viz = AdvancedVisualizations()
    
    # Test radar chart
    stats = {
        'Ataque': 85,
        'Defensa': 70,
        'Posesión': 75,
        'Pases': 80,
        'Físico': 65
    }
    
    fig = viz.create_radar_chart("Equipo Ejemplo", stats)
    print("✅ Radar chart creado")
    
    # Test heatmap
    data = np.random.randint(0, 100, size=(5, 5))
    fig2 = viz.create_heatmap(data, 
                                ['A', 'B', 'C', 'D', 'E'],
                                ['1', '2', '3', '4', '5'])
    print("✅ Heatmap creado")
    
    print("\n✅ Testing completo")
