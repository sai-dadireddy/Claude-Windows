# =============================================================================
# Sherpa Platform v4.1 - Outputs
# =============================================================================
# Exposes key resource ARNs, IDs, and endpoints for integration
# =============================================================================

# -----------------------------------------------------------------------------
# Account & Region
# -----------------------------------------------------------------------------

output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS Region"
  value       = data.aws_region.current.name
}

# -----------------------------------------------------------------------------
# DynamoDB Tables
# -----------------------------------------------------------------------------

output "dynamodb_tables" {
  description = "DynamoDB table details"
  value = {
    beads = {
      name = aws_dynamodb_table.sherpa_beads.name
      arn  = aws_dynamodb_table.sherpa_beads.arn
    }
    memory_store = {
      name = aws_dynamodb_table.sherpa_memory_store.name
      arn  = aws_dynamodb_table.sherpa_memory_store.arn
    }
  }
}

output "dynamodb_beads_table_name" {
  description = "Beads DynamoDB table name"
  value       = aws_dynamodb_table.sherpa_beads.name
}

output "dynamodb_memory_table_name" {
  description = "Memory Store DynamoDB table name"
  value       = aws_dynamodb_table.sherpa_memory_store.name
}

# -----------------------------------------------------------------------------
# Lambda Functions
# -----------------------------------------------------------------------------

output "lambda_functions" {
  description = "Lambda function details"
  value = {
    mcp_router = {
      name = aws_lambda_function.mcp_router.function_name
      arn  = aws_lambda_function.mcp_router.arn
    }
    beads_sync = {
      name = aws_lambda_function.beads_sync.function_name
      arn  = aws_lambda_function.beads_sync.arn
    }
    agent_loader = {
      name = aws_lambda_function.agent_loader.function_name
      arn  = aws_lambda_function.agent_loader.arn
    }
    memory_kb = {
      name = aws_lambda_function.memory_kb.function_name
      arn  = aws_lambda_function.memory_kb.arn
    }
    kb_retrieve = {
      name = aws_lambda_function.kb_retrieve.function_name
      arn  = aws_lambda_function.kb_retrieve.arn
    }
  }
}

output "lambda_execution_role_arn" {
  description = "Lambda execution role ARN"
  value       = aws_iam_role.sherpa_lambda_execution.arn
}

output "lambda_layer_arn" {
  description = "Boto3 Bedrock Lambda layer ARN"
  value       = aws_lambda_layer_version.boto3_bedrock.arn
}

# -----------------------------------------------------------------------------
# API Gateway
# -----------------------------------------------------------------------------

output "api_gateway" {
  description = "API Gateway details"
  value = {
    id            = aws_api_gateway_rest_api.sherpa.id
    name          = aws_api_gateway_rest_api.sherpa.name
    stage_name    = aws_api_gateway_stage.prod.stage_name
    invoke_url    = aws_api_gateway_stage.prod.invoke_url
    execution_arn = aws_api_gateway_rest_api.sherpa.execution_arn
  }
}

output "api_gateway_invoke_url" {
  description = "API Gateway invoke URL"
  value       = aws_api_gateway_stage.prod.invoke_url
}

output "api_gateway_id" {
  description = "API Gateway REST API ID"
  value       = aws_api_gateway_rest_api.sherpa.id
}

# -----------------------------------------------------------------------------
# WAF
# -----------------------------------------------------------------------------

output "waf_web_acl" {
  description = "WAF Web ACL details"
  value = {
    id   = aws_wafv2_web_acl.sherpa_api.id
    arn  = aws_wafv2_web_acl.sherpa_api.arn
    name = aws_wafv2_web_acl.sherpa_api.name
  }
}

output "waf_web_acl_arn" {
  description = "WAF Web ACL ARN"
  value       = aws_wafv2_web_acl.sherpa_api.arn
}

# -----------------------------------------------------------------------------
# CloudTrail
# -----------------------------------------------------------------------------

