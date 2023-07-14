resource "helm_release" "external-dns" {
  repository = local.bitnami_helm_repo
  chart      = "external-dns"
  version    = "6.20.1"

  name      = "external-dns"
  namespace = "kube-system"

  set {
    name  = "provider"
    value = "cloudflare"
  }

  set_sensitive {
    name  = "cloudflare.apiToken"
    value = var.cloudflare_token
  }

  set {
    name  = "cloudflare.proxied"
    value = false
  }

  set {
    name  = "dryRun"
    value = false
  }
}
