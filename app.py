# ============================================================
# AI Powered Indian Wedding Cost Analytics Dashboard
# Netflix + Bloomberg + Power BI + Tableau Style
# Part 1
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="Indian Wedding Analytics",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

.stApp{
background-color:#050816;
color:white;
}

section[data-testid="stSidebar"]{
background:#111827;
}

h1,h2,h3,h4{
color:white;
}

.metric-card{
background:#111827;
padding:20px;
border-radius:20px;
box-shadow:0px 0px 20px cyan;
text-align:center;
}

</style>
""",unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown("""

<h1 style='text-align:center;
color:cyan;
font-size:45px;'>

💍 AI Powered Indian Wedding Cost Analytics

</h1>

<h4 style='text-align:center;color:white;'>

Netflix • Bloomberg • Power BI • Tableau

</h4>

""",unsafe_allow_html=True)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("Indian_Weddings_.csv")

    df.columns = (
        df.columns
        .str.replace("/","_",regex=False)
        .str.replace("(","",regex=False)
        .str.replace(")","",regex=False)
        .str.replace(" ","_",regex=False)
    )

    df = df.drop(columns=["Unnamed:_0"],errors="ignore")

    return df

df = load_data()

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title("🎛 Dashboard Filters")

wedding = st.sidebar.multiselect(

"Wedding Type",

sorted(df["Wedding_Type"].unique()),

default=sorted(df["Wedding_Type"].unique())

)

place = st.sidebar.multiselect(

"Place",

sorted(df["Place"].unique()),

default=sorted(df["Place"].unique())

)

df = df[
    (df["Wedding_Type"].isin(wedding))
    &
    (df["Place"].isin(place))
]

# ------------------------------------------------------------
# KPI VALUES
# ------------------------------------------------------------

total = len(df)

cost = df["Cost_of_Type"].sum()

average = df["Cost_of_Type"].mean()

maximum = df["Cost_of_Type"].max()

# ------------------------------------------------------------
# KPI CARDS
# ------------------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric("💍 Weddings",f"{total:,}")

c2.metric("💰 Total Cost",f"₹ {cost:,.0f}")

c3.metric("📊 Average",f"₹ {average:,.0f}")

c4.metric("🏆 Maximum",f"₹ {maximum:,.0f}")

st.markdown("---")

# ------------------------------------------------------------
# BAR CHART
# ------------------------------------------------------------

cost_df = df.groupby("Wedding_Type")["Cost_of_Type"].sum().reset_index()

fig = px.bar(

cost_df,

x="Wedding_Type",

y="Cost_of_Type",

color="Cost_of_Type",

text_auto=True,

color_continuous_scale="Turbo",

title="Wedding Cost by Type"

)

fig.update_layout(

paper_bgcolor="#050816",

plot_bgcolor="#050816",

font=dict(color="white"),

height=600

)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------------------
# DONUT CHART
# ------------------------------------------------------------

fig = px.pie(

df,

names="Wedding_Type",

hole=.65,

color="Wedding_Type",

color_discrete_sequence=px.colors.qualitative.Bold

)

fig.update_layout(

paper_bgcolor="#050816",

font=dict(color="white"),

height=600

)

st.plotly_chart(fig,use_container_width=True)

st.success("✅ Part 1 Completed")

# ==========================================================
# PART 2 - BUSINESS ANALYTICS
# ==========================================================

st.markdown("""
<h2 style='text-align:center;color:cyan'>
📊 Business Analytics Dashboard
</h2>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# ROW 1
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    tree = px.treemap(
        df,
        path=["Wedding_Type", "Decor_Category"],
        values="Cost_of_Type",
        color="Cost_of_Type",
        color_continuous_scale="Turbo",
        title="🌳 Wedding Cost Treemap"
    )

    tree.update_layout(
        paper_bgcolor="#050816",
        font=dict(color="white"),
        height=650
    )

    st.plotly_chart(tree, use_container_width=True)

with col2:

    sun = px.sunburst(
        df,
        path=["Wedding_Type", "Decor_Category"],
        values="Cost_of_Type",
        color="Cost_of_Type",
        color_continuous_scale="Rainbow",
        title="☀️ Sunburst Analytics"
    )

    sun.update_layout(
        paper_bgcolor="#050816",
        font=dict(color="white"),
        height=650
    )

    st.plotly_chart(sun, use_container_width=True)

