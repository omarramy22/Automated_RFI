
# 📄 README: RFI Auto-Responder – EDECS AI & Tech Internship Case Study

## 🧠 Overview

This prototype is an AI-powered assistant that automates responses to RFIs (Requests for Information) in construction projects. It is tailored to EDECS’s domain by simulating how an engineer at EDECS would respond professionally to RFIs. The tool reduces manual effort, speeds up communication, and ensures consistency in responses.

## ⚙️ Features

- Enter or paste any RFI text
- Generate a suggested professional response using OpenAI’s GPT-4o
- Edit and approve the response
- Save approved responses to a local log file
- View and delete past RFI entries via a web interface

---

## ▶️ How to Run Locally

1. **Clone the repo and install dependencies:**

```bash
pip install streamlit openai
```

2. **Paste your OpenAI API key directly into the script:**

In `rfi_auto_responder.py`, find:

```python
client = OpenAI(api_key="your_sk-proj-key-here")
```

3. **Run the app:**

```bash
streamlit run rfi_auto_responder.py
```

---

## 🧱 Key Design Choices

- **LLM integration:** Uses OpenAI’s `gpt-4o-mini` via `sk-proj-...` project-mode keys
- **UI:** Built with Streamlit for speed and simplicity
- **Persistence:** RFI logs saved in `rfi_log.json`
- **Session state** tracks generated responses across interactions
- **Delete button** allows removal of saved entries

---

## ⚠️ Known Limitations

- Responses are not grounded in project-specific documents
- File-based log storage isn’t scalable for production use
- No login or access control layer
