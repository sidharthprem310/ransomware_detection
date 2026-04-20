import os
import sys
import time
import numpy as np
import pandas as pd
import shap
from plyer import notification

# Safely map Root directory into path to allow cross-folder importing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blockchain import BlockchainLogger

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from train_model import train


# ===================== CONFIG =====================
BASE_PATH = r"E:\ransomware_testing"

# ===================== LOAD MODEL =====================
model, scaler = train()
explainer = shap.TreeExplainer(model)

# ===================== GLOBAL STORAGE =====================
events = []
timeline_data = []
shap_history = []
blockchain = BlockchainLogger()
RANSOMWARE_COUNT = 0


# ===================== ENTROPY FUNCTION =====================
def calculate_entropy(path):
    try:
        # Give OS a millisecond to release file hooks during fast parallel writes
        time.sleep(0.05)
        
        with open(path, "rb") as f:
            data = f.read()

        if len(data) == 0:
            return 0

        probs = [data.count(b) / len(data) for b in set(data)]
        return -sum(p * np.log2(p) for p in probs)

    except:
        return 0


# ===================== DETECTOR =====================
class Monitor(FileSystemEventHandler):

    def process(self, etype, path):

        if not os.path.isfile(path):
            return

        # ---------- FEATURE EXTRACTION ----------
        ent = calculate_entropy(path)
        
        # Skip pure lock-bumps or empty reads
        if ent == 0:
            return

        # detect rename (.locked files)
        rename_flag = 1 if path.endswith(".locked") else 0

        # count recent rename activity
        recent = events[-10:]
        rename_freq = sum(e["rename_flag"] for e in recent)

        file_activity = len(events) + 1

        sample = pd.DataFrame([{
            "entropy": ent,
            "rename_freq": rename_freq,
            "file_activity": file_activity
        }])

        # ---------- PREDICTION ----------
        sample_scaled = scaler.transform(sample)
        prediction = model.predict(sample_scaled)[0]

        # store event
        events.append({
            "entropy": ent,
            "rename_flag": rename_flag
        })
        timeline_data.append({
            "time": time.time(),
            "entropy": ent,
            "is_malicious": prediction == 1
        })

        # ---------- OUTPUT ----------
        print("\n-------------------------------")
        print(f"File: {os.path.basename(path)}")
        print(f"Entropy: {round(ent, 2)}")

        # ---------- EARLY WARNING ----------
        if ent > 5.5 and prediction == 0:
            print("⚠️ EARLY WARNING: Suspicious encryption behavior")

        # ---------- FINAL DETECTION ----------
        if prediction == 1 and ent > 6:
            global RANSOMWARE_COUNT
            RANSOMWARE_COUNT += 1
            print("🚨 RANSOMWARE DETECTED")

            # ---------- SHAP EXPLANATION ----------
            shap_values = explainer.shap_values(sample)

            if isinstance(shap_values, list):
                values = np.array(shap_values[1][0]).flatten()
            elif hasattr(shap_values, 'values'):
                val_arr = shap_values.values
                if len(val_arr.shape) == 3:
                    values = val_arr[0, :, 1].flatten()
                else:
                    values = val_arr[0].flatten()
            else:
                s_arr = np.array(shap_values)
                if len(s_arr.shape) == 3:
                    values = s_arr[0, :, 1].flatten()
                else:
                    values = s_arr[0].flatten()

            importance = sorted(
                zip(sample.columns, values),
                key=lambda x: abs(float(x[1])),
                reverse=True
            )
            shap_history.append((sample, values))

            print("\n🔍 WHY DETECTED:")
            shap_dict = {}
            for feature, value in importance[:3]:
                shap_dict[feature] = round(float(value), 3)
                print(f"{feature}: {round(float(value), 3)}")

            # ---------- HUMAN EXPLANATION ----------
            print("\n🧠 INTERPRETATION:")
            human_reasons = []
            if ent > 6:
                reason = "High entropy indicates file encryption"
                human_reasons.append(reason)
                print("→ " + reason)
            if rename_freq > 2:
                reason = "Frequent file renaming detected"
                human_reasons.append(reason)
                print("→ " + reason)
            if file_activity > 20:
                reason = "Rapid file modifications observed"
                human_reasons.append(reason)
                print("→ " + reason)

            # ---------- BLOCKCHAIN LOGGING ----------
            event_data = {
                "file": os.path.basename(path),
                "entropy": round(ent, 3),
                "shap_reasoning": shap_dict,
                "human_reasons": human_reasons
            }
            blockchain.add_block(event_data)

            # ---------- NATIVE DESKTOP ALERT ----------
            try:
                reason_str = " | ".join(human_reasons)
                notification.notify(
                    title="🚨 RANSOMWARE DETECTED",
                    message=f"File: {os.path.basename(path)}\nReason: {reason_str}",
                    app_name="Ransomware Defend",
                    timeout=3
                )
            except:
                pass # safely ignore if UI thread issues occur during mass loop

            # ---------- PREVENTOR (KILL-SWITCH) ----------
            if RANSOMWARE_COUNT >= 10:
                kill_path = os.path.join(BASE_PATH, ".kill_signal")
                with open(kill_path, "w") as kf:
                    kf.write("STOP")
                print("🛡️ MAX THREAT LIMIT REACHED! Deploying Kill-Switch Block.")

        # Sync plots globally occasionally so streamlit can fetch them live
        if len(timeline_data) % 5 == 0:
            pd.DataFrame(timeline_data).to_json("live_timeline.json", orient="records")

        print("-------------------------------")


    # ---------- EVENT HANDLERS ----------
    def on_created(self, event):
        self.process("created", event.src_path)

    def on_modified(self, event):
        self.process("modified", event.src_path)

    def on_moved(self, event):
        self.process("moved", event.dest_path)


# ===================== MAIN =====================
if __name__ == "__main__":

    print("🔍 REAL-TIME RANSOMWARE DETECTION STARTED...")
    print(f"Monitoring folder: {BASE_PATH}")

    observer = Observer()
    event_handler = Monitor()

    observer.schedule(event_handler, BASE_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopping detection...")
        observer.stop()

        if timeline_data:
            df_time = pd.DataFrame(timeline_data)
            df_time['time'] = df_time['time'] - df_time['time'].min()
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 5))
            plt.plot(df_time['time'], df_time['entropy'], label='Entropy', color='blue')
            attacks = df_time[df_time['is_malicious'] == True]
            plt.scatter(attacks['time'], attacks['entropy'], color='red', label='Ransomware Detected')
            plt.axhline(y=6, color='r', linestyle='--', label='Danger Threshold')
            plt.xlabel("Time (seconds)")
            plt.ylabel("Entropy")
            plt.title("Ransomware Affection Timeline")
            plt.legend()
            plt.tight_layout()
            plt.savefig("realtime_timeline.png")
            plt.close()
            print("📈 Saved realtime_timeline.png")

        if shap_history:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            X_cols = shap_history[0][0].columns
            agg_shap = np.mean([np.abs(sh[1]) for sh in shap_history], axis=0)
            plt.figure(figsize=(8, 5))
            plt.barh(X_cols, agg_shap, color='crimson')
            plt.xlabel("Mean |SHAP Value| (Impact on Detection)")
            plt.title("SHAP Feature Importance (Recent Attacks)")
            plt.tight_layout()
            plt.savefig("shap_summary.png")
            plt.close()
            print("📈 Saved shap_summary.png")

    observer.join()