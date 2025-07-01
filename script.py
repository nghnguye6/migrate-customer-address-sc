import pandas as pd
import sys
import time
import os
import zipfile

# --- progress bar ---
def print_progress(current, total, bar_length=40):
    percent = float(current) / total if total else 1
    percent = min(percent, 1.0)
    arrow = '█' * int(round(percent * bar_length))
    spaces = '-' * (bar_length - len(arrow))
    sys.stdout.write(f"\rProgress: [{arrow}{spaces}] {int(percent * 100)}%")
    sys.stdout.flush()

# --- main function ---
def delete_garbage_addresses(file_original, file_after_orders, max_rows=None):
    start = time.time()

    # Load and keep only required columns
    df_original = pd.read_csv(file_original, dtype=str)[['ID', 'Address ID']]
    df_after_orders = pd.read_csv(file_after_orders, dtype=str)[['ID', 'Address ID']]

    # Find rows in after_orders that don't exist in original
    df_diff = df_after_orders.merge(df_original, on=['ID', 'Address ID'], how='left', indicator=True)
    df_to_delete = df_diff[df_diff['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Add DELETE command
    df_to_delete['Address Command'] = 'DELETE'

    output_df = df_to_delete[['ID', 'Address ID', 'Address Command']]
    output_files = []

    if not max_rows:
        # Unlimited mode – write single file with chunked progress
        filename = 'delete_addresses.csv'
        total_rows = len(output_df)
        chunk_size = 1000
        print("📄 Writing full CSV without splitting...")

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            output_df.iloc[0:0].to_csv(f, index=False)  # write header
            for i in range(0, total_rows, chunk_size):
                output_df.iloc[i:i + chunk_size].to_csv(f, index=False, header=False)
                current = min(i + chunk_size, total_rows)
                print_progress(current, total_rows)

        output_files.append(filename)
        print()  # newline after progress bar

    else:
        # Split mode
        total_parts = (len(output_df) + max_rows - 1) // max_rows
        print("📄 Splitting output into multiple files...")
        for i in range(total_parts):
            part_df = output_df.iloc[i * max_rows: (i + 1) * max_rows]
            filename = f'delete_addresses_part{i + 1}.csv'
            part_df.to_csv(filename, index=False)
            output_files.append(filename)
            print_progress(i + 1, total_parts)
        print()  # newline after progress bar

    # Create ZIP file
    zip_name = f'delete_addresses_{int(time.time())}.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for f in output_files:
            zipf.write(f)
            os.remove(f)

    print(f"\n✅ Done. ZIP file created: {zip_name}")
    print(f"⏱️ Elapsed time: {time.time() - start:.2f} seconds")

# --- CLI entry point ---
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <original_addresses.csv> <after_orders.csv> [max_rows|unlimited]")
        sys.exit(1)

    file_original = sys.argv[1]
    file_after_orders = sys.argv[2]

    if len(sys.argv) >= 4:
        arg = sys.argv[3].lower()
        max_rows = None if arg == 'unlimited' else int(arg)
    else:
        max_rows = 1000

    delete_garbage_addresses(file_original, file_after_orders, max_rows)
