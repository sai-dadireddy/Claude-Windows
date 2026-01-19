# =============================================================================
# Sherpa Platform v4.1 - Main Terraform Configuration
# =============================================================================
# Account: 458798750195 | Region: us-east-1
#
# This module manages existing Sherpa infrastructure resources for import.
# Run import-commands.sh BEFORE terraform apply to import existing resources.
#
# Security Notes:
# - All secrets via Secrets Manager (NO hardcoded credentials)
# - Least-privilege IAM policies
# - WAF protection on API Gateway
# - CloudTrail audit logging enabled
# - Bedrock Guardrails for prompt safety
# =============================================================================

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "sherpa-terraform-state-458798750195"
    key            = "v4.1/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "sherpa-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Sherpa"
      Version     = "v4.1"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "platform-team"
    }
  }
}

# =============================================================================
# DATA SOURCES - Reference existing resources
# =============================================================================

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# Cognito User Pool (existing)
data "aws_cognito_user_pools" "sherpa" {
  name = "sherpa-users"
}

# =============================================================================
# DYNAMODB TABLES
# =============================================================================

# Beads Task Tracking Table
resource "aws_dynamodb_table" "sherpa_beads" {
  name         = "sherpa-beads"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "gsi1pk"
    type = "S"
  }

  attribute {
    name = "gsi1sk"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  # GSI for querying by status
  global_secondary_index {
    name            = "gsi1-index"
    hash_key        = "gsi1pk"
    range_key       = "gsi1sk"
    projection_type = "ALL"
  }

  # GSI for status-based queries
  global_secondary_index {
    name            = "status-index"
    hash_key        = "status"
    range_key       = "sk"
    projection_type = "ALL"
  }

  # TTL for automatic cleanup
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  # Point-in-time recovery for data protection
  point_in_time_recovery {
    enabled = true
  }

  # Server-side encryption with AWS managed key
  server_side_encryption {
    enabled = true
  }

  tags = {
    Name    = "sherpa-beads"
    Purpose = "Task and workflow tracking"
  }
}

# Memory Store Table
resource "aws_dynamodb_table" "sherpa_memory_store" {
  name         = "sherpa-memory-store"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "entity_type"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }

  # GSI for entity type queries
  global_secondary_index {
    name            = "entity-type-index"
    hash_key        = "entity_type"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  # TTL for memory expiration
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name    = "sherpa-memory-store"
    Purpose = "Agent memory and context storage"
  }
}

# =============================================================================
# IAM ROLES AND POLICIES
# =============================================================================

# Lambda Execution Role
resource "aws_iam_role" "sherpa_lambda_execution" {
  name = "sherpa-lambda-execution-role-v41"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name = "sherpa-lambda-execution-role"
  }
}

# Attach basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.sherpa_lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy for Sherpa Lambda functions (Least Privilege)
resource "aws_iam_role_policy" "sherpa_lambda_permissions" {
  name = "sherpa-lambda-permissions-v41"
  role = aws_iam_role.sherpa_lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "BedrockInvoke"
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.*",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.*"
        ]
      },
      {
        Sid    = "BedrockGuardrails"
        Effect = "Allow"
        Action = [
          "bedrock:ApplyGuardrail"
        ]
        Resource = "arn:aws:bedrock:${var.aws_region}:${data.aws_caller_identity.current.account_id}:guardrail/${var.guardrail_id}"
      },
      {
        Sid    = "BedrockKnowledgeBase"
        Effect = "Allow"
        Action = [
          "bedrock:Retrieve",
          "bedrock:RetrieveAndGenerate"
        ]
        Resource = "arn:aws:bedrock:${var.aws_region}:${data.aws_caller_identity.current.account_id}:knowledge-base/*"
      },
      {
        Sid    = "DynamoDBAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.sherpa_beads.arn,
          "${aws_dynamodb_table.sherpa_beads.arn}/index/*",
          aws_dynamodb_table.sherpa_memory_store.arn,
          "${aws_dynamodb_table.sherpa_memory_store.arn}/index/*"
        ]
      },
      {
        Sid    = "SecretsManagerRead"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:sherpa-*"
      },
      {
        Sid    = "CloudWatchLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/sherpa-*"
      }
    ]
  })
}

