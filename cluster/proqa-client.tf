locals {
  deploy_client = 0
}

resource "kubernetes_config_map" "client" {
  count = local.deploy_client
  metadata {
    name = "client"
  }
  data = {
    "PUBLIC_APP_URL"          = "https://proqa.gg.ax",
    "PUBLIC_API_URL"          = "https://api.proqa.gg.ax",
    "PUBLIC_EVENT_STREAM_URL" = "https://api.proqa.gg.ax/text-stream"
  }
}

resource "kubernetes_deployment" "client" {
  count = local.deploy_client
  metadata {
    name = "client"
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "client"
      }
    }

    template {
      metadata {
        labels = {
          app = "client"
        }
      }
      spec {
        container {
          image             = "registry.proqa.gg.ax/client:latest"
          image_pull_policy = "Always"
          name              = "app"

          env_from {
            config_map_ref {
              name = kubernetes_config_map.client[0].metadata.0.name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "client" {
  count = local.deploy_client
  metadata {
    name = "client"
    labels = {
      app = "client"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "client"
    }
    port {
      port = 3000
    }
  }
  depends_on = [
    kubernetes_deployment.client[0]
  ]
}

resource "kubernetes_ingress_v1" "client" {
  count = local.deploy_client
  metadata {
    name = "client"
    annotations = {
    }
  }
  spec {
    tls {
      secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    }
    rule {
      host = "proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.client[0].metadata.0.name
              port {
                number = 3000
              }
            }
          }
        }
      }
    }
  }
}
