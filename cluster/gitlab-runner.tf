resource "minio_s3_bucket" "gitlab_runner" {
  bucket = "gitlab-runner"
  acl    = "private"
}

resource "minio_iam_user" "gitlab_runner" {
  name          = "gitlab-runner"
  force_destroy = true
}

resource "minio_iam_policy" "gitlab_runner" {
  name   = "gitlab-runner"
  policy = <<EOT
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["${minio_s3_bucket.gitlab_runner.arn}", "${minio_s3_bucket.gitlab_runner.arn}/*"]
    }
  ]
}
EOT
}

resource "minio_iam_user_policy_attachment" "gitlab_runner" {
  user_name   = minio_iam_user.gitlab_runner.id
  policy_name = minio_iam_policy.gitlab_runner.id
}

resource "kubernetes_service_account" "gitlab_service_account" {
  metadata {
    name      = "gitlab-ci-kubernetes-executor"
    namespace = "default"
  }
}

resource "kubernetes_cluster_role_binding_v1" "gitlab_service_account" {
  metadata {
    name = "gitlab-ci-kubernetes-executor"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }
  subject {
    kind      = "ServiceAccount"
    name      = "default"
    namespace = kubernetes_service_account.gitlab_service_account.metadata.0.name
  }
}

resource "helm_release" "gitlab_runner" {
  repository = local.gitlab_helm_repo
  chart      = "gitlab-runner"
  version    = "0.53.2"

  name             = "gitlab-runner"
  namespace        = "default"
  create_namespace = false

  count = 1

  set_sensitive {
    name  = "runnerRegistrationToken"
    value = var.gitlab_runner_registration_token
  }

  set {
    name  = "gitlabUrl"
    value = var.gitlab_runner_address
  }

  set {
    name  = "rbac.create"
    value = "true"
  }

  set_sensitive {
    name = "runners.config"
    value = templatefile("gitlab-runner-config.tftpl",
      {
        s3_url      = "minio",
        bucket_name = minio_s3_bucket.gitlab_runner.id,
        accesskey   = minio_iam_user.gitlab_runner.name
        secretkey   = minio_iam_user.gitlab_runner.secret
      }
    )
  }

  depends_on = [
    kubernetes_cluster_role_binding_v1.gitlab_service_account
  ]
}
