# Workday Electron Test Suite - Time/Absence/Scheduling

## Overview

This directory contains automatically generated Electron test files for Workday scenarios across three functional areas:
- **Scheduling** (221 scenarios)
- **Absence** (178 scenarios)
- **Time Tracking** (152 scenarios)

**Total:** 551 test scenarios

## Directory Structure

```
electron_tests/
├── Scheduling/          # 221 test files
├── Absence/             # 178 test files
├── Time_Tracking/       # 152 test files
├── extract_scenarios.py # Excel extraction script
├── generate_electron_tests.py  # Test generator
├── check_status.py      # Status checker
├── generate_summary_report.py  # Report generator
└── README.md            # This file
```

## Test File Format

Each test file follows this structure:

```javascript
/**
 * Electron Test: {SCENARIO_ID} - {SCENARIO_NAME}
 * Functional Area: {AREA}
 *
 * CONFIDENCE: HIGH | MEDIUM | LOW | MANUAL
 * REASONING: {explanation}
 *
 * Scenario Description: {description}
 * Task/Step: {primary_task}
 * Expected Result: {verification_criteria}
 * Estimated Effort: {minutes}
 * Workday Role: {required_role}
 */
```

## Confidence Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **HIGH** | RAG found clear SOAP operations and UI steps | Ready for implementation |
| **MEDIUM** | Partial RAG match, some gaps | SME review recommended |
| **LOW** | Task defined but limited RAG guidance | Manual verification needed |
| **MANUAL** | No task/step or no RAG matches | Complete manual review required |

## Generated: 2025-12-30
## Source: WD_Test_Scenarios_Master.xlsx
## RAG Knowledge Base: 118 documents indexed
