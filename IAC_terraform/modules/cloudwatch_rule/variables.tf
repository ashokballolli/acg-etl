variable "region" {
  description = "The AWS region to create resources in."
  default = "eu-central-1"
}

variable "rule_name" {
  description = "The name of the CloudWatch Event Rule"
}

variable "target_name" {
  description = "The name of the CloudWatch Event Target"
}

variable "lambda_function_arn" {
  description = "lambda_function_arn"
}

variable "lambda_function_name" {
  description = "lambda_function_name"
  type = string
}

variable "schedule_expression" {
  description = "AWS cloudwatch event schedule expression"
  type = string
}
