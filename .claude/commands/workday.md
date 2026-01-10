# Workday Mode

Activates Workday integration and Electron test generation.

## Quick RAG
```bash
cd ~/OneDrive\ -\ ERPA/Claude/workday_docs
python workday_rag.py "{task}"        # Search
python workday_rag.py --list-wsdl     # 55 WSDLs, 3169 ops
python workday_rag.py --list          # REST APIs
```

## Decision
| RAG Score | Action |
|-----------|--------|
| >= 7.0 | Generate Electron steps |
| < 7.0 | Browser research required |

## Electron Commands
| Command | Example |
|---------|---------|
| enter | `enter search box as "Hire Employee"` |
| click | `click button "Submit"` |
| verify | `verify message contains "Success"` |
| screenshot | `screenshot as "HCM-1-0010.png"` |

## APIs
- **SOAP**: `{tenant}.myworkday.com/ccx/service/{tenant}/{Service}/v{ver}?wsdl`
- **REST**: `{host}.workday.com/ccx/api/v1/{tenant}/{resource}`

## What would you like help with?

$ARGUMENTS
