@echo off
cd "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests"

echo ================================================================================
echo PROCUREMENT TEST GENERATION - PROCESSING ALL 336 SCENARIOS
echo ================================================================================

python generate_procurement_batch.py 50 0
python generate_procurement_batch.py 50 50
python generate_procurement_batch.py 50 100
python generate_procurement_batch.py 50 150
python generate_procurement_batch.py 50 200
python generate_procurement_batch.py 50 250
python generate_procurement_batch.py 50 300

echo.
echo ================================================================================
echo ALL BATCHES COMPLETE
echo ================================================================================
echo.
echo Counting generated files...
dir /b Procurement\*.txt | find /c ".txt"
echo.
pause
