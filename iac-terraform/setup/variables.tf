variable "rds_password" {
  description = "The password of the RDS instance"
  type        = string
}

variable "rds_username" {
  description = "The username of the RDS instance"
  type        = string
}

variable "email_addresses" {
  type        = list(string)
  description = "Email address to send notifications to"
  default = ["write2agb@gmail.com"]
}
