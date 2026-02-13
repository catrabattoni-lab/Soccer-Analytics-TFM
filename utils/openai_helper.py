"""
============================================
OPENAI HELPER - IA GENERATIVA
============================================

Módulo para integrar OpenAI API y generar análisis con IA
Versión compatible con openai==0.28.0
"""

import openai
from .config import OPENAI_API_KEY, OPENAI_MODEL
import json

class OpenAIHelper:
    """
    Clase para interactuar con OpenAI API (versión 0.28)
    """
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada en .env")
        
        openai.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
    
    def _make_request(self, messages, temperature=0.7, max_tokens=1000):
        """
        Realiza una petición a OpenAI API
        
        Args:
            messages (list): Lista de mensajes
            temperature (float): Temperatura (creatividad)
            max_tokens (int): Máximo de tokens en la respuesta
            
        Returns:
            str: Respuesta de OpenAI
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al conectar con OpenAI: {str(e)}"
    
    def generate_match_summary(self, match_data):
        """
        Genera un resumen de un partido usando IA
        
        Args:
            match_data (dict): Datos del partido
            
        Returns:
            str: Resumen generado
        """
        prompt = f"""
        Como analista deportivo experto, genera un resumen conciso y profesional del siguiente partido:
        
        Datos del partido:
        {json.dumps(match_data, indent=2, ensure_ascii=False)}
        
        El resumen debe incluir:
        - Resultado final y contexto
        - Momentos clave del partido
        - Desempeño de ambos equipos
        - Estadísticas relevantes
        
        Formato: Párrafos concisos, máximo 200 palabras.
        """
        
        messages = [
            {"role": "system", "content": "Eres un analista deportivo profesional especializado en fútbol."},
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages, temperature=0.7)
    
    def analyze_strengths_weaknesses(self, team_stats):
        """
        Analiza fortalezas y debilidades de un equipo
        
        Args:
            team_stats (dict): Estadísticas del equipo
            
        Returns:
            dict: Análisis estructurado
        """
        prompt = f"""
        Como analista táctico, analiza las siguientes estadísticas del equipo:
        
        {json.dumps(team_stats, indent=2, ensure_ascii=False)}
        
        Proporciona un análisis estructurado en formato JSON con:
        {{
            "fortalezas": ["fortaleza 1", "fortaleza 2", "fortaleza 3"],
            "debilidades": ["debilidad 1", "debilidad 2", "debilidad 3"],
            "recomendaciones": ["recomendación 1", "recomendación 2"]
        }}
        
        Base tu análisis en los datos proporcionados.
        RESPONDE SOLO CON EL JSON VÁLIDO, SIN MARKDOWN NI TEXTO ADICIONAL.
        """
        
        messages = [
            {"role": "system", "content": "Eres un analista táctico experto. Respondes SOLO en formato JSON válido, sin markdown."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._make_request(messages, temperature=0.5)
        
        try:
            # Limpiar respuesta (quitar markdown si existe)
            clean_response = response.strip()
            
            # Quitar ```json y ``` si existen
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:]
            if clean_response.startswith('```'):
                clean_response = clean_response[3:]
            if clean_response.endswith('```'):
                clean_response = clean_response[:-3]
            
            clean_response = clean_response.strip()
            
            # Parsear JSON
            result = json.loads(clean_response)
            print(f"✅ Análisis de fortalezas parseado correctamente")
            return result
            
        except Exception as e:
            print(f"⚠️ Error parseando JSON: {str(e)}")
            print(f"Respuesta recibida: {response[:200]}...")
            return {
                "fortalezas": ["Análisis no disponible - error de formato"],
                "debilidades": ["Análisis no disponible - error de formato"],
                "recomendaciones": ["Análisis no disponible - error de formato"]
            }
    
    def generate_tactical_recommendations(self, opponent_data, team_data=None):
        """
        Genera recomendaciones tácticas para enfrentar un oponente
        
        Args:
            opponent_data (dict): Datos del oponente
            team_data (dict): Datos del propio equipo (opcional)
            
        Returns:
            str: Recomendaciones tácticas
        """
        prompt = f"""
        Como entrenador táctico, proporciona recomendaciones específicas para enfrentar al siguiente oponente:
        
        Oponente:
        {json.dumps(opponent_data, indent=2, ensure_ascii=False)}
        
        {"Nuestro equipo:" if team_data else ""}
        {json.dumps(team_data, indent=2, ensure_ascii=False) if team_data else ""}
        
        Proporciona:
        1. Formación recomendada
        2. Estrategia defensiva
        3. Estrategia ofensiva
        4. Jugadas a balón parado
        5. Puntos clave a explotar del rival
        
        Formato: Puntos concisos y accionables.
        """
        
        messages = [
            {"role": "system", "content": "Eres un entrenador táctico de fútbol con experiencia profesional."},
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages, temperature=0.6, max_tokens=1500)
    
    def generate_season_report(self, season_data):
        """
        Genera un reporte completo de temporada
        
        Args:
            season_data (dict): Datos de la temporada
            
        Returns:
            str: Reporte de temporada
        """
        prompt = f"""
        Como analista deportivo, genera un reporte ejecutivo de la temporada:
        
        {json.dumps(season_data, indent=2, ensure_ascii=False)}
        
        El reporte debe incluir:
        1. Resumen ejecutivo
        2. Análisis de rendimiento
        3. Evolución a lo largo de la temporada
        4. Áreas de mejora
        5. Conclusiones y proyecciones
        
        Formato: Profesional, estructurado en secciones.
        """
        
        messages = [
            {"role": "system", "content": "Eres un analista deportivo senior con experiencia en reportes ejecutivos."},
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages, temperature=0.7, max_tokens=2000)
    
    def custom_analysis(self, prompt_text, data=None):
        """
        Análisis personalizado con IA
        
        Args:
            prompt_text (str): Pregunta o solicitud personalizada
            data (dict): Datos adicionales (opcional)
            
        Returns:
            str: Respuesta de IA
        """
        full_prompt = prompt_text
        
        if data:
            full_prompt += f"\n\nDatos de contexto:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
        
        messages = [
            {"role": "system", "content": "Eres un asistente experto en análisis deportivo."},
            {"role": "user", "content": full_prompt}
        ]
        
        return self._make_request(messages)


# ============================================
# FUNCIONES DE AYUDA
# ============================================

def generate_summary(match_data):
    """
    Función auxiliar para generar resumen de partido
    """
    helper = OpenAIHelper()
    return helper.generate_match_summary(match_data)


def analyze_team(team_stats):
    """
    Función auxiliar para analizar equipo
    """
    helper = OpenAIHelper()
    return helper.analyze_strengths_weaknesses(team_stats)


def get_tactical_advice(opponent_data, team_data=None):
    """
    Función auxiliar para obtener recomendaciones tácticas
    """
    helper = OpenAIHelper()
    return helper.generate_tactical_recommendations(opponent_data, team_data)


# ============================================
# TESTING
# ============================================
if __name__ == "__main__":
    print("Testing OpenAI Helper...")
    
    # Datos de ejemplo
    match_data = {
        "equipo_local": "Equipo A",
        "equipo_visitante": "Equipo B",
        "resultado": "2-1",
        "goles": ["Min 23: Equipo A", "Min 45: Equipo B", "Min 78: Equipo A"]
    }
    
    try:
        helper = OpenAIHelper()
        
        print("\n1. Generando resumen de partido...")
        summary = helper.generate_match_summary(match_data)
        print(summary)
        
        print("\n✅ Testing completo")
    
    except ValueError as e:
        print(f"\n⚠️ {str(e)}")
        print("Por favor configura tu OPENAI_API_KEY en el archivo .env")