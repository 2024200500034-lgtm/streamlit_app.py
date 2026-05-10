import os
import subprocess
import sys

# অটোমেটিক লাইব্রেরি ইন্সটল করার হ্যাক
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    install('pandas')
    install('matplotlib')
    import pandas as pd
    import matplotlib.pyplot as plt

import streamlit as st

# বাকি অ্যাপ কোড এখান থেকে শুরু
st.title("🏎️ DC Motor Analysis Dashboard")
st.write("ম্যাম, এই টুলটি সরাসরি ল্যাব ডাটা থেকে গ্রাফ তৈরি করে।")

# ইনপুট সেকশন
v_supply = st.number_input("Supply Voltage (V)", value=9.0)
r_armature = st.number_input("Armature Resistance (Ra)", value=4.0)

# ডাটা এন্ট্রি টেবিল
st.subheader("⌨️ ডাটা ইনপুট দিন (নিচের টেবিলে ক্লিক করে মান লিখুন)")
input_data = pd.DataFrame({
    "Condition": ["No Load", "Small Fan", "Big Fan"],
    "Current_Ia": [0.20, 0.50, 1.10]
})

edited_df = st.data_editor(input_data, num_rows="dynamic")

# ক্যালকুলেশন
if not edited_df.empty:
    edited_df["Back_EMF_Eb"] = v_supply - (edited_df["Current_Ia"] * r_armature)
    
    st.write("### ফলাফল টেবিল:")
    st.dataframe(edited_df)

    # গ্রাফ তৈরি
    st.write("### গ্রাফ (Ia vs Eb):")
    fig, ax = plt.subplots()
    ax.plot(edited_df["Current_Ia"], edited_df["Back_EMF_Eb"], marker='o', color='red', label='Back EMF')
    ax.set_xlabel("Armature Current (Ia)")
    ax.set_ylabel("Back EMF (Eb)")
    ax.grid(True)
    st.pyplot(fig)import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DC Motor Analysis Tool", layout="wide")

st.title("🏎️ DC Motor Back EMF & Efficiency Live Analyzer")
st.markdown("ম্যাম, এই টুলটি ব্যবহার করে আমরা ল্যাবের ডাটা সরাসরি অ্যানালাইসিস করতে পারি।")

# Sidebar inputs
st.sidebar.header("Motor Parameters")
v_supply = st.sidebar.number_input("Supply Voltage (V)", value=9.0)
r_armature = st.sidebar.number_input("Armature Resistance (Ra in Ohms)", value=4.0)

# Data Table Input
st.subheader("📊 Enter Lab Readings")
data = st.data_editor(
    pd.DataFrame({
        "Load Condition": ["No Load", "Small Fan", "Big Fan", "Heavy Load"],
        "Current (Ia in Amps)": [0.2, 0.5, 1.2, 2.0]
    }),
    num_rows="dynamic"
)

# Calculations
if not data.empty:
    df = data.copy()
    df["Back EMF (Eb)"] = v_supply - (df["Current (Ia in Amps)"] * r_armature)
    df["Efficiency (%)"] = (df["Back EMF (Eb)"] / v_supply) * 100

    # Display Results
    st.subheader("✅ Calculated Results")
    st.write(df)

    # Graphing
    st.subheader("📈 Back EMF vs Armature Current Graph")
    fig, ax = plt.subplots()
    ax.plot(df["Current (Ia in Amps)"], df["Back EMF (Eb)"], marker='o', linestyle='-', color='red')
    ax.set_xlabel("Armature Current (Ia)")
    ax.set_ylabel("Back EMF (Eb)")
    ax.grid(True)
    st.pyplot(fig)
