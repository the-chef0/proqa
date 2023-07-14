resource "kubernetes_deployment" "ingress_demo" {
  metadata {
    name = "ingress-demo"
  }
  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "ing"
      }
    }

    template {
      metadata {
        labels = {
          app = "ing"
        }
      }
      spec {
        container {
          image = "nginxdemos/hello"
          name  = "demo-ing"
        }
      }
    }
  }
}

resource "kubernetes_service" "ingress_demo" {
  metadata {
    name = "ingress-demo"
    labels = {
      app = "ing"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "ing"
    }
    port {
      port = 80
    }
  }
  depends_on = [ 
    kubernetes_deployment.ingress_demo
   ]
}

resource "kubernetes_ingress_v1" "ingress_demo" {
  metadata {
    name = "ingress-demo"
    annotations = {
      #"kubernetes.io/ingress.class" = "nginx"
    }
  }
  spec {
    tls {
      secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    }
    rule {
      host = "demo.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.ingress_demo.metadata.0.name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