# =============================================================================
# LAMBDA LAYER - Boto3 with Bedrock support
# =============================================================================

resource "aws_lambda_layer_version" "boto3_bedrock" {
  layer_name          = "boto3-bedrock-latest"
  description         = "Latest boto3 with Bedrock support for Sherpa v4.1"
  compatible_runtimes = ["python3.11", "python3.12"]

  # Note: Upload layer zip to S3 first, then reference here
  s3_bucket = var.lambda_layer_bucket
  s3_key    = var.lambda_layer_key

  lifecycle {
    create_before_destroy = true
  }
}

# =============================================================================
# LAMBDA FUNCTIONS
# =============================================================================

# MCP Router Lambda
resource "aws_lambda_function" "mcp_router" {
  function_name = "sherpa-mcp-router"
  role          = aws_iam_role.sherpa_lambda_execution.arn
  handler       = "handler.route"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 1024

  # Placeholder - update after deployment package created
  filename         = var.lambda_package_path != "" ? "${var.lambda_package_path}/mcp-router.zip" : null
  s3_bucket        = var.lambda_package_path == "" ? var.lambda_s3_bucket : null
  s3_key           = var.lambda_package_path == "" ? "lambdas/mcp-router.zip" : null
  source_code_hash = var.lambda_source_hash

  layers = [aws_lambda_layer_version.boto3_bedrock.arn]

  environment {
    variables = {
      ENVIRONMENT       = var.environment
      LOG_LEVEL         = var.log_level
      GUARDRAIL_ID      = var.guardrail_id
      GUARDRAIL_VERSION = var.guardrail_version
      DYNAMODB_TABLE    = aws_dynamodb_table.sherpa_memory_store.name
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name     = "sherpa-mcp-router"
    Function = "MCPRouter"
  }
}

# Beads Sync Lambda
resource "aws_lambda_function" "beads_sync" {
  function_name = "sherpa-beads-sync"
  role          = aws_iam_role.sherpa_lambda_execution.arn
  handler       = "handler.sync"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  filename         = var.lambda_package_path != "" ? "${var.lambda_package_path}/beads-sync.zip" : null
  s3_bucket        = var.lambda_package_path == "" ? var.lambda_s3_bucket : null
  s3_key           = var.lambda_package_path == "" ? "lambdas/beads-sync.zip" : null
  source_code_hash = var.lambda_source_hash

  layers = [aws_lambda_layer_version.boto3_bedrock.arn]

  environment {
    variables = {
      ENVIRONMENT    = var.environment
      LOG_LEVEL      = var.log_level
      DYNAMODB_TABLE = aws_dynamodb_table.sherpa_beads.name
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name     = "sherpa-beads-sync"
    Function = "BeadsSync"
  }
}

# Agent Loader Lambda
resource "aws_lambda_function" "agent_loader" {
  function_name = "sherpa-agent-loader"
  role          = aws_iam_role.sherpa_lambda_execution.arn
  handler       = "handler.load"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  filename         = var.lambda_package_path != "" ? "${var.lambda_package_path}/agent-loader.zip" : null
  s3_bucket        = var.lambda_package_path == "" ? var.lambda_s3_bucket : null
  s3_key           = var.lambda_package_path == "" ? "lambdas/agent-loader.zip" : null
  source_code_hash = var.lambda_source_hash

  layers = [aws_lambda_layer_version.boto3_bedrock.arn]

  environment {
    variables = {
      ENVIRONMENT    = var.environment
      LOG_LEVEL      = var.log_level
      DYNAMODB_TABLE = aws_dynamodb_table.sherpa_memory_store.name
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name     = "sherpa-agent-loader"
    Function = "AgentLoader"
  }
}

# Memory KB Lambda
resource "aws_lambda_function" "memory_kb" {
  function_name = "sherpa-memory-kb"
  role          = aws_iam_role.sherpa_lambda_execution.arn
  handler       = "handler.query"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 1024

  filename         = var.lambda_package_path != "" ? "${var.lambda_package_path}/memory-kb.zip" : null
  s3_bucket        = var.lambda_package_path == "" ? var.lambda_s3_bucket : null
  s3_key           = var.lambda_package_path == "" ? "lambdas/memory-kb.zip" : null
  source_code_hash = var.lambda_source_hash

  layers = [aws_lambda_layer_version.boto3_bedrock.arn]

  environment {
    variables = {
      ENVIRONMENT       = var.environment
      LOG_LEVEL         = var.log_level
      DYNAMODB_TABLE    = aws_dynamodb_table.sherpa_memory_store.name
      GUARDRAIL_ID      = var.guardrail_id
      GUARDRAIL_VERSION = var.guardrail_version
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name     = "sherpa-memory-kb"
    Function = "MemoryKB"
  }
}

# KB Retrieve Lambda
resource "aws_lambda_function" "kb_retrieve" {
  function_name = "sherpa-kb-retrieve"
  role          = aws_iam_role.sherpa_lambda_execution.arn
  handler       = "handler.retrieve"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 1024

  filename         = var.lambda_package_path != "" ? "${var.lambda_package_path}/kb-retrieve.zip" : null
  s3_bucket        = var.lambda_package_path == "" ? var.lambda_s3_bucket : null
  s3_key           = var.lambda_package_path == "" ? "lambdas/kb-retrieve.zip" : null
  source_code_hash = var.lambda_source_hash

  layers = [aws_lambda_layer_version.boto3_bedrock.arn]

  environment {
    variables = {
      ENVIRONMENT       = var.environment
      LOG_LEVEL         = var.log_level
      GUARDRAIL_ID      = var.guardrail_id
      GUARDRAIL_VERSION = var.guardrail_version
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name     = "sherpa-kb-retrieve"
    Function = "KBRetrieve"
  }
}

# =============================================================================
# API GATEWAY
# =============================================================================

resource "aws_api_gateway_rest_api" "sherpa" {
  name        = "sherpa-api"
  description = "Sherpa Platform API v4.1"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "sherpa-api"
  }
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "sherpa" {
  rest_api_id = aws_api_gateway_rest_api.sherpa.id

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_rest_api.sherpa
  ]
}

# API Gateway Stage
resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.sherpa.id
  rest_api_id   = aws_api_gateway_rest_api.sherpa.id
  stage_name    = "prod"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId         = "$context.requestId"
      ip                = "$context.identity.sourceIp"
      caller            = "$context.identity.caller"
      user              = "$context.identity.user"
      requestTime       = "$context.requestTime"
      httpMethod        = "$context.httpMethod"
      resourcePath      = "$context.resourcePath"
      status            = "$context.status"
      protocol          = "$context.protocol"
      responseLength    = "$context.responseLength"
      integrationStatus = "$context.integrationStatus"
    })
  }

  xray_tracing_enabled = true

  tags = {
    Name = "sherpa-api-prod"
  }
}

