resource "helm_release" "gitlab_agent" {
  repository = local.gitlab_helm_repo
  chart      = "gitlab-agent"
  version    = "1.14.0"

  name             = "gitlab-agent"
  namespace        = "gitlab-agent"
  create_namespace = true

  set_sensitive {
    name  = "config.token"
    value = var.gitlab_agent_token
  }

  set {
    name  = "config.kasAddress"
    value = var.gitlab_agent_kas_address
  }

  set {
    name  = "rbac.create"
    value = true
  }
}
