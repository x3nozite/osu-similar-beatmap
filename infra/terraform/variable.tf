variable "azure_subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  type = string
}

variable "location" {
  type = string
}

variable "project" {
  type = string
}

variable "vm-username" {
  type = string
}

variable "vm-password" {
  type      = string
  sensitive = true
}

variable "image-rg" {
  type = string
}

variable "database-url" {
  type      = string
  sensitive = true
}

variable "osu-client-secret" {
  type      = string
  sensitive = true
}

variable "jwt-secret" {
  type      = string
  sensitive = true
}
variable "image" {
  type = string
}
