"""
============================================
WEB SCRAPER - 3C2A SPORTS
Scraper completo para Irvine Valley College
============================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

class Scraper3C2A:
    """
    Clase para hacer web scraping de 3C2A Sports
    Especializado en análisis de oponentes de Irvine Valley
    """
    
    def __init__(self):
        self.base_url = "https://3c2asports.org"
        self.irvine_team_id = "pd2msqrhfox3ougx"
        self.irvine_schedule_url = f"{self.base_url}/sports/msoc/2025-26/schedule?teamId={self.irvine_team_id}"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _get_soup(self, url):
        """
        Obtiene el contenido HTML parseado de una URL
        
        Args:
            url (str): URL a scrapear
            
        Returns:
            BeautifulSoup: Objeto parseado o None si falla
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"❌ Error al obtener {url}: {str(e)}")
            return None
    
    def get_irvine_matches(self):
        """
        Obtiene todos los partidos de Irvine Valley College
        
        Returns:
            pd.DataFrame: DataFrame con información de partidos
        """
        print(f"🔍 Obteniendo partidos de Irvine Valley...")
        
        soup = self._get_soup(self.irvine_schedule_url)
        if not soup:
            return pd.DataFrame()
        
        matches_data = []
        
        # Buscar todos los meses
        months = soup.find_all('span', class_='month-title')
        
        for month_tag in months:
            month_name = month_tag.text.strip()
            print(f"   📅 Mes: {month_name}")
            
            # Encontrar la sección de ese mes
            month_section = month_tag.find_parent('div')
            if not month_section:
                continue
            
            # Buscar todos los partidos en ese mes
            games = month_section.find_all('tr')
            
            for game in games:
                try:
                    # Fecha
                    date_div = game.find('div', class_='nowrap')
                    if not date_div:
                        continue
                    date_text = date_div.text.strip()
                    
                    # Oponente
                    opponent_span = game.find('span', class_='team-name')
                    if not opponent_span:
                        continue
                    opponent = opponent_span.text.strip()
                    
                    # Resultado
                    result_span = game.find('span', attrs={'data-context': 'result'})
                    if result_span:
                        result_type = result_span.text.strip()  # W, L, D
                        score_text = result_span.find_next_sibling(text=True)
                        if score_text:
                            score = score_text.strip().replace(',', '').strip()
                        else:
                            score = "N/A"
                    else:
                        result_type = "TBD"
                        score = "TBD"
                    
                    # Link al Box Score
                    box_score_link = None
                    links = game.find_all('a')
                    for link in links:
                        if 'Box Score' in link.get_text():
                            box_score_link = self.base_url + link.get('href')
                            break
                    
                    match_info = {
                        'mes': month_name,
                        'fecha': date_text,
                        'oponente': opponent,
                        'resultado': result_type,
                        'marcador': score,
                        'box_score_url': box_score_link
                    }
                    
                    matches_data.append(match_info)
                    print(f"      ✅ {date_text} vs {opponent}: {result_type} {score}")
                
                except Exception as e:
                    print(f"      ⚠️ Error procesando partido: {str(e)}")
                    continue
        
        df = pd.DataFrame(matches_data)
        print(f"\n✅ Total de partidos encontrados: {len(df)}")
        return df
    
    def get_box_score_data(self, box_score_url):
        """
        Extrae datos completos de un Box Score
        
        Args:
            box_score_url (str): URL del Box Score
            
        Returns:
            dict: Diccionario con rosters, scoring y penalties
        """
        print(f"\n🔍 Extrayendo datos del Box Score...")
        
        soup = self._get_soup(box_score_url)
        if not soup:
            return None
        
        data = {
            'rosters': {},
            'scoring': [],
            'penalties': []
        }
        
        # 1. EXTRAER ROSTERS
        print("   📋 Extrayendo rosters...")
        data['rosters'] = self._extract_rosters(soup)
        
        # 2. EXTRAER SCORING SUMMARY
        print("   ⚽ Extrayendo Scoring Summary...")
        data['scoring'] = self._extract_scoring_summary(soup)
        
        # 3. EXTRAER PENALTY SUMMARY
        print("   🟨 Extrayendo Penalty Summary...")
        data['penalties'] = self._extract_penalty_summary(soup)
        
        return data
    
    def _extract_rosters(self, soup):
        """
        Extrae los rosters de ambos equipos
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            dict: {'Team Name': [lista de jugadores]}
        """
        rosters = {}
        
        # Buscar todas las tablas con rosters
        tables = soup.find_all('table', class_='table')
        
        for table in tables:
            # Buscar el caption con el nombre del equipo
            caption = table.find('caption')
            if not caption:
                continue
            
            team_name_tag = caption.find('span', class_='team-name')
            if not team_name_tag:
                continue
            
            team_name = team_name_tag.text.strip()
            
            # Extraer jugadores
            players = []
            rows = table.find('tbody').find_all('tr')
            
            for row in rows:
                # Saltar la fila de totales
                if 'totals' in row.get('class', []):
                    continue
                
                player_link = row.find('a', class_='player-name')
                if not player_link:
                    # Puede ser "Team"
                    player_span = row.find('span', class_='player-name')
                    if player_span:
                        player_name = player_span.text.strip()
                    else:
                        continue
                else:
                    player_name = player_link.text.strip()
                
                # Obtener estadísticas
                cells = row.find_all('td')
                if len(cells) >= 4:
                    player_data = {
                        'nombre': player_name,
                        'sh': cells[0].text.strip(),   # Shots
                        'sog': cells[1].text.strip(),  # Shots on Goal
                        'g': cells[2].text.strip(),    # Goals
                        'a': cells[3].text.strip()     # Assists
                    }
                    players.append(player_data)
            
            rosters[team_name] = players
            print(f"      ✅ {team_name}: {len(players)} jugadores")
        
        return rosters
    
    def _extract_scoring_summary(self, soup):
        """
        Extrae el resumen de goles (Scoring Summary)
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            list: Lista de goles
        """
        scoring_data = []
        
        # Buscar tabla de Scoring Summary
        tables = soup.find_all('table', class_='table')
        
        for table in tables:
            caption = table.find('caption')
            if not caption or 'Scoring Summary' not in caption.text:
                continue
            
            rows = table.find('tbody').find_all('tr')
            
            for row in rows:
                try:
                    # Logo del equipo (para identificar)
                    logo_div = row.find('div', class_='team-logo')
                    team_name = "Unknown"
                    if logo_div:
                        team_span = logo_div.find('span', class_='offscreen')
                        if team_span:
                            team_name = team_span.text.strip()
                    
                    # Periodo
                    period_span = row.find('span', class_='period')
                    period = period_span.text.strip() if period_span else "N/A"
                    
                    # Tiempo
                    time_cell = row.find('td', class_='time')
                    time = time_cell.text.strip() if time_cell else "N/A"
                    
                    # Play (jugador y asistencia)
                    play_cell = row.find('td', class_='text')
                    play = play_cell.text.strip() if play_cell else "N/A"
                    
                    # Marcador
                    total_cell = row.find('td', class_='total')
                    score = total_cell.text.strip() if total_cell else "N/A"
                    
                    goal_data = {
                        'equipo': team_name,
                        'periodo': period,
                        'tiempo': time,
                        'play': play,
                        'marcador': score
                    }
                    
                    scoring_data.append(goal_data)
                    print(f"      ⚽ {team_name}: {play} ({time})")
                
                except Exception as e:
                    print(f"      ⚠️ Error extrayendo gol: {str(e)}")
                    continue
        
        return scoring_data
    
    def _extract_penalty_summary(self, soup):
        """
        Extrae el resumen de tarjetas (Penalty Summary)
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            list: Lista de tarjetas
        """
        penalty_data = []
        
        # Buscar tabla de Penalty Summary
        tables = soup.find_all('table', class_='table')
        
        for table in tables:
            caption = table.find('caption')
            if not caption or 'Penalty Summary' not in caption.text:
                continue
            
            rows = table.find('tbody').find_all('tr')
            
            for row in rows:
                try:
                    # Logo del equipo
                    logo_div = row.find('div', class_='team-logo')
                    team_name = "Unknown"
                    if logo_div:
                        team_span = logo_div.find('span', class_='offscreen')
                        if team_span:
                            team_name = team_span.text.strip()
                    
                    # Periodo
                    period_span = row.find('span', class_='period')
                    period = period_span.text.strip() if period_span else "N/A"
                    
                    # Tiempo
                    time_cell = row.find('td', class_='time')
                    time = time_cell.text.strip() if time_cell else "N/A"
                    
                    # Tipo de tarjeta y jugador
                    foul_cell = row.find('td', class_='text')
                    if foul_cell:
                        foul_text = foul_cell.text.strip()
                        # Extraer tipo de tarjeta
                        if 'Yellow card' in foul_text:
                            card_type = 'Yellow'
                        elif 'Red card' in foul_text:
                            card_type = 'Red'
                        else:
                            card_type = 'Unknown'
                        
                        # Extraer nombre del jugador (después del " - ")
                        parts = foul_text.split(' - ')
                        player = parts[-1].strip() if len(parts) > 1 else "Unknown"
                    else:
                        card_type = "Unknown"
                        player = "Unknown"
                    
                    penalty = {
                        'equipo': team_name,
                        'periodo': period,
                        'tiempo': time,
                        'tipo_tarjeta': card_type,
                        'jugador': player
                    }
                    
                    penalty_data.append(penalty)
                    print(f"      🟨 {team_name}: {card_type} - {player} ({time})")
                
                except Exception as e:
                    print(f"      ⚠️ Error extrayendo tarjeta: {str(e)}")
                    continue
        
        return penalty_data
    
    def analyze_match(self, box_score_url, opponent_name):
        """
        Análisis completo de un partido
        
        Args:
            box_score_url (str): URL del Box Score
            opponent_name (str): Nombre del oponente
            
        Returns:
            dict: Análisis completo del partido
        """
        print(f"\n{'='*60}")
        print(f"🔍 ANALIZANDO PARTIDO vs {opponent_name}")
        print(f"{'='*60}")
        
        # Extraer datos del Box Score
        box_data = self.get_box_score_data(box_score_url)
        
        if not box_data:
            print("❌ No se pudo extraer datos del Box Score")
            return None
        
        # Identificar jugadores de cada equipo
        irvine_players = set()
        opponent_players = set()
        
        for team_name, players in box_data['rosters'].items():
            for player in players:
                if 'Irvine Valley' in team_name:
                    irvine_players.add(player['nombre'])
                else:
                    opponent_players.add(player['nombre'])
        
        # Clasificar goles
        print(f"\n⚽ ANÁLISIS DE GOLES:")
        irvine_goals = []
        opponent_goals = []
        
        for goal in box_data['scoring']:
            # Extraer nombre del jugador del 'play'
            player_name = goal['play'].split('(')[0].strip()
            
            if goal['equipo'] == 'Irvine Valley' or player_name in irvine_players:
                irvine_goals.append(goal)
                print(f"   ✅ Irvine Valley: {goal['play']} - {goal['tiempo']}")
            else:
                opponent_goals.append(goal)
                print(f"   ⚠️ {opponent_name}: {goal['play']} - {goal['tiempo']}")
        
        # Clasificar tarjetas
        print(f"\n🟨 ANÁLISIS DE TARJETAS:")
        irvine_cards = []
        opponent_cards = []
        
        for penalty in box_data['penalties']:
            if penalty['equipo'] == 'Irvine Valley' or penalty['jugador'] in irvine_players:
                irvine_cards.append(penalty)
                print(f"   ⚠️ Irvine Valley: {penalty['tipo_tarjeta']} - {penalty['jugador']} ({penalty['tiempo']})")
            else:
                opponent_cards.append(penalty)
                print(f"   ℹ️ {opponent_name}: {penalty['tipo_tarjeta']} - {penalty['jugador']} ({penalty['tiempo']})")
        
        analysis = {
            'oponente': opponent_name,
            'rosters': box_data['rosters'],
            'goles_irvine': irvine_goals,
            'goles_oponente': opponent_goals,
            'tarjetas_irvine': irvine_cards,
            'tarjetas_oponente': opponent_cards,
            'total_goles_irvine': len(irvine_goals),
            'total_goles_oponente': len(opponent_goals),
            'total_tarjetas_irvine': len(irvine_cards),
            'total_tarjetas_oponente': len(opponent_cards)
        }
        
        print(f"\n📊 RESUMEN:")
        print(f"   Goles Irvine: {len(irvine_goals)}")
        print(f"   Goles {opponent_name}: {len(opponent_goals)}")
        print(f"   Tarjetas Irvine: {len(irvine_cards)}")
        print(f"   Tarjetas {opponent_name}: {len(opponent_cards)}")
        
        return analysis


