resource "random_password" "redis_password" {
  length = 32
  special = false
}

resource "helm_release" "redis" {
  repository = local.bitnami_helm_repo
  chart      = "redis"
  version    = "17.11.3"

  name             = "redis-db"
  namespace        = "default"
  create_namespace = false

  set_sensitive {
    name  = "auth.password"
    value = random_password.redis_password.result
  }
  set {
    name  = "architecture"
    value = "standalone"
  }
}
