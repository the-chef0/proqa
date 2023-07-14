resource "kubernetes_config_map" "pushpin" {
  count = local.deploy_backend
  metadata {
    name = "pushpin"
  }
  
  data = {
    "pushpin.conf" = "${file("${path.module}/pushpin/pushpin.conf")}"
    "routes" = "${file("${path.module}/pushpin/routes")}"
  }
}

resource "kubernetes_deployment" "pushpin" {
  count = local.deploy_backend
  metadata {
    name = "pushpin"
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "pushpin"
      }
    }

    template {
      metadata {
        labels = {
          app = "pushpin"
        }
      }
      spec {
        volume {
          name = "config"
          config_map {
            name = kubernetes_config_map.pushpin[0].metadata[0].name
            items {
              key = "pushpin.conf"
              path = "pushpin.conf"
            }
            items {
              key = "routes"
              path = "routes"
            }
          }
        }
        container {
          image = "fanout/pushpin"
          name  = "app"

          volume_mount {
            name = "config"
            mount_path = "/etc/pushpin/"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "pushpin" {
  count = local.deploy_backend
  metadata {
    name = "pushpin"
    labels = {
      app = "pushpin"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "pushpin"
    }
    port {
      name = "in-pull"
      port = 5560
    }
    port {
      name = "http-control-server"
      port = 5561
    }
    port {
      name = "in-sub"
      port = 5562
    }
    port {
      name = "control-server"
      port = 5563
    }
    port {
      name = "condure"
      port = 7999
    }
  }
  depends_on = [
    kubernetes_deployment.pushpin[0]
  ]
}
