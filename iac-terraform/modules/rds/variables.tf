variable "region" {
  description = "The region of the RDS instance"
  type        = string
  default     = "eu-central-1"
}
variable "availability_zone" {
  description = "The Availability Zone of the RDS instance"
  type        = string
  default     = "eu-central-1a"
}
variable "rds_username" {
  description = "The username of the RDS instance"
  type        = string
  default     = "postgres"
}

variable "rds_password" {
  description = "The password of the RDS instance"
  type        = string
}

variable "port" {
  description = "The port on which the DB accepts connections"
  type        = string
}

variable "identifier" {
  description = "The name of the RDS instance, if omitted, Terraform will assign a random, unique identifier"
  type        = string
}
variable "rds_database_name" {
  description = "The DB name to create. If omitted, no database is created initially"
  type        = string
  default     = ""
}
variable "max_allocated_storage" {
  description = "Specifies the value for Storage Autoscaling"
  type        = number
  default     = 20
}
variable "engine" {
  description = "The database engine to use"
  type        = string
}

variable "engine_version" {
  description = "The engine version to use"
  type        = string
}

variable "instance_class" {
  description = "The instance type of the RDS instance"
  type        = string
  default = "db.t2.micro"
}
variable "multi_az" {
  description = "Specifies if the RDS instance is multi-AZ"
  type        = bool
  default     = false
}
variable "publicly_accessible" {
  description = "Bool to control if instance is publicly accessible"
  type        = bool
  default     = false
}

//variable "post_db_create_command" {
//  description = "Script to run after the database has been created"
//  type        = string
//}
