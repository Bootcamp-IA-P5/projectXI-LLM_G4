# 🔍 Configuración de LangSmith Tracing

## ¿Qué es LangSmith?

LangSmith es una plataforma de observabilidad para aplicaciones LLM que permite:
- Ver todas las llamadas a los LLMs
- Analizar tiempos de respuesta
- Debuggear prompts
- Monitorear costos y uso

## 🚀 Configuración Rápida (5 minutos)

### Paso 1: Obtener API Key

1. Ve a: https://smith.langchain.com/
2. Inicia sesión (ya tienes cuenta)
3. Ve a "Settings" → "API Keys"
4. Crea una nueva API key o copia una existente

### Paso 2: Agregar al .env

Edita tu archivo `.env` y agrega:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_langsmith_api_key_aqui
LANGCHAIN_PROJECT=content-generator
```

### Paso 3: Reiniciar la aplicación

```bash
# Si usas Docker
docker restart content-gen-app

# O si usas local
# Detén Streamlit (Ctrl+C) y vuelve a ejecutar
streamlit run app.py
```

### Paso 4: Verificar que funciona

1. Genera algún contenido en la app
2. Ve a: https://smith.langchain.com/
3. Ve a "Projects" → "content-generator"
4. Deberías ver las trazas de las llamadas al LLM

## ✅ ¿Cómo saber que funciona?

- En el dashboard de LangSmith verás:
  - Cada llamada a `generate_content()`
  - Los prompts enviados
  - Las respuestas recibidas
  - Tiempo de ejecución
  - Tokens usados

## 📊 Beneficios

- **Debugging**: Ver exactamente qué se envía al LLM
- **Optimización**: Identificar prompts lentos o costosos
- **Monitoreo**: Trackear uso y costos
- **Análisis**: Comparar diferentes modelos/providers

## ⚠️ Notas

- LangSmith es **gratis** para desarrollo
- Las trazas se envían automáticamente (no requiere cambios en código)
- Los datos se almacenan en la nube de LangSmith
- Puedes desactivarlo quitando las variables de entorno