# ----------------------------------------------------------
# ROW 2
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    place_cost = (
        df.groupby("Place")["Cost_of_Type"]
        .sum()
        .reset_index()
        .sort_values("Cost_of_Type", ascending=False)
    )

    fig = px.bar(
        place_cost,
        x="Place",
        y="Cost_of_Type",
        color="Cost_of_Type",
        text_auto=True,
        color_continuous_scale="Turbo",
        title="📍 Cost by Place"
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        font=dict(color="white"),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    bubble = px.scatter(
        df,
        x="Photography",
        y="Entertainment",
        size="Cost_of_Type",
        color="Wedding_Type",
        hover_name="Place",
        size_max=60,
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="📷 Photography vs Entertainment"
    )

    bubble.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        font=dict(color="white"),
        height=600
    )

    st.plotly_chart(bubble, use_container_width=True)

# ----------------------------------------------------------
# ROW 3
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    decor = (
        df.groupby("Decor_Category")["Cost_of_Type"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        decor,
        x="Decor_Category",
        y="Cost_of_Type",
        color="Cost_of_Type",
        text_auto=True,
        color_continuous_scale="Plasma",
        title="🎨 Average Decor Cost"
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        font=dict(color="white"),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    heat = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Turbo",
        title="📈 Correlation Heatmap"
    )

    heat.update_layout(
        paper_bgcolor="#050816",
        font=dict(color="white"),
        height=600
    )

    st.plotly_chart(heat, use_container_width=True)

# ----------------------------------------------------------
# DATA TABLE
# ----------------------------------------------------------

st.markdown("""
<h2 style='color:cyan'>
📋 Complete Dataset
</h2>
""", unsafe_allow_html=True)

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# ----------------------------------------------------------
# DOWNLOAD BUTTON
# ----------------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Dataset",
    csv,
    "Filtered_Wedding_Data.csv",
    "text/csv"
)

# ==========================================================
# PART 3 - ADVANCED 3D ANALYTICS
# ==========================================================

st.markdown("""
<h1 style='text-align:center;color:#00E5FF'>
🚀 3D Analytics Dashboard
</h1>
""", unsafe_allow_html=True)

# ==========================================================
# 3D Scatter
# ==========================================================

st.subheader("🌍 3D Wedding Cost Distribution")

fig = px.scatter_3d(

    df,

    x="Photography",

    y="Decor",

    z="Entertainment",

    color="Wedding_Type",

    size="Cost_of_Type",

    hover_name="Place",

    opacity=0.85,

    color_discrete_sequence=px.colors.qualitative.Bold

)

fig.update_layout(

paper_bgcolor="#050816",

scene=dict(

bgcolor="#050816",

xaxis=dict(color="white"),

yaxis=dict(color="white"),

zaxis=dict(color="white")

),

font=dict(color="white"),

height=750

)

st.plotly_chart(fig,use_container_width=True)

# ==========================================================
# 3D Bubble Chart
# ==========================================================

st.subheader("💎 Luxury Wedding Bubble Analytics")

bubble = go.Figure()

bubble.add_trace(

go.Scatter3d(

x=df["Photography"],

y=df["Decor"],

z=df["Entertainment"],

mode="markers",

text=df["Place"],

marker=dict(

size=(df["Cost_of_Type"]/df["Cost_of_Type"].max())*35+5,

color=df["Cost_of_Type"],

colorscale="Turbo",

opacity=0.90,

line=dict(color="white",width=1)

)

)

)

bubble.update_layout(

paper_bgcolor="#050816",

scene=dict(bgcolor="#050816"),

font=dict(color="white"),

height=750

)

st.plotly_chart(bubble,use_container_width=True)

# ==========================================================
# Surface Plot
# ==========================================================

st.subheader("🌊 Average Cost Surface")

surface = df.pivot_table(

index="Wedding_Type",

columns="Decor_Category",

values="Cost_of_Type",

aggfunc="mean",

fill_value=0

)

fig = go.Figure(

go.Surface(

z=surface.values,

colorscale="Turbo"

)

)

fig.update_layout(

paper_bgcolor="#050816",

scene=dict(

xaxis_title="Decor Category",

yaxis_title="Wedding Type",

zaxis_title="Average Cost"

),

font=dict(color="white"),

height=750

)

st.plotly_chart(fig,use_container_width=True)

# ==========================================================
# Parallel Coordinates
# ==========================================================

st.subheader("📊 Multi Variable Analysis")

parallel = px.parallel_coordinates(

df,

dimensions=[

"Photography",

"Decor",

"Entertainment",

"Clothes_Bride",

"Clothes_Groom",

"Cost_of_Type"

],

color="Cost_of_Type",

color_continuous_scale=px.colors.sequential.Turbo

)

parallel.update_layout(

paper_bgcolor="#050816",

font=dict(color="white"),

height=700

)

st.plotly_chart(parallel,use_container_width=True)

# ==========================================================
# Radar Chart
# ==========================================================

st.subheader("🎯 Expense Comparison")

avg = df[

["Photography",

"Decor",

"Entertainment",

"Clothes_Bride",

"Clothes_Groom"]

].mean()

