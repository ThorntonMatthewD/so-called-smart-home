use axum::{
    extract::Json,
    handler::Handler,
    routing::get,
    routing::post,
    Router
};
use std::net::SocketAddr;
use serde::Deserialize;
use tower_http::cors::{Any, CorsLayer};

#[derive(Deserialize, Debug)]
pub struct Metric {
  metric_name: String,
  description: String,
  metric_type: String,
  data: f64
}

#[tokio::main]
async fn main() {
    // Let anything through since this only runs locally
    let cors = CorsLayer::new().allow_origin(Any);

    let app = Router::new()
        .route("/", get(root))
        .route("/receive_metrics", post(receive_metrics))
        .layer(cors);

    let addr = SocketAddr::from(([127, 0, 0, 1], 8000));
    println!("listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn shutdown_signal() {
    tokio::signal::ctrl_c()
        .await
        .expect("Expect shutdown signal handler");
    println!("signal shutdown");
}

//
// Routes
//

async fn root() -> &'static str {
    "Welcome to the Sensor Gateway - Now a bit rustier."
}

pub async fn receive_metrics(payload: String) -> String {
    let metrics: Vec<Metric> = match serde_json::from_str(payload.as_str()) {
        Ok(result) => result,
        Err(error) => return format!("ERROR: {}", error)
    };

    println!("stuff: {:#?}", metrics);

    "Your metrics have been received. Thanks!".to_string()
}
