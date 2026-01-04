variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "serverless-cicd"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "github_branch" {
  description = "GitHub branch"
  type        = string
  default     = "main"
}

variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  sensitive   = true
}

variable "alert_email" {
  description = "Email for alerts"
  type        = string
}

variable "lambda_environment" {
  description = "Environment variables for Lambda functions"
  type        = map(string)
  default = {
    ENVIRONMENT = "production"
    LOG_LEVEL   = "INFO"
  }
}

