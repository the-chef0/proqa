resource "helm_release" "minio_operator" {
  repository = local.minio_helm_repo
  chart      = "operator"

  name             = "minio-operator"
  namespace        = "minio-operator"
  create_namespace = true
}

resource "kubernetes_secret" "storage_configuration" {
  metadata {
    name      = "storage-configuration"
    namespace = "default"
  }
  binary_data = {
    "config.env" = filebase64("minio-storage-configuration.config")
  }
}

resource "kubernetes_secret" "storage_user" {
  metadata {
    name      = "storage-user"
    namespace = "default"
  }
  data = {
    "CONSOLE_ACCESS_KEY" = "console"
    "CONSOLE_SECRET_KEY" = "console123"
  }
}

resource "kubernetes_manifest" "tenant_myminio" {
  manifest = {
    "apiVersion" = "minio.min.io/v2"
    "kind"       = "Tenant"
    "metadata" = {
      "annotations" = {
        "prometheus.io/path"   = "/minio/v2/metrics/cluster"
        "prometheus.io/port"   = "9000"
        "prometheus.io/scrape" = "true"
      }
      "labels" = {
        "app" = "minio"
      }
      "name"      = "myminio"
      "namespace" = "default"
    }
    "spec" = {
      "certConfig" = {}
      "configuration" = {
        "name" = "storage-configuration"
      }
      "env" = [
        # {
        #   "name"  = "MINIO_DOMAIN"
        #   "value" = "minio.proqa.gg.ax"
        # },
        {
          "name"  = "MINIO_BROWSER_REDIRECT_URL"
          "value" = "https://console.proqa.gg.ax"
        },
        {
          "name"  = "MINIO_SERVER_URL"
          "value" = "http://minio"
        },
      ]
      "externalCaCertSecret"      = []
      "externalCertSecret"        = []
      "externalClientCertSecrets" = []
      "features" = {
        "bucketDNS" = false
        "domains"   = {}
      }
      "image"               = "quay.io/minio/minio:RELEASE.2023-06-02T23-17-26Z"
      "imagePullSecret"     = {}
      "mountPath"           = "/export"
      "podManagementPolicy" = "Parallel"
      "pools" = [
        {
          "affinity" = {
            "nodeAffinity"    = {}
            "podAffinity"     = {}
            "podAntiAffinity" = {}
          }
          "containerSecurityContext" = {
            "runAsGroup"   = 1000
            "runAsNonRoot" = true
            "runAsUser"    = 1000
          }
          "name"         = "pool-0"
          "nodeSelector" = {}
          "resources"    = {}
          "securityContext" = {
            "fsGroup"      = 1000
            "runAsGroup"   = 1000
            "runAsNonRoot" = true
            "runAsUser"    = 1000
          }
          "servers"     = 1
          "tolerations" = []
          "volumeClaimTemplate" = {
            "apiVersion" = "v1"
            "kind"       = "persistentvolumeclaims"
            "metadata"   = {}
            "spec" = {
              "accessModes" = [
                "ReadWriteOnce",
              ]
              "resources" = {
                "requests" = {
                  "storage" = "64Gi"
                }
              }
              "storageClassName" = "hcloud-volumes"
            }
            "status" = {}
          }
          "volumesPerServer" = 2
        },
      ]
      "priorityClassName"  = ""
      "requestAutoCert"    = false
      "serviceAccountName" = ""
      "serviceMetadata" = {
        "consoleServiceAnnotations" = {}
        "consoleServiceLabels"      = {}
        "minioServiceAnnotations"   = {}
        "minioServiceLabels"        = {}
      }
      "subPath" = ""
      "users" = [
        {
          "name" = "storage-user"
        },
      ]
    }
  }
  depends_on = [
    kubernetes_secret.storage_user,
    kubernetes_secret.storage_configuration
  ]
}

resource "kubernetes_ingress_v1" "minio" {
  metadata {
    name = "minio"
    annotations = {
    }
  }
  spec {
    tls {
      secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    }
    rule {
      host = "minio.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "minio"
              port {
                number = 80
              }
            }
          }
        }
      }
    }
    rule {
      host = "console.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "myminio-console"
              port {
                number = 9090
              }
            }
          }
        }
      }
    }
  }
}
