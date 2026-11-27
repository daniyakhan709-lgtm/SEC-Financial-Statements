import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

from theme import CSS


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SEC Financial Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# 2. HELPER FUNCTIONS
# =========================================================

def section_header(title, caption=""):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">{title}</div>
        <div class="section-caption">{caption}</div>
    </div>
    """, unsafe_allow_html=True)


def sub_header(title):
    st.markdown(f'<div class="sub-header">{title}</div>', unsafe_allow_html=True)


def metric_card(column, title, value):
    column.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)


def explainer(text):
    with st.expander("About this chart"):
        st.markdown(text)


# =========================================================
# 3. LOAD DATA
# =========================================================

DATA_PATH = Path(__file__).parent.parent / "Dataset" / "SEC_Data.csv"


@st.cache_data
def load_data(path):
    df = pd.read_csv(path, low_memory=False)

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["qtrs"] = pd.to_numeric(df["qtrs"], errors="coerce")

    # Dates are stored as numbers like 20250930
    for col in ["period", "ddate", "filed"]:
        df[col] = pd.to_datetime(df[col].astype(str), format="%Y%m%d", errors="coerce")

    for col in ["name", "form", "tag"]:
        df[col] = df[col].fillna("Unknown").astype(str)

    return df


if not DATA_PATH.exists():
    st.error("Dataset not found. Check Dataset/SEC_Data.csv.")
    st.stop()

df = load_data(DATA_PATH)


# =========================================================
# 4. HEADER
# =========================================================

st.markdown("""
<div class="page-header">
    <div class="page-title">SEC FINANCIAL ANALYTICS</div>
    <div class="page-subtitle">Exploring Financial Reporting Patterns Through Data</div>
    <div class="page-description">
        An interactive exploration of financial statement records
        published by the U.S. Securities and Exchange Commission.
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# =========================================================
# 5. SIDEBAR FILTERS
# =========================================================

companies = sorted(df["name"].unique())
forms = sorted(df["form"].unique())
periods = sorted(df["period"].dropna().dt.strftime("%Y-%m-%d").unique())
tags = sorted(df["tag"].unique())

# Filing type starts with all options selected
if "forms" not in st.session_state:
    st.session_state["forms"] = forms


def reset_filters():
    st.session_state["companies"] = []
    st.session_state["forms"] = forms
    st.session_state["periods"] = []
    st.session_state["tags"] = []


st.sidebar.markdown("# ⚙️ CONTROL CENTER")
st.sidebar.caption("Customize your financial data exploration.")

st.sidebar.button("🔄 Reset Filters", on_click=reset_filters, use_container_width=True)

st.sidebar.divider()

selected_companies = st.sidebar.multiselect(
    "🏢 Select Companies", companies, placeholder="All companies", key="companies"
)

selected_forms = st.sidebar.multiselect(
    "📑 Filing Type", forms, key="forms"
)

selected_periods = st.sidebar.multiselect(
    "📅 Reporting Period", periods, placeholder="All reporting periods", key="periods"
)

selected_tags = st.sidebar.multiselect(
    "📚 Accounting Concepts", tags, placeholder="All concepts", key="tags"
)

st.sidebar.divider()
st.sidebar.caption("SEC Financial Statements EDA | 2026")


# =========================================================
# 6. APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_companies:
    filtered_df = filtered_df[filtered_df["name"].isin(selected_companies)]

if selected_forms:
    filtered_df = filtered_df[filtered_df["form"].isin(selected_forms)]

if selected_periods:
    period_text = filtered_df["period"].dt.strftime("%Y-%m-%d")
    filtered_df = filtered_df[period_text.isin(selected_periods)]

if selected_tags:
    filtered_df = filtered_df[filtered_df["tag"].isin(selected_tags)]

if filtered_df.empty:
    st.warning("No records match your selected filters.")
    st.stop()


# =========================================================
# 7. DASHBOARD TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview & Filings",
    "📊 Values & Quarters",
    "🧮 Concepts & Companies",
    "🔍 Data Quality",
    "📋 Explore Records"
])


# =========================================================
# TAB 1: OVERVIEW & FILINGS
# =========================================================

