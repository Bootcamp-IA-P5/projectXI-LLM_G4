# 🚀 Content Generator - Sistema de Generación Automática de Contenido con IA

Sistema avanzado de generación automática de contenido para múltiples plataformas utilizando inteligencia artificial generativa, arquitectura multiagente, RAG científico y técnicas avanzadas de prompt engineering.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Componentes Técnicos](#componentes-técnicos)
6. [Características Implementadas](#características-implementadas)
7. [Instalación y Configuración](#instalación-y-configuración)
8. [Uso del Sistema](#uso-del-sistema)
9. [Flujo de Datos](#flujo-de-datos)
10. [Solución de Problemas](#solución-de-problemas)

---

## 📖 Descripción General

Este proyecto es una aplicación web completa que permite generar contenido de texto optimizado para diferentes plataformas (Blog, Twitter/X, Instagram, LinkedIn) utilizando modelos de lenguaje grande (LLMs) y técnicas avanzadas de IA generativa.

### Características Principales

- **Generación Multiplataforma**: Contenido optimizado para Blog, Twitter/X, Instagram y LinkedIn
- **Sistema Multiagente**: Arquitectura basada en CrewAI con agentes especializados
- **RAG Científico**: Sistema de recuperación aumentada de generación para contenido científico
- **Guardarraíles**: Validación automática de calidad y consistencia del contenido
- **Multi-LLM**: Soporte para Groq, OpenAI y Ollama
- **Multiidioma**: Generación en Español, Inglés, Francés e Italiano
- **Generación de Imágenes**: Integración con Unsplash API
- **Personalización**: Perfil de marca/empresa para personalizar todo el contenido

---

## 🏗️ Arquitectura del Sistema

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (app.py)                  │
│  ┌──────────────────┐  ┌────────────────────────────────────┐  │
│  │   Chat Tab       │  │   Content Generator Tab            │  │
│  │                  │  │  ┌──────────────────────────────┐  │  │
│  │  - Conversación  │  │  │  Form: Topic, Platform,       │  │  │
│  │  - Historial     │  │  │  Audience, Tone, Language    │  │  │
│  │                  │  │  └──────────────────────────────┘  │  │
│  └──────────────────┘  │  ┌──────────────────────────────┐  │
│                        │  │  Sidebar:                      │  │
│                        │  │  - LLM Provider Selector       │  │
│                        │  │  - User Profile Config         │  │
│                        │  │  - Agent Mode Toggle           │  │
│                        │  └──────────────────────────────┘  │
│                        └────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Capa de Lógica de Negocio                      │
│  ┌──────────────────┐  ┌────────────────────────────────────┐  │
│  │ content_generator│  │  agents/content_crew.py            │  │
│  │                  │  │  ┌──────────────────────────────┐  │  │
│  │  - Prompt Engine │  │  │  Director Agent              │  │  │
│  │  - LangChain     │  │  │  Blog Agent                  │  │  │
│  │  - Template      │  │  │  LinkedIn Agent              │  │  │
│  │  - Multiidioma   │  │  │  Twitter Agent               │  │  │
│  └──────────────────┘  │  │  Instagram Agent             │  │  │
│                        │  │  Revisor Agent                │  │  │
│  ┌──────────────────┐  │  └──────────────────────────────┘  │
│  │  llm_factory.py  │  │  ┌──────────────────────────────┐  │
│  │                  │  │  │  agents/tools/guardrails.py  │  │
│  │  - Factory       │  │  │  - Content Validation        │  │
│  │  - Groq          │  │  │  - Length Checks             │  │
│  │  - OpenAI        │  │  │  - Forbidden Words           │  │
│  │  - Ollama        │  │  │  - Tone Consistency          │  │
│  └──────────────────┘  │  └──────────────────────────────┘  │
│                        └────────────────────────────────────┘
│  ┌──────────────────┐  ┌────────────────────────────────────┐
│  │ image_generator  │  │  rag/                               │
│  │                  │  │  ┌──────────────────────────────┐  │
│  │  - Unsplash API  │  │  │  database.py                 │  │
│  │  - Keyword       │  │  │  - Chroma Vectorstore       │  │
│  │  Extraction      │  │  │  - Embeddings (HuggingFace)   │  │
│  └──────────────────┘  │  └──────────────────────────────┘  │
│                        │  ┌──────────────────────────────┐  │
│                        │  │  ingestion.py                 │  │
│                        │  │  - PDF Loading                │  │
│                        │  │  - Text Splitting             │  │
│                        │  └──────────────────────────────┘  │
│                        │  ┌──────────────────────────────┐  │
│                        │  │  retrieval.py                 │  │
│                        │  │  - RAG Chain                 │  │
│                        │  │  - Context Retrieval          │  │
│                        │  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Capa de Servicios Externos                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Groq API    │  │  OpenAI API  │  │  Ollama      │         │
│  │  (Llama 3.x) │  │  (GPT-4)     │  │  (Local)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐                          │
│  │  Unsplash    │  │  LangSmith    │                          │
│  │  API         │  │  (Tracing)    │                          │
│  └──────────────┘  └──────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

### Arquitectura Multiagente (CrewAI)

```
┌─────────────────────────────────────────────────────────────┐
│                    ContentCrew (Orchestrator)                │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Director Agent                          │   │
│  │  - Analiza requests                                 │   │
│  │  - Rutea a agentes especializados                  │   │
│  │  - Coordina workflow                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                        │                                     │
│        ┌───────────────┼───────────────┐                    │
│        ▼               ▼               ▼                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Blog    │  │ LinkedIn │  │ Twitter  │                 │
│  │  Agent   │  │  Agent   │  │  Agent   │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
│        │               │               │                     │
│        └───────────────┼───────────────┘                    │
│                        ▼                                     │
│              ┌──────────────────┐                            │
│              │  Revisor Agent    │                            │
│              │  - Validación     │                            │
│              │  - Guardrails     │                            │
│              │  - Quality Check  │                            │
│              └──────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### Arquitectura RAG (Retrieval-Augmented Generation)

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                              │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Ingestion Layer (ingestion.py)                     │   │
│  │  - Load PDFs from data/raw/                         │   │
│  │  - Split into chunks (1000 chars, 200 overlap)       │   │
│  │  - Create Document objects                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                        │                                     │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Embedding Layer (database.py)                      │   │
│  │  - HuggingFace Embeddings                           │   │
│  │  - Model: sentence-transformers/all-MiniLM-L6-v2    │   │
│  │  - Generate vector embeddings                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                        │                                     │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Vector Store (Chroma)                               │   │
│  │  - Persist in chroma_db/                            │   │
│  │  - Collection: "papers"                              │   │
│  │  - Metadata: filename, page, etc.                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                        │                                     │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Retrieval Layer (retrieval.py)                     │   │
│  │  - Query vectorstore (k=4 chunks)                   │   │
│  │  - RAG Chain: context + query → LLM                 │   │
│  │  - Generate scientific content                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

### Core Framework
- **Python 3.10+**: Lenguaje principal
- **Streamlit 1.51.0**: Framework web para interfaz de usuario
- **LangChain 1.2.0**: Framework para aplicaciones con LLMs
- **LangChain Core 1.2.2**: Componentes base de LangChain

### LLM Providers
- **Groq API**: Procesamiento rápido con modelos Llama 3.x
  - `llama-3.3-70b-versatile`
  - `llama-3.1-8b-instant`
  - `llama-3.1-70b-versatile`
  - `mixtral-8x7b-32768`
- **OpenAI API**: Modelos GPT (opcional)
  - `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, `gpt-4o`
- **Ollama**: Modelos locales (opcional)
  - `llama2`, `llama3`, `mistral`, `codellama`

### Multi-Agent System
- **CrewAI 1.8.1**: Framework para sistemas multiagente
- **CrewAI Tools 1.8.1**: Herramientas para agentes

### RAG & Vector Database
- **ChromaDB ~1.1.0**: Base de datos vectorial
- **langchain-huggingface**: Embeddings de HuggingFace
- **sentence-transformers**: Modelo de embeddings
- **pypdf 6.6.0**: Procesamiento de PDFs

### Image Generation
- **Unsplash API**: API gratuita para imágenes (50 req/hora)

### Observability
- **LangSmith 0.5.0**: Trazabilidad y observabilidad de LLMs

### Data Processing
- **transformers >=4.40.0**: Modelos de HuggingFace
- **pydantic ~2.11.9**: Validación de datos
- **numpy 1.26.4**: Operaciones numéricas

### Infrastructure
- **Docker**: Containerización
- **python-dotenv 1.1.1**: Gestión de variables de entorno
- **requests 2.32.5**: Cliente HTTP
- **httpx 0.28.1**: Cliente HTTP asíncrono

---

## 📁 Estructura del Proyecto

```
projectXI-LLM_G4/
├── app.py                          # Aplicación principal Streamlit
├── content_generator.py            # Generador de contenido con LangChain
├── llm_factory.py                  # Factory pattern para múltiples LLMs
├── image_generator.py              # Generación de imágenes con Unsplash
│
├── agents/                         # Sistema Multiagente
│   ├── __init__.py
│   ├── content_crew.py            # Orquestador de agentes (CrewAI)
│   └── tools/
│       ├── __init__.py
│       └── guardrails.py          # Validación y guardarraíles
│
├── rag/                            # Sistema RAG Científico
│   ├── __init__.py
│   ├── database.py                # Vectorstore (Chroma) y embeddings
│   ├── ingestion.py               # Carga y procesamiento de documentos
│   └── retrieval.py               # RAG chain y recuperación
│
├── data/                           # Datos del proyecto
│   └── raw/                        # PDFs científicos para RAG
│       └── ai&eeuu_economy2026.pdf
│
├── docs/                           # Documentación
│   ├── PROJECT_FLOW.md            # Flujo detallado del proyecto
│   ├── TEST_CASES.md              # Casos de prueba
│   ├── HOW_TO_USE_LLM_SELECTOR.md # Guía de uso del selector
│   ├── LANGSMITH_SETUP.md         # Configuración de LangSmith
│   └── DEMO_PREPARATION.md        # Preparación para demo
│
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Configuración Docker
├── .dockerignore                  # Archivos excluidos de Docker
├── .gitignore                     # Archivos excluidos de Git
├── .env.example                   # Template de variables de entorno
└── README.md                      # Este archivo
```

---

## 🔧 Componentes Técnicos

### 1. `app.py` - Interfaz Principal

**Responsabilidades:**
- Interfaz de usuario con Streamlit (tabs, forms, sidebar)
- Gestión de estado con `st.session_state`
- Selector de LLM provider y modelo
- Configuración de perfil de usuario
- Integración de chat conversacional
- Integración de generación de contenido
- Integración de sistema multiagente
- Manejo de errores y validaciones

**Funciones Clave:**
```python
@st.cache_resource
def get_cached_llm(provider, model, temperature):
    """Cachea instancias de LLM por sesión"""

def ensure_api_key(provider):
    """Valida configuración de API keys"""
```

**Estado de Sesión:**
```python
st.session_state = {
    "llm_provider": "groq",
    "llm_model": "llama-3.1-8b-instant",
    "llm_temperature": 0.7,
    "user_profile": {
        "name": "",
        "industry": "",
        "tone": "",
        "values": ""
    },
    "chat_history": [],
    "use_agents": False
}
```

### 2. `llm_factory.py` - Factory Pattern para LLMs

**Patrón de Diseño:** Factory Pattern

**Responsabilidades:**
- Crear instancias de LLM según provider
- Validar configuración de providers
- Listar modelos disponibles por provider
- Manejar dependencias opcionales (OpenAI, Ollama)

**Funciones:**
```python
def get_llm(provider: str, model: str, temperature: float) -> LLM:
    """Factory function - Crea instancia de LLM"""

def get_available_models(provider: str) -> list:
    """Retorna lista de modelos disponibles"""

def validate_provider_config(provider: str) -> tuple[bool, str]:
    """Valida configuración del provider"""
```

**Providers Soportados:**
- **Groq**: Requiere `GROQ_API_KEY`
- **OpenAI**: Requiere `OPENAI_API_KEY` (opcional)
- **Ollama**: Requiere Ollama corriendo localmente (opcional)

### 3. `content_generator.py` - Generador de Contenido

**Responsabilidades:**
- Construcción de prompts dinámicos con LangChain
- Integración de perfil de usuario en prompts
- Soporte multiidioma
- Creación de chains de LangChain
- Invocación de LLMs

**Función Principal:**
```python
def generate_content(
    topic: str,
    platform: str,
    audience: str,
    tone: str,
    language: str = "Spanish",
    user_profile: dict = None,
    provider: str = "groq",
    model: str = "llama-3.1-8b-instant",
    temperature: float = 0.7
) -> str:
    """Genera contenido usando LangChain y LLM"""
```

**Template de Prompt:**
- Incluye información de plataforma, audiencia, tono
- Integra perfil de usuario si está disponible
- Soporta múltiples idiomas
- Adaptado según la plataforma objetivo

### 4. `agents/content_crew.py` - Sistema Multiagente

**Framework:** CrewAI

**Arquitectura:**
- **Director Agent**: Rutea requests a agentes especializados
- **Blog Agent**: Especialista en contenido largo y SEO
- **LinkedIn Agent**: Especialista en contenido profesional B2B
- **Twitter Agent**: Especialista en contenido conciso
- **Instagram Agent**: Especialista en contenido visual y emojis
- **Revisor Agent**: Valida calidad y aplica guardarraíles

**Clase Principal:**
```python
class ContentCrew:
    def __init__(self, provider: str, model: str):
        """Inicializa el crew con LLM configurado"""
    
    def generate(self, topic, platform, audience, tone, 
                 user_profile=None, language="Spanish") -> dict:
        """Genera contenido usando sistema multiagente"""
```

**Workflow:**
1. Director analiza request
2. Director delega a agente especializado
3. Agente genera contenido
4. Revisor valida y aplica guardarraíles
5. Retorna contenido validado

### 5. `agents/tools/guardrails.py` - Guardarraíles

**Responsabilidades:**
- Validación de longitud por plataforma
- Detección de palabras prohibidas
- Verificación de elementos requeridos
- Validación de consistencia de tono

**Configuración:**
```python
GUARDRAILS = {
    "length": {
        "Blog": (800, 2000),
        "LinkedIn": (150, 300),
        "Twitter": (1, 280),
        "Instagram": (100, 150)
    },
    "forbidden_words": [...],
    "required_elements": {...}
}
```

**Funciones:**
```python
def validate_content(content: str, platform: str) -> tuple[bool, list]:
    """Valida contenido contra guardarraíles"""

def check_tone_consistency(content: str, expected_tone: str) -> bool:
    """Verifica consistencia de tono"""
```

### 6. `rag/database.py` - Vector Database

**Responsabilidades:**
- Creación y gestión de vectorstore con Chroma
- Generación de embeddings con HuggingFace
- Persistencia de vectores
- Carga de vectorstores existentes

**Funciones:**
```python
def get_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Crea instancia de embeddings"""

def create_vectorstore(documents, persist_directory, 
                      collection_name, embedding_model) -> Chroma:
    """Crea vectorstore desde documentos"""

def load_vectorstore(persist_directory, collection_name, 
                    embedding_model) -> Chroma:
    """Carga vectorstore existente"""
```

**Modelo de Embeddings:**
- Por defecto: `sentence-transformers/all-MiniLM-L6-v2`
- 384 dimensiones
- Optimizado para búsqueda semántica

### 7. `rag/ingestion.py` - Procesamiento de Documentos

**Responsabilidades:**
- Carga de PDFs desde `data/raw/`
- División de documentos en chunks
- Creación de objetos Document de LangChain
- Manejo de metadatos (filename, page, etc.)

**Funciones:**
```python
def load_documents(source_path: str) -> List[Document]:
    """Carga documentos desde archivo o directorio"""

def split_documents(documents, chunk_size=1000, 
                   chunk_overlap=200) -> List[Document]:
    """Divide documentos en chunks"""
```

**Estrategia de Chunking:**
- Tamaño: 1000 caracteres
- Overlap: 200 caracteres
- Preserva contexto entre chunks

### 8. `rag/retrieval.py` - RAG Chain

**Responsabilidades:**
- Creación de RAG chain con LangChain
- Recuperación de contexto relevante
- Generación de contenido científico
- Integración con LLM

**Funciones:**
```python
def retrieve_documents(retriever, query: str, k: int = 4) -> List[Dict]:
    """Recupera documentos relevantes"""

def create_rag_chain(retriever, llm, system_prompt=None):
    """Crea RAG chain completo"""

def query_rag(query, vectorstore=None, retriever=None, 
              llm=None, k=4) -> Dict:
    """Query completa al sistema RAG"""
```

**RAG Chain:**
```
Query → Retriever → Context → Prompt Template → LLM → Response
```

### 9. `image_generator.py` - Generación de Imágenes

**Responsabilidades:**
- Extracción de keywords del contenido
- Búsqueda de imágenes en Unsplash API
- Formateo de imágenes en Markdown
- Manejo de atribuciones

**Funciones:**
```python
def extract_keywords(text: str) -> List[str]:
    """Extrae keywords usando LLM"""

def get_images_for_content(content: str) -> Optional[dict]:
    """Obtiene imágenes de Unsplash"""

def format_image_markdown(image_data: dict) -> str:
    """Formatea imagen en Markdown"""
```

**API:**
- Unsplash API (gratuita, 50 req/hora)
- Requiere `UNSPLASH_ACCESS_KEY`

---



---

## 📦 Instalación y Configuración

### Prerrequisitos

- Python 3.10 o superior
- pip (gestor de paquetes Python)
- Docker (opcional, para ejecución en contenedor)
- Git (para clonar el repositorio)

### Opción 1: Ejecución Local

#### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd projectXI-LLM_G4
```

#### 2. Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Mac/Linux
# o en Windows: venv\Scripts\activate
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Si encuentras conflictos de dependencias, puedes instalar paquetes opcionales por separado:

```bash
# Para OpenAI (opcional)
pip install langchain-openai

# Para Ollama (opcional)
pip install langchain-ollama
```

#### 4. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tus API keys
nano .env  # o usa tu editor preferido
```

**Variables Mínimas Requeridas:**
```bash
# Groq API (requerido para uso básico)
GROQ_API_KEY=tu_api_key_aqui
```

**Obtener API Keys:**
- **Groq**: https://console.groq.com/ (gratis)
- **OpenAI**: https://platform.openai.com/ (pago)
- **Unsplash**: https://unsplash.com/developers (gratis, 50 req/hora)
- **LangSmith**: https://smith.langchain.com/ (gratis para desarrollo)

#### 5. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

### Opción 2: Ejecución con Docker

#### 1. Construir la Imagen

```bash
docker build -t content-generator .
```

#### 2. Crear Archivo .env

```bash
cp .env.example .env
# Editar .env y añadir tus API keys
```

#### 3. Ejecutar el Contenedor

```bash
docker run -p 8501:8501 --env-file .env content-generator
```

La aplicación estará disponible en `http://localhost:8501`

### Configuración Avanzada

#### Variables de Entorno Completas

```bash
# ======================================
# GROQ API (Requerido para uso básico)
# ======================================
GROQ_API_KEY=tu_api_key
GROQ_MODEL=llama-3.1-8b-instant
MODEL_TEMPERATURE=0.7

# ======================================
# OpenAI API (Opcional)
# ======================================
OPENAI_API_KEY=tu_openai_api_key

# ======================================
# Ollama (Opcional - para uso local)
# ======================================
# Instalar Ollama desde: https://ollama.ai/
OLLAMA_BASE_URL=http://localhost:11434

# ======================================
# System Prompt (Opcional)
# ======================================
SYSTEM_PROMPT=You are a helpful assistant

# ======================================
# Image Generation (Opcional)
# ======================================
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# ======================================
# MarketAux Financial News API (Opcional)
# ======================================
# Get your free API key at: https://www.marketaux.com/register
# Free tier: 50 requests/hour
# MARKETAUX_API_KEY=your_marketaux_api_key_here

# ======================================
# LangSmith Tracing (Opcional)
# ======================================
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=content-generator
```

---

## 🎮 Uso del Sistema

### Configuración Inicial

#### 1. Seleccionar LLM Provider (Sidebar)

- **Provider**: Elige entre Groq, OpenAI u Ollama
- **Model**: Selecciona el modelo específico
- **Temperature**: Ajusta la creatividad (0.0 = determinista, 1.0 = creativo)

#### 2. Configurar Perfil de Usuario (Sidebar - Opcional)

- **Nombre**: Nombre de empresa/persona
- **Sector/Industria**: Sector al que perteneces
- **Tono de Voz**: Tono característico de tu marca
- **Valores/Misión**: Valores y misión de tu marca

Este perfil se integrará automáticamente en todo el contenido generado.

#### 3. Modo de Generación (Sidebar)

- **Modo Simple**: Generación directa con LangChain
- **Modo Agentes**: Sistema multiagente con CrewAI (más avanzado)

### Pestaña "Chat"

- Chat conversacional con el modelo de IA seleccionado
- Respuestas en tiempo real
- Historial de conversación mantenido en memoria
- Útil para consultas rápidas y pruebas

### Pestaña "Content Generator"

#### Formulario de Generación:

1. **Tema**: Describe el tema sobre el que quieres generar contenido
2. **Plataforma**: Selecciona la plataforma objetivo
   - Blog (800-2000 palabras)
   - Twitter/X (1-280 caracteres)
   - Instagram (100-150 palabras)
   - LinkedIn (150-300 palabras)
3. **Audiencia**: Define tu audiencia objetivo
4. **Tono**: Elige el tono del contenido
   - Informativo, Profesional, Amigable, Divertido, etc.
5. **Idioma**: Selecciona el idioma de generación
   - Español, Inglés, Francés, Italiano
6. **Generate**: Haz clic para generar

#### Resultado:

- Contenido generado formateado en Markdown
- Imágenes relevantes integradas (si está configurado Unsplash)
- Contenido personalizado según tu perfil (si está configurado)
- Validado con guardarraíles (si usas modo agentes)

### Sistema RAG Científico

Para usar el sistema RAG:

1. Coloca PDFs científicos en `data/raw/`
2. El sistema procesará automáticamente los documentos
3. Los documentos se indexarán en Chroma vectorstore
4. El contenido generado incluirá información de los documentos

---

## 🔄 Flujo de Datos

### Flujo de Generación Simple

```
Usuario completa formulario
    │
    ▼
app.py valida inputs
    │
    ▼
app.py llama a generate_content()
    │
    ▼
content_generator.py construye prompt
    │
    ├─► Integra user_profile (si existe)
    ├─► Adapta a plataforma
    ├─► Añade idioma
    └─► Crea ChatPromptTemplate
    │
    ▼
llm_factory.py crea instancia de LLM
    │
    ├─► Groq → ChatGroq
    ├─► OpenAI → ChatOpenAI
    └─► Ollama → ChatOllama
    │
    ▼
LangChain crea chain: prompt | llm
    │
    ▼
LLM genera contenido
    │
    ▼
image_generator.py extrae keywords
    │
    ▼
Unsplash API busca imágenes
    │
    ▼
app.py muestra resultado
```

### Flujo de Generación con Agentes

```
Usuario completa formulario
    │
    ▼
app.py detecta modo agentes
    │
    ▼
agents/content_crew.py inicializa ContentCrew
    │
    ├─► Crea Director Agent
    ├─► Crea Content Agents (Blog, LinkedIn, Twitter, Instagram)
    └─► Crea Revisor Agent
    │
    ▼
Director Agent analiza request
    │
    ▼
Director delega a agente especializado
    │
    ▼
Agente especializado genera contenido
    │
    ▼
Revisor Agent valida contenido
    │
    ├─► agents/tools/guardrails.py
    │   ├─► Valida longitud
    │   ├─► Detecta palabras prohibidas
    │   ├─► Verifica elementos requeridos
    │   └─► Valida consistencia de tono
    │
    ▼
Contenido validado retornado
    │
    ▼
app.py muestra resultado
```

### Flujo RAG

```
Usuario hace query científica
    │
    ▼
rag/retrieval.py recibe query
    │
    ▼
rag/database.py carga vectorstore
    │
    ├─► Chroma busca vectores similares
    └─► Retorna top-k chunks (k=4)
    │
    ▼
rag/retrieval.py crea RAG chain
    │
    ├─► Context: chunks recuperados
    ├─► Query: pregunta del usuario
    └─► System Prompt: instrucciones científicas
    │
    ▼
LLM genera respuesta con contexto
    │
    ▼
app.py muestra respuesta científica
```

---

## 🐛 Solución de Problemas

### Error: "Model error: 'ascii' codec can't encode character"

✅ **Solucionado**: El código configura automáticamente UTF-8 encoding. Si persiste:
- Verifica que el archivo `.env` no tenga caracteres especiales
- Asegúrate de usar Python 3.10+

### Error: "GROQ_API_KEY is missing"

- Verifica que el archivo `.env` existe
- Confirma que la API key está correctamente copiada (sin espacios)
- Si usas Docker, verifica el flag `--env-file .env`

### Error: "OpenAI/Ollama is not available"

- **Groq** está incluido por defecto y funciona sin instalación adicional
- **OpenAI**: Instala con `pip install langchain-openai` (opcional)
- **Ollama**: 
  - Instala Ollama desde https://ollama.ai/
  - Instala con `pip install langchain-ollama` (opcional)
  - Asegúrate de que Ollama esté corriendo: `ollama serve`

### Error: Conflictos de Dependencias

Si encuentras conflictos al instalar `requirements.txt`:

```bash
# Instalar dependencias base primero
pip install langchain==1.2.0 langchain-core==1.2.2 langchain-groq==1.1.1 streamlit==1.51.0

# Luego instalar el resto
pip install -r requirements.txt
```

### Imágenes no aparecen

- La generación de imágenes requiere una API key de Unsplash (opcional)
- Obtén tu key gratuita en: https://unsplash.com/developers
- Agrega `UNSPLASH_ACCESS_KEY=tu_key` al archivo `.env`
- Sin la key, la aplicación funciona normalmente pero sin imágenes

### Error: "CrewAI telemetry" o problemas con agentes

✅ **Solucionado**: El código desactiva automáticamente la telemetría de CrewAI para evitar conflictos con Streamlit.

### Error: Docker build falla

- Verifica que Docker esté corriendo
- Asegúrate de tener suficiente espacio en disco
- Revisa los logs: `docker build -t content-generator . 2>&1 | tee build.log`

### Puerto 8501 ya en uso

```bash
# Encontrar proceso usando el puerto
lsof -i :8501

# Matar el proceso
kill -9 <PID>
```

---

## 📚 Documentación Adicional

- **`docs/PROJECT_FLOW.md`**: Flujo detallado del proyecto
- **`docs/TEST_CASES.md`**: Casos de prueba estructurados
- **`docs/HOW_TO_USE_LLM_SELECTOR.md`**: Guía del selector de LLMs
- **`docs/LANGSMITH_SETUP.md`**: Configuración de LangSmith
- **`docs/DEMO_PREPARATION.md`**: Preparación para demo

---

## 🤝 Contribuciones

Este es un proyecto académico desarrollado para el Bootcamp de IA. Las contribuciones son bienvenidas.

### Estructura de Ramas

- `main`: Código de producción estable
- `dev`: Rama de desarrollo principal
- `feature/*`: Features individuales
- `fix/*`: Correcciones de bugs

### Convenciones de Commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `refactor:` Refactorización
- `test:` Tests

---


## 🔗 Enlaces Útiles

- [Groq Console](https://console.groq.com/) - Obtener API key gratuita
- [LangChain Docs](https://python.langchain.com/) - Documentación de LangChain
- [Streamlit Docs](https://docs.streamlit.io/) - Documentación de Streamlit
- [CrewAI Docs](https://docs.crewai.com/) - Documentación de CrewAI
- [ChromaDB Docs](https://docs.trychroma.com/) - Documentación de ChromaDB
- [Unsplash API](https://unsplash.com/developers) - API de imágenes
- [LangSmith](https://smith.langchain.com/) - Observabilidad de LLMs

---

⭐ **¿Te gusta el proyecto? ¡Dale una estrella en GitHub!**
