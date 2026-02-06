# =============================================================================
# Sherpa Platform v4.1 - Variables
# =============================================================================
# All configurable parameters for the Sherpa infrastructure
#
# Security Note: NO default values for sensitive data.
# Use terraform.tfvars or environment variables for secrets.
# =============================================================================

# -----------------------------------------------------------------------------
# Core Settings
# -----------------------------------------------------------------------------

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "sherpa"
}

# -----------------------------------------------------------------------------
# Existing Resource IDs (for import)
# -----------------------------------------------------------------------------

variable "api_gateway_id" {
  description = "Existing API Gateway ID"
  type        = string
  default     = "hl98rmqgd6"
}

variable "cognito_user_pool_id" {
  description = "Existing Cognito User Pool ID"
  type        = string
  default     = "us-east-1_DS0DWtBpu"
}

variable "cloudfront_distribution_id" {
  description = "Existing CloudFront Distribution ID"
  type        = string
  default     = "dznfspanfl89s"
}

variable "guardrail_id" {
  description = "Existing Bedrock Guardrail ID"
  type        = string
  default     = "0izv8dtovrwx"
}

variable "guardrail_version" {
  description = "Bedrock Guardrail version"
  type        = string
  default     = "DRAFT"
}

# -----------------------------------------------------------------------------
# Lambda Configuration
# -----------------------------------------------------------------------------

variable "lambda_package_path" {
  description = "Local path to Lambda deployment packages (leave empty for S3)"
  type        = string
  default     = ""
}

variable "lambda_s3_bucket" {
  description = "S3 bucket containing Lambda deployment packages"
  type        = string
  default     = "sherpa-lambda-deployments-458798750195"
}

variable "lambda_source_hash" {
  description = "Source code hash for Lambda (triggers redeployment)"
  type        = string
  default     = null
}

variable "lambda_layer_bucket" {
  description = "S3 bucket for Lambda layer"
  type        = string
  default     = "sherpa-lambda-layers-458798750195"
}

variable "lambda_layer_key" {
  description = "S3 key for Lambda layer zip"
  type        = string
  default     = "layers/boto3-bedrock-latest.zip"
}

variable "lambda_memory_default" {
  description = "Default Lambda memory (MB)"
  type        = number
  default     = 512
}

variable "lambda_timeout_default" {
  description = "Default Lambda timeout (seconds)"
  type        = number
  default     = 30
}

variable "log_level" {
  description = "Lambda log level"
  type        = string
  default     = "INFO"

  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR"], var.log_level)
    error_message = "Log level must be DEBUG, INFO, WARNING, or ERROR."
  }
}

# -----------------------------------------------------------------------------
# DynamoDB Configuration
# -----------------------------------------------------------------------------

variable "dynamodb_billing_mode" {
  description = "DynamoDB billing mode"
  type        = string
  default     = "PAY_PER_REQUEST"

  validation {
    condition     = contains(["PAY_PER_REQUEST", "PROVISIONED"], var.dynamodb_billing_mode)
    error_message = "Billing mode must be PAY_PER_REQUEST or PROVISIONED."
  }
}

variable "dynamodb_read_capacity" {
  description = "DynamoDB read capacity units (only for PROVISIONED mode)"
  type        = number
  default     = 5
}

variable "dynamodb_write_capacity" {
  description = "DynamoDB write capacity units (only for PROVISIONED mode)"
  type        = number
  default     = 5
}

variable "enable_point_in_time_recovery" {
  description = "Enable DynamoDB point-in-time recovery"
  type        = bool
  default     = true
}

# -----------------------------------------------------------------------------
# API Gateway Configuration
# -----------------------------------------------------------------------------

variable "api_throttle_rate_limit" {
  description = "API Gateway throttle rate limit (requests/sec)"
  type        = number
  default     = 1000
}

variable "api_throttle_burst_limit" {
  description = "API Gateway throttle burst limit"
  type        = number
  default     = 2000
}

# -----------------------------------------------------------------------------
# WAF Configuration
# -----------------------------------------------------------------------------

variable "waf_rate_limit" {
  description = "WAF rate limit (requests per 5 min per IP)"
  type        = number
  default     = 2000
}

variable "waf_block_countries" {
  description = "List of country codes to block"
  type        = list(string)
  default     = []
}

# -----------------------------------------------------------------------------
# Cognito Configuration
# -----------------------------------------------------------------------------

variable "cognito_callback_urls" {
  description = "Allowed callback URLs for Cognito"
  type        = list(string)
  default = [
    "https://sherpa.example.com/callback",
    "http://localhost:3000/callback"
  ]
}

variable "cognito_logout_urls" {
  description = "Allowed logout URLs for Cognito"
  type        = list(string)
  default = [
    "https://sherpa.example.com/logout",
    "http://localhost:3000/logout"
  ]
}

variable "cognito_mfa_configuration" {
  description = "MFA configuration (OFF, ON, OPTIONAL)"
  type        = string
  default     = "OPTIONAL"

  validation {
    condition     = contains(["OFF", "ON", "OPTIONAL"], var.cognito_mfa_configuration)
    error_message = "MFA configuration must be OFF, ON, or OPTIONAL."
  }
}

# -----------------------------------------------------------------------------
# Logging & Monitoring
# -----------------------------------------------------------------------------

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 90

  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653], var.log_retention_days)
    error_message = "Log retention must be a valid CloudWatch retention period."
  }
}

variable "enable_xray_tracing" {
  description = "Enable X-Ray tracing for Lambda and API Gateway"
  type        = bool
  default     = true
}

variable "alarm_email" {
  description = "Email for CloudWatch alarm notifications"
  type        = string
  default     = ""
}

# -----------------------------------------------------------------------------
# Bedrock Model Configuration
# -----------------------------------------------------------------------------

variable "bedrock_model_primary" {
  description = "Primary Bedrock model ID (Opus 4.6)"
  type        = string
  default     = "us.anthropic.claude-opus-4-6-v1:0"
}

variable "bedrock_model_fallback" {
  description = "Fallback Bedrock model ID (Opus 4.5)"
  type        = string
  default     = "us.anthropic.claude-opus-4-5-20251101-v1:0"
}

variable "bedrock_max_tokens" {
  description = "Maximum tokens for Bedrock responses"
  type        = number
  default     = 4096
}

# -----------------------------------------------------------------------------
# Tags
# -----------------------------------------------------------------------------

variable "tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {}
}

variable "cost_center" {
  description = "Cost center for billing"
  type        = string
  default     = "platform"
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = "platform-team"
}
