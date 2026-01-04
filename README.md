# Serverless CI/CD with Monitoring & Alerting

## 🚀 Project Overview

This project demonstrates a complete serverless CI/CD pipeline using AWS Lambda, CodePipeline, CodeBuild, and comprehensive monitoring with CloudWatch, SNS, and automated alerting. It includes automated backup, disaster recovery, and cost optimization strategies.

## 📋 Features

- **Serverless Architecture**: AWS Lambda functions for automation
- **CI/CD Pipeline**: CodePipeline and CodeBuild integration
- **Monitoring & Alerting**: CloudWatch dashboards, alarms, and SNS notifications
- **Automated Backups**: Scheduled Lambda functions for data backup
- **Disaster Recovery**: Automated recovery scripts and procedures
- **Cost Optimization**: Lambda cost monitoring and optimization
- **Event-Driven Automation**: S3, CloudWatch Events, and EventBridge triggers

## 🏗️ Architecture

```
┌─────────────┐
│   GitHub    │
│  Repository │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  CodePipeline   │
│   CI/CD Pipeline│
└──────┬──────────┘
       │
       ├──► CodeBuild
       │
       ▼
┌─────────────────┐
│  Lambda Functions│
│  (Deploy/Backup) │
└──────┬──────────┘
       │
       ├──► CloudWatch
       ├──► SNS Alerts
       └──► S3 Storage
```

## 📁 Project Structure

```
.
├── lambda/
│   ├── deploy-function/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   ├── backup-function/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   └── monitoring-function/
│       ├── lambda_function.py
│       └── requirements.txt
├── infrastructure/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── buildspec.yml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── scripts/
│   ├── deploy.sh
│   └── setup.sh
└── README.md
```

## 🛠️ Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Terraform installed
- Python 3.9+ installed

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd 3-serverless-cicd-monitoring
```

### 2. Set Up AWS Credentials

```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"
```

### 3. Deploy Infrastructure

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

Or use the setup script:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 4. Configure GitHub Webhook

1. Go to your GitHub repository settings
2. Add webhook pointing to CodePipeline webhook URL
3. Set content type to `application/json`

### 5. Deploy Application

The pipeline will automatically trigger on push to main branch.

Or deploy manually:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 📝 Configuration

### Lambda Functions

Each Lambda function is in its own directory:

- **deploy-function**: Handles application deployment
- **backup-function**: Automated backup operations
- **monitoring-function**: Health checks and monitoring

### Environment Variables

Set in Terraform variables:

```hcl
variable "lambda_environment" {
  default = {
    ENVIRONMENT = "production"
    LOG_LEVEL   = "INFO"
  }
}
```

## 🔒 Security Features

- **IAM Roles**: Least privilege access for Lambda functions
- **VPC Configuration**: Lambda functions in private subnets
- **Secrets Management**: AWS Secrets Manager integration
- **Encryption**: KMS encryption for data at rest and in transit

## 📊 Monitoring

### CloudWatch Dashboards

- Lambda invocation metrics
- Error rates and durations
- Cost tracking
- Custom business metrics

### Alarms

- High error rates
- Function timeouts
- Cost thresholds
- Custom business alerts

### SNS Notifications

- Email notifications for critical alerts
- Slack integration
- PagerDuty integration (optional)

## 💰 Cost Optimization

- **Reserved Concurrency**: Control Lambda concurrency
- **Provisioned Concurrency**: For predictable workloads
- **Cost Monitoring**: CloudWatch billing alarms
- **Right-Sizing**: Monitor and optimize memory allocation

## 🧪 Testing

Test Lambda functions locally:

```bash
cd lambda/deploy-function
pip install -r requirements.txt
python -m pytest tests/
```

## 📚 Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License

## 👤 Author

Your Name - DevOps Engineer

