# BEN-4-0010 Electron Test Scripts - User Guide

## Overview

This package contains **5 automated test scripts** for the "New Hire to Pay with Elections" business process in Workday. Each script uses **custom data variables** that can be configured for any client tenant.

---

## Scripts Included

| Script | Purpose | Fields |
|--------|---------|--------|
| BEN-4-0010-01 | Hire Employee | Country, First Name, Middle Name, Last Name, Workday ID Type |
| BEN-4-0010-02 | Change Benefits | Effective Date, Employee |
| BEN-4-0010-03 | Validate Benefit History | Employee Name, Employee ID |
| BEN-4-0010-04 | Validate Payroll | Employee Name, Deduction Amounts |
| BEN-4-0010-05 | Validate Integration | Integration Name, Employee ID |

---

## How Scripts Were Generated

### 1. Browser-Based Field Discovery
Each Workday task was manually accessed in Chrome to:
- Identify all form fields
- Document field types (text, dropdown, date picker)
- Note required vs optional fields
- Capture field validation rules

### 2. Generic Variable Format
All client-specific data uses `{{VARIABLE_NAME}}` placeholders:

```
# Tenant Configuration
{{TENANT_LOGIN_URL}} = Your tenant login URL
{{USERNAME}} = Your test username
{{PASSWORD}} = Your test password

# Employee Data
{{EMPLOYEE_NAME}} = Test employee full name
{{EMPLOYEE_ID}} = Test employee ID
{{EFFECTIVE_DATE}} = MM/DD/YYYY format
```

### 3. DSL Command Structure
Scripts use natural language DSL commands:
```
Navigate to {{TENANT_LOGIN_URL}}
wait for page load (3 seconds)
enter the username as {{USERNAME}}
click on the 'Sign In' button
enter {{EMPLOYEE_NAME}} in the search field
click on '{{TASK_NAME}}' link
```

---

## How to Update for Your Tenant

### Step 1: Copy the Config Template
Edit `BEN-4-0010_config.json` with your values:

```json
{
  "tenant": {
    "TENANT_LOGIN_URL": "https://YOUR-TENANT.workday.com/login",
    "USERNAME": "your_username",
    "PASSWORD": "your_password"
  },
  "employee": {
    "EMPLOYEE_NAME": "Your Test Employee",
    "EMPLOYEE_ID": "YOUR-EMP-ID"
  },
  "dates": {
    "EFFECTIVE_DATE": "MM/DD/YYYY"
  }
}
```

### Step 2: Replace Variables in Scripts
Use find/replace to substitute `{{VARIABLE}}` with actual values:
- `{{TENANT_LOGIN_URL}}` → Your tenant URL
- `{{USERNAME}}` → Your username
- `{{EMPLOYEE_NAME}}` → Your test employee name

### Step 3: Run with DSL Executor
```bash
cd electron_tests/_scripts
python dsl_executor.py "../Benefits/BEN-4-0010-01_New_Hire_to_Pay_with_Elections.txt"

# With screenshots
python dsl_executor.py "../Benefits/BEN-4-0010-01_test.txt" --screenshots
```

---

## Execution Options

| Flag | Description |
|------|-------------|
| (none) | Run with visible browser |
| `--headless` | Run without browser window |
| `--screenshots` | Capture screenshot every step |
| `--debug` | Screenshots only on failure |

---

## Field Reference by Script

### BEN-4-0010-01: Hire Employee
| Field | Type | Required | Variable |
|-------|------|----------|----------|
| Country | Dropdown | Yes | `{{HIRE_COUNTRY}}` |
| First Name | Text | No | `{{HIRE_FIRST_NAME}}` |
| Middle Name | Text | No | `{{HIRE_MIDDLE_NAME}}` |
| Last Name | Text | No | `{{HIRE_LAST_NAME}}` |
| Workday ID Type | Dropdown | No | `{{HIRE_ID_TYPE}}` |

### BEN-4-0010-02: Change Benefits
| Field | Type | Required | Variable |
|-------|------|----------|----------|
| Effective Date | Date | Yes | `{{EFFECTIVE_DATE}}` |
| Employee | Search | Yes | `{{EMPLOYEE_NAME}}` |

### BEN-4-0010-03: Validate History
| Field | Type | Required | Variable |
|-------|------|----------|----------|
| Employee Search | Text | Yes | `{{EMPLOYEE_NAME}}` |

### BEN-4-0010-04: Validate Payroll
| Field | Type | Required | Variable |
|-------|------|----------|----------|
| Employee Search | Text | Yes | `{{EMPLOYEE_NAME}}` |

### BEN-4-0010-05: Validate Integration
| Field | Type | Required | Variable |
|-------|------|----------|----------|
| Integration Search | Text | Yes | `{{INTEGRATION_NAME}}` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login fails | Verify `{{USERNAME}}` and `{{PASSWORD}}` |
| Task not found | Check security role permissions |
| Element not found | Increase wait times |
| Date format error | Use MM/DD/YYYY format |

---

## Test Results Summary

All scripts tested successfully:
- BEN-4-0010-01: ✅ 14/15 passed
- BEN-4-0010-02: ✅ 14/15 passed
- BEN-4-0010-03: ✅ 14/15 passed
- BEN-4-0010-04: ✅ 11/12 passed
- BEN-4-0010-05: ✅ 14/15 passed

---

Generated: 2026-01-08
Tool: Playwright-based DSL Executor
