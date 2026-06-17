# SyncFlow (Automated Google Drive Backup System)

SyncFlow is a lightweight, robust command-line automation utility designed to index local ERP data packages and stream-compress them directly onto a virtual Google Drive for Desktop client storage directory (typically mapped to `G:\`). 

It natively incorporates automated path normalization, single-instance execution locking, cross-platform ZIP standard path compliance, and intuitive console dashboard metrics.

---

## 🚀 Key Functional Architecture

* **Dynamic Folder Targeting:** Scans the designated parent source directory to find and validate backup folders matching the current date (`YYYY-MM-DD`).
* **Conflict Resolution:** If multiple backups exist for the same day, the core logic isolates and targets the folder with the latest creation timestamp.
* **Single-Instance Execution:** Utilizes a socket-binding lock on localhost port `61999` at startup to prevent multiple concurrent runs from colliding and causing file write corruption.
* **Optimized Two-Pass Traversal:** Consolidates counting and total size calculations into a single initial `os.walk()` scan, followed by a streaming compression pass to write chunked data directly into the ZIP archive.
* **Cross-Platform ZIP Compatibility:** Automatically normalizes ZIP archive member path separators to forward slashes `/`, ensuring archives extract cleanly on macOS, Linux, and cloud extractors.
* **Unicode Console Support:** Automatically reconfigures standard console streams on Windows to prevent `UnicodeEncodeError` exceptions when rendering terminal emojis.
* **Fail-Safe Configurations:** Automatically creates a configuration template with safe path representations if `config.json` is missing.

---

## 🛠️ Project Structure

```text
📁 SyncFlow/
├── 📄 main.py          # Application entry-point, console dashboard, & single-instance lock
├── 📄 compressor.py    # Two-pass stream zipping module using tqdm
├── 📄 config.json      # Client-specific file paths (Generated at runtime)
└── 📄 .gitignore       # Prevents build files and environments from leaking to Git
```
