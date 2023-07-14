resource "minio_s3_bucket" "registry" {
  bucket = "registry"
  acl    = "private"
}

resource "minio_iam_user" "registry" {
  name          = "registry"
  force_destroy = true
}

resource "minio_iam_policy" "registry" {
  name   = "registry"
  policy = <<EOT
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Principal":"*",
      "Resource": ["${minio_s3_bucket.registry.arn}", "${minio_s3_bucket.registry.arn}/*"]
    }
  ]
}
EOT
}

resource "minio_iam_user_policy_attachment" "registry" {
  user_name   = minio_iam_user.registry.id
  policy_name = minio_iam_policy.registry.id
}

resource "kubernetes_deployment" "private_registry" {
  metadata {
    name = "private-registry"
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "registry"
      }
    }

    template {
      metadata {
        labels = {
          app = "registry"
        }
      }
      spec {
        container {
          image = "registry:2.8"
          name  = "private-registry"

          env {
            name  = "REGISTRY_STORAGE"
            value = "s3"
          }
          env {
            name  = "REGISTRY_STORAGE_S3_ACCESSKEY"
            value = minio_iam_user.registry.id
          }

          env {
            name  = "REGISTRY_STORAGE_S3_SECRETKEY"
            value = minio_iam_user.registry.secret
          }

          env {
            name  = "REGISTRY_STORAGE_S3_REGION"
            value = "us-east-1"
          }

          env {
            name  = "REGISTRY_STORAGE_S3_REGIONENDPOINT"
            value = "http://minio"
          }

          env {
            name  = "REGISTRY_STORAGE_S3_BUCKET"
            value = minio_s3_bucket.registry.id
          }

          env {
            name  = "REGISTRY_STORAGE_REDIRECT_DISABLE"
            value = true
          }

          env {
            name  = "REGISTRY_STORAGE_DELETE_ENABLED"
            value = true
          }
        }
      }
    }
  }
}

resource "kubernetes_cron_job_v1" "private_registry_garbage_collect" {
  metadata {
    name = "private-registry-garbage-collect"
    namespace = "default"
  }
  spec {
    concurrency_policy            = "Replace"
    schedule                      = "42 4 * * *"
    failed_jobs_history_limit     = 5
    successful_jobs_history_limit = 10

    job_template {
      metadata {}
      spec {
        backoff_limit              = 2
        ttl_seconds_after_finished = 10

        template {
          metadata {}
          spec {
            container {
              image = "registry:2.8"
              name  = "private-registry"

              env {
                name  = "REGISTRY_STORAGE"
                value = "s3"
              }
              env {
                name  = "REGISTRY_STORAGE_S3_ACCESSKEY"
                value = minio_iam_user.registry.id
              }

              env {
                name  = "REGISTRY_STORAGE_S3_SECRETKEY"
                value = minio_iam_user.registry.secret
              }

              env {
                name  = "REGISTRY_STORAGE_S3_REGION"
                value = "us-east-1"
              }

              env {
                name  = "REGISTRY_STORAGE_S3_REGIONENDPOINT"
                value = "http://minio"
              }

              env {
                name  = "REGISTRY_STORAGE_S3_BUCKET"
                value = minio_s3_bucket.registry.id
              }

              env {
                name  = "REGISTRY_STORAGE_REDIRECT_DISABLE"
                value = true
              }

              env {
                name  = "REGISTRY_STORAGE_DELETE_ENABLED"
                value = true
              }
              command = ["bin/registry", "garbage-collect", "/etc/docker/registry/config.yml"]
            }
          }
        }
      }
    }

  }
}

resource "kubernetes_service" "private_registry" {
  metadata {
    name = "private-registry"
    labels = {
      app = "registry"
    }
  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "registry"
    }
    port {
      port = 5000
    }
  }
  depends_on = [
    kubernetes_deployment.private_registry
  ]
}

resource "kubernetes_ingress_v1" "private_registry" {
  metadata {
    name = "private-registry"
    annotations = {
      #"kubernetes.io/ingress.class" = "nginx"
    }
  }
  spec {
    tls {
      secret_name = data.kubernetes_secret.prod-cert.metadata[0].name
    }
    rule {
      host = "registry.proqa.gg.ax"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.private_registry.metadata.0.name
              port {
                number = 5000
              }
            }
          }
        }
      }
    }
  }
}
