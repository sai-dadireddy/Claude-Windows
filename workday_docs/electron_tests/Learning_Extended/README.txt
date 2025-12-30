================================================================================
LEARNING EXTENDED ENTERPRISE TESTS - QUICK START GUIDE
================================================================================

This folder contains 48 auto-generated Electron test files for Workday Learning
Extended Enterprise functional area scenarios.

================================================================================
FILE CATEGORIES
================================================================================

1. AUTO-GENERATED (no suffix) - Confidence >= 7.0
   - Ready to use
   - Valid Electron commands
   - Example: LRNXE-2-0020_Create_External_Learning_User.txt

2. NEEDS REVIEW (_REVIEW.txt) - Confidence 5.0-6.9
   - Requires SME validation
   - May need field-level details
   - Example: LRNXE-2-0010_Create_Extended_Enterprise_Affiliation_REVIEW.txt

3. MANUAL REQUIRED (_MANUAL.txt) - Confidence < 5.0
   - Complex workflows
   - Requires manual implementation
   - Example: LRNXE-2-0060_Request_Extended_Enterprise_Learner_MANUAL.txt

================================================================================
WHAT IS LEARNING EXTENDED ENTERPRISE?
================================================================================

Learning Extended Enterprise enables organizations to deliver learning content
to external users (non-employees) such as:
  - Contractors
  - Partners
  - Vendors
  - Customers
  - External learners

Key Differences from Standard Learning:
  - External user management
  - Extended enterprise affiliations
  - External learner types
  - Restricted security model
  - Limited system access

================================================================================
COMMON TEST PATTERNS IN THIS FOLDER
================================================================================

External User Creation:
  LRNXE-2-0020 - Create External Learning User (7.0 confidence)
  LRNXE-4-0010-02 - Create Course for External Users (7.5 confidence)

Extended Enterprise Setup:
  LRNXE-2-0010 - Create Extended Enterprise Affiliation (6.5 confidence - REVIEW)
  LRNXE-2-0040 - Create Extended Enterprise Learner (6.5 confidence - REVIEW)
  LRNXE-2-0050 - Create Extended Enterprise Job Profile (6.5 confidence - REVIEW)

Learning Worklet Access:
  LRNXE-2-0110 - Learning Worklet (7.5 confidence)
  LRNXE-4-0020-01 - Learning Worklet (7.5 confidence)
  LRNXE-4-0100 - Learning Worklet (7.5 confidence)

Enrollment & Transcript:
  LRNXE-4-0040-03 - Enroll in Course (6.5 confidence - REVIEW)
  LRNXE-4-0040-02 - My Transcript (7.5 confidence)
  LRNXE-4-0060-01 - My Transcript (7.5 confidence)

Course Management:
  LRNXE-4-0030 - Create/Edit Course (7.0 confidence)
  LRNXE-4-0010-02 - Create Course (7.5 confidence)

Extended Enterprise Worklet:
  LRNXE-4-0130 - Extended Enterprise Worklet (6.5 confidence - REVIEW)
  LRNXE-4-0140 - Extended Enterprise Worklet (6.5 confidence - REVIEW)

================================================================================
STATISTICS FOR THIS FOLDER
================================================================================

Total Files: 48

Quality Distribution:
  AUTO-GENERATED:    20 files (41.7%)
  NEEDS REVIEW:      13 files (27.1%)
  MANUAL REQUIRED:   15 files (31.2%)

Coverage by Scenario Type:
  Setup/Configuration (LRNXE-2-*):     13 scenarios
  Functional Tests (LRNXE-4-*):        35 scenarios

Most Common Patterns:
  - Learning Worklet access (7.5 average confidence)
  - Create operations (7.0-7.5 average confidence)
  - External user management (6.5-7.0 average confidence)
  - Transcript views (7.5 average confidence)

================================================================================
UNIQUE EXTENDED ENTERPRISE COMMANDS
================================================================================

Create External Learning User:
  enter search box as "Create External Learning User"
  wait 2
  click search result containing "Create External Learning User"
  wait for page to load

View Extended Enterprise Affiliation:
  enter search box as "View Extended Enterprise Affiliation"
  wait 2
  click search result containing "Extended Enterprise Affiliation"
  wait for page to load

Extended Enterprise Worklet:
  click link "Extended Enterprise Worklet"
  wait 2

================================================================================
EXTERNAL USER TESTING WORKFLOW
================================================================================

Typical test sequence:

1. Setup Phase (LRNXE-2-* scenarios):
   a. Create Extended Enterprise Affiliation
   b. Create External Learning User
   c. Create External System User (if needed)
   d. Create Extended Enterprise Learner

2. Configuration Phase:
   a. Create Extended Enterprise Job Profile
   b. Maintain Extended Enterprise Learner Types
   c. Configure security settings

3. Enrollment Phase:
   a. Create courses for external users
   b. Enroll external learners
   c. Assign learning content

