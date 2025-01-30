import streamlit as st
import pandas as pd
import altair as alt
from database.firebase_database import init_database, read_from_database

# Call once at the start
init_database()
# Now read the data
data = read_from_database("/")

# Set page config to wide mode to use full width
st.set_page_config(page_title="RealEstate Dashboard", page_icon="🏢",layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>Appartement prices in Greater Montreal 🏢</h1>",
    unsafe_allow_html=True,
)

south_shore_regions = ["longueuil", "saint-hubert", "brossard"]
records = []
for region, region_dict in data.items():
    if region in south_shore_regions:
        continue
    for entry_id, stats in region_dict.items():
        record = {
            "region": region,
            "date": stats["date"],
            "average_price": stats["average_price"],
            "count": stats["count"],
            "maximum_price": stats["max_price"],
            "median_price": stats["median_price"],
            "minimum_price": stats["min_price"],
            "std_dev_price": stats["std_dev_price"],
        }
        records.append(record)

df_all = pd.DataFrame(records)
df_all["date"] = pd.to_datetime(df_all["date"])
unique_regions = df_all["region"].unique()

# Sidebar for region selection
st.sidebar.markdown("### Select regions of interest")
selected_regions = []
for i, region in enumerate(unique_regions):
    if st.sidebar.checkbox(region, value=(i == 0)):  # Checkbox for each region
        selected_regions.append(region)

# Filter data based on selected regions
if selected_regions:
    filtered_data = df_all[df_all["region"].isin(selected_regions)]
else:
    filtered_data = pd.DataFrame(columns=df_all.columns)

# Sidebar selector for price type
st.sidebar.markdown("### Select distribution price type")
st.markdown(
    """
    <style>
    [data-baseweb="select"] {
        margin-top: -30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
price_type = st.sidebar.selectbox(
    "Hidden",
    ["minimum_price", "maximum_price", "median_price"],
    label_visibility="hidden"
)

# Average price trend over time for selected regions
avg_chart = (
    alt.Chart(filtered_data)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "date:T",
            title="Date (Day/Month/Year)",
            axis=alt.Axis(
                labelAngle=-45, format="%d/%m/%Y", tickCount="day", grid=True
            ),
        ),
        y=alt.Y(
            "average_price:Q",
            title="Average price (CAD)",
        ),
        color=alt.Color("region:N", title="Region", legend=alt.Legend(title="Regions")),
        tooltip=[
            alt.Tooltip("date:T", title="Date (Day/Month/Year)", format="%d/%m/%Y"),
            alt.Tooltip("average_price:Q", title="Average price", format=","),
            alt.Tooltip("region:N", title="Region")
        ]

    )
    .properties(
        title="Average price trend over time by region",
        height=800,
    )
    .configure_title(fontSize=20, anchor="middle", color="white")
)

# Count of listings over time for selected regions
count_chart = (
    alt.Chart(filtered_data)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "date:T",
            title="Date (Day/Month/Year)",
            axis=alt.Axis(
                labelAngle=-45, format="%d/%m/%Y", tickCount="day", grid=True
            ),
        ),
        y=alt.Y(
            "count:Q",
            title="Number of listings",
        ),
        color=alt.Color("region:N", title="Region", legend=alt.Legend(title="Regions")),
    )
    .properties(
        title="Count of listings over time by region",
        height=800,
    )
    .configure_title(fontSize=20, anchor="middle", color="white")
)

# Price distribution chart for selected regions
dist_chart = (
    alt.Chart(filtered_data)
    .transform_bin(
        "binned_price",  # Bin start
        field=f"{price_type}",  # Field to bin
        bin=alt.Bin(maxbins=10)  # Number of bins
    )
    .mark_bar(opacity=0.7)
    .encode(
        x=alt.X(
            f"{price_type}:Q",
            bin=alt.Bin(maxbins=10),
            title=f"{price_type.replace('_', ' ').capitalize()} (Price ranges)",
        ),
        y=alt.Y("count()", title="Frequency"),
        color=alt.Color("region:N", legend=alt.Legend(title="Regions")),
        tooltip=[
            alt.Tooltip("binned_price:Q", title="Price Range (Low)", format=","),
            alt.Tooltip("binned_price_end:Q", title="Price Range (High)", format=","),
            alt.Tooltip("count():Q", title="Frequency", format=","),
            alt.Tooltip("region:N", title="Region")
        ]
    )
    .properties(
        title=f"Distribution of {price_type.replace('_', ' ')} by region",
        height=800,
    )
    .configure_title(fontSize=20, anchor="middle", color="white")
)

# Standard deviation price over time per regions
std_dev_chart = (
    alt.Chart(filtered_data)
    .mark_line(point=True)
        .encode(
        x=alt.X(
            "date:T",
            title="Date (Day/Month/Year)",
            axis=alt.Axis(
                labelAngle=-45, format="%d/%m/%Y", tickCount="day", grid=True
            ),
        ),
        y=alt.Y(
            "std_dev_price:Q",
            title="Standard deviation price",
        ),
        color=alt.Color("region:N", title="Region", legend=alt.Legend(title="Regions")),
        tooltip=[
            alt.Tooltip("date:T", title="Date (Day/Month/Year)", format="%d/%m/%Y"),
            alt.Tooltip("std_dev_price:Q", title="Standard deviation price", format=","),
            alt.Tooltip("region:N", title="Region")
        ]
    )
    .properties(
        title="Standard deviation price over time by region",
        height=800,
    )
    .configure_title(fontSize=20, anchor="middle", color="white")
)

st.altair_chart(avg_chart, use_container_width=True)
st.altair_chart(dist_chart, use_container_width=True)
st.altair_chart(count_chart, use_container_width=True)
st.altair_chart(std_dev_chart, use_container_width=True)

# Display filtered dataframe
st.markdown(
    "<h3 style='text-align: center;'>Real estate data</h3>",
    unsafe_allow_html=True,
)
st.dataframe(filtered_data, height=600, use_container_width=True)
