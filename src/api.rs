use anyhow::{Context, Result};
use reqwest::{Client, StatusCode};
use serde::{Deserialize, Serialize};

use crate::config::Config;
use crate::scanner::FileInfo;

/// Petición de clasificación enviada a la API
#[derive(Debug, Serialize)]
pub struct ClassificationRequest {
    /// ID único de la solicitud
    pub id: String,
    /// Nombre del archivo
    pub file_name: String,
    /// Ruta relativa del archivo
    pub relative_path: String,
    /// Extensión del archivo
    pub extension: Option<String>,
    /// Tipo MIME
    pub mime_type: Option<String>,
    /// Tamaño en bytes
    pub size: u64,
    /// Contenido del archivo (bytes en base64 o texto)
    pub content: FileContent,
    /// Timestamp del análisis
    pub timestamp: String,
    /// Metadata adicional
    pub metadata: Option<serde_json::Value>,
}

/// Contenido del archivo
#[derive(Debug, Serialize, Clone)]
#[serde(untagged)]
pub enum FileContent {
    /// Contenido como texto
    Text { text: String },
    /// Contenido como base64
    Binary { base64: String, encoding: String },
}

impl FileContent {
    /// Crea contenido desde bytes, detectando si es texto o binario
    pub fn from_bytes(bytes: Vec<u8>, mime_type: Option<&str>) -> Self {
        // Si es un tipo de texto conocido, intentamos convertir a string
        let is_text = mime_type.map(|m| {
            m.starts_with("text/") ||
            m == "application/json" ||
            m == "application/xml" ||
            m == "application/javascript" ||
            m.ends_with("+json") ||
            m.ends_with("+xml")
        }).unwrap_or(false);

        if is_text {
            if let Ok(text) = String::from_utf8(bytes.clone()) {
                return FileContent::Text { text };
            }
        }

        // Si no es texto o falló la conversión, usar base64
        FileContent::Binary {
            base64: base64::encode(&bytes),
            encoding: "base64".to_string(),
        }
    }

    /// Crea contenido de texto
    pub fn text(text: String) -> Self {
        FileContent::Text { text }
    }
}

/// Respuesta de clasificación de la API
#[derive(Debug, Deserialize)]
pub struct ClassificationResponse {
    /// ID de la solicitud
    pub id: String,
    /// Estado de la clasificación
    pub status: String,
    /// Categoría asignada
    pub category: Option<String>,
    /// Tags o etiquetas
    pub tags: Option<Vec<String>>,
    /// Score de confianza (0-1)
    pub confidence: Option<f64>,
    /// Metadata adicional de la respuesta
    pub metadata: Option<serde_json::Value>,
    /// Mensaje de error si aplica
    pub error: Option<String>,
}

/// Resultado del procesamiento de un archivo
#[derive(Debug)]
pub struct FileResult {
    pub file_path: String,
    pub success: bool,
    pub response: Option<ClassificationResponse>,
    pub error: Option<String>,
    pub duration_ms: u128,
}

/// Cliente de la API REST
pub struct ApiClient {
    client: Client,
    config: Config,
    base_url: String,
}

impl ApiClient {
    /// Crea un nuevo cliente de API
    pub fn new(config: Config) -> Result<Self> {
        let timeout = std::time::Duration::from_secs(config.api_timeout_secs);

        let client = Client::builder()
            .timeout(timeout)
            .build()
            .context("Error al crear cliente HTTP")?;

        let base_url = config.api_url.trim_end_matches('/').to_string();

        Ok(ApiClient {
            client,
            config,
            base_url,
        })
    }

