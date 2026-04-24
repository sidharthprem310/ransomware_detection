import streamlit as st
import pandas as pd
import json
import os
import time
import datetime

# --- Pager Settings ---
st.set_page_config(page_title="Ransomware Defend System", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom Antivirus Dark Theme Aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .status-banner-safe {
        background-color: #1b5e20;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #4caf50;
        margin-bottom: 25px;
    }
    .status-banner-danger {
        background-color: #b71c1c;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #f44336;
        margin-bottom: 25px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(244, 67, 54, 0); }
        100% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }
    }
    .threat-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Defender Framework Core")
st.markdown("Real-time behavioral monitoring and Explainable AI defense.")


# --- Data Loaders ---
ledger = []
attacks = []
if os.path.exists("blockchain_ledger.json"):
    try:
        with open("blockchain_ledger.json", "r") as f:
            ledger = json.load(f)
            attacks = [b for b in reversed(ledger) if isinstance(b.get('event_data'), dict)]
    except:
        pass


# --- Antivirus Status Banner ---
if len(attacks) > 0:
    st.markdown(f"""
    <div class="status-banner-danger">
        <h2 style="margin:0; color:white;">🚨 CRITICAL THREAT DETECTED & LOGGED</h2>
        <p style="margin:0; color:#ffcdd2;">System intercepted and logged {len(attacks)} ransomware payload(s) dynamically.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-banner-safe">
        <h2 style="margin:0; color:white;">✅ YOUR PC IS PROTECTED</h2>
        <p style="margin:0; color:#c8e6c9;">XAI monitors are active. Background file processes look normal.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

col_logs, col_metrics = st.columns([1.2, 1])

# --- Left Column: Live Incident Logs ---
with col_logs:
    st.subheader("📋 Active Threat Intelligence Logs")
    
    if attacks:
        for att in attacks[:8]: # show last 8
            data = att['event_data']
            fname = data.get('file', 'Unknown')
            ent = data.get('entropy', 'N/A')
            reasons = data.get('human_reasons', ["High Behavioral Anomaly Detected"])
            timestamp = datetime.datetime.fromtimestamp(att['timestamp']).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            
            # Formatting the human reason bullets
            reason_bullets = "".join([f"<li>{r}</li>" for r in reasons])
            
            st.markdown(f"""
            <div class="threat-card">
                <strong style="color:#ffb74d;">Timestamp:</strong> {timestamp} <br/>
                <strong style="color:#ef5350;">Infected Target:</strong> {fname} <br/>
                <strong style="color:#90caf9;">Payload Entropy:</strong> {ent} <br/>
                <strong style="color:#66bb6a;">🧠 AI Diagnostic Reasoning:</strong>
                <ul style="margin-top: 5px; margin-bottom: 0px; color:#e0e0e0; font-size:14px;">
                    {reason_bullets}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No suspicious activities logged. The system continues to monitor behavior.")


# --- Right Column: Plots & Analytics ---
with col_metrics:
    st.subheader("📈 System Behavioral Plots")
    
    tab1, tab2 = st.tabs(["Entropy Timeline", "XAI Global Model"])
    
    with tab1:
        if os.path.exists("live_timeline.json"):
            try:
                df_live = pd.read_json("live_timeline.json")
                if not df_live.empty:
                    df_live['time_index'] = df_live['time'] - df_live['time'].min()
                    st.line_chart(df_live.set_index("time_index")["entropy"], use_container_width=True)
                else:
                    st.caption("Awaiting baseline entropy sweeps...")
            except:
                st.caption("Syncing local filesystem...")
        else:
            if os.path.exists("detection/realtime_timeline.png"):
                st.image("detection/realtime_timeline.png", use_container_width=True)
            elif os.path.exists("realtime_timeline.png"):
                st.image("realtime_timeline.png", use_container_width=True)
            else:
                 st.caption("Timeline syncing...")
                 
    with tab2:
        st.write("SHAP (SHapley Additive exPlanations) evaluates which logic matrices carry the heaviest classification weight.")
        if os.path.exists("detection/shap_summary.png"):
            st.image("detection/shap_summary.png", use_container_width=True)
        elif os.path.exists("shap_summary.png"):
            st.image("shap_summary.png", use_container_width=True)
        else:
            st.caption("Waiting for verified ransomware payloads to construct SHAP global matrix.")

# --- Auto Refresh Logic ---
time.sleep(2)
st.rerun()
