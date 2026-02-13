"""
============================================
PROCESADOR DE DATOS DE EQUIPOS
============================================
Convierte datos crudos de 3C2A Sports a CSV estructurado
"""

import re
import pandas as pd
from datetime import datetime
from docx import Document

def extract_matches_from_text(text, team_name, season):
    """
    Extrae partidos del texto crudo
    
    Pattern esperado:
    "Tue. 26 at Bakersfield T, 0-0 Final"
    "Fri. 29 vs West Valley @ Mt.Sac L, 3-0 Final"
    """
    matches = []
    
    # Pattern mejorado para capturar diferentes formatos
    # Captura: día, at/vs, oponente, resultado (W/L/T), marcador
    pattern = r'(\w+\.\s+\d+)\s+(at|vs)\s+([^@\n]+?)(?:@[^WLTF]+?)?\s+([WLT]),\s+(\d+-\d+)\s+Final'
    
    for match in re.finditer(pattern, text, re.MULTILINE):
        day_str = match.group(1)      # "Tue. 26"
        location = match.group(2)      # "at" o "vs"
        opponent = match.group(3).strip()  # "Bakersfield"
        result = match.group(4)        # "W", "L", o "T"
        score = match.group(5)         # "3-2"
        
        # Determinar local/visitante
        venue = "Visitante" if location == "at" else "Local"
        
        # Parsear marcador
        goals_for, goals_against = map(int, score.split('-'))
        
        # Extraer mes (del contexto previo en el texto)
        month = extract_month_from_context(text, match.start())
        
        # Crear registro
        match_data = {
            'equipo': team_name,
            'oponente': opponent,
            'local_visitante': venue,
            'resultado': result,
            'marcador': score,
            'goles_favor': goals_for,
            'goles_contra': goals_against,
            'mes': month,
            'temporada': season
        }
        
        matches.append(match_data)
    
    return matches

def extract_month_from_context(text, position):
    """
    Extrae el mes del contexto previo al partido
    """
    # Buscar hacia atrás el mes más cercano
    months_spanish = {
        'Agosto': 'August',
        'Septiembre': 'September',
        'Octubre': 'October',
        'Noviembre': 'November',
        'Diciembre': 'December',
        'Enero': 'January',
        'Febrero': 'February',
        'Marzo': 'March',
        'Abril': 'April',
        'Mayo': 'May'
    }
    
    # Buscar en texto previo (últimos 200 caracteres)
    context = text[max(0, position-200):position]
    
    for spanish, english in months_spanish.items():
        if spanish in context:
            return english
    
    return "Unknown"

def process_word_document(docx_path):
    """
    Procesa documento Word completo con datos de múltiples equipos
    
    Estructura esperada:
    === EQUIPO NAME ===
    Temporada 2025-2026
    [partidos...]
    Temporada 2024-2025
    [partidos...]
    """
    doc = Document(docx_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    
    all_matches = []
    
    # Dividir por equipos
    teams_sections = re.split(r'===\s*([A-Z\s]+)\s*===', full_text)
    
    # Procesar cada equipo
    for i in range(1, len(teams_sections), 2):
        team_name = teams_sections[i].strip()
        team_text = teams_sections[i+1]
        
        print(f"\n🔍 Procesando: {team_name}")
        
        # Dividir por temporadas
        seasons = re.split(r'Temporada\s+(\d{4}-\d{4})', team_text)
        
        for j in range(1, len(seasons), 2):
            season = seasons[j]
            season_text = seasons[j+1]
            
            print(f"  📅 Temporada: {season}")
            
            # Extraer partidos
            matches = extract_matches_from_text(season_text, team_name, season)
            all_matches.extend(matches)
            
            print(f"    ✅ {len(matches)} partidos extraídos")
    
    # Crear DataFrame
    df = pd.DataFrame(all_matches)
    
    print(f"\n✅ Total de partidos extraídos: {len(df)}")
    
    return df

def add_advanced_features(df):
    """
    Agrega features avanzadas al DataFrame
    """
    print("\n🔧 Agregando features avanzadas...")
    
    # 1. Calcular opponent_quality (win% histórico)
    opponent_stats = df.groupby('oponente').agg({
        'resultado': lambda x: (x == 'W').sum() / len(x)
    }).rename(columns={'resultado': 'opponent_quality'})
    
    df = df.merge(
        opponent_stats, 
        left_on='oponente', 
        right_index=True, 
        how='left'
    )
    
    # 2. Agregar team_academic_rank
    academic_ranks = {
        'Irvine Valley': 1,
        'Fullerton': 41,
        'Santa Ana': 77,  # Estimado
        'Cypress': 77     # Estimado
    }
    
    df['team_academic_rank'] = df['equipo'].map(academic_ranks)
    
    # 3. Convertir mes a número
    month_map = {
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5
    }
    
    df['mes_num'] = df['mes'].map(month_map)
    
    print("✅ Features agregadas:")
    print("   - opponent_quality (win% histórico)")
    print("   - team_academic_rank")
    print("   - mes_num")
    
    return df

def main(docx_path, output_csv='multi_team_data.csv'):
    """
    Función principal de procesamiento
    """
    print("="*60)
    print("🏃 PROCESANDO DATOS DE EQUIPOS")
    print("="*60)
    
    # Procesar documento
    df = process_word_document(docx_path)
    
    # Agregar features avanzadas
    df = add_advanced_features(df)
    
    # Guardar CSV
    output_path = f"/home/claude/Soccer_Analytics_Streamlit/data/{output_csv}"
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n✅ CSV guardado en: {output_path}")
    print(f"📊 Total de registros: {len(df)}")
    
    # Mostrar resumen por equipo
    print("\n📈 RESUMEN POR EQUIPO:")
    print(df.groupby('equipo').size())
    
    return df

if __name__ == "__main__":
    # Ejemplo de uso
    docx_path = "/mnt/user-data/uploads/Datos_equipos_TFM.docx"
    df = main(docx_path)
