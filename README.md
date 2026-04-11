# File Agent

Agente de Rust para analizar archivos del computador y enviar su contenido a una API REST para clasificación.

## Características

- 🔍 Escaneo recursivo de directorios
- 📁 Filtrado por extensiones de archivo
- 📤 Envío de contenido a API REST con soporte para texto y binario (base64)
- ⚡ Procesamiento concurrente configurable
- 🔐 Soporte para autenticación via API Key
- 📊 Reporte de resultados con resumen final
- 📝 Logging configurable
- ⚙️ Configuración via CLI, archivo `.env` o variables de entorno

## Instalación

### Requisitos

- Rust 1.70+ y Cargo
- Conexión a internet para dependencias

### Compilación

```bash
cargo build --release
```

El binario estará en `target/release/file-agent`

## Uso

### Básico

```bash
# Escanear directorio actual y enviar a API
./file-agent --api-url https://api.ejemplo.com

# Escanear directorio específico
./file-agent --api-url https://api.ejemplo.com --root-dir /ruta/a/escanear
```

### Configuración via variables de entorno

```bash
export API_URL="https://api.ejemplo.com"
export ROOT_DIR="/home/usuario/documentos"
export EXTENSIONS="txt,pdf,md,rs"
export API_KEY="tu-api-key-secreta"
export CONCURRENCY=8
export MAX_FILE_SIZE_MB=5
export VERBOSE=true

./file-agent
```

### Archivo .env

Crear archivo `.env` en el directorio de ejecución:

```env
API_URL=https://api.ejemplo.com
ROOT_DIR=/home/usuario/documentos
EXTENSIONS=txt,pdf,md,rs
API_KEY=your-api-key
CONCURRENCY=4
MAX_FILE_SIZE_MB=10
INCLUDE_HIDDEN=false
VERBOSE=true
```

## Opciones de línea de comandos

```
./file-agent --help

Options:
  -a, --api-url <API_URL>           URL de la API REST [env: API_URL]
  -r, --root-dir <ROOT_DIR>         Directorio a escanear [env: ROOT_DIR]
  -e, --extensions <EXTENSIONS>     Extensiones a incluir, separadas por coma [env: EXTENSIONS]
      --max-file-size-mb <MB>       Tamaño máximo de archivo en MB [default: 10] [env: MAX_FILE_SIZE_MB]
      --api-timeout-secs <SECS>     Timeout de API en segundos [default: 30] [env: API_TIMEOUT_SECS]
      --include-hidden              Incluir archivos ocultos [env: INCLUDE_HIDDEN]
  -m, --max-files <MAX_FILES>       Número máximo de archivos (0 = ilimitado) [default: 0] [env: MAX_FILES]
  -c, --concurrency <CONCURRENCY>   Número de workers concurrentes [default: 4] [env: CONCURRENCY]
      --api-key <API_KEY>           API Key para autenticación [env: API_KEY]
  -v, --verbose                     Verbose logging
  -h, --help                        Print help
  -V, --version                     Print version
```

## Protocolo de API REST

El agente espera que la API REST implemente los siguientes endpoints:

### POST /classify

Envía un archivo para clasificación.

**Request Body:**
```json
{
  "id": "uuid-v4",
  "file_name": "documento.txt",
  "relative_path": "docs/documento.txt",
  "extension": "txt",
  "mime_type": "text/plain",
  "size": 1234,
  "content": {
    "text": "contenido del archivo..."
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "metadata": null
}
```

Para archivos binarios, el contenido se envía como base64:
```json
{
  "content": {
    "base64": "base64encodedcontent...",
    "encoding": "base64"
  }
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-v4",
  "status": "success",
  "category": "documentos/texto",
  "tags": ["importante", "trabajo"],
  "confidence": 0.95,
  "metadata": {},
  "error": null
}
```

### GET /health

Verificación de salud de la API.

**Response:** HTTP 200 para API saludable

**Headers:**
- `X-API-Key`: API key para autenticación (si está configurada)

## Estructura del Proyecto

```
.
├── Cargo.toml          # Dependencias del proyecto
├── src/
│   ├── main.rs         # Punto de entrada y orquestación
│   ├── config.rs       # Configuración y CLI args
│   ├── scanner.rs      # Escaneo de archivos
│   └── api.rs          # Cliente HTTP para la API
└── README.md
```

## Ejemplo de uso completo

```bash
# Compilar
cargo build --release

# Ejecutar con todas las opciones
./target/release/file-agent \
  --api-url https://clasificador.ejemplo.com \
  --root-dir ./documentos \
  --extensions txt,pdf,docx \
  --max-file-size-mb 5 \
  --concurrency 8 \
  --api-key mi-api-key-secreta \
  --verbose
```

## Desarrollo

### Ejecutar tests

```bash
cargo test
```

### Ejecutar en modo desarrollo

```bash
cargo run -- --api-url http://localhost:3000 --verbose
```

## Licencia

MIT
