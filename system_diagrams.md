# 🛡️ Main System Architecture (High Readability 16:9)

The previous diagram compressed the text because it tried to draw dozens of tiny individual boxes inside subgraphs. 

To make this **incredibly bold and readable** for a PowerPoint slide, I have consolidated the entire architecture into 5 massive, high-contrast layer blocks. The text will now render huge, allowing anyone in the back of the room to easily read the modules.

Copy this code and throw it into [Mermaid Live Editor](https://mermaid.live).

```mermaid
flowchart LR
    %% Define Massive Text Styles
    classDef L1 fill:#E3F2FD,stroke:#1565C0,stroke-width:3px,color:#0D47A1,font-size:20px
    classDef L2 fill:#E8F5E9,stroke:#2E7D32,stroke-width:3px,color:#1B5E20,font-size:20px
    classDef L3 fill:#FFF3E0,stroke:#EF6C00,stroke-width:3px,color:#E65100,font-size:20px
    classDef L4 fill:#F3E5F5,stroke:#6A1B9A,stroke-width:3px,color:#4A148C,font-size:20px
    classDef L5 fill:#FFEBEE,stroke:#C62828,stroke-width:3px,color:#B71C1C,font-size:20px

    %% -------------------------------------
    %% BIG BOLD LAYER BLOCKS
    %% -------------------------------------
    Monitor["<h1>LAYER 1: NATIVE MONITOR</h1><hr/><h2>• Watchdog Observer<br/>• File Event Handler<br/>• Ransomware Simulator</h2>"]:::L1

    Extract["<h1>LAYER 2: EXTRACTION</h1><hr/><h2>• Shannon Entropy Math<br/>• Rename Frequency Window<br/>• I/O Speed Tracker</h2>"]:::L2

    ML["<h1>LAYER 3: ML CLASSIFIER</h1><hr/><h2>• Random Forest Engine<br/>• Data Normalization<br/>• SHAP Explainer Matrices</h2>"]:::L3

    Forensics["<h1>LAYER 4: BLOCKCHAIN</h1><hr/><h2>• Passive Audit Logging<br/>• SHA-256 Security Hashes<br/>• Exact Millisecond Sync</h2>"]:::L4

    UI["<h1>LAYER 5: DASHBOARD</h1><hr/><h2>• Streamlit Subsystem<br/>• JSON Timeline Plots<br/>• Plyer Desktop Alerts</h2>"]:::L5

    %% -------------------------------------
    %% THICK HORIZONTAL CONNECTIONS
    %% -------------------------------------
    Monitor ===>|Intercepts Events| Extract
    Extract ===>|Normalized Vectors| ML
    ML ===>|Triggers Alert| Forensics
    Forensics ===>|Validates Logs| UI

```
