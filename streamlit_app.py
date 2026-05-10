import streamlit as st
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
