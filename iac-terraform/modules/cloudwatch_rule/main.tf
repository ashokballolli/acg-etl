terraform {
  required_version = ">= 0.13.4"
}

provider "aws" {
  region = var.region
}

resource "aws_cloudwatch_event_rule" "cloudwatch_event_rule" {
  name = var.rule_name
  description = "Fires every day at 01:00AM"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "event_target" {
  rule = aws_cloudwatch_event_rule.cloudwatch_event_rule.name
  target_id = var.target_name
  arn = var.lambda_function_arn

}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_function" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.cloudwatch_event_rule.arn
}