import streamlit as st
import pandas as pd
import altair as alt
from database.firebase_database import init_database, read_from_database

# Initialize database
init_database()
data = read_from_database("/")

# Dashbord layout
st.set_page_config(page_title="RealEstate Dashboard", page_icon="🏢", layout="wide")

# Dashboard title
st.markdown(
    """
    <h1 style='text-align: center; color: #89CFF0;'>Appartement Prices in Greater Montreal 🏢</h1>
    <hr style="border:1px solid #89CFF0;">
    """,
    unsafe_allow_html=True,
)

# Data preprocessing
south_shore_regions = ["longueuil", "saint-hubert", "brossard"]
records = []
for region, region_dict in data.items():
    if region in south_shore_regions:
        continue
    for entry_id, stats in region_dict.items():
        records.append(
            {
                "region": region,
                "date": stats["date"],
                "average_price": stats["average_price"],
                "count": stats["count"],
                "maximum_price": stats["max_price"],
                "median_price": stats["median_price"],
                "minimum_price": stats["min_price"],
                "std_dev_price": stats["std_dev_price"],
            }
        )

df_all = pd.DataFrame(records)
df_all["date"] = pd.to_datetime(df_all["date"])
unique_regions = df_all["region"].unique()

# Sidebar
with st.sidebar:
    st.markdown("## Filters 🔍")
    selected_regions = st.multiselect(
        "Select regions:", unique_regions, default=unique_regions[:3]
    )
    price_type = st.radio(
        "Choose price metric:",
        ["minimum_price", "maximum_price", "median_price"],
        horizontal=True,
    )

# Filter data based on user selection
filtered_data = (
    df_all[df_all["region"].isin(selected_regions)]
    if selected_regions
    else df_all.iloc[0:0]
)

# Function to create line charts based on date series data
def create_chart(data, x_col, y_col, title, y_title):
    return (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                x_col, title="Date", axis=alt.Axis(labelAngle=-45, format="%d/%m/%Y")
            ),
            y=alt.Y(y_col, title=y_title),
            color=alt.Color("region:N", legend=alt.Legend(title="Regions")),
            tooltip=[
                alt.Tooltip(x_col, format="%d/%m/%Y"),
                alt.Tooltip(y_col, format=","),
            ],
        )
        .properties(title=title, height=400)
        .configure_title(fontSize=18, anchor="middle", color="#89CFF0")
    )

# Display charts in a two-column layout
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(
        create_chart(
            filtered_data,
            "date:T",
            "average_price:Q",
            "Average Price Trend 📈",
            "Average Price",
        ),
        use_container_width=True,
    )
    st.altair_chart(
        create_chart(
            filtered_data,
            "date:T",
            "std_dev_price:Q",
            "Price Standard Deviation 📊",
            "Std Dev of Price",
        ),
        use_container_width=True,
    )

filtered_data["price_per_listing"] = filtered_data["average_price"] / filtered_data["count"]
with col2:
    st.altair_chart(
        create_chart(
            filtered_data,
            "date:T",
            "count:Q",
            "Number of Listings Over Time 🏠",
            "Number of Listings",
        ),
        use_container_width=True,
    )
    st.altair_chart(
        create_chart(
            filtered_data,
            "date:T",
            "price_per_listing:Q",
            "Price-to-Listing Ratio Over Time 💰",
            "Price per listing",
        ),
        use_container_width=True,
    )

# Distribution chart
dist_chart = (
    alt.Chart(filtered_data)
    .transform_bin("binned_price", field=price_type, bin=alt.Bin(maxbins=15))
    .mark_bar(opacity=0.7)
    .encode(
        x=alt.X(
            price_type,
            bin=alt.Bin(maxbins=15),
            title=f"{price_type.replace('_', ' ').capitalize()}",
        ),
        y=alt.Y("count()", title="Frequency"),
        color=alt.Color("region:N", legend=alt.Legend(title="Regions")),
        tooltip=[
            alt.Tooltip(price_type, format=",.0f"),
            alt.Tooltip("count()", format=","),
        ],
    )
    .properties(title=f"{price_type.replace('_', ' ').title()} Distribution 📊", height=400)
    .configure_title(fontSize=18, anchor="middle", color="#89CFF0")
)
st.altair_chart(dist_chart, use_container_width=True)

# Filtered data
st.markdown(
    "<h3 style='text-align: center;'>Real Estate Data 📄</h3>", unsafe_allow_html=True
)
st.dataframe(filtered_data, height=500, use_container_width=True)
