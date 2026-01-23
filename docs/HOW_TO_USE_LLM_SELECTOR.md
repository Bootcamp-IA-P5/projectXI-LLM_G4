# 🎯 Cómo Usar el Selector de LLMs

## 📍 Dónde Encontrarlo

El selector de LLMs está ubicado en el **sidebar izquierdo** de la aplicación, en la sección **"🤖 LLM Provider"**.

## 🚀 Pasos para Usarlo

### 1. Abrir la Aplicación
```
http://localhost:8501
```

### 2. Localizar el Sidebar
- El sidebar está en el lado izquierdo de la pantalla
- Busca la sección **"🤖 LLM Provider"** (expandida por defecto)

### 3. Seleccionar Provider
- **Dropdown "Select LLM Provider"**:
  - `groq` - Groq API (gratis, rápido)
  - `openai` - OpenAI GPT (requiere API key)
  - `ollama` - Ollama local (requiere instalación local)

### 4. Seleccionar Modelo
- El dropdown **"Select Model"** muestra modelos disponibles según el provider seleccionado
- Ejemplos:
  - **Groq**: llama-3.3-70b-versatile, llama-3.1-8b-instant
  - **OpenAI**: gpt-4, gpt-3.5-turbo, gpt-4o
  - **Ollama**: llama2, llama3, mistral

### 5. Ajustar Temperatura (Opcional)
- **Slider "Temperature"**:
  - 0.0 = Más determinista y predecible
  - 1.0 = Más creativo y variado
  - Valor por defecto: 0.7

### 6. Verificar Estado
- ✅ Verde: Provider configurado correctamente
- ⚠️ Amarillo: Falta API key o configuración

## 📝 Requisitos por Provider

### Groq
```bash
# En .env
GROQ_API_KEY=tu_api_key_aqui
```
- Obtener key: https://console.groq.com/
- Gratis con límites generosos

### OpenAI
```bash
# En .env
OPENAI_API_KEY=tu_api_key_aqui
```
- Obtener key: https://platform.openai.com/
- Requiere créditos (puede tener trial gratuito)

### Ollama
```bash
# Instalar Ollama primero
# https://ollama.ai/

# En .env (opcional)
OLLAMA_BASE_URL=http://localhost:11434
```
- Instalar: https://ollama.ai/
- Descargar modelos: `ollama pull llama2`
- Gratis, corre localmente

## 🎨 Visualización en la UI

```
┌─────────────────────────────┐
│  ⚙️ Configuration            │
│                             │
│  🤖 LLM Provider            │
│  ┌───────────────────────┐ │
│  │ Select LLM Provider    │ │
│  │ [groq ▼]              │ │
│  │                       │ │
│  │ Select Model          │ │
│  │ [llama-3.1-8b... ▼]  │ │
│  │                       │ │
│  │ Temperature           │ │
│  │ [━━━━━━━━━━━━━━] 0.7 │ │
│  │                       │ │
│  │ ✅ GROQ configured    │ │
│  └───────────────────────┘ │
│                             │
│  ───────────────────────   │
│                             │
│  👤 Brand / User Profile    │
│  ...                        │
└─────────────────────────────┘
```

## 🔄 Flujo Completo

1. **Seleccionar Provider** → Cambia modelos disponibles
2. **Seleccionar Modelo** → Actualiza instancia de LLM
3. **Ajustar Temperatura** → Afecta creatividad
4. **Generar Contenido** → Usa el LLM seleccionado

## ⚠️ Notas Importantes

- El LLM se cachea por sesión (cambiar provider/modelo puede requerir recargar)
- Cada provider tiene diferentes modelos disponibles
- La temperatura afecta tanto al Chat como al Content Generator
- Si cambias de provider, asegúrate de tener la API key correspondiente

## 🐛 Troubleshooting

### "API key not found"
- Verifica que el archivo `.env` existe
- Verifica que la variable está correctamente escrita
- Reinicia la aplicación después de agregar la key

### "Ollama not accessible"
- Verifica que Ollama está corriendo: `ollama serve`
- Verifica la URL en `.env` (por defecto: http://localhost:11434)
- Asegúrate de haber descargado el modelo: `ollama pull llama2`

### Modelo no aparece en la lista
- Algunos modelos pueden no estar disponibles en tu cuenta
- Para Ollama, descarga el modelo primero: `ollama pull <modelo>`
