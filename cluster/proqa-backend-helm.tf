resource "helm_release" "backend" {
  chart = "../helm/backend"

  name             = "prod"
  namespace        = "default"
  create_namespace = "false"

  set {
    name  = "ingress.tlsSecretName"
    value = data.kubernetes_secret.prod-cert.metadata[0].name
  }

  set {
    name  = "image.tag"
    value = "latest"
  }
  set {
    name  = "image.pullPolicy"
    value = "Always"
  }
  set {
    name  = "aiServiceURL"
    #value = "http://217.105.46.108:4723/"
    value = "http://217.105.36.220:4723/"
  }
  set_sensitive {
    name  = "database.url"
    value = format("psql://%s:%s@post-cluster/backend", data.kubernetes_secret.backend_db_creds.data.username, data.kubernetes_secret.backend_db_creds.data.password)
  }
  set {
    name  = "documentsPVCName"
    value = kubernetes_persistent_volume_claim_v1.documents.metadata[0].name
  }
  set_sensitive {
    name  = "cacheURL"
    value = format("redis://:%s@redis-db-master:6379/1", random_password.redis_password.result)
  }
  set_sensitive {
    name  = "celeryBrokerURL"
    value = format("redis://:%s@redis-db-master:6379/2", random_password.redis_password.result)
  }
}

resource "kubernetes_ingress_v1" "backend_pushpin_ingress" {
  metadata {
    name = "backend-pushpin"
  }
  spec {
    # tls {
    #   secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    # }
    rule {
      host = "pushpin.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "prod-backend-pushpin"
              port {
                number = 5561
              }
            }
          }
        }
      }
    }
  }
  depends_on = [ 
    helm_release.backend
  ]
}
