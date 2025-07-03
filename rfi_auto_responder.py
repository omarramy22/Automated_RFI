import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime

# Create OpenAI client for project mode
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxx") # Replace with your actual OpenAI API key

LOG_FILE = "rfi_log.json"

def save_rfi_log(question, answer):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_rfi_response(rfi_text):
    prompt = f"""You are an AI agent working for EDECS, a premier construction and engineering company with over 30 years of experience, recognized for delivering innovative, sustainable, and high-quality projects. As a Grade A Contractor, EDECS
operates in Egypt, Saudi Arabia (KSA), and United Arab Emirates (UAE), demonstrating expertise in
marine, infrastructure, and building construction. The company's reputation
is built on its ability to manage complex projects, from design to execution, in a timely and cost-effective
manner. Generate a clear, professional response to the following RFI from a subcontractor or consultant:\n\nRFI:\n{rfi_text}\n\nResponse:"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,  # Required for project keys (unless explicitly disabled in project settings)
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="EDECS RFI Auto-Responder", layout="centered")
st.title("📄 EDECS RFI Auto-Responder")

# Text input
rfi_text = st.text_area("Paste your RFI question here:", height=200)

# Generate button
if st.button("Generate Response") and rfi_text.strip():
    with st.spinner("Generating response..."):
        response = generate_rfi_response(rfi_text)
    st.session_state["rfi_question"] = rfi_text
    st.session_state["rfi_response"] = response
    st.session_state["ready_to_save"] = True

# Show suggested response if exists
if st.session_state.get("ready_to_save", False):
    st.subheader("✉️ Suggested Response:")
    edited = st.text_area("Edit if needed:", value=st.session_state["rfi_response"], key="edit_box", height=200)

    if st.button("✅ Approve & Save"):
        save_rfi_log(st.session_state["rfi_question"], edited)
        st.success("Saved successfully!")
        st.session_state["ready_to_save"] = False

# --- Log display checkbox ---
st.markdown("---")
if st.checkbox("📜 Show RFI Log"):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                data = json.load(f)
                if data:
                    for i, entry in enumerate(reversed(data[-5:])):  # Show last 5
                        idx = len(data) - 1 - i  # Get real index
                        st.markdown(f"**{entry['timestamp']}**")
                        st.markdown(f"🔸 **Q:** {entry['question']}")
                        st.markdown(f"✅ **A:** {entry['answer']}")
                        if st.button(f"🗑️ Delete Entry {i+1}", key=f"del_{i}"):
                            data.pop(idx)
                            with open(LOG_FILE, "w") as fw:
                                json.dump(data, fw, indent=2)
                            st.success("Entry deleted. Please refresh to update view.")
                            st.rerun()
                        st.markdown("---")
                else:
                    st.info("Log file exists but is empty.")
            except json.JSONDecodeError:
                st.error("Log file is corrupted or not valid JSON.")
    else:
        st.info("No RFIs saved yet.")

