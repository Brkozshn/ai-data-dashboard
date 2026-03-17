import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI

st.set_page_config(page_title="AI Dashboard", layout="wide")

st.title("📊 AI Data Analysis Dashboard")

uploaded_file = st.file_uploader("CSV veya Excel yükle", type=["csv", "xlsx"])

if uploaded_file:
    # Dosya oku
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # =========================
    # 🔹 TÜM VERİ ANALİZİ
    # =========================
    st.header("📊 Genel Veri Analizi (Tüm Dataset)")

    st.subheader("📌 Veri Önizleme")
    st.dataframe(df.head())

    st.subheader("📊 Genel İstatistik")
    st.write(df.describe())

    st.subheader("📈 Genel Grafik")

    col_all = st.selectbox("Kolon seç (genel)", df.columns)

    fig1, ax1 = plt.subplots()
    sns.histplot(df[col_all], kde=True, ax=ax1)
    st.pyplot(fig1)

    # =========================
    # 🔹 FİLTRELEME
    # =========================
    st.sidebar.header("🔍 Filtre")

    column_filter = st.sidebar.selectbox("Kolon seç", df.columns)
    unique_vals = df[column_filter].dropna().unique()

    selected_val = st.sidebar.selectbox("Değer seç", unique_vals)

    filtered_df = df[df[column_filter] == selected_val]

    # =========================
    # 🔹 FİLTRELİ ANALİZ
    # =========================
    st.header("🎯 Filtrelenmiş Veri Analizi")

    st.subheader("📌 Veri")
    st.dataframe(filtered_df)

    st.subheader("📊 İstatistik")
    st.write(filtered_df.describe())

    st.subheader("📈 Grafik")

    col = st.selectbox("Kolon seç (filtreli)", df.columns)
    chart_type = st.selectbox("Grafik tipi", ["Histogram", "Boxplot", "Line"])

    fig2, ax2 = plt.subplots()

    if chart_type == "Histogram":
        sns.histplot(filtered_df[col], kde=True, ax=ax2)
    elif chart_type == "Boxplot":
        sns.boxplot(x=filtered_df[col], ax=ax2)
    else:
        filtered_df[col].plot(ax=ax2)

    st.pyplot(fig2)

    # =========================
    # 🔹 EXPORT
    # =========================
    st.download_button(
        "📥 Filtrelenmiş veriyi indir",
        filtered_df.to_csv(index=False),
        "filtered_data.csv",
        "text/csv"
    )

    # =========================
    # 🔹 AI ANALİZ
    # =========================
    st.header("🤖 AI Yorum")

    api_key = st.text_input("OpenAI API Key gir", type="password")

    if api_key:
        client = OpenAI(api_key=api_key)

        if st.button("AI ile tüm veriyi yorumla"):
            summary = df.describe().to_string()

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Bu veri setini iş açısından analiz et:\n{summary}"}
                ]
            )

            st.write("### 📊 Genel Insight")
            st.write(response.choices[0].message.content)

        if st.button("AI ile filtreli veriyi yorumla"):
            summary_filtered = filtered_df.describe().to_string()

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Bu filtrelenmiş veriyi analiz et:\n{summary_filtered}"}
                ]
            )

            st.write("### 🎯 Filtre Insight")
            st.write(response.choices[0].message.content)