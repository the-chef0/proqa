terraform {
  required_version = ">= 1.3.3"
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = ">= 1.38.2"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
    helm = {
      source = "hashicorp/helm"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    minio = {
      source = "aminueza/minio"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token != "" ? var.hcloud_token : local.hcloud_token
}

provider "kubernetes" {
  host                   = module.kube-hetzner.kubeconfig_data.host
  client_certificate     = module.kube-hetzner.kubeconfig_data.client_certificate
  client_key             = module.kube-hetzner.kubeconfig_data.client_key
  cluster_ca_certificate = module.kube-hetzner.kubeconfig_data.cluster_ca_certificate
}

provider "helm" {
  kubernetes {
    host                   = module.kube-hetzner.kubeconfig_data.host
    client_certificate     = module.kube-hetzner.kubeconfig_data.client_certificate
    client_key             = module.kube-hetzner.kubeconfig_data.client_key
    cluster_ca_certificate = module.kube-hetzner.kubeconfig_data.cluster_ca_certificate
  }
}

provider "kubectl" {
  host                   = module.kube-hetzner.kubeconfig_data.host
  client_certificate     = module.kube-hetzner.kubeconfig_data.client_certificate
  client_key             = module.kube-hetzner.kubeconfig_data.client_key
  cluster_ca_certificate = module.kube-hetzner.kubeconfig_data.cluster_ca_certificate
}

provider "minio" {
  minio_server   = "minio.proqa.gg.ax"
  minio_user     = kubernetes_secret.storage_user.data.CONSOLE_ACCESS_KEY
  minio_password = kubernetes_secret.storage_user.data.CONSOLE_SECRET_KEY
  minio_ssl = true
}