with tab1:

    section_header(
        "🏠 OVERVIEW & FILINGS",
        "Key figures, filing types and reporting periods for the current selection"
    )

    col1, col2, col3, col4 = st.columns(4)

    metric_card(col1, "TOTAL RECORDS", f"{len(filtered_df):,}")
    metric_card(col2, "COMPANIES", f"{filtered_df['cik'].nunique():,}")
    metric_card(col3, "ACCOUNTING CONCEPTS", f"{filtered_df['tag'].nunique():,}")
    metric_card(col4, "MISSING VALUES", f"{filtered_df['value'].isna().sum():,}")

    st.divider()

    # Filing types (pie)
    sub_header("Distribution of Filing Types")

    form_counts = filtered_df["form"].value_counts().reset_index()
    form_counts.columns = ["Filing Type", "Records"]

    fig = px.pie(
        form_counts,
        names="Filing Type",
        values="Records",
        hole=0.55,
        title="Distribution of Filing Types",
        color_discrete_sequence=["#7955D9", "#2684D9"]
    )
    show_chart(fig)

    explainer("""
**What does it show?** The number of records from each SEC filing type.

- 10-Q represents quarterly reports.
- 10-K represents annual reports.
- Larger slices mean more records.

**Important:** Record counts are not the number of unique filings.
""")

    st.divider()

    # 10-K vs 10-Q (bar and table)
    sub_header("10-K vs 10-Q Filings")

    filing_comparison = pd.DataFrame({
        "Total Records": filtered_df.groupby("form").size(),
        "Unique Companies": filtered_df.groupby("form")["cik"].nunique()
    }).reset_index()

    fig = px.bar(
        filing_comparison,
        x="form",
        y="Total Records",
        color="form",
        text="Total Records",
        title="Financial Records by Filing Type",
        color_discrete_sequence=["#8055D9", "#2789E8"]
    )
    show_chart(fig)

    explainer("""
Compares the number of records from 10-K and 10-Q filings.
""")

    st.dataframe(filing_comparison, use_container_width=True, hide_index=True)

    st.divider()

    # Reporting periods
    sub_header("Financial Records by Reporting Period")

    period_counts = filtered_df["period"].value_counts().sort_index().reset_index()
    period_counts.columns = ["Period", "Records"]

    fig = px.line(
        period_counts,
        x="Period",
        y="Records",
        markers=True,
        title="Records Across Reporting Periods",
        color_discrete_sequence=["#448BEB"]
    )
    show_chart(fig)

    explainer("""
Shows the number of records in each reporting period. Peaks mean more records.

**Important:** The sample is heavily concentrated in September 2025. This comes from how the sample was built and limits comparisons across periods.
""")


# =========================================================
# TAB 2: VALUES & QUARTERS
# =========================================================

with tab2:

    section_header(
        "📊 VALUES & QUARTERS",
        "Distribution of financial values and reported quarters"
    )

    # Financial values
    sub_header("Distribution of Financial Values")

    values = filtered_df["value"].dropna()

    if len(values) > 0:
        value_chart = pd.DataFrame({"Log Magnitude": np.log10(np.abs(values) + 1)})

        fig = px.histogram(
            value_chart,
            x="Log Magnitude",
            nbins=50,
            title="Distribution of Financial Value Magnitudes",
            color_discrete_sequence=["#8061E8"]
        )
        show_chart(fig)

        explainer("""
**What does it show?** The size (absolute value) of reported financial values.

**Why a logarithmic scale?** Financial values vary hugely. The log scale lets small and large values be seen together.

**Important:** The chart ignores the sign, so it does not show positive or negative values.
""")
    else:
        st.info("No financial values available.")

    st.divider()

    # Quarters distribution
    sub_header("Reported Quarter Distribution")

    qtrs_data = filtered_df[["qtrs"]].dropna()

    fig = px.histogram(
        qtrs_data,
        x="qtrs",
        nbins=30,
        title="Distribution of Reported Quarters",
        labels={"qtrs": "Number of Quarters"},
        color_discrete_sequence=["#347FE0"]
    )
    show_chart(fig)

    explainer("""
**What does it show?** How many quarters each financial fact covers.

Higher bars mean more records with that duration.

`qtrs` is the duration of a reported fact, not how often a company files.
""")

    st.divider()

    # Quarters by filing type
    sub_header("Reported Quarters by Filing Type")

    fig = px.box(
        filtered_df,
        x="form",
        y="qtrs",
        color="form",
        title="Quarter Distribution Across Filing Types",
        color_discrete_sequence=["#8055D9", "#2686E8"]
    )
    show_chart(fig)

    explainer("""
**What does it show?** Quarter distributions for 10-K and 10-Q filings.

- The middle line is the median.
- The box is the interquartile range.
- Points beyond the whiskers are potential outliers.
""")


# =========================================================
# TAB 3: CONCEPTS & COMPANIES
# =========================================================