# ============================================
# FUNCIONES DE AYUDA
# ============================================

def get_irvine_matches():
    """Obtiene todos los partidos de Irvine Valley"""
    scraper = Scraper3C2A()
    return scraper.get_irvine_matches()


def analyze_opponent_match(box_score_url, opponent_name):
    """Analiza un partido específico contra un oponente"""
    scraper = Scraper3C2A()
    return scraper.analyze_match(box_score_url, opponent_name)


# ============================================
# TESTING
# ============================================
def get_conference_standings():
    """
    Obtiene la tabla de clasificación de Orange Empire Conference
    
    Returns:
        pd.DataFrame: Tabla de standings
    """
    url = "https://3c2asports.org/sports/msoc/2025-26/standings"
    
    try:
        print("🔍 Obteniendo clasificación de Orange Empire Conference...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar el título de Orange Empire Conference
        orange_empire_header = soup.find('h3', string='ORANGE EMPIRE')
        
        if not orange_empire_header:
            print("⚠️ No se encontró la sección de Orange Empire")
            return pd.DataFrame()
        
        # La tabla está después del h3, dentro de un div.standings-page
        standings_div = orange_empire_header.find_next('div', class_='standings-page')
        
        if not standings_div:
            print("⚠️ No se encontró el div de standings")
            return pd.DataFrame()
        
        # Buscar la tabla dentro del div
        table = standings_div.find('table')
        
        if not table:
            print("⚠️ No se encontró la tabla")
            return pd.DataFrame()
        
        teams_data = []
        
        # Extraer filas de equipos (tbody > tr)
        tbody = table.find('tbody')
        if not tbody:
            print("⚠️ No se encontró tbody")
            return pd.DataFrame()
        
        rows = tbody.find_all('tr')
        
        for idx, row in enumerate(rows, 1):
            # Obtener nombre del equipo
            team_cell = row.find('th', class_='team-name')
            if not team_cell:
                continue
            
            team_link = team_cell.find('a')
            if not team_link:
                continue
            
            team_name = team_link.text.strip()
            schedule_url = f"https://3c2asports.org{team_link['href']}" if team_link.has_attr('href') else None
            
            # Obtener todas las celdas de estadísticas
            stats_cols = row.find_all('td', class_='stats-col')
            
            if len(stats_cols) < 5:
                continue
            
            # Las primeras 5 columnas con bg-emphasis son de Conference
            # GP, W, L, TIES, PCT (Conference)
            try:
                conf_gp = stats_cols[0].text.strip()
                conf_w = stats_cols[1].text.strip()
                conf_l = stats_cols[2].text.strip()
                conf_ties = stats_cols[3].text.strip()
                conf_pct = stats_cols[4].text.strip()
                
                teams_data.append({
                    'posicion': idx,
                    'equipo': team_name,
                    'pj_conf': conf_gp,
                    'victorias': conf_w,
                    'derrotas': conf_l,
                    'empates': conf_ties,
                    'porcentaje': conf_pct,
                    'schedule_url': schedule_url
                })
                
                print(f"   ✅ {idx}. {team_name}: {conf_w}-{conf_l}-{conf_ties} ({conf_pct})")
                
            except Exception as e:
                print(f"   ⚠️ Error procesando {team_name}: {str(e)}")
                continue
        
        df = pd.DataFrame(teams_data)
        print(f"✅ Total de equipos en Orange Empire: {len(df)}")
        
        return df
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return pd.DataFrame()