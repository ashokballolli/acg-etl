provider "aws" {
  region = "eu-central-1"
}

terraform {
  required_version = ">= 0.13.4"
}

terraform {
  backend "s3" {
    bucket = "acg-etl-terraform-state"
    key    = "default-infrastructure"
    region = "eu-central-1"
  }
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "acg-etl-terraform-state"

  versioning {
    enabled = true
  }
}

module "rds" {
  source = "../modules/rds"
  rds_database_name = "acg_challenge_sept"
  engine = "postgres"
  engine_version = "12.3"
  identifier = "rds-acg-tf"
  multi_az = false
  port = 5432
  publicly_accessible = true
  rds_username = var.rds_username
  rds_password = var.rds_password
}

module "s3_create_bucket" {
  source = "../modules/s3"
  region = "eu-central-1"
  bucket = "acglambdafiles"
  acl = "private"
}

module "s3_upload" {
  source = "../modules/s3_upload"
  region = "eu-central-1"
  bucket = module.s3_create_bucket.s3_bucket
  acl = "public-read"
  upload_files_path = "./files_to_upload/"
  depends_on = [
    module.s3_create_bucket]
}

module "sns" {
  source = "../modules/sns"
  region = "eu-central-1"
  sns_topic_name = "sns-acg-etl"
  display_name = "acg-etl-alert"
  stack_name = "CloudformationStackNameACGEtl"
  email_addresses = var.email_addresses
}

module "lambda_function" {
  source = "../modules/lambda_function"
  lambda_function_name = "acg-etl"
  lambda_handler = "etl_wrapper.load_data"
  lambda_runtime = "python3.7"
  lambda_timeout = 30
  s3_bucket = module.s3_create_bucket.s3_bucket
  s3_key = "acg-etl.zip"
  s3_bucket_layer = module.s3_create_bucket.s3_bucket
  s3_key_layer = "python.zip"
  rds_host = module.rds.rds_hostname
  rds_database_name = module.rds.rds_db_name
  rds_username = module.rds.rds_db_username
  rds_password = module.rds.rds_db_password
  port = module.rds.rds_port
  send_notification = "True"
  sns_arn = module.sns.sns_topic_arn
  depends_on = [
    module.s3_upload
  ]
  lambda_layer_name = "pythonlibs"
}

module "cloudwatch_rule_event" {
  source = "../modules/cloudwatch_rule"
  region = "eu-central-1"
  rule_name = "schedule-acg-etl"
  target_name = module.lambda_function.function_name
  lambda_function_arn = module.lambda_function.function_arn
  lambda_function_name = module.lambda_function.function_name
//  schedule_expression = "cron(0 1 * * ? *)"
  schedule_expression = "rate(6 minutes)"
}
