use anyhow::{Context, Result};
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

use crate::config::Config;

/// Información de un archivo escaneado
#[derive(Debug, Clone)]
pub struct FileInfo {
    pub path: PathBuf,
    pub relative_path: String,
    pub size: u64,
    pub extension: Option<String>,
    pub is_hidden: bool,
    pub mime_type: Option<String>,
}

impl FileInfo {
    /// Obtiene el nombre del archivo
    pub fn file_name(&self) -> String {
        self.path
            .file_name()
            .map(|s| s.to_string_lossy().to_string())
            .unwrap_or_default()
    }

    /// Lee el contenido del archivo como bytes
    pub async fn read_bytes(&self) -> Result<Vec<u8>> {
        tokio::fs::read(&self.path)
            .await
            .with_context(|| format!("Fallo al leer archivo: {:?}", self.path))
    }

    /// Lee el contenido del archivo como string (solo para archivos de texto)
    pub async fn read_string(&self) -> Result<String> {
        let bytes = self.read_bytes().await?;
        String::from_utf8(bytes)
            .with_context(|| format!("El archivo no es UTF-8 válido: {:?}", self.path))
    }
}

/// Escáner de archivos
pub struct FileScanner {
    config: Config,
}

impl FileScanner {
    /// Crea un nuevo escáner con la configuración dada
    pub fn new(config: Config) -> Self {
        Self { config }
    }

    /// Escanea el directorio raíz y retorna los archivos encontrados
    pub fn scan(&self) -> Result<Vec<FileInfo>> {
        let root_path = Path::new(&self.config.root_dir);
        let mut files = Vec::new();

        tracing::info!("Iniciando escaneo en: {:?}", root_path);

        let walker = WalkDir::new(root_path)
            .follow_links(false)
            .into_iter()
            .filter_entry(|e| {
                // Filtrar archivos ocultos si no se incluyen
                if !self.config.include_hidden {
                    let name = e.file_name().to_string_lossy();
                    if name.starts_with('.') {
                        return false;
                    }
                }
                true
            });

        for entry in walker {
            let entry = entry.with_context(|| "Error al leer entrada del directorio")?;

            if !entry.file_type().is_file() {
                continue;
            }

            let path = entry.path().to_path_buf();

            // Verificar tamaño
            let metadata = entry.metadata()?;
            let size = metadata.len();

            if size > self.config.max_file_size as u64 {
                tracing::debug!("Archivo excede tamaño máximo: {:?}", path);
                continue;
            }

            // Obtener extensión
            let extension = path
                .extension()
                .map(|e| e.to_string_lossy().to_lowercase().to_string());

            // Filtrar por extensión si hay extensiones configuradas
            if !self.config.extensions.is_empty() {
                let ext_match = extension
                    .as_ref()
                    .map(|e| self.config.extensions.contains(e))
                    .unwrap_or(false);
                if !ext_match {
                    continue;
                }
            }

            // Calcular ruta relativa
            let relative_path = path
                .strip_prefix(root_path)
                .map(|p| p.to_string_lossy().to_string())
                .unwrap_or_else(|_| path.to_string_lossy().to_string());

            // Detectar si es oculto
            let is_hidden = path
                .file_name()
                .map(|n| n.to_string_lossy().starts_with('.'))
                .unwrap_or(false);

            // Detectar MIME type
            let mime_type = mime_guess::from_path(&path)
                .first()
                .map(|m| m.to_string());

            let file_info = FileInfo {
                path,
                relative_path,
                size,
                extension,
                is_hidden,
                mime_type,
            };

            files.push(file_info);

            // Verificar límite de archivos
            if self.config.max_files > 0 && files.len() >= self.config.max_files {
                tracing::info!("Límite de archivos alcanzado: {}", self.config.max_files);
                break;
            }
        }

        tracing::info!("Escaneo completado. Archivos encontrados: {}", files.len());

        Ok(files)
    }

    /// Escanea asíncronamente (wrapper para compatibilidad con código async)
    pub async fn scan_async(&self) -> Result<Vec<FileInfo>> {
        // WalkDir no es async, pero el I/O de disco es bloqueante
        // Usamos tokio::task::spawn_blocking para no bloquear el runtime
        let config = self.config.clone();
        tokio::task::spawn_blocking(move || {
            let scanner = FileScanner::new(config);
            scanner.scan()
        })
        .await
        .context("Error en task de escaneo")?
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    fn create_test_config(root: &Path) -> Config {
        Config {
            api_url: "http://test.com".to_string(),
            root_dir: root.to_string_lossy().to_string(),
            extensions: vec![],
            max_file_size: 1024 * 1024,
            api_timeout_secs: 30,
            include_hidden: false,
            max_files: 0,
            concurrency: 1,
            api_key: None,
            verbose: false,
        }
    }

    #[test]
    fn test_scan_finds_files() {
        let temp_dir = TempDir::new().unwrap();
        let root = temp_dir.path();

        // Crear archivos de prueba
        fs::write(root.join("test.txt"), "contenido de prueba").unwrap();
        fs::write(root.join("test.rs"), "fn main() {}").unwrap();

        let config = create_test_config(root);
        let scanner = FileScanner::new(config);
        let files = scanner.scan().unwrap();

        assert_eq!(files.len(), 2);
    }
}
