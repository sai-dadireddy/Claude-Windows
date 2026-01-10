
## [2025-12-10 14:57:30]
Migrated project from Windows to Linux. Cleaned up 500+ legacy files, kept only essential folders: agupgrade-ui, BackEnd, .github, .claude. Downloaded fresh 64 Lambda functions from AWS API Gateway V2.

## [2025-12-10 15:03:10]
All 64 Lambda functions upgraded to Python 3.12 via AWS Console (Dec 2024). Python 3.9 EOL migration complete.

## [2025-12-29 11:06:24]
AWS profile 'agupgrade' for Account 558760008985. SSO URL: erpacloud.awsapps.com. Frontend in agupgrade-ui/, Backend IaC in BackEnd/. Use frontend-builder agent for React work, lead-architect for Terraform.

## [2025-12-29 15:47:52]
Cleaned up AGUPGRADE project: Deleted 38 legacy agupgrade-react-* Lambdas from AWS us-east-2, removed 33 local Lambda folders. Added missing fields to UI pages (EC2: AZ/IP/platform/launchTime, RDS: action/executionArn, DB Refresh: executionArn/envType/envName). Removed demo/placeholder data from 4 API routes - now return empty arrays.

## [2025-12-30 12:03:41]
Completed UI/API audit: Fixed PIA Activity (account/region + component mapping), RefreshWizard (dynamic RDS list), About page (dynamic tenant ID), Analytics routes. 11 audit reports in audit-report/. Build verified (226 pages).

## [2025-12-30 12:27:31]
Deployed 5 parallel QA agents to test AGUPGRADE UI: Dashboard, Operations, Env Discovery, Security, Analytics. Using Claude-in-Chrome for Lambda response testing.

## [2025-12-30 13:14:28]
Fixed 4 API errors in AGUPGRADE UI: Created /api/admin/roles route (Cognito+DB), /api/operations/RealTimeApplicationMonitoring route, made tenant ID optional for account-level APIs (analytics, discovery, ami-list, history). Compiled list of 50+ missing Lambda backend APIs. Build verified (226 pages).
