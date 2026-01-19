# 🚀 Content Generator - Generador Automático de Contenido con IA

Sistema de generación automática de contenido para múltiples plataformas utilizando inteligencia artificial generativa.

## 📋 Descripción

Este proyecto es una aplicación web que permite generar contenido de texto optimizado para diferentes plataformas (Blog, Twitter/X, Instagram, LinkedIn) utilizando modelos de lenguaje grande (LLMs) y técnicas de prompt engineering.

## 🎯 Características

### ✅ Implementado
- ✅ Generación de contenido para múltiples plataformas (Blog, Twitter/X, Instagram, LinkedIn)
- ✅ Personalización por audiencia y tono
- ✅ Interfaz web interactiva con Streamlit
- ✅ Chat conversacional con IA
- ✅ Uso de LangChain framework
- ✅ Integración con Groq (Llama 3.3 70B)
- ✅ Dockerización completa

### 🚧 En desarrollo
- 🔄 Selección entre múltiples LLMs (Groq, OpenAI, Ollama)
- 🔄 Generación de imágenes con IA
- 🔄 Soporte multiidioma (ES, EN, FR, IT)
- 🔄 RAG científico con arXiv
- 🔄 Sistema multiagente
- 🔄 Trazabilidad con LangSmith

## 🛠️ Tecnologías

- **Python 3.10**
- **LangChain** - Framework para aplicaciones con LLMs
- **Groq API** - LLM backend (Llama 3.3 70B)
- **Streamlit** - Frontend web interactivo
- **Docker** - Containerización
- **python-dotenv** - Gestión de variables de entorno

## 📦 Instalación

### Opción 1: Ejecución Local

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd projectXI-LLM_G4
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Mac/Linux
# o en Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key de Groq
nano .env  # o usa tu editor preferido
```

Añade tu API key de Groq (obtenerla gratis en https://console.groq.com/):
```
GROQ_API_KEY=tu_api_key_aqui
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

### Opción 2: Ejecución con Docker

1. **Construir la imagen**
```bash
docker build -t content-generator .
```

2. **Crear archivo .env**
```bash
cp .env.example .env
# Editar .env y añadir tu GROQ_API_KEY
```

3. **Ejecutar el contenedor**
```bash
docker run -p 8501:8501 --env-file .env content-generator
```

La aplicación estará disponible en `http://localhost:8501`

## 🎮 Uso

### Pestaña "Chat"
- Chat conversacional con el modelo de IA
- Respuestas en tiempo real
- Historial de conversación en memoria

### Pestaña "Content Generator"
1. **Tema**: Describe el tema sobre el que quieres generar contenido
2. **Plataforma**: Selecciona la plataforma objetivo (Blog, Twitter, Instagram, LinkedIn)
3. **Audiencia**: Define tu audiencia objetivo
4. **Tono**: Elige el tono del contenido (Informativo, Profesional, Amigable, etc.)
5. Haz clic en **"Generate"** y espera el resultado

## 🔧 Configuración Avanzada

### Variables de Entorno Disponibles

```bash
# Configuración de Groq (Requerido)
GROQ_API_KEY=tu_api_key
GROQ_MODEL=llama-3.3-8b-versatile
MODEL_TEMPERATURE=0.7

# System Prompt personalizado (Opcional)
SYSTEM_PROMPT=You are a helpful assistant

# APIs adicionales (Futuras implementaciones)
# OPENAI_API_KEY=...
# LANGCHAIN_API_KEY=...
# UNSPLASH_ACCESS_KEY=...
```

## 📁 Estructura del Proyecto

```
projectXI-LLM_G4/
├── app.py                    # Aplicación principal Streamlit
├── content_generator.py      # Lógica de generación de contenido
├── requirements.txt          # Dependencias Python
├── Dockerfile               # Configuración Docker
├── .dockerignore            # Archivos excluidos de Docker
├── .gitignore               # Archivos excluidos de Git
├── .env.example             # Template de variables de entorno
└── README.md                # Este archivo
```

## 🐛 Solución de Problemas

### Error: "Model error: 'ascii' codec can't encode character"
✅ **Solucionado**: El código ahora configura automáticamente UTF-8 encoding.

### Error: Docker build falla con "software-properties-common"
✅ **Solucionado**: El Dockerfile ha sido actualizado para no requerir este paquete.

### Error: "GROQ_API_KEY is missing"
- Asegúrate de haber creado el archivo `.env`
- Verifica que la API key esté correctamente copiada sin espacios
- Si usas Docker, verifica que el flag `--env-file .env` esté presente

## 🤝 Contribuciones

Este es un proyecto académico desarrollado para el Bootcamp de IA. Las contribuciones son bienvenidas.

## 📄 Licencia

Este proyecto es de uso educativo.

## 👥 Equipo

Grupo 4 - Bootcamp IA

## 🔗 Enlaces Útiles

- [Groq Console](https://console.groq.com/) - Obtener API key gratuita
- [LangChain Docs](https://python.langchain.com/) - Documentación de LangChain
- [Streamlit Docs](https://docs.streamlit.io/) - Documentación de Streamlit

---

⭐ **¿Te gusta el proyecto? ¡Dale una estrella en GitHub!**

