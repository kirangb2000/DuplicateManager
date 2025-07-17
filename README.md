# Duplicate File Mover and Verifier 🧹🔍

A Python-based utility to **detect**, **move**, and **verify** duplicate files using cryptographic hash matching (`SHA-256` or `MD5`). It ensures 100% file-level match before any move operation, with detailed logs, Excel reports, and visual pie charts.

---

## 🔧 Features

- ✅ Detects exact duplicates based on content (not just name)
- ✅ Supports **recursive scan** of all subfolders
- ✅ Moves only duplicates, retains one original
- ✅ Verifies if destination files exist in source (perfect for backups)
- ✅ Logs all actions
- ✅ Generates Excel summary reports
- ✅ Creates pie charts for visual analysis
- ✅ Command-line runner to choose between: Move / Verify / Both

---

## 📁 Folder Structure

```
Duplicate-File-Mover-and-Verifier/
│
├── mover.py        # Moves duplicate files to a given folder
├── verifier.py     # Verifies files in dest are present in source
├── main.py         # CLI runner: choose Move / Verify / Both
├── README.md       # You're reading it :)
└── Logs/           # Auto-created folder to store logs, Excel reports, and charts
```

---

## ▶️ How to Run

### 1. Install Requirements

```bash
pip install pandas matplotlib
```

### 2. Run the Tool

```bash
python main.py
```

You'll be prompted to enter:

- Source folder path
- Destination folder path
- Choose:  
  `1` – Move duplicates  
  `2` – Verify  
  `3` – Move + Verify

---

## 📊 Output

- ✅ `Logs/duplicates_move_log.txt`
- ✅ `Logs/Duplicate_Move_Summary_<timestamp>.xlsx`
- ✅ `Logs/Duplicate_Move_Chart_<timestamp>.png`
- ✅ `Logs/verification_log.txt`
- ✅ `Logs/Duplicate_Verification_Summary_<timestamp>.xlsx`

---

## 🧪 Use Cases

- Organize photo libraries
- Detect duplicate research files
- Backup validation
- Clear cloud sync folders

---

## 📘 License

MIT License – free to use, modify, and distribute.

---

## ✨ Author

**Dr. Kirankumar Gudagudi**

---