4. Validation Phase:
   a. Verify transcript access
   b. Verify worklet functionality
   c. Verify course completion
   d. Verify certification tracking

================================================================================
SECURITY CONSIDERATIONS
================================================================================

External User Access:
  - Limited to assigned courses only
  - Cannot access internal Workday data
  - Restricted search capabilities
  - Specific security segments

Testing Requirements:
  - Test with external user credentials
  - Verify access restrictions work
  - Validate data isolation
  - Check security segment enforcement

Common Issues:
  - External users cannot see internal courses
  - Security groups must be properly configured
  - Affiliation setup required before user creation
  - Job profiles must match learner types

================================================================================
HOW TO USE THESE TESTS
================================================================================

1. SETUP YOUR TEST ENVIRONMENT
   - Configure Extended Enterprise in Workday
   - Create test external user accounts
   - Set up affiliations and learner types
   - Configure security segments

2. SELECT APPROPRIATE TESTS
   - Start with setup tests (LRNXE-2-*)
   - Then run functional tests (LRNXE-4-*)
   - Use AUTO-GENERATED files first
   - Review REVIEW files with SME

3. CUSTOMIZE FOR YOUR TENANT
   - Replace affiliation names
   - Adjust learner type names
   - Update security group references
   - Modify course names as needed

4. EXECUTE TESTS
   - Run setup tests first
   - Execute in sequence (dependencies exist)
   - Validate each step before proceeding
   - Document results and issues

5. VALIDATE RESULTS
   - Check external user can log in
   - Verify learning worklet displays correctly
   - Confirm course enrollment works
   - Validate transcript accuracy

================================================================================
EXAMPLE: CREATING AN EXTERNAL USER
================================================================================

File: LRNXE-2-0020_Create_External_Learning_User.txt

Prerequisites:
  - Extended Enterprise Affiliation exists
  - External learner types configured
  - Security segments set up

Steps:
1. enter search box as "Create External Learning User"
2. wait 2
3. click search result containing "Create External Learning User"
4. wait for page to load
5. [Add field entries based on your requirements]
6. screenshot as "LRNXE-2-0020_complete.png"

Post-Validation:
  - Verify user created successfully
  - Check affiliation assignment
  - Validate security access
  - Test login with new credentials

================================================================================
HANDLING REVIEW FILES (CRITICAL FOR EXTENDED ENTERPRISE)
================================================================================

Extended Enterprise tests have higher REVIEW rates because:
  - Complex affiliation structures vary by tenant
  - Custom learner types differ
  - Security configurations are unique
  - Field names may be customized

Recommended approach:
1. Identify all _REVIEW.txt files (13 files)
2. Document your tenant's specific configuration
3. Map generic terms to your custom terms
4. Add field-level details
5. Test with actual external user accounts
6. Update files with validated steps

Priority REVIEW files:
  - LRNXE-2-0010 - Affiliation setup (critical)
  - LRNXE-2-0040 - External learner creation (critical)
  - LRNXE-2-0050 - Job profile setup (critical)

================================================================================
INTEGRATION WITH STANDARD LEARNING
================================================================================

Related Standard Learning Tests:
  ../Learning/ (128 additional test files)

Common Integration Points:
  - Courses can be shared between internal/external
  - Instructors may teach both audiences
  - Transcripts have similar structure
  - Dashboards have similar functionality

Key Differences:
  - External users have limited search
  - Cannot access internal worker data
  - Restricted to assigned learning only
  - Different security model

================================================================================
TROUBLESHOOTING EXTENDED ENTERPRISE TESTS
================================================================================

Issue: External user cannot log in
Solution: Check affiliation status, verify account enabled

Issue: User cannot see courses
Solution: Verify security segments, check course visibility settings

Issue: Enrollment fails
Solution: Validate learner type matches course settings

Issue: Transcript empty
Solution: Ensure course completion recorded, check equivalency rules

Issue: Worklet not displaying
Solution: Verify user has Extended Enterprise role, check security

================================================================================
RESOURCES
================================================================================

Standard Learning Tests:
  ../Learning/ (related internal learning tests)

Generation Report:
  ../LEARNING_GENERATION_REPORT.txt (detailed statistics)

Workday RAG Tool:
  ../../workday_rag.py (query for Extended Enterprise help)

Example RAG Queries:
  python ../../workday_rag.py "extended enterprise affiliation"
  python ../../workday_rag.py "external learning user setup"
  python ../../workday_rag.py "extended enterprise security"

Workday Documentation:
  - Learning Extended Enterprise Admin Guide
  - External User Management Guide
  - Security Configuration Guide

================================================================================
NEXT STEPS
================================================================================

1. Review tenant's Extended Enterprise configuration
2. Document affiliation names and learner types
3. Validate AUTO-GENERATED tests (20 files)
4. Schedule SME review for REVIEW files (13 files)
5. Research MANUAL scenarios (15 files)
6. Create test data for external users
7. Execute tests in sandbox environment
8. Document results and customizations

================================================================================