# CloudWatch Log Group for API Gateway
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/api-gateway/sherpa-api"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "sherpa-api-logs"
  }
}

# =============================================================================
# WAF WEB ACL
# =============================================================================

resource "aws_wafv2_web_acl" "sherpa_api" {
  name        = "sherpa-api-waf"
  description = "WAF rules for Sherpa API Gateway"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  # Rate limiting rule
  rule {
    name     = "RateLimitRule"
    priority = 1

    override_action {
      none {}
    }

    statement {
      rate_based_statement {
        limit              = var.waf_rate_limit
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "SherpaRateLimitRule"
      sampled_requests_enabled   = true
    }
  }

  # AWS Managed Rules - Common Rule Set
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "SherpaCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }

  # AWS Managed Rules - Known Bad Inputs
  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 3

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "SherpaKnownBadInputs"
      sampled_requests_enabled   = true
    }
  }

  # SQL Injection protection
  rule {
    name     = "AWSManagedRulesSQLiRuleSet"
    priority = 4

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "SherpaSQLiRuleSet"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "SherpaAPIWAF"
    sampled_requests_enabled   = true
  }

  tags = {
    Name = "sherpa-api-waf"
  }
}

# Associate WAF with API Gateway
resource "aws_wafv2_web_acl_association" "sherpa_api" {
  resource_arn = aws_api_gateway_stage.prod.arn
  web_acl_arn  = aws_wafv2_web_acl.sherpa_api.arn
}

# =============================================================================
# CLOUDTRAIL - Audit Logging
# =============================================================================

