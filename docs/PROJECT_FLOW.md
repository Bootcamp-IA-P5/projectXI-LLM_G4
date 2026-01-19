# 🔄 Flujo del Proyecto - Content Generator

Guía completa del flujo de funcionamiento del sistema de generación automática de contenido.

## 📋 Índice

1. [Arquitectura General](#arquitectura-general)
2. [Flujo de Usuario](#flujo-de-usuario)
3. [Flujo Técnico](#flujo-técnico)
4. [Componentes Principales](#componentes-principales)
5. [Flujo de Datos](#flujo-de-datos)
6. [Gestión de Estado](#gestión-de-estado)

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│  ┌──────────────┐  ┌────────────────────────────────┐  │
│  │   Chat Tab   │  │   Content Generator Tab        │  │
│  │              │  │  ┌──────────────────────────┐  │  │
│  │  - Chat UI   │  │  │  Form: Topic, Platform,   │  │  │
│  │  - History   │  │  │  Audience, Tone           │  │  │
│  │              │  │  └──────────────────────────┘  │  │  │
│  └──────────────┘  │  ┌──────────────────────────┐  │  │
│                    │  │  Sidebar:                 │  │  │
│                    │  │  - LLM Provider Selector  │  │  │
│                    │  │  - User Profile           │  │  │
│                    │  │  - Name, Industry, Tone   │  │  │
│                    │  └──────────────────────────┘  │  │  │
│                    └────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              llm_factory.py                             │
│  ┌──────────────────────────────────────────────────┐   │
│  │  get_llm(provider, model, temperature)           │   │
│  │  - Factory pattern para crear LLM instances       │   │
│  │  - Soporta: Groq, OpenAI, Ollama                  │   │
│  └──────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              content_generator.py                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  generate_content()                               │   │
│  │  - Recibe: topic, platform, audience, tone        │   │
│  │  - Recibe: user_profile (opcional)               │   │
│  │  - Recibe: provider, model, temperature          │   │
│  │  - Usa llm_factory para crear LLM                │   │
│  │  - Construye prompt dinámico                      │   │
│  │  - Inyecta perfil si existe                       │   │
│  └──────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    LangChain Chain                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Prompt Template → LLM → Response                 │   │
│  │  - ChatPromptTemplate                             │   │
│  │  - Groq/OpenAI/Ollama (según selección)           │   │
│  └──────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    LLM Provider                          │
│  - Groq API (Llama 3.3)                                 │
│  - OpenAI API (GPT-4)                                   │
│  - Ollama (local)                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 👤 Flujo de Usuario

### Escenario 1: Generar Contenido Básico

```
1. Usuario abre aplicación → http://localhost:8501
   │
   ├─► Ve sidebar con selector de LLM
   ├─► Selecciona provider (Groq/OpenAI/Ollama)
   ├─► Selecciona modelo específico
   ├─► Ajusta temperatura (opcional)
   │
2. Usuario va a pestaña "Content Generator"
   │
3. Usuario completa formulario:
   │
   ├─► Topic: "The benefits of AI in healthcare"
   ├─► Platform: "Blog Post"
   ├─► Audience: "Healthcare professionals"
   ├─► Tone: "Professional"
   │
4. Usuario hace clic en "Generate"
   │
   ├─► Sistema valida campos
   ├─► Sistema verifica API key del provider seleccionado
   ├─► Sistema llama a generate_content() con provider y modelo
   ├─► llm_factory crea instancia del LLM correcto
   │
5. Sistema muestra contenido generado
   │
   └─► Usuario puede copiar/usar el contenido
```

### Escenario 2: Generar Contenido con Perfil Personalizado

```
1. Usuario abre aplicación
   │
2. Usuario configura perfil en sidebar:
   │
   ├─► Name: "TechCorp"
   ├─► Industry: "Technology"
   ├─► Tone: "Innovative and bold"
   ├─► Values: "Innovation, sustainability"
   │
   └─► Clic en "Save profile" → Guardado en st.session_state
   │
3. Usuario completa formulario de contenido
   │
4. Usuario hace clic en "Generate"
   │
   ├─► Sistema pasa user_profile a generate_content()
   ├─► Prompt incluye información del perfil
   │
5. Contenido generado refleja el perfil de la empresa
   │
   └─► Ejemplo: "At TechCorp, we believe in innovation..."
```

### Escenario 3: Chat con IA

```
1. Usuario abre pestaña "Chat"
   │
2. Usuario escribe mensaje
   │
3. Sistema envía mensaje al LLM
   │
4. Sistema muestra respuesta
   │
5. Historial se mantiene en st.session_state.chat_history
```

---

## ⚙️ Flujo Técnico

### Paso 1: Inicialización

```python
# app.py - Al iniciar la aplicación

1. load_dotenv() → Carga variables de entorno (.env)
2. st.set_page_config() → Configura página Streamlit
3. Inicializa st.session_state.user_profile (si no existe)
4. get_llm() → Crea instancia de LLM (cached)
```

### Paso 2: Usuario Completa Formulario

```python
# app.py - Content Generator Tab

1. Usuario ingresa: topic, platform, audience, tone
2. Usuario hace clic en "Generate"
3. Validación: all([topic, platform, audience, tone])
4. Verificación: ensure_api_key()
```

### Paso 3: Llamada a Generación

```python
# app.py - Línea ~171

generate_content(
    topic=topic,
    platform=platform,
    audience=audience,
    tone=tone,
    user_profile=st.session_state.get("user_profile", {})
)
```

### Paso 4: Construcción del Prompt

```python
# content_generator.py - generate_content()

1. Define base_template (prompt base)
2. Verifica si user_profile existe y tiene datos
3. Si hay perfil:
   ├─► Construye profile_section con:
   │   - Name
   │   - Industry
   │   - Voice/Tone
   │   - Values
   └─► Concatena: base_template + profile_section
4. Si no hay perfil:
   └─► Usa solo base_template
5. Crea ChatPromptTemplate dinámico
6. Crea chain: prompt | llm
```

### Paso 5: Invocación del LLM

```python
# content_generator.py

1. chain.invoke({
     "topic": topic,
     "platform": platform,
     "audience": audience,
     "tone": tone
   })
2. LLM procesa el prompt
3. LLM genera respuesta
4. Retorna response.content (string)
```

### Paso 6: Visualización

```python
# app.py

1. Recibe output (string)
2. st.markdown(output) → Muestra contenido formateado
3. Usuario puede copiar/usar
```

---

## 🧩 Componentes Principales

### 1. `app.py` - Interfaz Principal

**Responsabilidades:**
- UI con Streamlit (tabs, forms, sidebar)
- Gestión de estado (`st.session_state`)
- Selector de LLM provider
- Validación de inputs
- Llamada a funciones de generación
- Manejo de errores

**Funciones clave:**
- `get_cached_llm()`: Crea/cachea instancia de LLM usando factory
- `ensure_api_key()`: Valida API key según provider
- Sidebar: Selector de LLM y gestión de perfil de usuario

### 2. `llm_factory.py` - Factory Pattern para LLMs

**Responsabilidades:**
- Crear instancias de LLM según provider
- Validar configuración de providers
- Listar modelos disponibles

**Funciones clave:**
- `get_llm(provider, model, temperature)`: Factory function
- `get_available_models(provider)`: Lista modelos por provider
- `validate_provider_config(provider)`: Valida configuración

### 3. `content_generator.py` - Lógica de Generación

**Responsabilidades:**
- Construcción de prompts dinámicos
- Integración con LangChain
- Manejo de perfil de usuario
- Creación dinámica de LLM usando factory

**Funciones clave:**
- `generate_content()`: Función principal de generación
  - Parámetros: topic, platform, audience, tone, user_profile, provider, model, temperature
  - Usa `llm_factory.get_llm()` para crear instancia de LLM

### 3. `st.session_state` - Estado de Sesión

**Datos almacenados:**
```python
{
    "user_profile": {
        "name": "TechCorp",
        "industry": "Technology",
        "tone": "Innovative",
        "values": "Innovation, sustainability"
    },
    "chat_history": [
        AIMessage(...),
        HumanMessage(...),
        ...
    ]
}
```

**Características:**
- Persiste durante la sesión del navegador
- Se pierde al recargar/cerrar
- Único por pestaña/sesión

---

## 🔄 Flujo de Datos

```
Usuario Input
    │
    ├─► Form Fields (topic, platform, audience, tone)
    │
    └─► Sidebar (user_profile)
         │
         ▼
st.session_state
    │
    ├─► user_profile (dict)
    │
    └─► chat_history (list)
         │
         ▼
generate_content()
    │
    ├─► Parámetros: topic, platform, audience, tone
    │
    └─► Parámetro: user_profile (opcional)
         │
         ▼
Prompt Construction
    │
    ├─► base_template (siempre)
    │
    └─► profile_section (condicional)
         │
         ▼
LangChain Chain
    │
    ├─► ChatPromptTemplate
    │
    └─► LLM (Groq/OpenAI/Ollama)
         │
         ▼
Response (AIMessage)
    │
    └─► .content (string)
         │
         ▼
UI Display
    │
    └─► st.markdown(output)
```

---

## 💾 Gestión de Estado

### Estado Persistente (st.session_state)

| Variable | Tipo | Inicialización | Uso |
|----------|------|----------------|-----|
| `user_profile` | dict | `{"name": "", "industry": "", "tone": "", "values": ""}` | Perfil de empresa/persona |
| `chat_history` | list | `[AIMessage("Hi!...")]` | Historial de chat |
| `llm_provider` | str | `"groq"` | Provider seleccionado (groq/openai/ollama) |
| `llm_model` | str | `"llama-3.1-8b-instant"` | Modelo seleccionado |
| `llm_temperature` | float | `0.7` | Temperatura para generación |

### Estado Temporal

- Variables de formulario (se pierden al recargar)
- Mensajes de error/éxito (temporales)

---

## 🔐 Variables de Entorno

### Requeridas (según provider usado)

```bash
# Para Groq
GROQ_API_KEY=tu_api_key_aqui

# Para OpenAI (opcional)
OPENAI_API_KEY=tu_openai_api_key

# Para Ollama (opcional - local)
# No requiere API key, solo instalar Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Opcionales

```bash
GROQ_MODEL=llama-3.1-8b-instant
MODEL_TEMPERATURE=0.7
SYSTEM_PROMPT=You are a helpful assistant
```

---

## 🚀 Flujo de Ejecución Completo

```
1. Usuario inicia aplicación
   │
   ├─► Docker container inicia
   ├─► Streamlit server inicia
   └─► Carga app.py
        │
2. Inicialización
   │
   ├─► load_dotenv() → Carga .env
   ├─► st.set_page_config()
   ├─► Inicializa session_state
   └─► get_llm() → Crea LLM (cached)
        │
3. Usuario interactúa
   │
   ├─► Opción A: Configura perfil
   │   └─► Guarda en session_state.user_profile
   │
   ├─► Opción B: Completa formulario
   │   └─► Topic, Platform, Audience, Tone
   │
   └─► Opción C: Clic en "Generate"
        │
4. Procesamiento
   │
   ├─► Validación de campos
   ├─► Verificación de API key
   ├─► Llamada a generate_content()
   │   │
   │   ├─► Construye prompt base
   │   ├─► Agrega perfil (si existe)
   │   ├─► Crea ChatPromptTemplate
   │   ├─► Crea chain: prompt | llm
   │   └─► Invoca chain.invoke()
        │
5. Respuesta
   │
   ├─► LLM genera contenido
   ├─► Retorna AIMessage
   ├─► Extrae .content
   └─► Muestra en UI
        │
6. Usuario usa contenido
   │
   └─► Copia, edita, publica
```

---

## 📝 Notas Importantes

### Persistencia de Datos

- **Perfil de usuario**: Solo durante la sesión (st.session_state)
- **Historial de chat**: Solo durante la sesión
- **No hay base de datos**: Todo es en memoria

### Manejo de Errores

- Validación de campos antes de generar
- Verificación de API key
- Try/except en llamadas a LLM
- Mensajes de error claros en UI

### Performance

- LLM se cachea con `@st.cache_resource`
- Prompt se construye dinámicamente (eficiente)
- No hay llamadas innecesarias a APIs

---

## 🔮 Próximas Mejoras (Roadmap)

1. ✅ **Selector de LLMs**: Implementado - Elegir entre Groq, OpenAI, Ollama
2. **Persistencia**: Guardar perfil en archivo/BD
3. **Generación de imágenes**: Integrar APIs de imágenes
4. **Multiidioma**: Soporte ES, EN, FR, IT
5. **Historial**: Guardar generaciones anteriores
6. **Exportar**: Descargar contenido en diferentes formatos

---

## 📚 Referencias

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Groq API](https://console.groq.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Última actualización**: Enero 2025  
**Versión**: 1.0.0

