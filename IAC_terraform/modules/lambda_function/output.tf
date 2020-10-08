output "function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.acg-etl.arn
}

output "function_invoke_arn" {
  description = "The Invoke ARN of the Lambda function"
  value       = aws_lambda_function.acg-etl.invoke_arn
}

output "function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.acg-etl.function_name
}

output "function_qualified_arn" {
  description = "The qualified ARN of the Lambda function"
  value       = aws_lambda_function.acg-etl.qualified_arn
}

//output "provider" {
//  description = "The qualified ARN of the Lambda function"
//  value       = aws_lambda_function.acg-etl.provider
//}