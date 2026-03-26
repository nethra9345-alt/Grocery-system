import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Grocery Price Analyzer", layout="wide")

st.title("🛒 Smart Grocery Price Analysis App")

# -------------------------------
# OPTION SELECTOR
# -------------------------------
option = st.radio("Choose Input Method", ["Use Sliders", "Edit Table"])

# -------------------------------
# ITEMS & SHOPS
# -------------------------------
items = [
    "Rice", "Milk", "Sugar", "Eggs", "Wheat Flour",
    "Oil", "Salt", "Tea", "Coffee", "Dal"
]

shop_cols = ["Shop_A", "Shop_B", "Shop_C", "Shop_D", "Shop_E"]

# -------------------------------
# SLIDER INPUT
# -------------------------------
if option == "Use Sliders":
    st.sidebar.header("Enter Prices")

    def get_prices(shop_name, defaults):
        return [
            st.sidebar.slider(f"{item} - {shop_name}", 10, 200, defaults[i])
            for i, item in enumerate(items)
        ]

    data = {
        "Item": items,
        "Shop_A": get_prices("Shop A", [50, 30, 45, 60, 55, 120, 20, 80, 150, 90]),
        "Shop_B": get_prices("Shop B", [55, 32, 47, 58, 60, 115, 22, 85, 145, 95]),
        "Shop_C": get_prices("Shop C", [52, 31, 44, 62, 58, 118, 21, 82, 148, 92]),
        "Shop_D": get_prices("Shop D", [48, 29, 46, 59, 54, 122, 19, 78, 152, 88]),
        "Shop_E": get_prices("Shop E", [53, 33, 43, 61, 57, 119, 23, 83, 149, 91])
    }

    df = pd.DataFrame(data)

# -------------------------------
# EDITABLE TABLE INPUT
# -------------------------------
else:
    st.subheader("✏️ Edit Grocery Data")

    default_data = {
        "Item": items,
        "Shop_A": [50, 30, 45, 60, 55, 120, 20, 80, 150, 90],
        "Shop_B": [55, 32, 47, 58, 60, 115, 22, 85, 145, 95],
        "Shop_C": [52, 31, 44, 62, 58, 118, 21, 82, 148, 92],
        "Shop_D": [48, 29, 46, 59, 54, 122, 19, 78, 152, 88],
        "Shop_E": [53, 33, 43, 61, 57, 119, 23, 83, 149, 91]
    }

    df = pd.DataFrame(default_data)
    df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    df = df.dropna()

# -------------------------------
# DATA PROCESSING
# -------------------------------
df[shop_cols] = df[shop_cols].apply(pd.to_numeric, errors='coerce')

df["Average"] = df[shop_cols].mean(axis=1)
df["Cheapest Shop"] = df[shop_cols].idxmin(axis=1)

# -------------------------------
# DISPLAY TABLE
# -------------------------------
st.subheader("📊 Grocery Price Table")
st.dataframe(df, use_container_width=True)

# -------------------------------
# INSIGHTS
# -------------------------------
st.subheader("💡 Insights")

col1, col2 = st.columns(2)

with col1:
    if not df.empty:
        st.success(f"🥇 Cheapest Item: {df.loc[df['Average'].idxmin(), 'Item']}")

with col2:
    if not df.empty:
        st.error(f"💸 Costliest Item: {df.loc[df['Average'].idxmax(), 'Item']}")

# -------------------------------
# BAR CHART
# -------------------------------
st.subheader("📊 Price Comparison Chart")

if not df.empty:
    fig, ax = plt.subplots()
    df.plot(x="Item", y=shop_cols, kind="bar", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -------------------------------
# HEATMAP
# -------------------------------
st.subheader("🔥 Price Heatmap")

if not df.empty:
    fig2, ax2 = plt.subplots()
    numeric_df = df.set_index("Item")[shop_cols + ["Average"]]
    sns.heatmap(numeric_df, annot=True, fmt=".0f", cmap="coolwarm", ax=ax2)
    st.pyplot(fig2)

# -------------------------------
# FILTER
# -------------------------------
st.subheader("🔍 Filter by Item")

if not df.empty:
    selected_item = st.selectbox("Choose an Item", df["Item"])
    st.write(df[df["Item"] == selected_item])

# -------------------------------
# DOWNLOAD
# -------------------------------
st.subheader("⬇ Download Data")

csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "grocery_prices.csv")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Built using Streamlit | Advanced Data Analysis Project")
