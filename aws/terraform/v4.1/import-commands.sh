#!/bin/bash
# =============================================================================
# Sherpa Platform v4.1 - Terraform Import Commands
# =============================================================================
# Account: 458798750195 | Region: us-east-1
#
# IMPORTANT: Run these commands BEFORE 'terraform apply' to import existing
# resources into Terraform state. This prevents Terraform from trying to
# create resources that already exist.
#
# Usage:
#   chmod +x import-commands.sh
#   ./import-commands.sh
#
# Prerequisites:
#   - AWS CLI configured with correct credentials
#   - Terraform initialized (terraform init)
#   - Correct AWS account (458798750195)
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ACCOUNT_ID="458798750195"
REGION="us-east-1"

echo -e "${YELLOW}============================================${NC}"
echo -e "${YELLOW}Sherpa v4.1 - Terraform Import Script${NC}"
echo -e "${YELLOW}============================================${NC}"
echo ""

# -----------------------------------------------------------------------------
# Verify AWS Account
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[1/9] Verifying AWS account...${NC}"
CURRENT_ACCOUNT=$(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo "ERROR")

if [ "$CURRENT_ACCOUNT" != "$ACCOUNT_ID" ]; then
    echo -e "${RED}ERROR: Wrong AWS account!${NC}"
    echo "Expected: $ACCOUNT_ID"
    echo "Current:  $CURRENT_ACCOUNT"
    echo ""
    echo "Please configure correct credentials and try again."
    exit 1
fi
echo -e "${GREEN}Account verified: $ACCOUNT_ID${NC}"
echo ""

# -----------------------------------------------------------------------------
# Initialize Terraform
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[2/9] Checking Terraform initialization...${NC}"
if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init
fi
echo -e "${GREEN}Terraform initialized${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import DynamoDB Tables
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[3/9] Importing DynamoDB tables...${NC}"

# Check if sherpa-beads exists
if aws dynamodb describe-table --table-name sherpa-beads --region $REGION >/dev/null 2>&1; then
    echo "Importing sherpa-beads table..."
    terraform import aws_dynamodb_table.sherpa_beads sherpa-beads || echo "Already imported or import failed"
else
    echo "Table sherpa-beads does not exist (will be created)"
fi

# Check if sherpa-memory-store exists
if aws dynamodb describe-table --table-name sherpa-memory-store --region $REGION >/dev/null 2>&1; then
    echo "Importing sherpa-memory-store table..."
    terraform import aws_dynamodb_table.sherpa_memory_store sherpa-memory-store || echo "Already imported or import failed"
else
    echo "Table sherpa-memory-store does not exist (will be created)"
fi

echo -e "${GREEN}DynamoDB import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import Lambda Functions
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[4/9] Importing Lambda functions...${NC}"

LAMBDAS=(
    "sherpa-mcp-router:aws_lambda_function.mcp_router"
    "sherpa-beads-sync:aws_lambda_function.beads_sync"
    "sherpa-agent-loader:aws_lambda_function.agent_loader"
    "sherpa-memory-kb:aws_lambda_function.memory_kb"
    "sherpa-kb-retrieve:aws_lambda_function.kb_retrieve"
)

for item in "${LAMBDAS[@]}"; do
    FUNC_NAME="${item%%:*}"
    TF_RESOURCE="${item##*:}"

    if aws lambda get-function --function-name $FUNC_NAME --region $REGION >/dev/null 2>&1; then
        echo "Importing $FUNC_NAME..."
        terraform import $TF_RESOURCE $FUNC_NAME || echo "Already imported or import failed"
    else
        echo "Lambda $FUNC_NAME does not exist (will be created)"
    fi
done

echo -e "${GREEN}Lambda import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import Lambda Layer
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[5/9] Importing Lambda layer...${NC}"

# Get the latest version of the layer
LAYER_ARN=$(aws lambda list-layer-versions \
    --layer-name boto3-bedrock-latest \
    --region $REGION \
    --query 'LayerVersions[0].LayerVersionArn' \
    --output text 2>/dev/null || echo "")

