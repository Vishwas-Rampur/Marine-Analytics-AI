import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils import load_from_zip
from pipeline import run_pipeline, to_csv_bytes


st.set_page_config(
    page_title="AI-Driven Unified Data Platform",
    page_icon="🌊",
    layout="wide"
)


def inject_css():
    try:
        with open("styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass


inject_css()

st.title("🌊 AI-Driven Unified Data Platform")


# SIDEBAR
with st.sidebar:
    st.header("Upload Dataset ZIP")

    z = st.file_uploader("Upload ZIP", type=["zip"])

    run_btn = st.button("Run Pipeline", type="primary", use_container_width=True)


if not z:
    st.info("Upload a ZIP file to begin.")
    st.stop()


# LOAD DATA
loaded, all_files = load_from_zip(z.getvalue())

st.divider()

st.subheader("📦 ZIP Contents")
st.write(f"Detected **{len(all_files)}** dataset files.")


# METRICS
c1, c2, c3 = st.columns(3)

c1.metric("🌊 Ocean", "Loaded" if loaded.ocean is not None else "Missing")
c2.metric("🐟 Fisheries", "Loaded" if loaded.fisheries is not None else "Missing")
c3.metric("🧬 Biodiversity", "Loaded" if loaded.biodiversity is not None else "Missing")


if not run_btn:
    st.warning("Click Run Pipeline")
    st.stop()


res = run_pipeline(loaded.ocean, loaded.fisheries, loaded.biodiversity)


tabs = st.tabs(["🌊 Ocean", "🐟 Fisheries", "🧬 Biodiversity", "📊 All Data"])


# COMMON PANEL
def show_df(df, name):

    if df is None:
        st.info("No dataset")
        return

    rows, cols = df.shape
    missing = df.isna().sum().sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", rows)
    c2.metric("Columns", cols)
    c3.metric("Missing", int(missing))

    st.dataframe(df.head(100), use_container_width=True)

    if "latitude" in df.columns and "longitude" in df.columns:
        st.subheader("Geographic Map")
        st.map(df[["latitude", "longitude"]].dropna())

    st.download_button("Download CSV", to_csv_bytes(df), file_name=name)


# 🌊 OCEAN TAB
with tabs[0]:

    st.header("🌊 Ocean Data")

    show_df(res.ocean, "ocean.csv")

    if res.ocean is not None and "date" in res.ocean.columns:

        df = res.ocean.copy()
        df["date"] = pd.to_datetime(df["date"])

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            col = numeric_cols[0]

            st.header("📈 Ocean Trend Analysis")

            fig = plt.figure(figsize=(6,3))
            plt.plot(df["date"], df[col])
            plt.title("Ocean Temperature Trend")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            trend = df[col].iloc[-1] - df[col].iloc[0]

            if trend > 0:
                st.success("Temperature Increasing 📈")
            else:
                st.warning("Temperature Decreasing 📉")


# 🐟 FISHERIES TAB
with tabs[1]:

    st.header("🐟 Fisheries Data")

    show_df(res.fisheries, "fisheries.csv")

    if res.fisheries is not None:

        df = res.fisheries

        numeric_cols = [
            col for col in df.select_dtypes(include="number").columns
            if "id" not in col.lower()
        ]

        if len(numeric_cols) > 0:

            selected = st.selectbox("Select Column", numeric_cols)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Catch Distribution")
                fig = plt.figure(figsize=(4,3))
                plt.hist(df[selected], bins=20)
                st.pyplot(fig)

            with col2:
                if "species" in df.columns:
                    st.subheader("Species Share")
                    counts = df["species"].value_counts()
                    fig = plt.figure(figsize=(4,3))
                    plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
                    st.pyplot(fig)

            # AI Prediction
            st.header("🤖 AI Prediction Module")

            y = df[selected].values
            x = np.arange(len(y))

            coef = np.polyfit(x, y, 1)
            poly = np.poly1d(coef)

            future_x = np.arange(len(y) + 10)

            fig = plt.figure(figsize=(5,3))
            plt.plot(x, y, label="Actual")
            plt.plot(future_x, poly(future_x), "--", label="Prediction")
            plt.legend()
            st.pyplot(fig)

            prediction = poly(len(y) + 5)
            st.metric("Predicted Future Catch", round(prediction, 2))

            # 🔥 AUTO INSIGHTS
            st.subheader("📊 Insights")

            st.write(f"Average Catch: {round(df[selected].mean(),2)}")
            st.write(f"Maximum Catch: {round(df[selected].max(),2)}")
            st.write(f"Minimum Catch: {round(df[selected].min(),2)}")

            if coef[0] > 0:
                st.success("Overall trend is increasing 📈")
            else:
                st.warning("Overall trend is decreasing 📉")


# 🧬 BIODIVERSITY TAB
with tabs[2]:

    st.header("🧬 Biodiversity Data")

    show_df(res.biodiversity, "bio.csv")

    if res.biodiversity is not None:

        df = res.biodiversity

        numeric_cols = [
            col for col in df.select_dtypes(include="number").columns
            if "id" not in col.lower()
        ]

        if len(numeric_cols) > 0:

            selected = st.selectbox("Select Column", numeric_cols)

            st.subheader("Sequence Length Analysis")

            fig = plt.figure(figsize=(4,3))
            plt.hist(df[selected], bins=20)
            st.pyplot(fig)


# 📊 ALL DATA
with tabs[3]:

    st.header("📊 All Uploaded Data")

    for name, df in all_files.items():
        st.write(name)
        st.dataframe(df.head())