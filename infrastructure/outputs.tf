output "codepipeline_name" {
  description = "CodePipeline name"
  value       = aws_codepipeline.main.name
}

output "codepipeline_arn" {
  description = "CodePipeline ARN"
  value       = aws_codepipeline.main.arn
}

output "lambda_deploy_function_name" {
  description = "Deploy Lambda function name"
  value       = aws_lambda_function.deploy.function_name
}

output "lambda_backup_function_name" {
  description = "Backup Lambda function name"
  value       = aws_lambda_function.backup.function_name
}

output "lambda_monitoring_function_name" {
  description = "Monitoring Lambda function name"
  value       = aws_lambda_function.monitoring.function_name
}

output "sns_topic_arn" {
  description = "SNS topic ARN for alerts"
  value       = aws_sns_topic.alerts.arn
}

output "cloudwatch_dashboard_url" {
  description = "CloudWatch Dashboard URL"
  value       = "https://${var.aws_region}.console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.main.dashboard_name}"
}