if [ -n "$LAYER_ARN" ] && [ "$LAYER_ARN" != "None" ]; then
    echo "Importing boto3-bedrock-latest layer..."
    terraform import aws_lambda_layer_version.boto3_bedrock "$LAYER_ARN" || echo "Already imported or import failed"
else
    echo "Lambda layer boto3-bedrock-latest does not exist (will be created)"
fi

echo -e "${GREEN}Lambda layer import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import API Gateway
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[6/9] Importing API Gateway...${NC}"

API_ID="hl98rmqgd6"

if aws apigateway get-rest-api --rest-api-id $API_ID --region $REGION >/dev/null 2>&1; then
    echo "Importing API Gateway..."
    terraform import aws_api_gateway_rest_api.sherpa $API_ID || echo "Already imported or import failed"

    # Import stage
    echo "Importing API Gateway stage (prod)..."
    terraform import aws_api_gateway_stage.prod "${API_ID}/prod" || echo "Already imported or import failed"
else
    echo "API Gateway $API_ID does not exist (will be created)"
fi

echo -e "${GREEN}API Gateway import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import WAF Web ACL
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[7/9] Importing WAF Web ACL...${NC}"

WAF_NAME="sherpa-api-waf"

# Get WAF ARN
WAF_ARN=$(aws wafv2 list-web-acls \
    --scope REGIONAL \
    --region $REGION \
    --query "WebACLs[?Name=='$WAF_NAME'].ARN" \
    --output text 2>/dev/null || echo "")

if [ -n "$WAF_ARN" ] && [ "$WAF_ARN" != "None" ]; then
    # Extract ID and Name from ARN for import
    # ARN format: arn:aws:wafv2:region:account:regional/webacl/name/id
    WAF_ID=$(echo $WAF_ARN | rev | cut -d'/' -f1 | rev)
    echo "Importing WAF Web ACL (ID: $WAF_ID)..."
    terraform import aws_wafv2_web_acl.sherpa_api "${WAF_ID}/${WAF_NAME}/REGIONAL" || echo "Already imported or import failed"
else
    echo "WAF Web ACL $WAF_NAME does not exist (will be created)"
fi

echo -e "${GREEN}WAF import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import CloudTrail
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[8/9] Importing CloudTrail...${NC}"

TRAIL_NAME="sherpa-audit-trail"

if aws cloudtrail describe-trails --trail-name-list $TRAIL_NAME --region $REGION >/dev/null 2>&1; then
    TRAIL_ARN=$(aws cloudtrail describe-trails \
        --trail-name-list $TRAIL_NAME \
        --region $REGION \
        --query 'trailList[0].TrailARN' \
        --output text 2>/dev/null || echo "")

    if [ -n "$TRAIL_ARN" ] && [ "$TRAIL_ARN" != "None" ]; then
        echo "Importing CloudTrail..."
        terraform import aws_cloudtrail.sherpa_audit $TRAIL_NAME || echo "Already imported or import failed"
    fi
else
    echo "CloudTrail $TRAIL_NAME does not exist (will be created)"
fi

echo -e "${GREEN}CloudTrail import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import Cognito User Pool
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[9/9] Importing Cognito User Pool...${NC}"

COGNITO_POOL_ID="us-east-1_DS0DWtBpu"

if aws cognito-idp describe-user-pool --user-pool-id $COGNITO_POOL_ID --region $REGION >/dev/null 2>&1; then
    echo "Importing Cognito User Pool..."
    terraform import aws_cognito_user_pool.sherpa $COGNITO_POOL_ID || echo "Already imported or import failed"

    # Get client ID (assuming single client)
    CLIENT_ID=$(aws cognito-idp list-user-pool-clients \
        --user-pool-id $COGNITO_POOL_ID \
        --region $REGION \
        --query 'UserPoolClients[0].ClientId' \
        --output text 2>/dev/null || echo "")

    if [ -n "$CLIENT_ID" ] && [ "$CLIENT_ID" != "None" ]; then
        echo "Importing Cognito User Pool Client..."
        terraform import aws_cognito_user_pool_client.sherpa_web "${COGNITO_POOL_ID}/${CLIENT_ID}" || echo "Already imported or import failed"
    fi
