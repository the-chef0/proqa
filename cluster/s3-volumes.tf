resource "helm_release" "s3-csi" {
  chart = "oci://cr.yandex/crp9ftr22d26age3hulg/yandex-cloud/csi-s3/csi-s3"

  name             = "s3-csi"
  namespace        = "kube-system"
  create_namespace = false

  set {
    name  = "secret.endpoint"
    value = "https://minio.proqa.gg.ax"
  }

  set_sensitive {
    name  = "secret.accessKey"
    value = kubernetes_secret.storage_user.data.CONSOLE_ACCESS_KEY
  }

  set_sensitive {
    name  = "secret.secretKey"
    value = kubernetes_secret.storage_user.data.CONSOLE_SECRET_KEY
  }

  set {
    name  = "storageClass.singleBucket"
    value = "cluster-volumes"
  }

  set {
    name = "storageClass.mountOptions"
    value = "--memory-limit 1000 --dir-mode 0777 --file-mode 0777"
  }
}

data "kubernetes_storage_class" "s3-csi" {
  metadata {
    name = "csi-s3"
  }
  depends_on = [ helm_release.s3-csi ]
}

# resource "kubernetes_persistent_volume_claim" "gitlab_builds_cache" {
#   metadata {
#     name      = "gitlab-ci-kubernetes-executor-builds-cache"
#     namespace = "default"
#   }
#   spec {
#     storage_class_name = data.kubernetes_storage_class.s3-csi.metadata[0].name
#     access_modes       = ["ReadWriteMany"]
#     resources {
#       requests = {
#         storage = "30Gi"
#       }
#     }
#   }
#   wait_until_bound = false
# }