output "cloudtrail" {
  description = "CloudTrail details"
  value = {
    name      = aws_cloudtrail.sherpa_audit.name
    arn       = aws_cloudtrail.sherpa_audit.arn
    s3_bucket = aws_s3_bucket.cloudtrail_logs.id
    log_group = aws_cloudwatch_log_group.cloudtrail.name
  }
}

output "cloudtrail_s3_bucket" {
  description = "CloudTrail S3 bucket name"
  value       = aws_s3_bucket.cloudtrail_logs.id
}

# -----------------------------------------------------------------------------
# Cognito
# -----------------------------------------------------------------------------

output "cognito" {
  description = "Cognito User Pool details"
  value = {
    user_pool_id       = aws_cognito_user_pool.sherpa.id
    user_pool_arn      = aws_cognito_user_pool.sherpa.arn
    user_pool_endpoint = aws_cognito_user_pool.sherpa.endpoint
    client_id          = aws_cognito_user_pool_client.sherpa_web.id
  }
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.sherpa.id
}

output "cognito_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.sherpa_web.id
}

# -----------------------------------------------------------------------------
# CloudFront
# -----------------------------------------------------------------------------

output "cloudfront" {
  description = "CloudFront distribution details"
  value = {
    id          = aws_cloudfront_distribution.sherpa.id
    domain_name = aws_cloudfront_distribution.sherpa.domain_name
    arn         = aws_cloudfront_distribution.sherpa.arn
  }
}

output "cloudfront_domain" {
  description = "CloudFront domain name"
  value       = aws_cloudfront_distribution.sherpa.domain_name
}

# -----------------------------------------------------------------------------
# Bedrock Guardrail
# -----------------------------------------------------------------------------

output "bedrock_guardrail" {
  description = "Bedrock Guardrail details"
  value = {
    id      = var.guardrail_id
    version = var.guardrail_version
  }
}

# -----------------------------------------------------------------------------
# IAM Summary (for review)
# -----------------------------------------------------------------------------

output "iam_roles" {
  description = "IAM roles created"
  value = {
    lambda_execution = {
      name = aws_iam_role.sherpa_lambda_execution.name
      arn  = aws_iam_role.sherpa_lambda_execution.arn
    }
    cloudtrail_cloudwatch = {
      name = aws_iam_role.cloudtrail_cloudwatch.name
      arn  = aws_iam_role.cloudtrail_cloudwatch.arn
    }
  }
}

# -----------------------------------------------------------------------------
# Environment Configuration
# -----------------------------------------------------------------------------

output "environment_config" {
  description = "Environment configuration for applications"
  value = {
    region            = data.aws_region.current.name
    environment       = var.environment
    api_endpoint      = aws_api_gateway_stage.prod.invoke_url
    cloudfront_url    = "https://${aws_cloudfront_distribution.sherpa.domain_name}"
    cognito_domain    = aws_cognito_user_pool.sherpa.endpoint
    dynamodb_beads    = aws_dynamodb_table.sherpa_beads.name
    dynamodb_memory   = aws_dynamodb_table.sherpa_memory_store.name
    guardrail_id      = var.guardrail_id
    guardrail_version = var.guardrail_version
  }
}

# -----------------------------------------------------------------------------
# Security Summary
# -----------------------------------------------------------------------------

output "security_summary" {
  description = "Security configuration summary"
  value = {
    waf_enabled            = true
    cloudtrail_enabled     = true
    encryption_at_rest     = true
    cognito_mfa            = var.cognito_mfa_configuration
    xray_tracing           = var.enable_xray_tracing
    log_retention_days     = var.log_retention_days
    point_in_time_recovery = var.enable_point_in_time_recovery
  }
}

# -----------------------------------------------------------------------------
# Import Commands Reference
# -----------------------------------------------------------------------------

output "import_commands_reference" {
  description = "Reference IDs for terraform import"
  value = {
    note = "Run import-commands.sh before terraform apply"
    resources = {
      api_gateway_id          = var.api_gateway_id
      cognito_user_pool_id    = var.cognito_user_pool_id
      cloudfront_distribution = var.cloudfront_distribution_id
      guardrail_id            = var.guardrail_id
    }
  }
}
