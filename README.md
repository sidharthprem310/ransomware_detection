# 🛡️ XAI-Driven Behavioral Ransomware Detector

An advanced, real-time ransomware early detection and prevention system built on **Behavioral Machine Learning**, **Immutable Blockchain Auditing**, and **Explainable AI (XAI)**. 

This framework natively intercepts malicious cryptography by mapping file-level interactions dynamically without relying on static signature extensions, operating successfully as a Next-Gen Endpoint Detection and Response (EDR) logic system.

![System Shield](https://img.shields.io/badge/Security-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Machine Learning](https://img.shields.io/badge/ML-Random_Forest-9C27B0)
![Blockchain](https://img.shields.io/badge/Ledger-SHA_256-orange)

## 🌟 Key Features
- **Zero-Day Predictive Detection:** The Random Forest Machine Learning framework learns mathematical payload structures via Shannon Entropy equations rather than `.locked` extension footprints, catching attacks millliseconds *before* files are renamed natively.
- **Explainable AI (XAI):** Integrated with Game Theory's `SHAP` matrices calculating human-interpretable reasoning on *why* a file was targeted and what features (file activity speed, renaming frequency, OS entropy metrics) triggered the alarm.
- **Immutable Blockchain Ledger:** Every verified malicious interception is hashed globally via `SHA-256` cryptographic mapping resulting in a completely tamper-proof event audit trail visible in your application.
- **Native OS Preventor (Kill-Switch):** Features a dynamic OS trap loop that artificially paralyzes attacker processes natively if they breach maximum threshold parameters (10 encrypted files limit).
- **Streamlit Web Dashboard:** Run your system while monitoring a beautiful, live-updating Streamlit web command center projecting live threat maps and structural timeline plotting.

## 🏗️ System Architecture
The framework acts upon the following core loop:
1. `watchdog` intercepts real-time `Create/Modify/Rename` OS disk calls.
2. The payload is chunked and subjected to algorithmic mathematical equation metrics.
3. The dataset array is rapidly fed into the trained `Random Forest (model.pkl)` parameter.
4. Positive predictions fire desktop alert hooks (`plyer`) and create a `Blockchain` hash block.

## 🚀 Installation & Usage

**1. Setup Environment**
Ensure you have python installed. Load the directory.
```bash
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

**2. Access the Command Center (Dashboard)**
Launch the primary GUI dashboard.
```bash
streamlit run dashboard.py
```
> The dashboard serves as a monitoring layout. The background executable engines must be run manually through standard separated terminals.

**3. Launch the Defender**
In a new terminal, launch the live OS detection guard algorithm:
```bash
py detection/realtime_detector.py
```

**4. Trigger a Simulation Payload**
To verify the system natively, open a final terminal and launch the simulated hacker script that encrypts synthetic local text files dynamically. 
```bash
py simulation/file_activity_simulator.py
```

Watch the Web Dashboard light up with Threat Map instances natively, intercepting and blocking the payload.
To clean the testing environment, run `py simulation/file_restore_tool.py`.

## 📜 Disclaimer
This project is built purely as a strictly controlled academic and architectural framework for analyzing cybersecurity detection methods. The simulation scripts utilize synthetic payloads natively bound strictly to their local sandbox configurations. Always deploy responsibly.
