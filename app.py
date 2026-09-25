import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.datasets import fetch_openml

st.set_page_config(page_title="Credit Risk Dashboard", page_icon="💳", layout="wide")

BLUE = "#1f4fb2"
DARK = "#123a8c"

# ---------- Theme (CSS) ----------
st.markdown(f"""
<style>
.stApp {{ background-color: #eaf0fb; }}
[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {BLUE}, {DARK}); }}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] label p,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{ color: white !important; }}
.header {{ background: linear-gradient(90deg, {BLUE}, {DARK}); color: white;
  padding: 18px 25px; border-radius: 14px; font-size: 30px; font-weight: 700;
  margin-bottom: 18px; }}
.card {{ background: white; border-radius: 14px; padding: 16px;
  box-shadow: 0 4px 12px rgba(31,79,178,.25); border-left: 6px solid {BLUE}; }}
.card .label {{ color: #5b6b8c; font-size: 14px; }}
.card .value {{ color: {BLUE}; font-size: 30px; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
@st.cache_data
def load_data():
    df = fetch_openml(name="credit-g", version=1, as_frame=True).frame
    for col in df.select_dtypes(include="category").columns:
        df[col] = df[col].astype(str)
    return df

df = load_data()

# ---------- Sidebar: menu + filters ----------
st.sidebar.title("💳 Credit Risk")
page = st.sidebar.radio("Menu", ["Dashboard", "Summary", "Data"])
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

purpose = st.sidebar.multiselect("Purpose", sorted(df["purpose"].unique()))
housing = st.sidebar.multiselect("Housing", sorted(df["housing"].unique()))
job = st.sidebar.multiselect("Job", sorted(df["job"].unique()))
age = st.sidebar.slider("Age", int(df["age"].min()), int(df["age"].max()),
                        (int(df["age"].min()), int(df["age"].max())))

f = df[df["age"].between(*age)]
if purpose:
    f = f[f["purpose"].isin(purpose)]
if housing:
    f = f[f["housing"].isin(housing)]
if job:
    f = f[f["job"].isin(job)]

if f.empty:
    st.warning("No applicants match these filters. Try widening them.")
    st.stop()

# ---------- Header ----------
st.markdown('<div class="header">📊 Credit Risk Performance Dashboard</div>',
            unsafe_allow_html=True)

def kpi(col, icon, label, value):
    col.markdown(
        f'<div class="card"><div class="label">{icon} {label}</div>'
        f'<div class="value">{value}</div></div>', unsafe_allow_html=True)

# ---------- Dashboard page ----------
if page == "Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "👥", "Total Applicants", f"{len(f):,}")
    kpi(c2, "💰", "Total Credit Amount", f"{f['credit_amount'].sum()/1e6:.2f}M DM")
    kpi(c3, "📈", "Avg Credit Amount", f"{f['credit_amount'].mean():,.0f} DM")
    kpi(c4, "⚠️", "Default Rate", f"{(f['class'] == 'bad').mean():.1%}")

def style(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=DARK)),
        margin=dict(t=50, b=20, l=10, r=10),
        height=340,
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig


if page == "Dashboard":
    st.write("")

    # ---------- Row 1 ----------
    col_a, col_b = st.columns([3, 2])

    by_dur = f.groupby("duration")["credit_amount"].mean().reset_index()
    fig = px.line(by_dur, x="duration", y="credit_amount", markers=True,
                  color_discrete_sequence=[BLUE])
    fig.update_xaxes(title="Duration (months)")
    fig.update_yaxes(title="Avg credit (DM)")
    col_a.plotly_chart(style(fig, "Average Credit Amount by Duration"))

    ages = f.copy()
    age_labels = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
    ages["age_group"] = pd.cut(ages["age"], bins=[0, 25, 35, 45, 55, 65, 120],
                               labels=age_labels, right=False).astype(str)
    by_age = ages.groupby("age_group")["class"].apply(
        lambda s: (s == "bad").mean() * 100).reset_index(name="rate")
    fig = px.bar(by_age, x="age_group", y="rate", text_auto=".1f",
                 category_orders={"age_group": age_labels},
                 color_discrete_sequence=[BLUE])
    fig.update_xaxes(title="Age group")
    fig.update_yaxes(title="Default rate (%)")
    col_b.plotly_chart(style(fig, "Default Rate by Age Group"))

    # ---------- Row 2 ----------
    col_c, col_d, col_e = st.columns([3, 2, 3])

    by_purpose = (f.groupby("purpose")["credit_amount"].sum()
                  .sort_values(ascending=False).reset_index())
    fig = px.bar(by_purpose, x="purpose", y="credit_amount",
                 color_discrete_sequence=[BLUE])
    fig.update_xaxes(title="", tickangle=-45)
    fig.update_yaxes(title="Total credit (DM)")
    col_c.plotly_chart(style(fig, "Credit Amount by Purpose"))

    counts = f["class"].value_counts().reset_index()
    counts.columns = ["class", "count"]
    fig = px.pie(counts, names="class", values="count", hole=0.55,
                 color="class",
                 color_discrete_map={"good": BLUE, "bad": "#e76f51"})
    col_d.plotly_chart(style(fig, "Good vs Bad Credit"))

    top5 = f["purpose"].value_counts().head(5).reset_index()
    top5.columns = ["purpose", "applicants"]
    fig = px.bar(top5.sort_values("applicants"), x="applicants", y="purpose",
                 orientation="h", color_discrete_sequence=[BLUE])
    fig.update_yaxes(title="")
    fig.update_xaxes(title="Applicants")
    col_e.plotly_chart(style(fig, "Top 5 Purposes by Applicants"))

    # ---------- Summary page ----------
if page == "Summary":
    good = f[f["class"] == "good"]
    bad = f[f["class"] == "bad"]

    s1, s2, s3, s4 = st.columns(4)
    kpi(s1, "✅", "Good Credit", f"{len(good):,}")
    kpi(s2, "❌", "Bad Credit", f"{len(bad):,}")
    kpi(s3, "⏱️", "Avg Duration (Bad)", f"{bad['duration'].mean():.1f} mo")
    kpi(s4, "⏱️", "Avg Duration (Good)", f"{good['duration'].mean():.1f} mo")

    st.write("")
    st.subheader("Riskiest purposes (at least 20 applicants)")
    risk = (f.groupby("purpose")["class"]
              .agg(applicants="count", bad_rate=lambda s: (s == "bad").mean() * 100)
              .reset_index())
    risk = risk[risk["applicants"] >= 20].sort_values("bad_rate", ascending=False)

    if risk.empty:
        st.info("Not enough applicants for this comparison. Try widening the filters.")
    else:
        top = risk.iloc[0]
        st.success(f"Highest default rate: **{top['purpose']}** at "
                   f"**{top['bad_rate']:.1f}%** ({int(top['applicants'])} applicants).")
        fig = px.bar(risk, x="purpose", y="bad_rate", text_auto=".1f",
                     color_discrete_sequence=[BLUE])
        fig.update_xaxes(title="", tickangle=-45)
        fig.update_yaxes(title="Default rate (%)")
        st.plotly_chart(style(fig, "Default Rate by Purpose"))

    st.subheader("Good vs Bad: averages")
    avg = f.groupby("class")[["duration", "credit_amount", "age",
                              "installment_commitment"]].mean().round(1)
    st.dataframe(avg)

# ---------- Data page ----------
if page == "Data":
    st.subheader("Filtered data")
    st.dataframe(f, height=450)
    st.download_button("Download filtered data as CSV",
                       f.to_csv(index=False).encode("utf-8"),
                       file_name="german_credit_filtered.csv",
                       mime="text/csv")

   streamlit
   pandas
   scikit-learn
   plotly