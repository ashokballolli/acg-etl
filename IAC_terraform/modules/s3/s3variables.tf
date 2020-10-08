variable "region" {
  type = string
}

variable "bucket" {
  description = "(Optional, Forces new resource) The name of the bucket. If omitted, Terraform will assign a random, unique name."
  type = string
  default = null
}

variable "acl" {
  description = "(Optional) The canned ACL to apply. Defaults to 'private'."
  type = string
  default = "private"
}