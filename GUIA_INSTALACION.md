# 📘 GUÍA DE INSTALACIÓN PASO A PASO
## Soccer Analytics - Multi-Team Platform

Esta guía te llevará paso a paso desde cero hasta tener la aplicación funcionando.

---

## ✅ REQUISITOS PREVIOS

Antes de empezar, verifica que tienes:

### 1. **Python 3.10 o superior**
```bash
# Verifica tu versión de Python
python --version
# o
py --version
```

**Si no tienes Python:** Descárgalo de https://www.python.org/downloads/

### 2. **Cuenta de OpenAI**
- Ve a: https://platform.openai.com/
- Crea una cuenta (si no tienes)
- Agrega método de pago (requerido para usar la API)

---

## 📥 PASO 1: OBTENER EL PROYECTO

### Opción A: Descargar ZIP
1. Descarga el archivo `Soccer_Analytics_Streamlit.zip`
2. Descomprímelo en una carpeta de tu elección
3. Ejemplo: `C:\Users\TuNombre\Escritorio\Soccer_Analytics_Streamlit`

### Opción B: Clonar con Git (si tienes Git instalado)
```bash
git clone [URL_DEL_REPOSITORIO]
cd Soccer_Analytics_Streamlit
```

---

## 🔑 PASO 2: OBTENER API KEY DE OPENAI

### 1. **Inicia sesión en OpenAI**
- Ve a: https://platform.openai.com/api-keys

### 2. **Crea una API Key**
- Haz clic en **"Create new secret key"**
- Dale un nombre (ejemplo: "Soccer Analytics")
- **COPIA LA KEY INMEDIATAMENTE** (solo se muestra una vez)
- Formato: `sk-proj-abc123...`

### 3. **Guarda la key en un lugar seguro**
- Pégala en un documento temporal
- La usaremos en el Paso 4

---

## 💻 PASO 3: INSTALAR DEPENDENCIAS

### 1. **Abre la terminal/símbolo del sistema**

**Windows:**
- Presiona `Windows + R`
- Escribe `cmd` y presiona Enter

**Mac/Linux:**
- Abre Terminal

### 2. **Navega a la carpeta del proyecto**
```bash
cd ruta\a\Soccer_Analytics_Streamlit
```

Ejemplo en Windows:
```bash
cd C:\Users\TuNombre\Escritorio\Soccer_Analytics_Streamlit
```

### 3. **Instala las dependencias**
```bash
py -m pip install -r requirements.txt
```

**Espera 1-2 minutos** mientras se instalan todas las librerías.

### 4. **Verifica la instalación de OpenAI**
```bash
py -m pip show openai
```

**Debe mostrar:**
```
Name: openai
Version: 0.28.1
```

**Si muestra otra versión:**
```bash
py -m pip uninstall openai
py -m pip install openai==0.28.1
```

---

## ⚙️ PASO 4: CONFIGURAR API KEY

### 1. **Crea el archivo .env**

En la **raíz del proyecto** (donde está Home.py), crea un archivo llamado `.env`

**Opción 1 - Con Bloc de notas:**
1. Abre Bloc de notas
2. Copia y pega:
```
OPENAI_API_KEY=sk-proj-tu-key-aqui
```
3. Reemplaza `sk-proj-tu-key-aqui` con tu API Key real
4. Guarda como: `.env` (con el punto al inicio)
5. **IMPORTANTE:** En "Guardar como tipo" selecciona "Todos los archivos (*.*)"

**Opción 2 - Con la terminal:**
```bash
# Windows
echo OPENAI_API_KEY=sk-proj-tu-key-aqui > .env

# Mac/Linux
echo "OPENAI_API_KEY=sk-proj-tu-key-aqui" > .env
```

### 2. **Verifica que el archivo existe**
```bash
# Windows
dir .env

# Mac/Linux
ls -la .env
```

---

## 🚀 PASO 5: EJECUTAR LA APLICACIÓN

