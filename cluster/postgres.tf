resource "helm_release" "postgres_operator" {
  repository = local.postgres_helm_repo
  chart      = "postgres-operator"

  name             = "postgres-operator"
  namespace        = "default"
  create_namespace = false
}

resource "helm_release" "postgres_operator_ui" {
  repository = local.postgres_ui_helm_repo
  chart      = "postgres-operator-ui"

  name             = "postgres-operator-ui"
  namespace        = "default"
  create_namespace = false
}

resource "kubernetes_manifest" "postgresql_post_cluster" {
  manifest = {
    "apiVersion" = "acid.zalan.do/v1"
    "kind"       = "postgresql"
    "metadata" = {
      "labels" = {
        "team" = "acid"
      }
      "name"      = "post-cluster"
      "namespace" = "default"
    }
    "spec" = {
      "databases" = {
        "backend" = "backend-django"
      }
      "numberOfInstances" = 1
      "postgresql" = {
        "version" = "15"
      }
      "resources" = {
        "limits" = {
          "cpu"    = "500m"
          "memory" = "500Mi"
        }
        "requests" = {
          "cpu"    = "100m"
          "memory" = "100Mi"
        }
      }
      "teamId" = "acid"
      "users" = {
        "backend-django" = []
      }
      "volume" = {
        "size" = "10Gi"
      }
    }
  }
  depends_on = [
    helm_release.postgres_operator
  ]
}

data "kubernetes_secret" "backend_db_creds" {
  metadata {
    name = "backend-django.post-cluster.credentials.postgresql.acid.zalan.do"
  }
  depends_on = [
    kubernetes_manifest.postgresql_post_cluster
  ]
}
