locals {
  deploy_backend = 0
}

resource "kubernetes_secret" "backend_db" {
  count = local.deploy_backend
  metadata {
    name = "backend-db"
  }
  data = {
    "DATABASE_URL" : format("psql://%s:%s@post-cluster/backend", data.kubernetes_secret.backend_db_creds.data.username, data.kubernetes_secret.backend_db_creds.data.password)
  }
}

resource "kubernetes_config_map" "backend" {
  count = local.deploy_backend
  metadata {
    name = "backend"
  }
  data = {
    "APP_URL" : "api.proqa.gg.ax",
    "INTERNAL_NAME" : "backend",
    "FRONTEND_URL" : "https://proqa.gg.ax",
    "BACKEND_URL" : "https://api.proqa.gg.ax",
    "PUSHPIN_CONTROL_URI" : "http://pushpin:5561",
    "AI_SERVICE_URL" : "http://ai-service:8001/",
    "QDRANT_URL" : "http://qdrant-db:6333/"
  }
}

resource "kubernetes_deployment" "backend" {
  count = local.deploy_backend
  metadata {
    name = "backend"
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "backend"
      }
    }

    template {
      metadata {
        labels = {
          app = "backend"
        }
      }
      spec {
        volume {
          name = "documents"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim_v1.documents.metadata.0.name
            read_only  = true
          }
        }
        container {
          image             = "registry.proqa.gg.ax/backend:latest"
          image_pull_policy = "Always"
          name              = "app"

          env_from {
            config_map_ref {
              name = kubernetes_config_map.backend[0].metadata[0].name
            }
          }
          env_from {
            secret_ref {
              name = kubernetes_secret.backend_db[0].metadata[0].name
            }
          }

          volume_mount {
            name       = "documents"
            mount_path = "/documents"
          }
        }
        init_container {
          image             = "registry.proqa.gg.ax/backend:latest"
          image_pull_policy = "Always"
          name              = "migrate"

          env_from {
            config_map_ref {
              name = kubernetes_config_map.backend[0].metadata[0].name
            }
          }
          env_from {
            secret_ref {
              name = kubernetes_secret.backend_db[0].metadata[0].name
            }
          }
          env {
            name  = "FIRST"
            value = "1"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "backend" {
  count = local.deploy_backend
  metadata {
    name = "backend"
    labels = {
      app = "backend"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "backend"
    }
    port {
      port = 8000
    }
  }
  depends_on = [
    kubernetes_deployment.backend[0]
  ]
}

resource "kubernetes_ingress_v1" "backend" {
  count = local.deploy_backend
  metadata {
    name = "backend"
    annotations = {
    }
  }
  spec {
    tls {
      secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    }
    rule {
      host = "api.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.backend[0].metadata.0.name
              port {
                number = 8000
              }
            }
          }
        }
        path {
          path      = "/text-stream"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.pushpin[0].metadata.0.name
              port {
                number = 7999
              }
            }
          }
        }
      }
    }
  }
}
