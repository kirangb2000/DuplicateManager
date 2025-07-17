import os
import shutil
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

def move_duplicates(source_folder, target_folder, hash_type='sha256'):
    hashes = {}
    moved_files = []
    unique_files = []
    os.makedirs(target_folder, exist_ok=True)

    logs_dir = os.path.join(target_folder, "Logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "duplicates_move_log.txt")

    summary = {
        "total_files": 0,
        "unique_files": 0,
        "duplicate_files": 0
    }

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"--- Duplicate Move Run: {datetime.now()} ---\n")

        for root, _, files in os.walk(source_folder):
            for file in files:
                summary["total_files"] += 1
                filepath = os.path.join(root, file)
                try:
                    file_hash = calculate_hash(filepath, hash_type)
                    if file_hash in hashes:
                        new_name = os.path.basename(filepath)
                        dest_path = os.path.join(target_folder, new_name)

                        counter = 1
                        while os.path.exists(dest_path):
                            name, ext = os.path.splitext(new_name)
                            dest_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
                            counter += 1

                        shutil.move(filepath, dest_path)
                        moved_files.append((filepath, dest_path))
                        summary["duplicate_files"] += 1
                        log.write(f"MOVED: {filepath} → {dest_path}\n")
                    else:
                        hashes[file_hash] = filepath
                        unique_files.append(filepath)
                        summary["unique_files"] += 1
                except Exception as e:
                    log.write(f"ERROR: {filepath} → {e}\n")

    df_moved = pd.DataFrame(moved_files, columns=["Source_Path", "Moved_To"])
    df_unique = pd.DataFrame(unique_files, columns=["Unique_File_Path"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = os.path.join(logs_dir, f"Duplicate_Move_Summary_{timestamp}.xlsx")

    with pd.ExcelWriter(excel_path) as writer:
        if not df_moved.empty:
            df_moved.to_excel(writer, sheet_name="Moved Duplicates", index=False)
        if not df_unique.empty:
            df_unique.to_excel(writer, sheet_name="Unique Files", index=False)
        pd.DataFrame([summary]).to_excel(writer, sheet_name="Summary", index=False)

    if summary["total_files"] > 0:
        labels = ['Unique Files', 'Duplicate Files']
        sizes = [summary['unique_files'], summary['duplicate_files']]
        colors = ['#66b3ff', '#ff9999']
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('File Analysis Summary')
        pie_chart_path = os.path.join(logs_dir, f"Duplicate_Move_Chart_{timestamp}.png")
        plt.savefig(pie_chart_path)
        plt.close()

    return summary
