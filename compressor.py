import os
import sys
import shutil
import zipfile
from tqdm import tqdm

# Force UTF-8 encoding for standard output and error to support emojis on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def zip_folder(g_drive_destination, source_folder, output_zip_name):
    """
    Compresses a source folder into a ZIP file at the given destination.
    Uses ZIP64 to support files/archives > 2GB.
    Aborts and cleans up if any file is disrupted during scanning or compression.
    """
    final_output_path = os.path.normpath(os.path.join(g_drive_destination, output_zip_name))

    print(f"Scanning source: {source_folder}")
    
    total_files = 0
    total_bytes = 0
    
    try:
        # Step 1: Scan files and calculate size. Abort on any disruption.
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip symbolic links to avoid loops or out-of-bounds files
                if os.path.islink(file_path):
                    continue
                
                try:
                    total_files += 1
                    total_bytes += os.path.getsize(file_path)
                except (FileNotFoundError, PermissionError) as fe:
                    raise RuntimeError(f"File disruption detected during initial scan: '{file_path}' ({fe})")

        if total_files == 0:
            print("\n⚠️   Warning: Target folder is completely empty. Sync canceled.")
            print("=" * 60)
            return

        print(f"📊 Status: Found {total_files} files ready for extraction.")
        print("-" * 60)

        # Step 2: Validate disk space at destination
        try:
            dest_dir = os.path.dirname(final_output_path) or g_drive_destination
            _, _, free_space = shutil.disk_usage(dest_dir)
            if free_space < total_bytes:
                raise RuntimeError(
                    f"Insufficient disk space on destination drive.\n"
                    f"   Required:  {total_bytes / (1024**3):.2f} GB\n"
                    f"   Available: {free_space / (1024**3):.2f} GB"
                )
        except OSError:
            # disk_usage may raise OSError for certain virtual stream/network drives, skip if unsupported
            pass

        # Step 3: Compress files into destination ZIP
        with zipfile.ZipFile(final_output_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
            
            # Setup progress bar
            with tqdm(total=total_bytes, desc="⚡ Syncing to Cloud", unit="B", unit_scale=True, unit_divisor=1024, leave=True, ncols=75, file=sys.stdout) as pbar:
                
                for root, dirs, files in os.walk(source_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        if os.path.islink(file_path):
                            continue
                        
                        # Use forward slashes inside ZIP to be cross-platform compliant
                        arcname = os.path.relpath(file_path, start=source_folder).replace("\\", "/")
                        
                        # Path Traversal Protection
                        normalized_arcname = os.path.normpath(arcname)
                        if normalized_arcname.startswith("..") or os.path.isabs(normalized_arcname):
                            raise RuntimeError(f"Security Warning: Out-of-bounds file access blocked: '{arcname}'")
                        
                        # Verify file presence and stream bytes
                        if not os.path.exists(file_path):
                            raise FileNotFoundError(f"Source file was deleted or moved mid-operation: '{file_path}'")
                            
                        try:
                            with open(file_path, "rb") as src_file:
                                with zipf.open(arcname, "w", force_zip64=True) as dest_file:
                                    chunk_size = 1024 * 1024  # 1 MB Buffer size
                                    while True:
                                        chunk = src_file.read(chunk_size)
                                        if not chunk:
                                            break
                                        dest_file.write(chunk)
                                        pbar.update(len(chunk))
                        except PermissionError:
                            raise RuntimeError(f"Source file is locked or in use: {file_path}")
                        except FileNotFoundError:
                            raise RuntimeError(f"Source file was deleted mid-operation: {file_path}")
                        except Exception as write_err:
                            raise RuntimeError(f"Failed to write file '{file_path}' to archive: {write_err}")
                            
        print("-" * 60)
        print(" SUCCESS: BACKUP COMPRESSION COMPLETE ".center(60, "✅"))
        print("=" * 60)

    except (Exception, KeyboardInterrupt) as e:
        # Atomic Cleanup: Remove corrupted/partial zip archive from destination
        if os.path.exists(final_output_path):
            try:
                os.remove(final_output_path)
                print("\n🧹 Cleaned up incomplete/corrupted archive file.")
            except Exception as cleanup_err:
                print(f"\n⚠️ Warning: Could not clean up partial archive '{final_output_path}': {cleanup_err}")
        
        # Display context-specific friendly output before raising
        if isinstance(e, PermissionError):
            print("\n❌ Write Access Denied: Windows kernel blocked file output stream.")
            print("👉 Solution: Right-click this app executable and select 'Run as Administrator'.")
            print("=" * 60)
        else:
            print(f"\n❌ Crash Handler Intercepted: {e}")
            print("=" * 60)
            
        raise e
