


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# টাইটেল ও বর্ণনা
st.set_page_config(page_title="Motor Analysis", layout="wide")
st.title("🏎️ DC Motor Back EMF Live Analyzer")
st.write("ম্যাম, এই টুলের মাধ্যমে আমরা রিয়েল-টাইমে ল্যাব ডাটা ইনপুট দিয়ে গ্রাফ দেখতে পারি।")

# ইনপুট প্যারামিটার (বাম পাশের সাইডবারে থাকবে)
st.sidebar.header("⚙️ Motor Settings")
v_supply = st.sidebar.number_input("Supply Voltage (V)", value=9.0)
r_armature = st.sidebar.number_input("Armature Resistance (Ra)", value=4.0)

# ডাটা এন্ট্রি সেকশন
st.subheader("📊 ল্যাব রিডিং এখানে বসান")
st.info("নিচের টেবিলের 'Current_Ia' কলামের সংখ্যায় ডাবল ক্লিক করে আপনার ডাটা লিখুন এবং এন্টার চাপুন।")

# প্রাথমিক ডাটা ফ্রেম
df_init = pd.DataFrame({
    "Condition": ["No Load", "Small Fan", "Big Fan"],
    "Current_Ia": [0.20, 0.60, 1.20]
})

# ডাটা এডিটর (এটাই আসল ম্যাজিক)
edited_df = st.data_editor(df_init, num_rows="dynamic")

# ক্যালকুলেশন
if not edited_df.empty:
    # Eb = V - Ia*Ra সূত্র প্রয়োগ
    edited_df["Back_EMF_Eb"] = v_supply - (edited_df["Current_Ia"] * r_armature)
    
    # ফলাফল দেখানো
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### ফলাফল টেবিল:")
        st.dataframe(edited_df)
    
    with col2:
        st.write("### গ্রাফ (Current vs Back EMF):")
        fig, ax = plt.subplots()
        ax.plot(edited_df["Current_Ia"], edited_df["Back_EMF_Eb"], marker='o', linestyle='-', color='red', label='Eb')
        ax.set_xlabel("Armature Current (Ia) in Amps")
        ax.set_ylabel("Back EMF (Eb) in Volts")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
else:
    st.warning("টেবিলে অন্তত একটি ডাটা রাখুন।")
    
