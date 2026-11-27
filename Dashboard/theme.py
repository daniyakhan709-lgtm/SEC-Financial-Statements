# =========================================================
# THEME: all the dashboard styling lives here
# =========================================================

CSS = """
<style>

.stApp {
    background: linear-gradient(135deg, #080817, #10112B, #101D38);
    color: #E8EAF6;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17132F, #101C35);
    border-right: 1px solid #34305D;
}

h1, h2, h3 {
    color: #E6E4FF;
}

p, label, span {
    color: #D0D4E8;
}

/* ---------- Page header ---------- */

.page-header {
    padding: 28px 32px;
    border-radius: 16px;
    background: linear-gradient(135deg, #211C45, #142B4B);
    border: 1px solid #514A83;
    border-left: 8px solid #7955D9;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
    margin-bottom: 10px;
}

.page-title {
    color: #FFFFFF;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0;
}

.page-subtitle {
    color: #B9A9F5;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 6px;
}

.page-description {
    color: #A9A7D8;
    font-size: 15px;
    margin-top: 10px;
}

/* ---------- Section headers ---------- */

.section-header {
    margin: 28px 0 14px 0;
    padding: 10px 0 10px 16px;
    border-left: 6px solid #397FEA;
    background: linear-gradient(90deg, rgba(57, 127, 234, 0.12), rgba(0, 0, 0, 0));
}

.section-title {
    color: #FFFFFF;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin: 0;
}

.section-caption {
    color: #A9A7D8;
    font-size: 14px;
    margin-top: 4px;
}

.sub-header {
    color: #E6E4FF;
    font-size: 20px;
    font-weight: 700;
    margin: 22px 0 8px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #42436F;
}

/* ---------- Cards ---------- */

.metric-card {
    background: linear-gradient(135deg, #211C45, #142B4B);
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #514A83;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
}

.metric-title {
    color: #A9A7D8;
    font-size: 14px;
    letter-spacing: 1px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: bold;
}

div[data-testid="stExpander"] {
    background: rgba(30, 32, 69, 0.65);
    border: 1px solid #42436F;
    border-radius: 12px;
}

/* ---------- Tabs ---------- */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1B2041;
    border-radius: 8px;
    color: white;
}

.stTabs [aria-selected="true"] {
    background-color: #51418A;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #7955D9 !important;
}

/* ---------- Replace the red / pink color ---------- */

/* Selected items inside the filters */
span[data-baseweb="tag"] {
    background-color: #51418A !important;
}

span[data-baseweb="tag"] span {
    color: #FFFFFF !important;
}

/* Filter box border when clicked */
[data-baseweb="select"] > div:focus-within {
    border-color: #7955D9 !important;
}

/* Checkbox */
label[data-baseweb="checkbox"] > span:first-child {
    background-color: #7955D9 !important;
    border-color: #7955D9 !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    background-color: #211C45;
    border: 1px solid #514A83;
    color: #FFFFFF;
}

.stButton button:hover,
.stDownloadButton button:hover {
    border-color: #7955D9;
    color: #B9A9F5;
}

</style>
"""