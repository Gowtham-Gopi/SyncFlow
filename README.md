# SyncFlow (Automated Google Drive Backup System)

SyncFlow is an enterprise-ready, robust command-line automation utility designed to index local ERP data packages and stream-compress them directly onto a virtual Google Drive for Desktop client storage directory (typically mapped to `G:\`). 

By natively integrating robust validation checks, single-instance execution locking, path traversal protections, large-file ZIP64 support, and real-time console progress feedback, SyncFlow guarantees safe, efficient, and reliable backups without user intervention.

---

## 🚀 Key Functional Architecture

### 📁 Dynamic Folder Targeting & Conflict Resolution
- **Today's Backup Identification:** Automatically scans the designated parent source directory for folders generated on the current date (`YYYY-MM-DD`).
- **Conflict Resolution:** If multiple backups exist for the same day (e.g., from consecutive ERP runs), the application isolates and targets the folder with the latest creation timestamp (`os.path.getctime`), appending a time suffix (e.g., `_15-45.zip`) to the backup name.

### 🔒 Single-Instance Execution (Locking)
- **Socket-Based Locking:** Utilizes a socket-binding lock on localhost port `61999` at startup. This prevents multiple concurrent runs from colliding and causing file write corruption or race conditions.
- **Graceful Lock Release:** Ensures the socket lock is safely released via a global `finally` block, even during unexpected failures or keyboard interrupts.

### ⚡ Two-Pass Streaming Compression
- **Structural Pre-Scan:** Consolidates counting and total size calculations into a single initial `os.walk()` pass. This determines precise backup size benchmarks and validates files beforehand.
- **Chunked Stream Buffer:** Reads files in a 1 MB chunked buffer and streams them directly into the target ZIP file rather than buffering large files in memory.
- **Stationary Progress Visualization:** Powered by `tqdm`, displays a clean, stationary, non-scrolling progress bar indicating completion percentage, total bytes synced, real-time throughput, and estimated time remaining (ETA).

### 🛡️ Enterprise-Grade Safety & Resiliency
- **ZIP64 Architecture:** Uses `allowZip64=True` and `force_zip64=True` to support backup files and archives exceeding 2GB, preventing standard library zip crashes on large ERP databases.
- **Security Check (Path Traversal Protection):** Sanitizes and validates each archive name. If any member path points outside the source directory (using `..` or absolute paths), it blocks the operation.
- **Pre-Emptive Disk Space Check:** Validates available disk space on the destination drive before compression starts, preventing disk-full crashes.
- **Mid-Operation Resilience:** Safely handles folders/files that are modified, locked, or deleted mid-operation, gracefully skipping inaccessible paths or raising descriptive errors.
- **Atomic Cleanup:** Intercepts failures (such as `KeyboardInterrupt`, write errors, or write access denials) and automatically cleans up/deletes partial or corrupted ZIP archives from the destination.

### 🛠️ Configuration & Unicode Compatibility
- **Unicode Support:** Automatically reconfigures Windows terminal output to UTF-8 to support progress emojis and avoid `UnicodeEncodeError` crashes.
- **Failsafe Parsing:** Uses regex-based parsing to auto-correct raw Windows backslashes (e.g. `C:\Users\Name`) inside `config.json` without breaking JSON formatting.
- **Self-Healing:** If `config.json` is missing, SyncFlow automatically generates a template config file with safe defaults.

---

## 🔒 Licensing & Machine Binding

SyncFlow features an offline, node-locked licensing system designed for high reliability and ease of use:
- **Hardware-User Binding:** Automatically generates a machine fingerprint using a normalized (lowercase) combination of the local `COMPUTERNAME` and `USERNAME` environment variables.
- **Zero-Network Dependency:** Runs completely offline, avoiding issues with firewalls, VPNs, or network changes.
- **Base32 Encoded Keys:** Hashes the fingerprint using SHA-256 and formats it to a readable, case-insensitive 12-character string (e.g., `445D-GN7F-P575`).
- **Support-Friendly Output:** If the license is missing or invalid, the app displays the computer's **Primary Key** and the entered **License Key** in a clean, formatted style for easy copy-pasting.

---

## ⚙️ Configuration Setup

Configure SyncFlow by editing the `config.json` file located in the application's root directory:

```json
{
    "source": "C:/Users/gowth/Downloads/Backups",
    "destination": "G:/My Drive",
    "folder_name": "Backups",
    "key": "XXXX-XXXX-XXXX"
}
```

### 📋 Configuration Fields
| Key | Type | Description |
| :--- | :--- | :--- |
| `source` | `String` | The local parent folder containing ERP generated backups. |
| `destination` | `String` | Path to Google Drive for Desktop virtual mount (e.g. `G:/My Drive`). |
| `folder_name` | `String` | Subdirectory inside the destination where backup archives will be stored. |
| `key` | `String` | The 12-character license key issued by support (e.g., `XXXX-XXXX-XXXX`). |

---

## 🛠️ Project Structure

```text
📁 SyncFlow/
├── 📄 main.py            # Entry point, console UI dashboard, config validation, & socket locking
├── 📄 compressor.py      # Two-pass streaming ZIP64 compression with tqdm metrics and atomic cleanup
├── 📄 config.json        # Client configuration paths (Auto-created if missing)
├── 📄 requirements.txt   # Third-party Python dependencies
├── 📄 SyncFlow.spec      # PyInstaller spec for building a unified executable
└── 📄 README.md          # Project documentation and architectural overview
```

---

## 🚀 Installation & Local Development

### 1. Prerequisites
- Python 3.8 or higher.
- Google Drive for Desktop installed and running.

### 2. Dependency Setup
Clone the repository, navigate to the `SyncFlow` folder, and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the backup utility manually:
```bash
python main.py
```

### 4. Build Executable
To freeze the script into a standalone Windows executable:
```bash
pyinstaller SyncFlow.spec
```
The compiled executable will be available inside the `dist/` directory.
