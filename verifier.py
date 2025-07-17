import os
import hashlib
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def calculate_hash(filepath, hash_type='sha256'):
    hash_func = hashlib.sha256() if hash_type == 'sha256' else hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def verify_duplicates(original_folder, duplicate_folder, hash_type='sha256'):
    def build_hash_map(folder):
        hash_map = {}
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    file_hash = calculate_hash(path, hash_type)
                    hash_map[file_hash] = path
                except Exception as e:
                    pass
        return hash_map

    original_hashes = build_hash_map(original_folder)
    matched = []
    missing = []
    logs_dir = os.path.join(duplicate_folder, "Logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "verification_log.txt")

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"--- Verification Run: {datetime.now()} ---\n")
        for root, _, files in os.walk(duplicate_folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    file_hash = calculate_hash(path, hash_type)
                    if file_hash in original_hashes:
                        matched.append((path, original_hashes[file_hash]))
                        log.write(f"MATCHED: {path} → {original_hashes[file_hash]}\n")
                    else:
                        missing.append(path)
                        log.write(f"NOT FOUND: {path}\n")
                except Exception as e:
                    log.write(f"ERROR: {path} → {e}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = os.path.join(logs_dir, f"Duplicate_Verification_Summary_{timestamp}.xlsx")
    with pd.ExcelWriter(excel_path) as writer:
        if matched:
            pd.DataFrame(matched, columns=["Duplicate_File", "Original_File"]).to_excel(writer, sheet_name="Matched", index=False)
        if missing:
            pd.DataFrame(missing, columns=["Missing_File"]).to_excel(writer, sheet_name="Missing", index=False)
        summary = {
            "Total Checked": len(matched) + len(missing),
            "Matched": len(matched),
            "Missing": len(missing)
        }
        pd.DataFrame([summary]).to_excel(writer, sheet_name="Summary", index=False)

    if summary["Total Checked"] > 0:
        labels = ['Matched', 'Missing']
        sizes = [summary['Matched'], summary['Missing']]
        colors = ['#99ff99', '#ff6666']
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Verification Summary')
        pie_chart_path = os.path.join(logs_dir, f"Duplicate_Verification_Chart_{timestamp}.png")
        plt.savefig(pie_chart_path)
        plt.close()

    return summary
