import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Grocery Price Analyzer", layout="wide")

st.title("🛒 Smart Grocery Price Analysis App")


st.sidebar.header("Enter Prices")

items = ["Rice", "Milk", "Sugar", "Eggs"]

data = {
    "Item": items,
    "Shop_A": [
        st.sidebar.slider("Rice - Shop A", 30, 100, 50),
        st.sidebar.slider("Milk - Shop A", 20, 80, 30),
        st.sidebar.slider("Sugar - Shop A", 30, 90, 45),
        st.sidebar.slider("Eggs - Shop A", 40, 100, 60)
    ],
    "Shop_B": [
        st.sidebar.slider("Rice - Shop B", 30, 100, 55),
        st.sidebar.slider("Milk - Shop B", 20, 80, 32),
        st.sidebar.slider("Sugar - Shop B", 30, 90, 47),
        st.sidebar.slider("Eggs - Shop B", 40, 100, 58)
    ],
    "Shop_C": [
        st.sidebar.slider("Rice - Shop C", 30, 100, 52),
        st.sidebar.slider("Milk - Shop C", 20, 80, 31),
        st.sidebar.slider("Sugar - Shop C", 30, 90, 44),
        st.sidebar.slider("Eggs - Shop C", 40, 100, 62)
    ]
}

df = pd.DataFrame(data)


df["Average"] = df[["Shop_A", "Shop_B", "Shop_C"]].mean(axis=1)
df["Cheapest Shop"] = df[["Shop_A", "Shop_B", "Shop_C"]].idxmin(axis=1)


st.subheader("📊 Grocery Price Table")
st.dataframe(df, use_container_width=True)

st.subheader("💡 Insights")

col1, col2 = st.columns(2)

with col1:
    cheapest_item = df.loc[df["Average"].idxmin(), "Item"]
    st.success(f"🥇 Cheapest Item Overall: {cheapest_item}")

with col2:
    costly_item = df.loc[df["Average"].idxmax(), "Item"]
    st.error(f"💸 Costliest Item Overall: {costly_item}")


st.subheader("📊 Price Comparison Chart")

fig, ax = plt.subplots()
df.plot(x="Item", y=["Shop_A", "Shop_B", "Shop_C"], kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)


st.subheader("🔥 Price Heatmap")

fig2, ax2 = plt.subplots()

numeric_df = df.set_index("Item")[["Shop_A", "Shop_B", "Shop_C", "Average"]]

sns.heatmap(numeric_df, annot=True, cmap="coolwarm", ax=ax2)

st.pyplot(fig2)

st.subheader("🔍 Filter by Item")

selected_item = st.selectbox("Choose an Item", df["Item"])

filtered = df[df["Item"] == selected_item]
st.write(filtered)


st.subheader("⬇ Download Data")

csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "grocery_prices.csv")
