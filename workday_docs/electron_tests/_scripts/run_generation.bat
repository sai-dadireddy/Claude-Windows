@echo off
REM Electron Test Generation - Batch Launcher
REM Generates test files for Inventory and Asset Management

echo ================================================================================
echo Workday Electron Test Generator
echo ================================================================================
echo.
echo This will generate test files for:
echo   - Inventory (313 scenarios)
echo   - Asset Management (285 scenarios)
echo.
echo Output folders:
echo   - electron_tests\Inventory\
echo   - electron_tests\Asset_Management\
echo.
pause

cd /d "%~dp0"

echo.
echo Starting generation...
echo ================================================================================
python generate_tests_batch.py 2>&1 | tee generation_log.txt

echo.
echo ================================================================================
echo Generation complete! Running verification...
echo ================================================================================
python verify_generation.py

echo.
echo ================================================================================
echo All done!
echo.
echo Log saved to: generation_log.txt
echo ================================================================================
pause