radar = go.Figure()

radar.add_trace(

go.Scatterpolar(

r=avg.values,

theta=avg.index,

fill="toself",

line=dict(color="#00E5FF",width=4)

)

)

radar.update_layout(

paper_bgcolor="#050816",

polar=dict(

bgcolor="#050816",

radialaxis=dict(

visible=True,

color="white"

)

),

font=dict(color="white"),

height=700

)

st.plotly_chart(radar,use_container_width=True)

# ==========================================================
# Violin Plot
# ==========================================================

st.subheader("🎻 Cost Distribution")

violin = px.violin(

df,

x="Wedding_Type",

y="Cost_of_Type",

color="Wedding_Type",

box=True,

points="all",

color_discrete_sequence=px.colors.qualitative.Bold

)

violin.update_layout(

paper_bgcolor="#050816",

plot_bgcolor="#050816",

font=dict(color="white"),

height=700

)

st.plotly_chart(violin,use_container_width=True)

# ==========================================================
# 3D Summary
# ==========================================================

st.success("✅ Part 3 Completed Successfully")

st.info("""
Included in Part 3

✅ 3D Scatter

✅ 3D Bubble

✅ 3D Surface

✅ Parallel Coordinates

✅ Radar Chart

✅ Violin Plot
""")

# ==========================================================
# PART 4 - AI & MACHINE LEARNING
# ==========================================================

st.markdown("""
<h1 style='text-align:center;color:#00E5FF'>
🤖 AI Prediction Dashboard
</h1>
""", unsafe_allow_html=True)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

# ----------------------------------------------------------
# Prepare Data
# ----------------------------------------------------------

ml_df = df.copy()

# Encode categorical columns
encoders = {}
for col in ml_df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    ml_df[col] = le.fit_transform(ml_df[col].astype(str))
    encoders[col] = le

X = ml_df.drop("Cost_of_Type", axis=1)
y = ml_df["Cost_of_Type"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42
)

# ----------------------------------------------------------
# Train Random Forest
# ----------------------------------------------------------

rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

rf_r2 = r2_score(y_test, rf_pred)
rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

# ----------------------------------------------------------
# Optional XGBoost
# ----------------------------------------------------------

xgb_available = False

try:
    import xgboost as xgb

    xgb_model = xgb.XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        random_state=42
    )

    xgb_model.fit(X_train, y_train)

    xgb_pred = xgb_model.predict(X_test)

    xgb_r2 = r2_score(y_test, xgb_pred)

    xgb_available = True

except Exception:
    xgb_r2 = None

# ----------------------------------------------------------
# KPI Metrics
# ----------------------------------------------------------

st.subheader("📊 Model Performance")

c1, c2, c3 = st.columns(3)

c1.metric("🌲 RF R²", f"{rf_r2:.3f}")
c2.metric("📉 MAE", f"{rf_mae:,.2f}")
c3.metric("📈 RMSE", f"{rf_rmse:,.2f}")

if xgb_available:
    st.success(f"🚀 XGBoost R² : {xgb_r2:.3f}")
else:
    st.warning("XGBoost not installed. Showing Random Forest only.")

# ----------------------------------------------------------
# Feature Importance
# ----------------------------------------------------------

importance = (
    pd.DataFrame({
        "Feature": X.columns,
        "Importance": rf.feature_importances_
    })
    .sort_values("Importance", ascending=False)
)

fig = px.bar(
    importance,
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    color_continuous_scale="Turbo",
    title="🔥 Feature Importance"
)

