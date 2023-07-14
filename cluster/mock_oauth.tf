resource "kubernetes_deployment" "mock_oauth" {
  metadata {
    name = "mock-oauth"
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "mock"
      }
    }

    template {
      metadata {
        labels = {
          app = "mock"
        }
      }
      spec {
        container {
          image = "ghcr.io/navikt/mock-oauth2-server:0.5.8"
          name  = "mock-oauth"
        }
      }
    }
  }
}

resource "kubernetes_service" "mock_oauth" {
  metadata {
    name = "mock-oauth"
    labels = {
      app = "mock"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "mock"
    }
    port {
      port = 8080
    }
  }
  depends_on = [ 
    kubernetes_deployment.mock_oauth
   ]
}

resource "kubernetes_ingress_v1" "mock_oauth" {
  metadata {
    name = "mock-oauth"
    annotations = {
      #"kubernetes.io/ingress.class" = "nginx"
    }
  }
  spec {
    tls {
      secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    }
    rule {
      host = "oauth.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.mock_oauth.metadata.0.name
              port {
                number = 8080
              }
            }
          }
        }
      }
    }
  }
}
