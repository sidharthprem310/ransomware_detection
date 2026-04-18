import os, random, time

base = r"E:\ransomware_testing"
os.makedirs(base, exist_ok=True)

for i in range(random.randint(20, 40)):
    folder = os.path.join(base, f"folder_{i}")
    os.makedirs(folder, exist_ok=True)

    for j in range(random.randint(2, 5)):
        file_path = os.path.join(folder, f"file_{j}.txt")

        with open(file_path, "w") as f:
            f.write("Normal file content\n" * random.randint(5, 15))

        time.sleep(0.05)

print("✅ Normal file activity generated")