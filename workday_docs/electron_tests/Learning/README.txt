================================================================================
LEARNING ELECTRON TESTS - QUICK START GUIDE
================================================================================

This folder contains 128 auto-generated Electron test files for Workday Learning
functional area scenarios.

================================================================================
FILE CATEGORIES
================================================================================

1. AUTO-GENERATED (no suffix) - Confidence >= 7.0
   - Ready to use
   - Valid Electron commands
   - Example: LRN-2-0160_Create_Course.txt

2. NEEDS REVIEW (_REVIEW.txt) - Confidence 5.0-6.9
   - Requires SME validation
   - May need field-level details
   - Example: LRN-2-0260_Edit_Audience_REVIEW.txt

3. MANUAL REQUIRED (_MANUAL.txt) - Confidence < 5.0
   - Complex workflows
   - Requires manual implementation
   - Example: LRN-2-0060_Report_Manage_Learning_Security_Segments_MANUAL.txt

================================================================================
COMMON TEST PATTERNS IN THIS FOLDER
================================================================================

Security Group Tests:
  LRN-2-0010 - View Security Group (8.0 confidence)
  LRN-4-0040 - View Security Group (8.0 confidence)
  LRN-5-0010 - View Security Group (8.0 confidence)

Course Management:
  LRN-2-0160 - Create Course (7.5 confidence)
  LRN-2-0170 - Create Course (7.5 confidence)
  LRN-4-0090-02 - Create Course (7.5 confidence)

Dashboard Access:
  LRN-4-0190 - Onboarding Dashboard (8.0 confidence)
  LRN-4-0200 - Learning Dashboard (8.0 confidence)
  LRN-4-0350 - Learning Admin Dashboard (8.0 confidence)

Learning Worklet:
  LRN-2-0020 - Learning Worklet (7.5 confidence)
  LRN-2-0030 - Learning Worklet (7.5 confidence)
  LRN-4-0110 - Learning Worklet (7.5 confidence)

Enrollment:
  LRN-2-0230 - Find Workers Mass Enroll (7.5 confidence)
  LRN-2-0240 - Find Workers to Enroll (7.5 confidence)
  LRN-4-0020-01 - Find Workers Mass Enroll (7.5 confidence)

Transcript Views:
  LRN-4-0390 - My Team's Learning Transcript (8.0 confidence)
  LRN-4-0120-05 - My Transcript (7.5 confidence)
  LRN-4-0140-01 - My Transcript (7.5 confidence)

================================================================================
HOW TO USE THESE TESTS
================================================================================

1. SELECT A TEST FILE
   - Start with AUTO-GENERATED files (no suffix)
   - Check confidence score in file header
   - Review test description and original task

2. REVIEW ELECTRON STEPS
   - Each file contains numbered Electron commands
   - Commands are ready to copy/paste into Electron framework
   - Wait times are included for page loads

3. CUSTOMIZE IF NEEDED
   - Replace search terms with your tenant-specific terms
   - Adjust wait times for system performance
   - Add verification steps as needed

4. EXECUTE IN ELECTRON
   - Copy steps to your Electron test script
   - Run in Workday test environment
   - Capture screenshots as indicated

5. VALIDATE RESULTS
   - Check expected results section
   - Verify screenshots captured correctly
   - Document any discrepancies

================================================================================
EXAMPLE: RUNNING A SIMPLE TEST
================================================================================

File: LRN-2-0160_Create_Course.txt

Steps to execute:
1. Open Electron test framework
2. Configure Workday login credentials
3. Copy these commands:

   enter search box as "Create Course"
   wait 2
   click search result containing "Create Course"
   wait for page to load
   screenshot as "LRN-2-0160_complete.png"

4. Run test
5. Verify screenshot captured
6. Check course creation was successful

================================================================================
HANDLING REVIEW FILES
================================================================================

For files marked _REVIEW.txt:

1. Read the original task description
2. Consult with Learning SME
3. Validate navigation paths in your Workday tenant
4. Add missing field-level details
5. Test manually first
6. Update file with validated steps
7. Remove _REVIEW suffix once validated

================================================================================
HANDLING MANUAL FILES
================================================================================

For files marked _MANUAL.txt:

1. Use Workday RAG tool:
   cd ../../
   python workday_rag.py "Task description here"

2. Search Workday Knowledge Base:
   https://resourcecenter.workday.com

3. Review Workday documentation:
   - Learning Admin Guide
   - Learning User Guide

4. Document detailed workflow
5. Create custom Electron script
6. Test thoroughly before production use

================================================================================
STATISTICS FOR THIS FOLDER
================================================================================

Total Files: 128

Quality Distribution:
  AUTO-GENERATED:    52 files (40.6%)
  NEEDS REVIEW:      34 files (26.6%)
  MANUAL REQUIRED:   42 files (32.8%)

Most Common Patterns:
  - Learning Worklet access (highest confidence)
  - Dashboard navigation (8.0 average)
  - Course creation/editing (7.5 average)
  - Security group viewing (8.0 average)
  - Report running (7.0-8.0 average)

================================================================================
TROUBLESHOOTING
================================================================================

Issue: Search term not found
Solution: Check if term exists in your tenant, adjust search text

Issue: Wait time too short
Solution: Increase wait time based on system performance

Issue: Screenshot not captured
Solution: Verify Electron screenshot configuration

Issue: Click target not found
Solution: Use read_page to identify correct element reference

Issue: Test fails validation
Solution: Review expected results, check field values

================================================================================
RELATED RESOURCES
================================================================================

Learning Extended Enterprise Tests:
  ../Learning_Extended/ (48 additional test files)

Generation Report:
  ../LEARNING_GENERATION_REPORT.txt (detailed statistics)

Generation Script:
  ../generate_learning_batch.py (regenerate if needed)

Workday RAG Tool:
  ../../workday_rag.py (query knowledge base)

Excel Source:
  ../WD_Test_Scenarios_Master.xlsx (original scenarios)

================================================================================
SUPPORT
================================================================================

For questions about:
  - Test execution: Consult Electron documentation
  - Workday tasks: Use RAG tool or contact Learning SME
  - File regeneration: Run generate_learning_batch.py
  - Missing scenarios: Check Excel source for data issues

================================================================================
