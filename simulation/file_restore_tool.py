#This is a controlled academic simulation of ransomware behavior for 
#testing detection systems.
#It encrypts files in a specified directory using a generated key
#and renames them with a .locked extension.
#The key is printed for potential decryption later.
#It DOESN'T PERFORM any MALICIOUS ACTIONS outside the test directory, 
# but always use with caution
#This tool is intended for educational and testing purposes only, 
#and should not be used on important or sensitive data.
#Always ensure you have backups before running such simulations.

import os
import time
import zlib

base = r"E:\ransomware_testing"

print("\n🔍 Scanning for .locked files to restore...")

folders = [os.path.join(base, f) for f in os.listdir(base) if os.path.isdir(os.path.join(base, f))]
# Also include base root if files are directly inside it
folders.append(base)

restored_count = 0

for folder in folders:
    for file in os.listdir(folder):
        
        path = os.path.join(folder, file)

        if os.path.isfile(path) and path.endswith(".locked"):
            try:
                with open(path, "rb") as f:
                    data = f.read()

                try:
                    decrypted = zlib.decompress(data)
                    if b"||NOISE||" in decrypted:
                        decrypted = decrypted.split(b"||NOISE||")[0]
                except zlib.error:
                    # If it wasn't valid zlib (e.g. from a past failed run), skip or clear it
                    continue

                with open(path, "wb") as f:
                    f.write(decrypted)

                original_path = path[:-7] # Remove '.locked'
                
                # if the original path already exists somehow, remove it first
                if os.path.exists(original_path):
                    os.remove(original_path)
                    
                os.rename(path, original_path)

                print(f"🔓 Restored: {original_path}")
                time.sleep(0.01)
                restored_count += 1
            except Exception as e:
                print(f"Error restoring {path}: {e}")

print(f"\n✅ File restoration complete! Restored {restored_count} files.")