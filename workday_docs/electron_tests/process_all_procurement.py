import subprocess
import sys
import pandas as pd

# Read total count
df = pd.read_excel('WD_Test_Scenarios_Master.xlsx')
proc = df[df['Functional Area'] == 'Procurement']
total = len(proc)

print("="*80)
print(f"PROCUREMENT TEST GENERATION - FULL RUN")
print(f"Total scenarios: {total}")
print("="*80)

batch_size = 50
total_batches = (total + batch_size - 1) // batch_size

print(f"Processing in {total_batches} batches of {batch_size}...\n")

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    print(f"\n{'='*80}")
    print(f"BATCH {batch_num + 1}/{total_batches}")
    print(f"{'='*80}")

    result = subprocess.run(
        ['python', 'generate_procurement_batch.py', str(batch_size), str(start_idx)],
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR in batch {batch_num + 1}")
        sys.exit(1)

print("\n" + "="*80)
print("ALL PROCUREMENT SCENARIOS GENERATED SUCCESSFULLY")
print("="*80)
print(f"Total scenarios: {total}")
print(f"Output directory: Procurement/")
print("="*80)
