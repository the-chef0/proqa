resource "kubernetes_secret" "cloudflare_apitoken_secret_cert_manager" {
  metadata {
    name      = "cloudflare-apitoken-secret"
    namespace = "cert-manager"
  }

  data = {
    "apitoken" = var.cloudflare_token
  }
}


resource "kubernetes_manifest" "clusterissuer_letsencrypt_staging" {
  manifest = {
    "apiVersion" = "cert-manager.io/v1"
    "kind"       = "ClusterIssuer"
    "metadata" = {
      "name" = "letsencrypt-staging"
    }
    "spec" = {
      "acme" = {
        "email" = var.cert_email
        "privateKeySecretRef" = {
          "name" = "staging-issuer-account-key"
        }
        "server" = "https://acme-staging-v02.api.letsencrypt.org/directory"
        "solvers" = [
          {
            "dns01" = {
              "cloudflare" = {
                "apiTokenSecretRef" = {
                  "key"  = "apitoken"
                  "name" = kubernetes_secret.cloudflare_apitoken_secret_cert_manager.metadata.0.name
                }
              }
            }
            "selector" = {
              "dnsNames" = [
                "proqa.gg.ax",
                "*.proqa.gg.ax",
              ]
            }
          },
        ]
      }
    }
  }
  depends_on = [
    kubernetes_secret.cloudflare_apitoken_secret_cert_manager
  ]
}

resource "kubernetes_manifest" "clusterissuer_letsencrypt_prod" {
  manifest = {
    "apiVersion" = "cert-manager.io/v1"
    "kind"       = "ClusterIssuer"
    "metadata" = {
      "name" = "letsencrypt-prod"
    }
    "spec" = {
      "acme" = {
        "email" = var.cert_email
        "privateKeySecretRef" = {
          "name" = "prod-issuer-account-key"
        }
        "server" = "https://acme-v02.api.letsencrypt.org/directory"
        "solvers" = [
          {
            "dns01" = {
              "cloudflare" = {
                "apiTokenSecretRef" = {
                  "key"  = "apitoken"
                  "name" = kubernetes_secret.cloudflare_apitoken_secret_cert_manager.metadata.0.name
                }
              }
            }
            "selector" = {
              "dnsNames" = [
                "proqa.gg.ax",
                "*.proqa.gg.ax",
              ]
            }
          },
        ]
      }
    }
  }
  depends_on = [
    kubernetes_secret.cloudflare_apitoken_secret_cert_manager
  ]
}

resource "kubernetes_manifest" "certificate_proqa_gg_ax" {
  manifest = {
    "apiVersion" = "cert-manager.io/v1"
    "kind"       = "Certificate"
    "metadata" = {
      "name"      = "proqa-gg-ax"
      "namespace" = "default"
    }
    "spec" = {
      "commonName" = "proqa.gg.ax"
      "dnsNames" = [
        "*.proqa.gg.ax",
        "proqa.gg.ax",
      ]
      "issuerRef" = {
        "kind" = "ClusterIssuer"
        "name" = kubernetes_manifest.clusterissuer_letsencrypt_prod.manifest.metadata.name
      }
      "secretName" = "proqa-tls"
      "usages" = [
        "server auth",
        "client auth",
      ]
    }
  }
}

data "kubernetes_secret" "prod-cert" {
  metadata {
    name = kubernetes_manifest.certificate_proqa_gg_ax.manifest.spec.secretName
  }
}
