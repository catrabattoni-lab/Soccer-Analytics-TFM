"""
Parser simple para datos de equipos
Extrae información básica línea por línea
"""

import re
import pandas as pd

def parse_match_line(line):
    """
    Parsea una línea de partido
    
    Formatos esperados:
    "Tue. 26 at Bakersfield T, 0-0 Final"
    "Fri. 29 vs West Valley @ Mt.Sac L, 3-0 Final"
    """
    # Pattern para capturar datos
    pattern = r'(\d+)\s+(at|vs)\s+([^@\n]+?)(?:@[^WLTF]+?)?\s+([WLT]),\s+(\d+-\d+)'
    
    match = re.search(pattern, line)
    
    if match:
        day = match.group(1)
        location = match.group(2)
        opponent = match.group(3).strip()
        result = match.group(4)
        score = match.group(5)
        
        goals_for, goals_against = map(int, score.split('-'))
        
        return {
            'day': day,
            'location': location,
            'opponent': opponent,
            'result': result,
            'score': score,
            'goals_for': goals_for,
            'goals_against': goals_against
        }
    
    return None

def process_text_file(text, team_name):
    """
    Procesa texto completo de un equipo
    """
    matches = []
    current_season = None
    current_month = None
    
    lines = text.split('\n')
    
    for line in lines:
        # Detectar temporada
        season_match = re.search(r'Temporada\s+(\d{4}-\d{4})', line)
        if season_match:
            current_season = season_match.group(1)
            continue
        
        # Detectar mes
        month_match = re.search(r'(Agosto|Septiembre|Octubre|Noviembre|Diciembre|Enero|Febrero|Marzo|Abril|Mayo)', line)
        if month_match:
            current_month = month_match.group(1)
            continue
        
        # Parsear partido
        match_data = parse_match_line(line)
        if match_data and current_season:
            match_data['team'] = team_name
            match_data['season'] = current_season
            match_data['month'] = current_month or 'Unknown'
            matches.append(match_data)
    
    return matches

# Test
if __name__ == "__main__":
    test_text = """
    Temporada 2025-2026
    Agosto
    Tue. 26 at Bakersfield T, 0-0 Final
    Fri. 29 vs West Valley L, 3-0 Final
    """
    
    result = process_text_file(test_text, "Fullerton")
    print(f"Extraídos: {len(result)} partidos")
    for r in result:
        print(r)
