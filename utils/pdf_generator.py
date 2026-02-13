from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import pandas as pd


class PDFReportGenerator:
    """
    Generador de reportes PDF para análisis deportivo
    """
    
    def __init__(self, filename="reporte_irvine_valley.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Estilos personalizados
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
        )
    
    def add_title(self, text):
        """Agrega título principal"""
        self.story.append(Paragraph(text, self.title_style))
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_heading(self, text):
        """Agrega subtítulo"""
        self.story.append(Spacer(1, 0.3 * inch))
        self.story.append(Paragraph(text, self.heading_style))
        self.story.append(Spacer(1, 0.1 * inch))
    
    def add_paragraph(self, text):
        """Agrega párrafo de texto"""
        self.story.append(Paragraph(text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.1 * inch))
    
    def add_stats_table(self, data, title=None):
        """
        Agrega tabla de estadísticas
        
        Args:
            data: Lista de listas con los datos [[header], [row1], [row2], ...]
            title: Título opcional para la tabla
        """
        if title:
            self.add_heading(title)
        
        # Crear tabla
        table = Table(data, hAlign='LEFT')
        
        # Estilo de tabla
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3 * inch))
    
    def generate_full_report(self, stored_data):
        """
        Genera reporte completo desde datos del store
        
        Args:
            stored_data: Dict con todos los datos del scraping
        """
        # Extraer información según el tipo de datos
        if not stored_data:
            raise ValueError("No hay datos disponibles")
        
        # Determinar tipo de datos y extraer información
        if 'total_goals' in stored_data and 'players' in stored_data:
            # Es un scraping de estadísticas de equipo
            team_stats = self._extract_team_stats_from_stats(stored_data)
            top_scorers = self._extract_top_scorers(stored_data)
            conference_standings = pd.DataFrame()  # Vacío por ahora
        else:
            # Es otro tipo de datos (calendario, etc)
            raise ValueError("Tipo de datos no soportado para generar PDF")
        
        # Título principal
        self.add_title("📊 Reporte de Temporada<br/>Irvine Valley College - Men's Soccer")
        
        # Fecha del reporte
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.add_paragraph(f"<b>Fecha del reporte:</b> {fecha}")
        self.add_paragraph(f"<b>Temporada:</b> 2024-25")
        
        # Resumen ejecutivo
        self.add_heading("📈 Resumen Ejecutivo")
        self.add_paragraph(f"<b>Equipo:</b> Irvine Valley College")
        self.add_paragraph(f"<b>Goles totales:</b> {stored_data.get('total_goals', 0)}")
        self.add_paragraph(f"<b>Tarjetas totales:</b> {stored_data.get('total_cards', 0)}")
        
        # Top Goleadores
        if not top_scorers.empty:
            self.add_heading("⚽ Top 10 Goleadores")
            
            # Preparar datos para tabla
            scorers_data = [['#', 'Jugador', 'Goles', 'Asistencias', 'Tiros']]
            for idx, row in top_scorers.head(10).iterrows():
                scorers_data.append([
                    str(idx + 1),
                    row.get('nombre', 'N/A'),
                    str(row.get('goles', 0)),
                    str(row.get('asistencias', 0)),
                    str(row.get('tiros', 0))
                ])
            
            self.add_stats_table(scorers_data)
        
        # Nota final
        self.add_heading("📝 Notas")
        self.add_paragraph("Este reporte fue generado automáticamente por el Dashboard IA Deportivo.")
        self.add_paragraph("Los datos fueron extraídos de 3C2A Sports mediante web scraping.")
        
        # Generar PDF
        # Generar PDF
        import os
        
        # Crear carpeta outputs si no existe
        os.makedirs('outputs', exist_ok=True)
        
        output_path = f"outputs/{self.filename}"
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        print(f"📄 Generando PDF: {output_path}")
        self.doc.build(self.story)
        print(f"✅ PDF generado exitosamente")
        
        return output_path
    
    def _extract_team_stats_from_stats(self, stored_data):
        """Extrae estadísticas del equipo desde el formato de scraping"""
        return {
            'total_goals': stored_data.get('total_goals', 0),
            'total_cards': stored_data.get('total_cards', 0),
        }
    
    def _extract_top_scorers(self, stored_data):
        """Extrae top goleadores desde el formato de scraping"""
        players_dict = stored_data.get('players', {})
        
        players_list = []
        for nombre, stats in players_dict.items():
            if stats.get('goles', 0) > 0:
                players_list.append({
                    'nombre': nombre,
                    'goles': stats.get('goles', 0),
                    'asistencias': stats.get('asistencias', 0),
                    'tiros': stats.get('tiros', 0)
                })
        
        # Ordenar por goles
        players_list = sorted(players_list, key=lambda x: x['goles'], reverse=True)
        
        return pd.DataFrame(players_list)