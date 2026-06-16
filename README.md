# SyncFlow (Automated Google Drive Backup System)

SyncFlow is a lightweight, robust command-line automation utility designed to index local ERP data packages and stream compress them directly onto a virtual Google Drive for Desktop client storage directory (`G:\`). 

It natively incorporates automated path normalization, single-instance execution target resolution, and intuitive terminal dashboard logging metrics.

---

## 🚀 Key Functional Architecture

* **Dynamic Folder Targeting:** Scans a parent directory to find and validate backup folders matching the current date (`DD-MM-YYYY`).
* **Conflict Resolution:** If multiple backups exist for the same day, the core logic automatically isolates and targets the latest creation timestamp.
* **Stream Compression:** Uses an optimized two-pass `os.walk()` compression matrix to stream data packets directly into the cloud file allocation table without clogging local memory caches.
* **Fail-Safe Configurations:** Automatically generates a formatted configuration template if missing from the application root path.

---

## 🛠️ Project Structure

```text
📁 SyncFlow/
├── 📄 main.py          # Application entry-point & CLI dashboard logic
├── 📄 compressor.py    # Multi-pass stream zipping module using tqdm
├── 📄 config.json      # Client-specific file paths (Generated at runtime)
└── 📄 .gitignore       # Prevents caching & environment leakages to Git