else
    echo "Cognito User Pool $COGNITO_POOL_ID does not exist (will be created)"
fi

echo -e "${GREEN}Cognito import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Import CloudFront Distribution
# -----------------------------------------------------------------------------
echo -e "${YELLOW}Importing CloudFront Distribution...${NC}"

CF_ID="dznfspanfl89s"

if aws cloudfront get-distribution --id $CF_ID >/dev/null 2>&1; then
    echo "Importing CloudFront Distribution..."
    terraform import aws_cloudfront_distribution.sherpa $CF_ID || echo "Already imported or import failed"
else
    echo "CloudFront Distribution $CF_ID does not exist (will be created)"
fi

echo -e "${GREEN}CloudFront import complete${NC}"
echo ""

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo -e "${YELLOW}============================================${NC}"
echo -e "${YELLOW}Import Complete!${NC}"
echo -e "${YELLOW}============================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Run 'terraform plan' to see planned changes"
echo "  2. Review the plan carefully"
echo "  3. Run 'terraform apply' to apply changes"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC} If you see drift between imported state"
echo "and actual resources, you may need to update the Terraform"
echo "configuration to match existing resource settings."
echo ""

# -----------------------------------------------------------------------------
# Manual Import Commands (for reference)
# -----------------------------------------------------------------------------
cat << 'EOF'
# =============================================================================
# MANUAL IMPORT COMMANDS (for reference)
# =============================================================================
# If the script fails, you can run these commands manually:

# DynamoDB Tables
terraform import aws_dynamodb_table.sherpa_beads sherpa-beads
terraform import aws_dynamodb_table.sherpa_memory_store sherpa-memory-store

# Lambda Functions
terraform import aws_lambda_function.mcp_router sherpa-mcp-router
terraform import aws_lambda_function.beads_sync sherpa-beads-sync
terraform import aws_lambda_function.agent_loader sherpa-agent-loader
terraform import aws_lambda_function.memory_kb sherpa-memory-kb
terraform import aws_lambda_function.kb_retrieve sherpa-kb-retrieve

# Lambda Layer (get ARN first)
# aws lambda list-layer-versions --layer-name boto3-bedrock-latest
# terraform import aws_lambda_layer_version.boto3_bedrock <layer-arn>

# API Gateway
terraform import aws_api_gateway_rest_api.sherpa hl98rmqgd6
terraform import aws_api_gateway_stage.prod hl98rmqgd6/prod

# WAF Web ACL (get ID first)
# aws wafv2 list-web-acls --scope REGIONAL
# terraform import aws_wafv2_web_acl.sherpa_api <id>/sherpa-api-waf/REGIONAL

# CloudTrail
terraform import aws_cloudtrail.sherpa_audit sherpa-audit-trail

# Cognito
terraform import aws_cognito_user_pool.sherpa us-east-1_DS0DWtBpu
# Get client ID: aws cognito-idp list-user-pool-clients --user-pool-id us-east-1_DS0DWtBpu
# terraform import aws_cognito_user_pool_client.sherpa_web us-east-1_DS0DWtBpu/<client-id>

# CloudFront
terraform import aws_cloudfront_distribution.sherpa dznfspanfl89s

# IAM Roles (if they exist)
# terraform import aws_iam_role.sherpa_lambda_execution sherpa-lambda-execution-role-v41
# terraform import aws_iam_role.cloudtrail_cloudwatch sherpa-cloudtrail-cloudwatch-role

# S3 Buckets
# terraform import aws_s3_bucket.cloudtrail_logs sherpa-cloudtrail-logs-458798750195
EOF
