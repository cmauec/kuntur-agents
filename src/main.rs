mod api;
mod config;
mod scanner;

use anyhow::{Context, Result};
use std::sync::Arc;
use tokio::sync::{mpsc, Semaphore};
use tracing::{error, info, warn};

use crate::api::{ApiClient, FileResult};
use crate::config::Config;
use crate::scanner::FileScanner;

/// Resumen de la ejecución
#[derive(Debug, Default)]
struct Summary {
    total_files: usize,
    successful: usize,
    failed: usize,
    total_duration_ms: u128,
}

#[tokio::main]
async fn main() -> Result<()> {
    // Inicializar logging
    let _ = tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env()
            .add_directive(tracing::Level::INFO.into()))
        .with_target(false)
        .with_thread_ids(false)
        .with_line_number(false)
        .compact()
        .try_init();

    info!("=== File Agent v{} ===", env!("CARGO_PKG_VERSION"));

    // Cargar configuración
    let config = Config::load().context("Error al cargar configuración")?;
    config.validate().context("Configuración inválida")?;

    if config.verbose {
        info!("Configuración: {:?}", config);
    }

    // Crear escáner
    let scanner = FileScanner::new(config.clone());

    // Crear cliente de API
    let api_client = ApiClient::new(config.clone()).context("Error al crear cliente API")?;

    // Verificar salud de la API
    info!("Verificando conexión con API: {}", config.api_url);
    match api_client.health_check().await {
        Ok(true) => info!("API está disponible"),
        Ok(false) => {
            warn!("API no responde al health check, continuando de todas formas...");
        }
        Err(e) => {
            warn!("No se pudo verificar salud de API: {}", e);
        }
    }

    // Escanear archivos
    info!("Escaneando directorio: {}", config.root_dir);
    let files = scanner
        .scan_async()
        .await
        .context("Error al escanear archivos")?;

    if files.is_empty() {
        info!("No se encontraron archivos para procesar");
        return Ok(());
    }

    info!("Archivos encontrados: {}", files.len());

    // Procesar archivos concurrentemente
    let (tx, mut rx) = mpsc::channel::<FileResult>(100);
    let semaphore = Arc::new(Semaphore::new(config.concurrency));
    let api_client = Arc::new(api_client);

    // Spawn workers
    for file_info in files {
        let permit = semaphore
            .clone()
            .acquire_owned()
            .await
            .context("Error al adquirir semáforo")?;
        let tx = tx.clone();
        let client = api_client.clone();
        let verbose = config.verbose;

        tokio::spawn(async move {
            let _permit = permit; // Mantener el permit hasta que termine

            if verbose {
                info!("Procesando: {}", file_info.relative_path);
            }

            let result = client.process_file(&file_info).await;

            if let Err(e) = tx.send(result).await {
                error!("Error al enviar resultado: {}", e);
            }
        });
    }

    // Cerrar el canal de transmisión ya que no enviaremos más
    drop(tx);

    // Recolectar resultados
    let mut summary = Summary::default();
    let mut results = Vec::new();

    while let Some(result) = rx.recv().await {
        summary.total_files += 1;
        summary.total_duration_ms += result.duration_ms;

        if result.success {
            summary.successful += 1;
            if config.verbose {
                if let Some(ref response) = result.response {
                    info!(
                        "✓ {} -> Categoría: {:?}, Confianza: {:?}",
                        result.file_path,
                        response.category,
                        response.confidence
                    );
                }
            }
        } else {
            summary.failed += 1;
            if let Some(ref error) = result.error {
                warn!("✗ {} -> Error: {}", result.file_path, error);
            }
        }

        results.push(result);
    }

    // Reporte final
    println!("\n");
    println!("╔═══════════════════════════════════════════════════╗");
    println!("║            RESUMEN DE PROCESAMIENTO               ║");
    println!("╠═══════════════════════════════════════════════════╣");
    println!("║  Archivos procesados: {:>28} ║", summary.total_files);
    println!("║  Exitosos:           {:>28} ║", summary.successful);
    println!("║  Fallidos:            {:>28} ║", summary.failed);
    println!(
        "║  Tiempo promedio:     {:>24} ms ║",
        if summary.total_files > 0 {
            summary.total_duration_ms / summary.total_files as u128
        } else {
            0
        }
    );
    println!("╚═══════════════════════════════════════════════════╝");

    if summary.failed > 0 {
        std::process::exit(1);
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_summary() {
        let mut summary = Summary::default();
        summary.total_files = 10;
        summary.successful = 8;
        summary.failed = 2;
        summary.total_duration_ms = 1000;

        assert_eq!(summary.total_files, 10);
        assert_eq!(summary.successful, 8);
        assert_eq!(summary.failed, 2);
    }
}