resource "aws_cloudtrail" "sherpa_audit" {
  name                          = "sherpa-audit-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail         = false
  enable_logging                = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::Lambda::Function"
      values = ["arn:aws:lambda"]
    }

    data_resource {
      type   = "AWS::DynamoDB::Table"
      values = ["arn:aws:dynamodb"]
    }
  }

  cloud_watch_logs_group_arn = "${aws_cloudwatch_log_group.cloudtrail.arn}:*"
  cloud_watch_logs_role_arn  = aws_iam_role.cloudtrail_cloudwatch.arn

  tags = {
    Name = "sherpa-audit-trail"
  }
}

# S3 Bucket for CloudTrail logs
resource "aws_s3_bucket" "cloudtrail_logs" {
  bucket = "sherpa-cloudtrail-logs-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "sherpa-cloudtrail-logs"
  }
}

resource "aws_s3_bucket_policy" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.cloudtrail_logs.arn
      },
      {
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.cloudtrail_logs.arn}/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

resource "aws_s3_bucket_server_side_encryption_configuration" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_versioning" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudWatch Log Group for CloudTrail
resource "aws_cloudwatch_log_group" "cloudtrail" {
  name              = "/aws/cloudtrail/sherpa-audit"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "sherpa-cloudtrail-logs"
  }
}

# IAM Role for CloudTrail to CloudWatch
resource "aws_iam_role" "cloudtrail_cloudwatch" {
  name = "sherpa-cloudtrail-cloudwatch-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "cloudtrail.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name = "sherpa-cloudtrail-cloudwatch-role"
  }
}

resource "aws_iam_role_policy" "cloudtrail_cloudwatch" {
  name = "sherpa-cloudtrail-cloudwatch-policy"
  role = aws_iam_role.cloudtrail_cloudwatch.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "${aws_cloudwatch_log_group.cloudtrail.arn}:*"
    }]
  })
}

# =============================================================================
# COGNITO USER POOL (Import existing)
# =============================================================================

resource "aws_cognito_user_pool" "sherpa" {
  name = "sherpa-users"

  # Password policy
  password_policy {
    minimum_length                   = 12
    require_lowercase                = true
    require_numbers                  = true
    require_symbols                  = true
    require_uppercase                = true
    temporary_password_validity_days = 7
  }

  # MFA configuration
  mfa_configuration = "OPTIONAL"

  software_token_mfa_configuration {
    enabled = true
  }

  # Account recovery
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # User attribute settings
  auto_verified_attributes = ["email"]

  # Schema
  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = true

    string_attribute_constraints {
      min_length = 5
      max_length = 256
    }
  }

  # Advanced security
  user_pool_add_ons {
    advanced_security_mode = "ENFORCED"
  }

  tags = {
    Name = "sherpa-users"
  }
}

# Cognito User Pool Client
resource "aws_cognito_user_pool_client" "sherpa_web" {
  name         = "sherpa-web-client"
  user_pool_id = aws_cognito_user_pool.sherpa.id

  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  supported_identity_providers = ["COGNITO"]

  callback_urls = var.cognito_callback_urls
  logout_urls   = var.cognito_logout_urls

  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["email", "openid", "profile"]

  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }

  access_token_validity  = 1
  id_token_validity      = 1
  refresh_token_validity = 30
}

# =============================================================================
# CLOUDFRONT DISTRIBUTION (Import existing)
# =============================================================================

resource "aws_cloudfront_distribution" "sherpa" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Sherpa Platform CDN"
  default_root_object = "index.html"
  price_class         = "PriceClass_100"

  origin {
    domain_name = "${aws_api_gateway_rest_api.sherpa.id}.execute-api.${var.aws_region}.amazonaws.com"
    origin_id   = "sherpa-api"
    origin_path = "/prod"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "sherpa-api"

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Origin", "Accept"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  # WAF association
  web_acl_id = aws_wafv2_web_acl.sherpa_api.arn

  tags = {
    Name = "sherpa-cdn"
  }
}

# =============================================================================
# BEDROCK GUARDRAIL (Reference existing)
# =============================================================================

# Note: Bedrock Guardrails are managed via AWS Console or separate module
# This data source references the existing guardrail
data "aws_bedrock_guardrail" "sherpa" {
  guardrail_id = var.guardrail_id
  version      = var.guardrail_version
}
