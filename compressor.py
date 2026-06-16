import os
import zipfile
from tqdm import tqdm

def zip_folder(g_drive_destination, source_folder, output_zip_name):

    final_output_path = os.path.join(g_drive_destination, output_zip_name)

    print(f"Scanning source: {source_folder}")
    
    total_files = 0
    for root, dirs, files in os.walk(source_folder):
        total_files += len(files)
        
    if total_files == 0:
        print("\n⚠️   Warning: Target folder is completely empty. Sync canceled.")
        print("=" * 60)
        return

    print(f"📊 Status: Found {total_files} files ready for extraction.")
    print("-" * 60)

    try:
        with zipfile.ZipFile(final_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
         
            with tqdm(total=total_files, desc="⚡ Syncing to Cloud", unit="file", leave=True, ncols=75) as pbar:
                
                for root, dirs, files in os.walk(source_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                     
                        arcname = os.path.relpath(file_path, start=source_folder)
                    
                        zipf.write(file_path, arcname)
                        
                        pbar.update(1)
                        
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
