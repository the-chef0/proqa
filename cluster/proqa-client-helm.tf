resource "helm_release" "client" {
  chart = "../helm/client"

  name             = "frontend"
  namespace        = "default"
  create_namespace = "false"

  set {
    name  = "ingress.tlsSecretName"
    value = data.kubernetes_secret.prod-cert.metadata[0].name
  }

  set {
    name  = "image.tag"
    value = "latest"
  }
  set {
    name  = "image.pullPolicy"
    value = "Always"
  }
}
