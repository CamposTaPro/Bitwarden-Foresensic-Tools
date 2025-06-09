# 🔍 Bitwarden Forensic Analysis Toolkit

This repository contains Python scripts created during a forensic investigation of the Bitwarden password manager. Each script targets a specific component of Bitwarden’s data storage—ranging from Chrome extension data to SQLite databases and memory dumps. The goal is to aid in the recovery or analysis of sensitive user data, including master passwords, key derivation settings, and email identifiers.

## 📁 Contents

### 1. `chrome_extension_data_parser.py`

**Purpose:**  
Extracts sensitive configuration and credential metadata from Bitwarden’s Chrome extension LevelDB storage.

**Key Functions:**  
- Detects OS and auto-locates LevelDB directory.
- Extracts:
  - User ID (UUID)
  - KDF Type & Iteration count
  - Associated Email Address
  - Master Key Hash

**Note:** Requires `plyvel` to interface with LevelDB.

---

### 2. `extract_masterPassword_memory.py`

**Purpose:**  
Scans raw memory dump text files to identify and extract potential master passwords based on common patterns and repetition.

**Key Features:**  
- Filters strings that meet likely password criteria (length, character diversity, exclusion of common terms).
- Detects repeated candidate passwords.
- Saves results into a `wordlist.txt` file for further analysis (e.g., brute force or dictionary attacks).

---

### 3. `sql_extract.py`

**Purpose:**  
Analyzes a SQLite database used by Bitwarden or its extensions, extracting compressed JSON-like blobs and decompressing them for pattern matching.

**Key Features:**  
- Decompresses data from the `object_data` table using Snappy compression.
- Extracts and prints segments related to:
  - `iterations`
  - `email`
  - `kdfType`
  - Possible 44-character master key hashes

---

## ⚙️ Requirements

Make sure to install the following Python libraries:

```bash
pip install plyvel python-snappy
```

## 📌 Disclaimer

This repository is intended for **educational and lawful forensic analysis only**.
