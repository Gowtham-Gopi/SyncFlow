import os
import sys
import zipfile
from tqdm import tqdm

def zip_folder(g_drive_destination, source_folder, output_zip_name):

    final_output_path = os.path.join(g_drive_destination, output_zip_name)

    print(f"Scanning source: {source_folder}")
    
    total_files = 0
    total_bytes = 0
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip symbolic links to avoid calculating infinite loops or breaking paths
            if not os.path.islink(file_path):
                total_files += 1
                total_bytes += os.path.getsize(file_path)
        
    if total_files == 0:
        print("\n⚠️   Warning: Target folder is completely empty. Sync canceled.")
        print("=" * 60)
        return

    print(f"📊 Status: Found {total_files} files ready for extraction.")
    print("-" * 60)

    try:
       # Open the master Zip file archive
        with zipfile.ZipFile(final_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Setup a master progress bar tracking total bytes with dynamic scale (KB/MB/GB)
            with tqdm(total=total_bytes, desc="⚡ Syncing to Cloud", unit="B", unit_scale=True, unit_divisor=1024, leave=False, ncols=75, file=sys.stdout) as pbar:
                
                # Walk through your target source directory structures
                for root, dirs, files in os.walk(source_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Skip symbolic links in the actual compression walk too
                        if os.path.islink(file_path):
                            continue
                        # Use forward slashes inside ZIP file member names to be cross-platform compliant
                        arcname = os.path.relpath(file_path, start=source_folder).replace("\\", "/")
                        
                        # Stream the current file out in 1MB chunks instead of writing all at once
                        try:
                            with open(file_path, "rb") as src_file:
                                with zipf.open(arcname, "w") as dest_file:
                                    chunk_size = 1024 * 1024  # 1 MB Buffer size
                                    while True:
                                        chunk = src_file.read(chunk_size)
                                        if not chunk:
                                            break
                                        dest_file.write(chunk)
                                        pbar.update(len(chunk))  # Move progress ticker smoothly by the chunk size
                        except PermissionError:
                            raise RuntimeError(f"Source file is locked or in use: {file_path}")
                        
        print("-" * 60)
        print(" SUCCESS: BACKUP COMPRESSION COMPLETE ".center(60, "✅"))
        print("=" * 60)

    except PermissionError:
        print("\n❌ Write Access Denied: Windows kernel blocked file output stream.")
        print("👉 Solution: Right-click this app executable and select 'Run as Administrator'.")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Crash Handler Intercepted: {e}")
        print("=" * 60)
