resource "helm_release" "ai_service" {
  count = 0
  chart = "../helm/ai-service"

  name             = "ai-prod"
  namespace        = "default"
  create_namespace = "false"

  set {
    name  = "image.tag"
    value = "latest"
  }
  set {
    name  = "image.pullPolicy"
    value = "Always"
  }

  set {
    name  = "backendHTTPURL"
    value = "http://prod-backend-app:8000"
  }

  set {
    name  = "pushpinHTTPURL"
    value = "http://prod-backend-pushpin:5561"
  }

  set {
    name  = "threadCount"
    value = 4
  }

#   set {
#     name  = "weightsPVC"
#     value = kubernetes_persistent_volume_claim_v1.ai_models.metadata.0.name
#   }

  set {
    name = "weightsS3.secretName"
    value = kubernetes_secret.ai_models.metadata.0.name
  }
}