    /// Envía un archivo para clasificación
    pub async fn classify_file(
        &self,
        file_info: &FileInfo,
        content: FileContent,
    ) -> Result<ClassificationResponse> {
        let id = uuid::Uuid::new_v4().to_string();
        let timestamp = chrono::Utc::now().to_rfc3339();

        let request = ClassificationRequest {
            id,
            file_name: file_info.file_name(),
            relative_path: file_info.relative_path.clone(),
            extension: file_info.extension.clone(),
            mime_type: file_info.mime_type.clone(),
            size: file_info.size,
            content,
            timestamp,
            metadata: None,
        };

        let url = format!("{}/classify", self.base_url);

        let mut request_builder = self.client.post(&url).json(&request);

        // Agregar API key si está configurada
        if let Some(ref api_key) = self.config.api_key {
            request_builder = request_builder.header("X-API-Key", api_key);
        }

        let response = request_builder
            .send()
            .await
            .context("Error al enviar solicitud a la API")?;

        let status = response.status();

        if status.is_success() {
            let classification: ClassificationResponse = response
                .json()
                .await
                .context("Error al parsear respuesta de la API")?;
            Ok(classification)
        } else {
            let error_text = response
                .text()
                .await
                .unwrap_or_else(|_| "Error desconocido".to_string());

            anyhow::bail!(
                "API retornó error {}: {}",
                status.as_u16(),
                error_text
            )
        }
    }

    /// Verifica la salud de la API
    pub async fn health_check(&self) -> Result<bool> {
        let url = format!("{}/health", self.base_url);

        match self.client.get(&url).send().await {
            Ok(response) => {
                let status = response.status();
                Ok(status == StatusCode::OK || status == StatusCode::NO_CONTENT)
            }
            Err(_) => Ok(false),
        }
    }

    /// Procesa un archivo completo (lee + envía)
    pub async fn process_file(&self, file_info: &FileInfo) -> FileResult {
        let start = std::time::Instant::now();

        // Leer archivo
        let content_bytes = match file_info.read_bytes().await {
            Ok(bytes) => bytes,
            Err(e) => {
                return FileResult {
                    file_path: file_info.relative_path.clone(),
                    success: false,
                    response: None,
                    error: Some(format!("Error al leer archivo: {}", e)),
                    duration_ms: start.elapsed().as_millis(),
                }
            }
        };

        // Crear contenido
        let content = FileContent::from_bytes(content_bytes, file_info.mime_type.as_deref());

        // Enviar a API
        match self.classify_file(file_info, content).await {
            Ok(response) => FileResult {
                file_path: file_info.relative_path.clone(),
                success: true,
                response: Some(response),
                error: None,
                duration_ms: start.elapsed().as_millis(),
            },
            Err(e) => FileResult {
                file_path: file_info.relative_path.clone(),
                success: false,
                response: None,
                error: Some(format!("Error al clasificar: {}", e)),
                duration_ms: start.elapsed().as_millis(),
            },
        }
    }
}

// Implementación simple de base64 para no depender de crate externo
mod base64 {
    pub fn encode(input: &[u8]) -> String {
        const CHARSET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        let mut result = String::new();

        for chunk in input.chunks(3) {
            let b = match chunk.len() {
                1 => {
                    let b = [chunk[0], 0, 0];
                    let n = (b[0] as usize) << 16;
                    (n, 2)
                }
                2 => {
                    let b = [chunk[0], chunk[1], 0];
                    let n = ((b[0] as usize) << 16) | ((b[1] as usize) << 8);
                    (n, 1)
                }
                _ => {
                    let n = ((chunk[0] as usize) << 16)
                        | ((chunk[1] as usize) << 8)
                        | (chunk[2] as usize);
                    (n, 0)
                }
            };

            result.push(CHARSET[(b.0 >> 18) & 0x3F] as char);
            result.push(CHARSET[(b.0 >> 12) & 0x3F] as char);
            if b.1 <= 1 {
                result.push(CHARSET[(b.0 >> 6) & 0x3F] as char);
            } else {
                result.push('=');
            }
            if b.1 == 0 {
                result.push(CHARSET[b.0 & 0x3F] as char);
            } else {
                result.push('=');
            }
        }

        result
    }
}
