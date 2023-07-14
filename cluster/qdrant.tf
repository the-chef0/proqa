resource "helm_release" "qdrant" {
  repository = local.qdrant_helm_repo
  chart      = "qdrant"

  name             = "qdrant-db"
  namespace        = "default"
  create_namespace = false
}