with tab3:

    section_header(
        "🧮 CONCEPTS & COMPANIES",
        "Most frequently reported accounting concepts and companies"
    )

    # Top concepts
    sub_header("Top Accounting Concepts")

    top_tags = filtered_df["tag"].value_counts().head(10).reset_index()
    top_tags.columns = ["Concept", "Records"]

    fig = px.bar(
        top_tags,
        x="Records",
        y="Concept",
        orientation="h",
        title="Top 10 Accounting Concepts",
        color="Records",
        color_continuous_scale=["#34236D", "#397FEA"]
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    show_chart(fig)

    explainer("""
**What does it show?** The ten most frequently reported accounting concepts.

Longer bars mean the concept appears in more records.

**Important:** A frequent concept does not mean a larger financial amount.
""")

    st.divider()

    # Top companies
    sub_header("Leading Companies by Record Count")

    top_companies = filtered_df["name"].value_counts().head(10).reset_index()
    top_companies.columns = ["Company", "Records"]

    fig = px.bar(
        top_companies,
        x="Records",
        y="Company",
        orientation="h",
        title="Top 10 Companies",
        color="Records",
        color_continuous_scale=["#34236D", "#398BEB"]
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    show_chart(fig)

    explainer("""
**What does it show?** Companies with the most financial records.

Record counts do not measure company size, profitability, or performance.
""")


# =========================================================
# TAB 4: DATA QUALITY
# =========================================================

with tab4:

    section_header(
        "🔍 DATA QUALITY",
        "Missing financial values and accounting concepts with incomplete records"
    )

    total_missing = filtered_df["value"].isna().sum()
    missing_percentage = total_missing / len(filtered_df) * 100

    col1, col2 = st.columns(2)
    col1.metric("Missing Financial Values", f"{total_missing:,}")
    col2.metric("Missing Percentage", f"{missing_percentage:.2f}%")

    st.divider()

      # Missing values by concept
    sub_header("Missing Values by Accounting Concept")

    missing_rows = filtered_df[filtered_df["value"].isna()]

    missing_by_tag = (
        missing_rows["tag"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    missing_by_tag.columns = ["Concept", "Missing Values"]

    short_names = {
        "NetIncomeLoss": "Net Income / Loss",
        "CommitmentsAndContingencies": "Commitments & Contingencies",
        "StockholdersEquity": "Stockholders' Equity",
        "AdjustmentsToAdditionalPaidInCapitalSharebasedCompensationRequisiteServicePeriodRecognitionValue": "APIC - Share-based Compensation",
        "ProfitLoss": "Profit / Loss",
        "StockIssuedDuringPeriodValueNewIssues": "Stock Issued - New Issues",
        "AdjustmentsToAdditionalPaidInCapitalShareBasedCompensationStockOptionsRequisiteServicePeriodRecognition": "APIC - Stock Options",
        "PreferredStockValue": "Preferred Stock Value",
        "StockIssuedDuringPeriodValueIssuedForServices": "Stock Issued for Services",
        "SharesOutstanding": "Shares Outstanding"
    }

    missing_by_tag["SEC Tag"] = missing_by_tag["Concept"]

    missing_by_tag["Short Concept"] = (
        missing_by_tag["SEC Tag"]
        .map(short_names)
        .fillna(missing_by_tag["SEC Tag"])
    )

    fig = px.bar(
        missing_by_tag,
        x="Missing Values",
        y="Short Concept",
        orientation="h",
        title="Top 10 Accounting Concepts with Missing Financial Values",
        color="Missing Values",
        color_continuous_scale=["#38216F", "#438BEB"],
        custom_data=["SEC Tag"]
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Missing Values: %{x:,}<br>"
            "SEC Tag: %{customdata[0]}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    show_chart(fig)

    explainer("""
    **What does it show?** Concepts with the most missing financial values.

    Missing values are not always errors. Some concepts do not apply to every company or filing.
    """)

    st.divider()

    # Missing values by column
    sub_header("Missing Values Across All Columns")

    missing_summary = filtered_df.isnull().sum().reset_index()
    missing_summary.columns = ["Column", "Missing Values"]
    missing_summary = missing_summary[missing_summary["Missing Values"] > 0]

    fig = px.bar(
        missing_summary,
        x="Column",
        y="Missing Values",
        title="Missing Values by Column",
        color="Missing Values",
        color_continuous_scale=["#38216F", "#438BEB"]
    )
    fig.update_layout(xaxis_tickangle=-35)
    show_chart(fig)

    explainer("""
Compares missing-value counts across all columns.

Read each count in light of what the column means.
""")


# =========================================================
# TAB 5: EXPLORE RECORDS
# =========================================================

with tab5:

    section_header(
        "📋 EXPLORE RECORDS",
        "Browse and download the filtered SEC dataset"
    )

    st.caption(f"Displaying {len(filtered_df):,} records.")

    if st.checkbox("Show filtered financial records"):

        st.dataframe(filtered_df, use_container_width=True, height=500)

        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Filtered Data",
            data=csv,
            file_name="SEC_filtered_data.csv",
            mime="text/csv"
        )


# =========================================================
# 8. FOOTER
# =========================================================

st.divider()

st.markdown("""
<div style="text-align:center; color:#9295BD;">
<b>SEC FINANCIAL STATEMENTS EDA</b><br>
Exploring financial reporting patterns through data.<br>
Built with Python, Pandas, Streamlit and Plotly.
</div>
""", unsafe_allow_html=True)