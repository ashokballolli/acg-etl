# aws_lambda_layer_version.lambda_layer:

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name = var.lambda_layer_name
  s3_bucket = var.s3_bucket_layer
  s3_key = var.s3_key_layer
}


resource "aws_lambda_function" "acg-etl" {
  function_name = var.lambda_function_name
  role = aws_iam_role.lambda_sns_role01.arn
  handler = var.lambda_handler
  runtime = var.lambda_runtime
  timeout = var.lambda_timeout
  s3_bucket = var.s3_bucket
  s3_key = var.s3_key
  depends_on = [
    aws_iam_role.lambda_sns_role01
  ]
  layers = [
    aws_lambda_layer_version.lambda_layer.arn
  ]
  environment {
    variables = {
      "rds_host" = var.rds_host
      "rds_database_name" = var.rds_database_name
      "rds_username" = var.rds_username
      "rds_password" = var.rds_password
      "rds_port" = var.port
      "send_notification" = var.send_notification
      "sns_arn" = var.sns_arn
    }
  }
}

