resource "minio_s3_bucket" "ai_models" {
  bucket = "ai-models"
  acl    = "private"
}

resource "minio_iam_user" "ai_models" {
  name          = "ai-models"
  force_destroy = true
}

resource "minio_iam_policy" "ai_models" {
  name   = "ai-models"
  policy = <<EOT
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["${minio_s3_bucket.ai_models.arn}", "${minio_s3_bucket.ai_models.arn}/*"]
    }
  ]
}
EOT
}

resource "minio_iam_user_policy_attachment" "ai_models" {
  user_name   = minio_iam_user.ai_models.id
  policy_name = minio_iam_policy.ai_models.id
}

resource "kubernetes_persistent_volume_v1" "ai_models" {
  metadata {
    name = "ai-models-pv"
  }
  spec {
    storage_class_name = data.kubernetes_storage_class.s3-csi.metadata.0.name
    capacity = {
      storage = "32Gi"
    }

    access_modes = ["ReadOnlyMany"]
    claim_ref {
      name      = "ai-models-pvc"
      namespace = "default"
    }
    persistent_volume_source {
      csi {
        driver        = "ru.yandex.s3.csi"
        volume_handle = minio_s3_bucket.ai_models.bucket
        volume_attributes = {
          capacity = "32Gi",
          mounter  = "geesefs"
        }
        controller_publish_secret_ref {
          name      = "csi-s3-secret"
          namespace = "kube-system"
        }
        node_publish_secret_ref {
          name      = "csi-s3-secret"
          namespace = "kube-system"
        }
        node_stage_secret_ref {
          name      = "csi-s3-secret"
          namespace = "kube-system"
        }
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim_v1" "ai_models" {
  metadata {
    name      = "ai-models-pvc"
    namespace = "default"
  }
  spec {
    storage_class_name = data.kubernetes_storage_class.s3-csi.metadata.0.name
    access_modes       = ["ReadOnlyMany"]
    resources {
      requests = {
        storage = "32Gi"
      }
    }
  }

  wait_until_bound = false
  depends_on = [
    kubernetes_persistent_volume_v1.ai_models
  ]
}

resource "kubernetes_secret" "ai_models" {
  metadata {
    name = "ai-models"
  }
  data = {
    "ACCESS_KEY": minio_iam_user.ai_models.name,
    "SECRET_KEY": minio_iam_user.ai_models.secret,
    "BUCKET_NAME": "${minio_s3_bucket.ai_models.bucket}/new",
    "SERVER_ENDPOINT": "http://minio"
  }
}
