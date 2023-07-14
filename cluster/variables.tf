variable "gitlab_agent_token" {
  type = string
}

variable "gitlab_agent_kas_address" {
  default = "wss://gitlab.tue.nl/-/kubernetes-agent/"
}

variable "gitlab_runner_registration_token" {
  type = string
}

variable "gitlab_runner_address" {
  default = "https://gitlab.tue.nl"
}

variable "cloudflare_token" {
  type = string
}

variable "cert_email" {
  type = string
}

variable "minio_user" {
  type = string
}

variable "minio_pass" {
  type = string
}