fig.update_layout(
    paper_bgcolor="#050816",
    plot_bgcolor="#050816",
    font=dict(color="white"),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Actual vs Predicted
# ----------------------------------------------------------

comparison = pd.DataFrame({
    "Actual": y_test,
    "Predicted": rf_pred
})

fig = px.scatter(
    comparison,
    x="Actual",
    y="Predicted",
    color="Predicted",
    opacity=0.8,
    color_continuous_scale="Turbo",
    title="🎯 Actual vs Predicted"
)

fig.update_layout(
    paper_bgcolor="#050816",
    plot_bgcolor="#050816",
    font=dict(color="white"),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Prediction Form
# ----------------------------------------------------------

st.subheader("💰 Predict Wedding Cost")

input_data = {}

for col in X.columns:

    if col in encoders:

        options = list(encoders[col].classes_)

        selected = st.selectbox(col.replace("_", " "), options)

        input_data[col] = encoders[col].transform([selected])[0]

    else:

        input_data[col] = st.number_input(
            col.replace("_", " "),
            value=float(df[col].mean())
        )

if st.button("🔮 Predict Cost"):

    input_df = pd.DataFrame([input_data])

    prediction = rf.predict(input_df)[0]

    st.success(f"💰 Estimated Wedding Cost: ₹ {prediction:,.2f}")

# ----------------------------------------------------------
# Download Feature Importance
# ----------------------------------------------------------

csv = importance.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Feature Importance",
    csv,
    "feature_importance.csv",
    "text/csv"
)

st.success("✅ Part 4 Completed Successfully")


# ==========================================================
# PART 5 - EXECUTIVE DASHBOARD
# ==========================================================

import io

st.markdown("""
<div style="
background:linear-gradient(90deg,#0F172A,#1E3A8A,#0EA5E9);
padding:25px;
border-radius:20px;
box-shadow:0px 0px 25px cyan;
">

<h1 style="text-align:center;color:white;">
🚀 Executive Analytics Dashboard
</h1>

<h4 style="text-align:center;color:white;">
Netflix • Bloomberg • Microsoft Power BI • Tableau Enterprise
</h4>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# Executive KPI Cards
# ==========================================================

total_weddings = len(df)
total_cost = df["Cost_of_Type"].sum()
avg_cost = df["Cost_of_Type"].mean()
max_cost = df["Cost_of_Type"].max()

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("💍 Weddings", f"{total_weddings:,}")

with c2:
    st.metric("💰 Total Cost", f"₹ {total_cost:,.0f}")

with c3:
    st.metric("📈 Average Cost", f"₹ {avg_cost:,.0f}")

with c4:
    st.metric("🏆 Highest Cost", f"₹ {max_cost:,.0f}")

st.markdown("---")

# ==========================================================
# Summary Table
# ==========================================================

summary = (
    df.groupby("Wedding_Type")["Cost_of_Type"]
      .agg(["count","sum","mean","max","min"])
      .reset_index()
)

summary.columns = [
    "Wedding Type",
    "Total Weddings",
    "Total Cost",
    "Average Cost",
    "Maximum Cost",
    "Minimum Cost"
]

st.subheader("📊 Executive Summary")

st.dataframe(
    summary,
    use_container_width=True,
    height=300
)

# ==========================================================
# Business Insights
# ==========================================================

st.subheader("💡 AI Business Insights")

highest = summary.loc[
    summary["Total Cost"].idxmax(),
    "Wedding Type"
]

lowest = summary.loc[
    summary["Total Cost"].idxmin(),
    "Wedding Type"
]

best_model = "Random Forest"

if "xgb_r2" in locals():
    if xgb_available and xgb_r2 > rf_r2:
        best_model = "XGBoost"

st.success(f"""
🏆 Highest Revenue Wedding Type : **{highest}**

📉 Lowest Revenue Wedding Type : **{lowest}**

🤖 Recommended Prediction Model : **{best_model}**

📈 Average Wedding Cost : ₹ {avg_cost:,.0f}

💰 Total Revenue : ₹ {total_cost:,.0f}
""")

# ==========================================================
# AI Performance Chart
# ==========================================================

import plotly.graph_objects as go

models = ["Random Forest"]
scores = [rf_r2]

if "xgb_r2" in locals() and xgb_available:
    models.append("XGBoost")
    scores.append(xgb_r2)

fig = go.Figure()

fig.add_trace(

go.Bar(

x=models,

y=scores,

text=[round(x,3) for x in scores],

textposition="outside",

marker_color=["cyan","orange"][:len(models)]

)

)

fig.update_layout(

paper_bgcolor="#050816",

plot_bgcolor="#050816",

font=dict(color="white"),

title="🤖 AI Model Comparison",

height=500

)

st.plotly_chart(fig,use_container_width=True)

# ==========================================================
# Download Report
# ==========================================================

st.subheader("📥 Download Executive Report")

buffer = io.StringIO()

summary.to_csv(buffer,index=False)

st.download_button(

label="⬇ Download Summary CSV",

data=buffer.getvalue(),

file_name="Executive_Report.csv",

mime="text/csv"

)

# ==========================================================
# About Project
# ==========================================================

st.markdown("---")

st.subheader("ℹ About This Project")

st.info("""

💍 Indian Wedding Cost Analytics

Features Included

✅ Executive Dashboard

✅ Interactive Analytics

✅ 3D Visualizations

✅ Machine Learning

✅ AI Prediction

✅ Feature Importance

✅ Business Insights

✅ Professional Streamlit Dashboard

Technology Stack

• Python

• Streamlit

• Plotly

• Scikit-Learn

• XGBoost

• Pandas

""")

# ==========================================================
# Footer
# ==========================================================

st.markdown("""

<hr>

<center>

<h3 style="color:cyan;">

🚀 AI Powered Indian Wedding Cost Analytics

</h3>

<h5 style="color:white;">

Developed using Python • Streamlit • Plotly • Machine Learning

</h5>

</center>

""",unsafe_allow_html=True)