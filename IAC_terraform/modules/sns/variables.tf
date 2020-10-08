variable "region" {
  description = "The region of the RDS instance"
  type        = string
  default     = "eu-central-1"
}

variable "display_name" {
  type        = string
  description = "Name shown in confirmation emails"
}

variable "email_addresses" {
  type        = list(string)
  description = "Email address to send notifications to"
}

variable "protocol" {
  default     = "email"
  description = "SNS Protocol to use. email or email-json"
  type        = string
}

variable "stack_name" {
  type        = string
  description = "Unique Cloudformation stack name that wraps the SNS topic."
}

variable "sns_topic_name" {
  type        = string
  description = "sns_topic_name"
}
