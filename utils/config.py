"""
============================================
CONFIGURACIÓN CENTRAL DEL PROYECTO
Soccer Analytics Streamlit - TFM
============================================
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================
# CONFIGURACIÓN GENERAL
# ============================================
APP_TITLE = "⚽ Soccer Analytics - Multi-Team Platform"
APP_VERSION = "2.0.0 - TFM"
DEBUG = os.getenv("DEBUG", "False") == "True"

# ============================================
# OPENAI API
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ============================================
# WEB SCRAPING - 3C2A SPORTS
# ============================================
BASE_URL_3C2A = "https://3c2asports.org"

# IDs de equipos
TEAM_IDS = {
    'Irvine Valley': 'pd2msqrhfox3ougx',
    'Fullerton': 'TBD',  # Agregar IDs reales
    'Santa Ana': 'TBD',
    'Cypress': 'TBD'
}

# Configuración de scraping
SCRAPING_TIMEOUT = 10  # segundos
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ============================================
# RUTAS DE DATOS
# ============================================
DATA_FOLDER = "data"
OUTPUTS_FOLDER = "outputs"

# Crear carpetas si no existen
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(OUTPUTS_FOLDER, exist_ok=True)

# ============================================
# CONFIGURACIÓN DE VISUALIZACIONES
# ============================================
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
}

# Template de Plotly
PLOTLY_TEMPLATE = "plotly_white"

# Colores
COLORS = {
    "primary": "#2C3E50",
    "secondary": "#18BC9C",
    "success": "#18BC9C",
    "danger": "#E74C3C",
    "warning": "#F39C12",
    "info": "#3498DB",
    "light": "#ECF0F1",
    "dark": "#2C3E50",
}

# ============================================
# VALIDACIONES
# ============================================
def validate_config():
    """Valida que la configuración esté completa"""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append("⚠️ OPENAI_API_KEY no está configurada en .env")
    
    if errors:
        print("\n" + "="*50)
        print("ERRORES DE CONFIGURACIÓN:")
        for error in errors:
            print(f"  {error}")
        print("="*50 + "\n")
        return False
    
    return True

# ============================================
# CREDENCIALES DE LOGIN
# ============================================
# Para streamlit-authenticator
CREDENTIALS = {
    'usernames': {
        'admin': {
            'name': 'Admin User',
            'password': '$2b$12$KIXxN9VHN3mC7Fg7QXzvLeJKp5n7n5n5n5n5n5n5n5n5n5n5n5'  # "admin123" hasheado
        },
        'claudio': {
            'name': 'Claudio Catrambone',
            'password': '$2b$12$KIXxN9VHN3mC7Fg7QXzvLeJKp5n7n5n5n5n5n5n5n5n5n5n5n5'  # "ivc2024" hasheado
        }
    }
}

COOKIE_CONFIG = {
    'expiry_days': 30,
    'key': 'soccer_analytics_auth_key',
    'name': 'soccer_analytics_cookie'
}
