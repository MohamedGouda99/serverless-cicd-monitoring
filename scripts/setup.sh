#!/bin/bash

set -e

echo "🚀 Setting up Serverless CI/CD infrastructure..."

# Check prerequisites
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install it first."
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure'."
    exit 1
fi

cd infrastructure

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Prompt for variables
read -p "GitHub Owner: " GITHUB_OWNER
read -p "GitHub Repository: " GITHUB_REPO
read -p "GitHub Token: " GITHUB_TOKEN
read -p "Alert Email: " ALERT_EMAIL

# Plan
echo "📋 Planning infrastructure..."
terraform plan \
  -var="github_owner=$GITHUB_OWNER" \
  -var="github_repo=$GITHUB_REPO" \
  -var="github_token=$GITHUB_TOKEN" \
  -var="alert_email=$ALERT_EMAIL"

# Apply
read -p "Apply these changes? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
    echo "🚀 Applying infrastructure..."
    terraform apply \
      -var="github_owner=$GITHUB_OWNER" \
      -var="github_repo=$GITHUB_REPO" \
      -var="github_token=$GITHUB_TOKEN" \
      -var="alert_email=$ALERT_EMAIL"
    
    echo "✅ Setup complete!"
    echo "📧 Please confirm the SNS subscription email."
else
    echo "❌ Setup cancelled."
fi

