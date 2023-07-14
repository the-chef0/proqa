locals {
  deploy_ai = 0
}

resource "kubernetes_config_map" "ai_service" {
  count = local.deploy_ai
  metadata {
    name = "ai-service"
  }
  data = {
    "MODEL_PATH": "/weights",
    "BACKEND_HTTP_URL": "http://prod-backend-app:8000",
    "PUSHPIN_HTTP_URL": "http://prod-backend-pushpin:5561",
    "THREAD_COUNT": "7"
  }
  
}

resource "kubernetes_deployment" "ai_service" {
  count = local.deploy_ai
  metadata {
    name = "ai-service"
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "ai-service"
      }
    }

    template {
      metadata {
        labels = {
          app = "ai-service"
        }
      }
      spec {
        volume {
          name = "weights"
          empty_dir {}
        }
        init_container {
          image = "minio/mc"
          name  = "copy-weights"

          env_from {
            secret_ref {
              name = kubernetes_secret.ai_models.metadata.0.name
            }
          }

          volume_mount {
            name       = "weights"
            mount_path = "/weights"
          }

          command = ["sh", "-c", "mc alias set storage $SERVER_ENDPOINT $ACCESS_KEY $SECRET_KEY && mc cp -r storage/$BUCKET_NAME/ /weights"]
        }
        container {
          image             = "registry.proqa.gg.ax/ai-service:latest"
          image_pull_policy = "Always"
          name              = "app"

          env_from {
            config_map_ref {
              name = kubernetes_config_map.ai_service.0.metadata.0.name
            }
          }
          volume_mount {
            name       = "weights"
            mount_path = "/weights"
          }
          resources {
            requests = {
              cpu    = "7000m"
              memory = "12Gi"
            }
            # limits = {
            #   memory = "7Gi"
            # }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "ai_service" {
  count = local.deploy_ai
  metadata {
    name = "ai-service"
    labels = {
      app = "ai-service"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "ai-service"
    }
    port {
      port = 8001
    }
  }
  depends_on = [
    kubernetes_deployment.ai_service
  ]
}
