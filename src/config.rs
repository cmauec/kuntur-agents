use anyhow::{Context, Result};
use clap::Parser;
use std::env;

/// Configuración del agente de archivos
#[derive(Debug, Clone)]
pub struct Config {
    /// URL de la API REST para clasificación
    pub api_url: String,
    /// Directorio raíz para escanear archivos
    pub root_dir: String,
    /// Extensiones de archivo a incluir (vacío = todas)
    pub extensions: Vec<String>,
    /// Tamaño máximo de archivo en bytes (default: 10MB)
    pub max_file_size: usize,
    /// Timeout de la API en segundos
    pub api_timeout_secs: u64,
    /// Incluir archivos ocultos
    pub include_hidden: bool,
    /// Número máximo de archivos a procesar (0 = ilimitado)
    pub max_files: usize,
    /// Número de workers concurrentes
    pub concurrency: usize,
    /// API Key opcional para autenticación
    pub api_key: Option<String>,
    /// Verbose logging
    pub verbose: bool,
}

#[derive(Parser, Debug)]
#[command(name = "file-agent")]
#[command(about = "Agente que escanea archivos y los envía a una API REST para clasificación")]
#[command(version)]
struct Cli {
    /// URL de la API REST
    #[arg(short, long, env = "API_URL")]
    api_url: Option<String>,

    /// Directorio a escanear
    #[arg(short, long, env = "ROOT_DIR")]
    root_dir: Option<String>,

    /// Extensiones a incluir (separadas por coma)
    #[arg(short, long, env = "EXTENSIONS")]
    extensions: Option<String>,

    /// Tamaño máximo de archivo en MB
    #[arg(long, env = "MAX_FILE_SIZE_MB", default_value = "10")]
    max_file_size_mb: usize,

    /// Timeout de API en segundos
    #[arg(long, env = "API_TIMEOUT_SECS", default_value = "30")]
    api_timeout_secs: u64,

    /// Incluir archivos ocultos
    #[arg(long, env = "INCLUDE_HIDDEN")]
    include_hidden: bool,

    /// Número máximo de archivos (0 = ilimitado)
    #[arg(short, long, env = "MAX_FILES", default_value = "0")]
    max_files: usize,

    /// Número de workers concurrentes
    #[arg(short, long, env = "CONCURRENCY", default_value = "4")]
    concurrency: usize,

    /// API Key para autenticación
    #[arg(long, env = "API_KEY")]
    api_key: Option<String>,

    /// Verbose logging
    #[arg(short, long)]
    verbose: bool,
}

impl Config {
    /// Carga la configuración desde variables de entorno y argumentos CLI
    pub fn load() -> Result<Self> {
        // Cargar .env si existe
        let _ = dotenv::dotenv();

        let cli = Cli::parse();

        let api_url = cli
            .api_url
            .or_else(|| env::var("API_URL").ok())
            .context("API_URL debe estar configurada via --api-url, .env o variable de entorno")?;

        let root_dir = cli
            .root_dir
            .or_else(|| env::var("ROOT_DIR").ok())
            .unwrap_or_else(|| ".".to_string());

        let extensions = cli
            .extensions
            .map(|e| e.split(',').map(|s| s.trim().to_lowercase()).collect())
            .unwrap_or_default();

        let max_file_size = cli.max_file_size_mb * 1024 * 1024;

        Ok(Config {
            api_url,
            root_dir,
            extensions,
            max_file_size,
            api_timeout_secs: cli.api_timeout_secs,
            include_hidden: cli.include_hidden,
            max_files: cli.max_files,
            concurrency: cli.concurrency,
            api_key: cli.api_key,
            verbose: cli.verbose,
        })
    }

    /// Valida la configuración
    pub fn validate(&self) -> Result<()> {
        if self.api_url.is_empty() {
            anyhow::bail!("API_URL no puede estar vacía");
        }

        let root = std::path::Path::new(&self.root_dir);
        if !root.exists() {
            anyhow::bail!("El directorio raíz '{}' no existe", self.root_dir);
        }

        if !root.is_dir() {
            anyhow::bail!("'{}' no es un directorio", self.root_dir);
        }

        if self.concurrency == 0 {
            anyhow::bail!("CONCURRENCY debe ser mayor a 0");
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extension_parsing() {
        let ext_str = "txt,pdf,rs,md";
        let extensions: Vec<String> = ext_str
            .split(',')
            .map(|s| s.trim().to_lowercase())
            .collect();
        assert_eq!(extensions, vec!["txt", "pdf", "rs", "md"]);
    }
}
