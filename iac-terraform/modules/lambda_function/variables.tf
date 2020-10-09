variable "region" {
  description = "The region of the RDS instance"
  type = string
  default = "eu-central-1"
}

variable "lambda_function_name" {
  description = "The Availability Zone of the RDS instance"
  type = string
}
//variable "lambda_role" {
//  description = "The Availability Zone of the RDS instance"
//  type = string
//}

variable "lambda_handler" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "lambda_runtime" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "lambda_timeout" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "lambda_layer_name" {
  description = "lambda_layer_name"
  type = string
}

variable "lambda_layer_compatible_runtimes" {
  type = list(string)
  default = [
    "python3.7"]
}

variable "s3_bucket" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "s3_key" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "s3_bucket_layer" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "s3_key_layer" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "rds_host" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "rds_database_name" {
  description = "The Availability Zone of the RDS instance"
  type = string
}

variable "rds_username" {
  description = "The username of the RDS instance"
  type = string
  default = "postgres"
}

variable "rds_password" {
  description = "The password of the RDS instance"
  type = string
}

variable "port" {
  description = "The port on which the DB accepts connections"
  type = string
}

variable "send_notification" {
  description = "The name of the RDS instance, if omitted, Terraform will assign a random, unique identifier"
  type = string
}

variable "sns_arn" {
  description = "The DB name to create. If omitted, no database is created initially"
  type = string
}
//variable "provider_from_s3" {
//  description = "The DB name to create. If omitted, no database is created initially"
//  type = string
//}
