resource "minio_s3_bucket" "documents" {
  bucket = "documents"
  acl    = "private"
}

resource "random_password" "documents" {
  special = false
  length = 8
}

output "documents_password" {
  value = random_password.documents.result
  sensitive = true
}

resource "minio_iam_user" "documents" {
  name          = "documents"
}

resource "minio_iam_policy" "documents" {
  name   = "documents"
  policy = <<EOT
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["${minio_s3_bucket.documents.arn}", "${minio_s3_bucket.documents.arn}/*"]
    }
  ]
}
EOT
}

resource "minio_iam_user_policy_attachment" "documents" {
  user_name   = minio_iam_user.documents.id
  policy_name = minio_iam_policy.documents.id
}

resource "kubernetes_persistent_volume_v1" "documents" {
  metadata {
    name = "documents-pv"
  }
  spec {
    storage_class_name = data.kubernetes_storage_class.s3-csi.metadata.0.name
    capacity = {
      storage = "32Gi"
    }

    access_modes = ["ReadOnlyMany"]
    claim_ref {
      name      = "documents-pvc"
      namespace = "default"
    }
    persistent_volume_source {
      csi {
        driver        = "ru.yandex.s3.csi"
        volume_handle = minio_s3_bucket.documents.bucket
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

resource "kubernetes_persistent_volume_claim_v1" "documents" {
  metadata {
    name      = "documents-pvc"
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
    kubernetes_persistent_volume_v1.documents
  ]
}