### 1. **Inicia Streamlit**

Desde la carpeta del proyecto:
```bash
streamlit run Home.py
```

### 2. **Espera a que se abra**
- Se abrirá automáticamente en tu navegador
- URL: `http://localhost:8501`
- Si no se abre automáticamente, copia la URL de la terminal

### 3. **¡Listo!**
Deberías ver la página principal de Soccer Analytics

---

## 🧪 PASO 6: PROBAR QUE TODO FUNCIONA

### Test Rápido:

1. **Ve a "Multi-Team Analysis"** (en la barra lateral)

2. **Verifica los gráficos:**
   - ¿Se ven 4 gráficos?
   - ¿Puedes cambiar equipos y temporadas?

3. **Prueba la IA:**
   - Scroll hasta "🤖 Análisis con IA"
   - Haz clic en "🔄 Generar Análisis Comparativo"
   - Espera 3-5 segundos
   - ¿Aparece un análisis en español?

**Si todo funciona:** ✅ ¡Instalación exitosa!

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ Error: "streamlit: command not found"

**Solución:**
```bash
py -m pip install streamlit==1.31.0
```

---

### ❌ Error: "No se encontró OPENAI_API_KEY"

**Causas posibles:**
1. El archivo `.env` no existe
2. El archivo se llama `.env.txt` (incorrecto)
3. La API Key está mal escrita

**Solución:**
1. Verifica que el archivo se llama exactamente `.env` (con punto)
2. Abre el archivo y verifica que dice: `OPENAI_API_KEY=tu-key`
3. Verifica que la key empieza con `sk-`

---

### ❌ Error: "ModuleNotFoundError: No module named 'X'"

**Solución:**
```bash
# Reinstalar todas las dependencias
py -m pip install -r requirements.txt
```

---

### ❌ Error de versión de OpenAI

**Síntomas:**
- "Client.init() got an unexpected keyword argument 'proxies'"
- "cannot import name 'OpenAI' from 'openai'"

**Solución:**
```bash
py -m pip uninstall openai
py -m pip install openai==0.28.1
```

---

### ❌ Los gráficos no se actualizan

**Solución:**
```bash
streamlit cache clear
streamlit run Home.py
```

---

### ❌ La aplicación está lenta

**Causas:**
- Primera ejecución (carga inicial)
- Caché de Streamlit lleno
- Muchos datos seleccionados

**Solución:**
```bash
# Limpiar caché
streamlit cache clear
```

---

## 📊 VERIFICACIÓN FINAL

Si todo funciona correctamente, deberías poder:

✅ Abrir la aplicación en el navegador
✅ Ver las 4 páginas en la barra lateral
✅ Cambiar filtros en Multi-Team Analysis
✅ Ver los 4 gráficos principales
✅ Abrir las 4 métricas avanzadas
✅ Generar análisis con IA (los 3 botones)

---

## 🎉 ¡FELICIDADES!

Tu instalación está completa. Ahora puedes:

1. **Explorar la aplicación** - Prueba diferentes filtros
2. **Generar análisis IA** - Guarda los mejores para tu TFM
3. **Exportar reportes** - Usa la página de Reports
4. **Personalizar** - Modifica el código según tus necesidades

---

## 📞 AYUDA ADICIONAL

Si sigues teniendo problemas:

1. Revisa el archivo `README.md` para más información
2. Verifica que Python 3.10+ está instalado
3. Verifica que todas las dependencias están instaladas
4. Revisa que tu API Key de OpenAI es válida

---

## 💰 NOTA SOBRE COSTOS DE OPENAI

- OpenAI cobra por uso de la API
- GPT-4 cuesta aproximadamente $0.03-0.06 por análisis
- Revisa tu billing en: https://platform.openai.com/account/billing
- Puedes establecer límites de gasto

---

**Multi-Team Soccer Analytics | Powered by Streamlit + OpenAI**

*¡Disfruta analizando datos de soccer!* ⚽📊
