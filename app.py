import csv
import html
import io
import re
from datetime import date

import streamlit as st


st.set_page_config(
    page_title="VisaFit AI",
    page_icon="💼",
    layout="wide",
)


# -----------------------------
# Styling
# -----------------------------

st.markdown(
    """
    <style>
    :root {
        --vf-bg: #f6f8fb;
        --vf-card: #ffffff;
        --vf-border: #dbe4ee;
        --vf-text: #0f172a;
        --vf-muted: #64748b;
        --vf-blue: #1d4ed8;
        --vf-blue-soft: #eff6ff;
        --vf-green: #059669;
        --vf-green-soft: #ecfdf5;
        --vf-amber: #d97706;
        --vf-orange: #ea580c;
        --vf-red: #dc2626;
        --vf-shadow: 0 12px 32px rgba(15, 23, 42, 0.06);
        --vf-shadow-soft: 0 6px 18px rgba(15, 23, 42, 0.045);
    }
    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.055), transparent 26rem),
            linear-gradient(180deg, #fbfdff 0%, var(--vf-bg) 48%, #f8fafc 100%);
        color: var(--vf-text);
    }
    .block-container {
        padding-top: 0.95rem;
        padding-bottom: 2.4rem;
        max-width: 1120px;
    }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e7edf5;
        box-shadow: inset -1px 0 0 rgba(148, 163, 184, 0.08);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #64748b;
        line-height: 1.45;
        font-size: 0.9rem;
    }
    [data-testid="stSidebar"] h1 {
        color: #1e293b;
        font-size: 1.28rem;
        letter-spacing: 0;
    }
    [data-testid="stSidebar"] h3 {
        color: #475569;
        font-size: 0.78rem;
        margin-top: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        border-radius: 8px;
        border: 1px solid #fde68a;
        background: #fffbeb;
    }
    [data-testid="stSidebar"] details {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.035);
        margin-bottom: 0.55rem;
    }
    [data-testid="stSidebar"] details summary p {
        color: #1e293b;
        font-weight: 750;
        font-size: 0.9rem;
    }
    [data-testid="stSidebar"] details [data-testid="stMarkdownContainer"] {
        color: #475569;
        font-size: 0.88rem;
    }
    .sidebar-card {
        border: 1px solid #e1e9f3;
        border-radius: 8px;
        background: #ffffff;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.055);
        padding: 0.95rem 1rem;
        margin-bottom: 0.85rem;
    }
    .sidebar-brand-card {
        background:
            linear-gradient(135deg, rgba(239, 246, 255, 0.98), rgba(255, 255, 255, 0.98)),
            #ffffff;
        border-color: #d7e5f6;
    }
    .sidebar-kicker {
        color: #1d4ed8;
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .sidebar-title {
        color: #0f172a;
        font-size: 1.22rem;
        font-weight: 850;
        line-height: 1.12;
        margin-bottom: 0.18rem;
    }
    .sidebar-subtitle {
        color: #334155;
        font-size: 0.88rem;
        font-weight: 750;
        margin-bottom: 0.45rem;
    }
    .sidebar-copy {
        color: #64748b;
        font-size: 0.84rem;
        line-height: 1.42;
        margin: 0;
    }
    .sidebar-section-title {
        color: #475569;
        font-size: 0.7rem;
        font-weight: 850;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 1rem 0 0.48rem 0;
    }
    .sidebar-workflow {
        display: grid;
        gap: 0.42rem;
        margin-bottom: 0.9rem;
    }
    .sidebar-step {
        display: grid;
        grid-template-columns: 1.45rem 1fr;
        align-items: center;
        gap: 0.52rem;
        color: #334155;
        font-size: 0.86rem;
        line-height: 1.28;
    }
    .sidebar-step-number {
        width: 1.45rem;
        height: 1.45rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        font-size: 0.78rem;
        font-weight: 850;
    }
    .sidebar-legend {
        display: grid;
        gap: 0.44rem;
        margin-bottom: 0.9rem;
    }
    .sidebar-pill {
        display: inline-flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
        border-radius: 999px;
        border: 1px solid var(--legend-border, #e2e8f0);
        background: var(--legend-bg, #f8fafc);
        color: var(--legend-color, #334155);
        font-size: 0.8rem;
        font-weight: 750;
        line-height: 1.15;
        padding: 0.42rem 0.62rem;
    }
    .legend-green {
        --legend-bg: #ecfdf5;
        --legend-border: #bbf7d0;
        --legend-color: #166534;
    }
    .legend-blue {
        --legend-bg: #eff6ff;
        --legend-border: #bfdbfe;
        --legend-color: #1d4ed8;
    }
    .legend-amber {
        --legend-bg: #fffbeb;
        --legend-border: #fde68a;
        --legend-color: #92400e;
    }
    .legend-yellow {
        --legend-bg: #fefce8;
        --legend-border: #fde047;
        --legend-color: #854d0e;
    }
    .legend-gray {
        --legend-bg: #f8fafc;
        --legend-border: #cbd5e1;
        --legend-color: #475569;
    }
    .legend-red {
        --legend-bg: #fef2f2;
        --legend-border: #fecaca;
        --legend-color: #991b1b;
    }
    .sidebar-disclaimer {
        border-top: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        color: #64748b;
        font-size: 0.78rem;
        line-height: 1.35;
        padding: 0.65rem 0;
        margin: 0.85rem 0;
    }
    .sidebar-link {
        display: block;
        border: 1px solid #cbd8e7;
        border-radius: 8px;
        background: #ffffff;
        color: #1d4ed8 !important;
        font-size: 0.84rem;
        font-weight: 800;
        line-height: 1.2;
        text-align: center;
        text-decoration: none !important;
        padding: 0.62rem 0.7rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.035);
    }
    .sidebar-link:hover {
        border-color: #93b4d9;
        background: #f8fbff;
    }
    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid #d9e5f3;
        border-radius: 8px;
        padding: 1.25rem 1.35rem;
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(239, 246, 255, 0.92)),
            #ffffff;
        box-shadow: var(--vf-shadow-soft);
        margin-bottom: 0.8rem;
    }
    .hero:after {
        content: "";
        position: absolute;
        right: -4rem;
        top: -5.5rem;
        width: 16rem;
        height: 16rem;
        border-radius: 999px;
        background: rgba(5, 150, 105, 0.08);
    }
    .eyebrow {
        color: var(--vf-blue);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: 0 0 0.25rem 0;
        color: #102033;
        font-size: 2.08rem;
        line-height: 1.15;
        letter-spacing: 0;
        position: relative;
        z-index: 1;
    }
    .hero p {
        margin: 0;
        color: #526173;
        font-size: 0.98rem;
        max-width: 720px;
        position: relative;
        z-index: 1;
    }
    .hero-stats {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.85rem;
        position: relative;
        z-index: 1;
    }
    .hero-chip {
        border: 1px solid #cfe0f5;
        border-radius: 999px;
        padding: 0.34rem 0.68rem;
        background: #ffffff;
        color: #315172;
        font-size: 0.8rem;
        font-weight: 650;
    }
    .top-action-row {
        display: flex;
        align-items: center;
        min-height: 2.55rem;
    }
    .section-card {
        border: 1px solid var(--vf-border);
        border-radius: 8px;
        padding: 1rem 1.05rem;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: var(--vf-shadow-soft);
        margin-bottom: 1rem;
    }
    .result-card {
        border: 1px solid var(--vf-border);
        border-radius: 8px;
        padding: 1rem 1rem 0.95rem 1rem;
        min-height: 152px;
        background: #ffffff;
        box-shadow: var(--vf-shadow-soft);
        border-top: 4px solid var(--card-accent, var(--vf-blue));
    }
    .result-label {
        color: var(--vf-muted);
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.4rem;
    }
    .result-value {
        color: var(--vf-text);
        font-size: 1.48rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.45rem;
    }
    .result-note {
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.35;
    }
    .tone-fit { --card-accent: #0ea5e9; }
    .tone-support { --card-accent: var(--vf-green); }
    .tone-friendly { --card-accent: #eab308; }
    .tone-unclear { --card-accent: #94a3b8; }
    .tone-no { --card-accent: var(--vf-red); }
    .tone-apply { --card-accent: var(--vf-green); }
    .tone-apply-network { --card-accent: var(--vf-blue); }
    .tone-network { --card-accent: var(--vf-amber); }
    .tone-skip { --card-accent: var(--vf-red); }
    .tone-role { --card-accent: var(--vf-blue); }
    .tone-match { --pill-bg: #ecfdf5; --pill-border: #bbf7d0; --pill-color: #166534; }
    .tone-gap { --pill-bg: #fff7ed; --pill-border: #fed7aa; --pill-color: #9a3412; }
    .tone-risk { --pill-bg: #eff6ff; --pill-border: #bfdbfe; --pill-color: #1d4ed8; }
    .pill {
        display: inline-block;
        border-radius: 999px;
        padding: 0.34rem 0.7rem;
        background: var(--pill-bg, #f1f5f9);
        color: var(--pill-color, #334155);
        font-size: 0.84rem;
        font-weight: 650;
        border: 1px solid var(--pill-border, var(--vf-border));
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.4rem 0 0.9rem 0;
    }
    .small-muted {
        color: var(--vf-muted);
        font-size: 0.9rem;
        line-height: 1.45;
    }
    .caption {
        color: var(--vf-muted);
        font-size: 0.86rem;
        line-height: 1.4;
        margin: -0.2rem 0 0.85rem 0;
    }
    .action-card {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
        border: 1px solid var(--vf-border);
        border-radius: 8px;
        padding: 0.85rem 0.9rem;
        background: #ffffff;
        margin-bottom: 0.65rem;
        box-shadow: var(--vf-shadow-soft);
    }
    .action-number {
        width: 1.75rem;
        height: 1.75rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #eff6ff;
        color: #1d4ed8;
        font-weight: 800;
        flex: 0 0 auto;
    }
    .signal-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        border-bottom: 1px solid #eef2f7;
        padding: 0.5rem 0;
        color: #334155;
    }
    .signal-score {
        color: #0f172a;
        font-weight: 800;
    }
    div[data-testid="stTabs"] button p {
        font-weight: 750;
        color: #334155;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid #e5edf6;
    }
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding-top: 0.65rem;
        padding-bottom: 0.65rem;
    }
    div[data-testid="column"] {
        min-width: 0;
    }
    div[data-testid="stTextArea"] {
        padding: 0.95rem 1rem 0.85rem 1rem;
        border: 1px solid var(--vf-border);
        border-radius: 8px;
        background: #ffffff;
        box-shadow: var(--vf-shadow-soft);
    }
    div[data-testid="stTextArea"] label p {
        color: #1e293b;
        font-size: 0.92rem;
        font-weight: 800;
    }
    div[data-testid="stTextArea"] textarea {
        border-radius: 8px;
        border-color: #d6e0eb;
        background: #fbfdff;
        box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.025);
        font-size: 0.92rem;
        line-height: 1.48;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.18);
    }
    div[data-testid="stButton"] button {
        border-radius: 8px;
        font-weight: 750;
        min-height: 2.55rem;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8, #047857);
        border: 1px solid rgba(29, 78, 216, 0.85);
        color: #ffffff !important;
        box-shadow: 0 8px 18px rgba(29, 78, 216, 0.16);
    }
    div[data-testid="stButton"] button[kind="primary"] p {
        color: #ffffff !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1e40af, #03685f);
        border-color: #1e40af;
        color: #ffffff !important;
        box-shadow: 0 10px 22px rgba(30, 64, 175, 0.22);
    }
    div[data-testid="stButton"] button[kind="primary"]:hover p {
        color: #ffffff !important;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        border-color: #cbd8e7;
        color: #1e3a5f;
        background: #ffffff;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        border-color: #93b4d9;
        color: #1d4ed8;
        background: #f8fbff;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
    }
    .stCaption {
        color: var(--vf-muted);
    }
    hr {
        margin: 1.05rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Reference Data
# -----------------------------

DEFAULT_PROFILE = """
International MBA candidate at William & Mary concentrating in Finance and Business Analytics.
Experience in strategic finance, business analytics, growth strategy, valuation, financial modeling,
market research, executive communication, SQL, Python, Excel, Tableau, Power BI, FP&A, and strategy.
Target roles include investment banking, corporate development, corporate strategy, strategic finance,
FP&A, business analytics, consulting, and business operations. Requires work authorization support as
an international student.
"""

SAMPLE_JOB = """
Strategic Finance Analyst

We are seeking a Strategic Finance Analyst to support forecasting, budgeting, dashboard reporting,
variance analysis, and executive presentations for a high-growth technology business. This role partners
closely with product, sales, operations, and corporate strategy teams to translate business performance
into clear recommendations.

Responsibilities:
- Build financial models for new market and product investments.
- Create Tableau dashboards and recurring KPI reporting.
- Use SQL and Excel to analyze revenue, margin, and customer trends.
- Prepare presentations for senior leadership.
- Support annual planning, monthly forecasting, and cross-functional decision making.

Qualifications:
- MBA or relevant finance, analytics, or strategy experience.
- Strong financial modeling, Excel, SQL, and presentation skills.
- Experience with Tableau, Power BI, or similar BI tools.
- Clear communication and stakeholder management skills.

Work authorization:
Candidates requiring current or future work authorization support are welcome to apply. The company has
experience supporting OPT, CPT, and H-1B sponsorship for selected roles.
"""

ROLE_CATEGORIES = {
    "Investment Banking": [
        "investment banking analyst",
        "investment banking associate",
        "investment banker",
        "investment banking team",
        "pitchbook",
        "cim",
        "confidential information memorandum",
        "deal execution",
        "transaction execution",
        "sell-side advisory",
        "buy-side advisory",
        "capital raising",
        "debt advisory",
        "equity capital markets",
        "leveraged finance",
        "fairness opinion",
        "client transactions",
        "live deal",
    ],
    "Corporate Development": [
        "corporate development",
        "corporate development team",
        "corp dev",
        "deal lifecycle",
        "mergers and acquisitions",
        "m&a transactions",
        "inorganic growth",
        "joint ventures",
        "minority investments",
        "strategic investments",
        "corporate venture",
        "transaction processes",
        "divestitures",
        "due diligence",
        "valuation and negotiation",
        "merger consequences analysis",
        "accretion and dilution",
        "lbo",
        "dcf",
        "trading comparables",
        "precedent transactions",
        "venture investments",
        "integration planning",
    ],
    "Strategic Finance / FP&A": [
        "fp&a",
        "strategic finance",
        "financial planning",
        "forecasting",
        "budgeting",
        "variance analysis",
        "financial modeling",
        "scenario analysis",
        "scenario testing",
        "performance reporting",
        "pricing",
        "pricing analysis",
        "unit economics",
        "cohort analysis",
        "product analytics",
        "long-range planning",
        "bottom-up forecasting",
        "business case modeling",
        "cash flow forecasting",
        "financial model automation",
        "kpi reporting",
        "finance leadership",
        "financial performance management",
        "annual planning",
    ],
    "Corporate Strategy": [
        "corporate strategy",
        "strategy analyst",
        "strategic planning",
        "annual strategic planning",
        "enterprise risk management",
        "competitive intelligence",
        "business continuity planning",
        "executive team",
        "ceo",
        "cfo",
        "excom",
        "board of directors",
        "5-year strategic plan",
        "5 year strategic plan",
        "capex plan",
        "capex planning",
        "market landscape",
        "strategic questions",
        "long-term strategy",
    ],
    "Private Equity": [
        "private equity",
        "pe associate",
        "investment associate",
        "portfolio company",
        "buyout",
        "lbo",
        "investment committee",
        "fund",
        "portfolio monitoring",
        "deal sourcing",
        "investment thesis",
        "transaction diligence",
        "value creation plan",
    ],
    "Venture Capital": [
        "venture capital",
        "vc analyst",
        "vc associate",
        "startup investing",
        "seed",
        "series a",
        "early-stage",
        "sourcing startups",
        "investment memo",
        "founder meetings",
        "portfolio support",
        "market mapping",
        "thesis-driven investing",
        "venture fund",
    ],
    "Business Analyst / General Analyst": [
        "business analyst",
        "analyst",
        "sql",
        "tableau",
        "power bi",
        "dashboard",
        "dashboarding",
        "reporting",
        "data analysis",
        "requirements gathering",
        "process improvement",
        "stakeholder requirements",
        "business intelligence",
        "operational analysis",
    ],
    "Consulting / Transformation": [
        "consulting",
        "transformation",
        "process improvement",
        "change management",
        "operating model",
    ],
    "Business Operations": [
        "business operations",
        "strategy and operations",
        "cross-functional",
        "operational efficiency",
        "go-to-market",
    ],
}

INVESTMENT_BANKING_ANCHOR_TERMS = [
    "investment banking analyst",
    "investment banking analysts",
    "investment banking associate",
    "investment banking associates",
    "investment banker",
    "investment banking team",
    "ib analyst",
    "ib analysts",
    "ib associate",
    "ib associates",
    "deal execution",
    "transaction execution",
    "sell-side advisory",
    "buy-side advisory",
    "capital raising",
    "debt advisory",
    "equity capital markets",
    "leveraged finance",
    "pitchbook",
    "cim",
    "confidential information memorandum",
    "fairness opinion",
    "client transactions",
    "live deal",
]

CORPORATE_DEVELOPMENT_ANCHOR_TERMS = [
    "corporate development",
    "corporate development team",
    "corp dev",
    "deal lifecycle",
    "mergers and acquisitions",
    "m&a transactions",
    "inorganic growth",
    "joint ventures",
    "minority investments",
    "strategic investments",
    "corporate venture",
    "venture investments",
    "transaction processes",
    "divestitures",
    "due diligence",
    "valuation and negotiation",
    "merger consequences analysis",
    "accretion and dilution",
    "lbo",
    "dcf",
    "trading comparables",
    "precedent transactions",
]

CORPORATE_STRATEGY_ANCHOR_TERMS = [
    "corporate strategy",
    "strategy analyst",
    "strategic planning",
    "annual strategic planning",
    "enterprise risk management",
    "competitive intelligence",
    "business continuity planning",
    "executive team",
    "ceo",
    "cfo",
    "excom",
    "board of directors",
    "5-year strategic plan",
    "5 year strategic plan",
    "capex plan",
    "capex planning",
    "market landscape",
    "strategic questions",
    "long-term strategy",
]

TRANSFERABLE_DEAL_FINANCE_TERMS = [
    "banking",
    "m&a",
    "mergers",
    "acquisitions",
    "financial modeling",
    "npv",
    "irr",
    "valuation",
    "payback",
]

CORPORATE_DEVELOPMENT_DEAL_TERMS = [
    "m&a",
    "mergers",
    "acquisitions",
    "mergers and acquisitions",
    "m&a transactions",
    "deal lifecycle",
    "inorganic growth",
    "joint ventures",
    "minority investments",
    "strategic investments",
    "transaction processes",
    "divestitures",
    "due diligence",
    "valuation and negotiation",
    "merger consequences analysis",
    "accretion and dilution",
    "lbo",
    "dcf",
    "trading comparables",
    "precedent transactions",
    "venture investments",
]

FINANCE_INTENT_TERMS = [
    "strategic finance",
    "fp&a",
    "financial planning",
    "forecasting",
    "budgeting",
    "variance analysis",
    "financial modeling",
    "scenario analysis",
    "scenario testing",
    "performance reporting",
    "pricing analysis",
    "unit economics",
    "finance leadership",
    "financial performance management",
    "annual planning",
    "monthly forecasting",
    "revenue",
    "margin",
]

ANALYTICS_TOOL_TERMS = [
    "sql",
    "tableau",
    "power bi",
    "dashboard",
    "dashboards",
    "kpi",
    "reporting",
]

PRIVATE_EQUITY_ANCHOR_TERMS = [
    "private equity",
    "pe associate",
    "investment associate",
    "portfolio company",
    "buyout",
    "lbo",
    "investment committee",
    "portfolio monitoring",
    "deal sourcing",
    "investment thesis",
    "transaction diligence",
    "value creation plan",
]

VENTURE_CAPITAL_ANCHOR_TERMS = [
    "venture capital",
    "vc analyst",
    "vc associate",
    "startup investing",
    "seed",
    "series a",
    "early-stage",
    "sourcing startups",
    "investment memo",
    "founder meetings",
    "portfolio support",
    "market mapping",
    "thesis-driven investing",
    "venture fund",
]

BUSINESS_ANALYST_ANCHOR_TERMS = [
    "business analyst",
    "analyst",
    "data analysis",
    "reporting",
    "dashboarding",
    "requirements gathering",
    "process improvement",
    "stakeholder requirements",
    "business intelligence",
    "operational analysis",
    "sql",
    "tableau",
    "power bi",
]

TRACKED_KEYWORDS = [
    "strategic finance",
    "financial modeling",
    "valuation",
    "fp&a",
    "forecasting",
    "budgeting",
    "variance analysis",
    "sql",
    "python",
    "tableau",
    "power bi",
    "excel",
    "strategy",
    "market research",
    "data analysis",
    "dashboard",
    "kpi",
    "m&a",
    "investment banking",
    "corporate development",
    "corporate strategy",
    "private equity",
    "venture capital",
    "due diligence",
    "lbo",
    "dcf",
    "stakeholder management",
    "cross-functional",
    "presentation",
    "analytics",
    "executive communication",
]

CORE_REQUIREMENT_WEIGHTS = {
    "strategic finance": 1.5,
    "fp&a": 1.5,
    "financial modeling": 1.45,
    "forecasting": 1.4,
    "budgeting": 1.1,
    "variance analysis": 1.1,
    "excel": 1.0,
    "sql": 1.0,
    "presentation": 0.9,
    "stakeholder management": 0.9,
    "cross-functional": 0.8,
    "analytics": 0.75,
    "dashboard": 0.7,
    "kpi": 0.7,
    "data analysis": 0.7,
}

SECONDARY_REQUIREMENT_WEIGHTS = {
    "valuation": 0.8,
    "python": 0.7,
    "tableau": 0.7,
    "power bi": 0.7,
    "strategy": 0.65,
    "market research": 0.65,
    "m&a": 0.75,
    "investment banking": 0.75,
    "corporate development": 0.75,
    "executive communication": 0.7,
}

ADVANCED_REQUIREMENTS = {
    "cohort analysis": ["cohort analysis", "cohort analyses"],
    "3-statement modeling": [
        "3-statement modeling",
        "3 statement modeling",
        "three statement modeling",
        "three-statement modeling",
    ],
    "unit economics": ["unit economics"],
    "pricing analysis": ["pricing analysis", "pricing analyses"],
    "A/B testing": ["a/b testing", "a/b tests", "ab testing", "ab tests"],
    "Looker": ["looker"],
    "bottom-up forecasting": ["bottom-up forecasting", "bottom up forecasting"],
    "product analytics": ["product analytics"],
    "financial performance management": ["financial performance management"],
    "fintech": ["fintech", "financial technology"],
    "SQL": ["sql"],
    "Excel": ["excel"],
    "forecasting": ["forecasting"],
    "financial modeling": ["financial modeling"],
    "scenario analysis": ["scenario analysis", "scenario testing", "scenario planning"],
}

ROLE_ADVANCED_REQUIREMENTS = {
    "Strategic Finance / FP&A": {
        "cohort analysis": ["cohort analysis", "cohort analyses"],
        "unit economics": ["unit economics"],
        "Looker": ["looker"],
        "bottom-up forecasting": ["bottom-up forecasting", "bottom up forecasting"],
        "A/B testing": ["a/b testing", "a/b tests", "ab testing", "ab tests"],
        "pricing analysis": ["pricing analysis", "pricing analyses"],
        "long-range planning": ["long-range planning", "long range planning"],
    },
    "Corporate Development": {
        "M&A": ["m&a", "mergers and acquisitions", "m&a transactions"],
        "due diligence": ["due diligence"],
        "accretion/dilution": ["accretion and dilution", "accretion/dilution"],
        "LBO": ["lbo", "leveraged buyout"],
        "DCF": ["dcf", "discounted cash flow"],
        "trading comparables": ["trading comparables", "trading comps"],
        "precedent transactions": ["precedent transactions"],
        "negotiation": ["negotiation", "valuation and negotiation"],
    },
    "Corporate Strategy": {
        "enterprise risk management": ["enterprise risk management"],
        "competitive intelligence": ["competitive intelligence"],
        "strategic planning": ["strategic planning", "annual strategic planning"],
        "Board/ExCom communication": ["board of directors", "excom", "executive team"],
        "CapEx planning": ["capex planning", "capex plan"],
    },
    "Investment Banking": {
        "live deal execution": ["live deal", "live deal execution", "deal execution"],
        "pitchbooks": ["pitchbook", "pitchbooks"],
        "CIM": ["cim", "confidential information memorandum"],
        "transaction execution": ["transaction execution"],
        "capital raising": ["capital raising"],
        "sell-side/buy-side advisory": ["sell-side advisory", "buy-side advisory"],
    },
    "Venture Capital": {
        "deal sourcing": ["deal sourcing"],
        "startup investing": ["startup investing"],
        "founder meetings": ["founder meetings"],
        "investment memo": ["investment memo"],
        "thesis-driven investing": ["thesis-driven investing", "thesis driven investing"],
        "portfolio support": ["portfolio support"],
    },
    "Private Equity": {
        "LBO": ["lbo", "leveraged buyout"],
        "portfolio company analysis": ["portfolio company", "portfolio company analysis"],
        "investment committee memo": ["investment committee", "investment committee memo"],
        "deal diligence": ["deal diligence", "transaction diligence"],
        "value creation": ["value creation", "value creation plan"],
    },
}

ADVANCED_REQUIREMENT_WEIGHTS = {
    "cohort analysis": 1.0,
    "3-statement modeling": 1.1,
    "unit economics": 1.0,
    "pricing analysis": 0.95,
    "A/B testing": 0.95,
    "Looker": 0.85,
    "bottom-up forecasting": 1.0,
    "product analytics": 0.95,
    "financial performance management": 0.95,
    "fintech": 0.75,
    "SQL": 0.7,
    "Excel": 0.65,
    "forecasting": 0.8,
    "financial modeling": 0.85,
    "scenario analysis": 0.9,
    "M&A": 1.0,
    "due diligence": 1.0,
    "accretion/dilution": 1.0,
    "LBO": 1.05,
    "DCF": 1.0,
    "trading comparables": 0.95,
    "precedent transactions": 0.95,
    "negotiation": 0.9,
    "enterprise risk management": 0.95,
    "competitive intelligence": 0.9,
    "strategic planning": 1.0,
    "Board/ExCom communication": 0.95,
    "CapEx planning": 0.9,
    "live deal execution": 1.1,
    "pitchbooks": 0.95,
    "CIM": 0.95,
    "transaction execution": 1.05,
    "capital raising": 1.0,
    "sell-side/buy-side advisory": 1.0,
    "deal sourcing": 1.0,
    "startup investing": 1.0,
    "founder meetings": 0.9,
    "investment memo": 1.0,
    "thesis-driven investing": 0.95,
    "portfolio support": 0.85,
    "portfolio company analysis": 1.0,
    "investment committee memo": 1.0,
    "deal diligence": 1.0,
    "value creation": 0.95,
}

HARD_AUTHORIZATION_BLOCKERS = [
    "u.s. citizenship is required",
    "us citizenship is required",
    "u.s. citizen required",
    "us citizen required",
    "must be a u.s. citizen",
    "must be a us citizen",
    "u.s. citizens only",
    "us citizens only",
    "citizenship is required",
    "security clearance required",
    "active security clearance",
    "ability to obtain security clearance",
    "clearance required",
    "requires government clearance",
    "due to the nature of work performed, u.s. citizenship is required",
    "due to the nature of work performed, us citizenship is required",
    "no sponsorship",
    "will not sponsor",
    "sponsorship is not available",
    "must be authorized to work without sponsorship",
    "must be authorized to work in the united states without sponsorship",
    "must be authorized to work in the us without sponsorship",
]

ENTRY_LEVEL_TERMS = [
    "analyst",
    "junior analyst",
    "associate analyst",
    "early career",
    "0-2 years",
    "0 to 2 years",
]

MID_LEVEL_TERMS = [
    "associate",
    "senior analyst",
    "2+ years",
    "3+ years",
    "lead",
    "manager",
]

SENIOR_LEVEL_TERMS = [
    "director",
    "vp",
    "vice president",
    "head of",
    "principal",
    "senior manager",
    "7+ years",
]


# -----------------------------
# Helper Functions
# -----------------------------

def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def term_pattern(term):
    escaped = re.escape(term.lower())
    escaped = escaped.replace(r"\ ", r"\s+")
    return rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"


def has_term(text, term):
    return re.search(term_pattern(term), normalize_text(text), flags=re.IGNORECASE) is not None


def find_terms(text, terms):
    return [term for term in terms if has_term(text, term)]


def find_canonical_terms(text, requirement_map):
    matches = []
    for canonical, variants in requirement_map.items():
        if any(has_term(text, variant) for variant in variants):
            matches.append(canonical)
    return matches


def authorization_hard_blockers(job_text):
    return find_terms(job_text, HARD_AUTHORIZATION_BLOCKERS)


def has_hard_authorization_blocker(risk_matches):
    return any(match in HARD_AUTHORIZATION_BLOCKERS for match in risk_matches)


def role_requirement_map(function):
    requirements = dict(ADVANCED_REQUIREMENTS)
    requirements.update(ROLE_ADVANCED_REQUIREMENTS.get(function, {}))
    return requirements


def detect_seniority(job_text):
    senior_matches = find_terms(job_text, SENIOR_LEVEL_TERMS)
    mid_matches = find_terms(job_text, MID_LEVEL_TERMS)
    entry_matches = find_terms(job_text, ENTRY_LEVEL_TERMS)

    year_matches = [int(year) for year in re.findall(r"(?<!\d)(\d{1,2})\+?\s*(?:years|yrs)", normalize_text(job_text))]
    if any(year >= 7 for year in year_matches):
        senior_matches.append("7+ years")
    elif any(year >= 2 for year in year_matches):
        mid_matches.append("2+ years")
    elif any(year <= 2 for year in year_matches):
        entry_matches.append("0-2 years")

    if senior_matches:
        return "Senior", sorted(set(senior_matches))
    if mid_matches:
        return "Mid-level", sorted(set(mid_matches))
    if entry_matches:
        return "Entry-level", sorted(set(entry_matches))
    return "Not specified", []


def detect_sponsorship_risk(job_text):
    explicit_support_terms = [
        "visa sponsorship available",
        "sponsorship available",
        "h-1b sponsorship",
        "h1b sponsorship",
        "will sponsor",
        "support h-1b",
        "support h1b",
        "support visa sponsorship",
        "supports opt",
        "supports cpt",
        "visa sponsorship support",
        "work authorization support",
        "requiring current or future work authorization support are welcome",
    ]

    likely_no_terms = HARD_AUTHORIZATION_BLOCKERS + [
        "no sponsorship",
        "will not sponsor",
        "will not provide sponsorship",
        "do not sponsor",
        "doesn't sponsor",
        "does not sponsor",
        "not sponsor",
        "not provide sponsorship",
        "not offer sponsorship",
        "without sponsorship",
        "sponsorship is not available",
        "must be authorized to work in the united states without sponsorship",
        "must be authorized to work in the us without sponsorship",
        "must be authorized to work without sponsorship",
        "must not require sponsorship",
        "must not require visa sponsorship",
        "unable to sponsor",
        "cannot sponsor",
        "cannot provide sponsorship",
        "u.s. citizen",
        "us citizen",
        "green card holder",
        "permanent resident",
        "security clearance required",
    ]

    possibly_friendly_terms = [
        "opt",
        "cpt",
        "h-1b",
        "h1b",
        "visa sponsorship",
        "international students",
        "e-verify",
        "stem opt",
    ]

    explicit_matches = find_terms(job_text, explicit_support_terms)
    likely_no_matches = sorted(set(find_terms(job_text, likely_no_terms)))
    possible_matches = find_terms(job_text, possibly_friendly_terms)

    if likely_no_matches:
        return "Likely No", likely_no_matches

    if explicit_matches:
        return "Explicitly Supports", explicit_matches

    if possible_matches:
        return "Possibly Friendly", possible_matches

    return "Unclear", []


def classify_function(job_text):
    scores = {}

    for category, keywords in ROLE_CATEGORIES.items():
        scores[category] = len(find_terms(job_text, keywords))

    investment_banking_anchors = find_terms(job_text, INVESTMENT_BANKING_ANCHOR_TERMS)
    corporate_development_anchors = find_terms(job_text, CORPORATE_DEVELOPMENT_ANCHOR_TERMS)
    corporate_strategy_anchors = find_terms(job_text, CORPORATE_STRATEGY_ANCHOR_TERMS)
    corporate_development_deal_signals = find_terms(job_text, CORPORATE_DEVELOPMENT_DEAL_TERMS)
    private_equity_anchors = find_terms(job_text, PRIVATE_EQUITY_ANCHOR_TERMS)
    venture_capital_anchors = find_terms(job_text, VENTURE_CAPITAL_ANCHOR_TERMS)
    business_analyst_anchors = find_terms(job_text, BUSINESS_ANALYST_ANCHOR_TERMS)

    explicit_corp_dev = find_terms(job_text, ["corporate development", "corporate development team", "corp dev"])
    explicit_corp_strategy = find_terms(job_text, ["corporate strategy", "strategy analyst"])
    explicit_corporate_venture = find_terms(job_text, ["corporate venture"])

    if corporate_development_anchors:
        scores["Corporate Development"] += min(len(corporate_development_anchors) * 3, 15)

    if corporate_development_deal_signals and not investment_banking_anchors:
        scores["Corporate Development"] += min(len(corporate_development_deal_signals) * 2, 12)

    if corporate_strategy_anchors:
        scores["Corporate Strategy"] += min(len(corporate_strategy_anchors) * 3, 9)

    if private_equity_anchors:
        scores["Private Equity"] += min(len(private_equity_anchors) * 3, 12)

    if venture_capital_anchors:
        scores["Venture Capital"] += min(len(venture_capital_anchors) * 3, 12)

    if business_analyst_anchors:
        scores["Business Analyst / General Analyst"] += min(len(business_analyst_anchors) * 2, 8)

    if (corporate_development_anchors or corporate_strategy_anchors) and not investment_banking_anchors:
        transferable_deal_finance_signals = find_terms(job_text, TRANSFERABLE_DEAL_FINANCE_TERMS)
        scores["Investment Banking"] = max(
            0,
            scores["Investment Banking"] - len(transferable_deal_finance_signals),
        )

    finance_signals = find_terms(job_text, FINANCE_INTENT_TERMS)
    analytics_tool_signals = find_terms(job_text, ANALYTICS_TOOL_TERMS)

    if finance_signals:
        scores["Strategic Finance / FP&A"] += min(len(finance_signals) * 2, 10)

    if finance_signals and analytics_tool_signals:
        scores["Business Analyst / General Analyst"] = max(
            0,
            scores["Business Analyst / General Analyst"] - min(len(analytics_tool_signals), 5),
        )
        if scores["Business Analyst / General Analyst"] >= scores["Strategic Finance / FP&A"]:
            scores["Business Analyst / General Analyst"] = max(0, scores["Strategic Finance / FP&A"] - 1)

    clearly_signaled_specialist = (
        investment_banking_anchors
        or corporate_development_anchors
        or corporate_strategy_anchors
        or finance_signals
        or private_equity_anchors
        or venture_capital_anchors
    )
    if clearly_signaled_specialist and business_analyst_anchors:
        scores["Business Analyst / General Analyst"] = min(
            scores["Business Analyst / General Analyst"],
            max(0, max(scores.values()) - 2),
        )

    if explicit_corp_dev or explicit_corporate_venture:
        scores["Corporate Development"] = max(scores["Corporate Development"], max(scores.values()) + 3)
        scores["Corporate Strategy"] = min(scores["Corporate Strategy"], scores["Corporate Development"] - 1)
        scores["Private Equity"] = min(scores["Private Equity"], scores["Corporate Development"] - 1)
        scores["Venture Capital"] = min(scores["Venture Capital"], scores["Corporate Development"] - 1)

    if corporate_strategy_anchors and not investment_banking_anchors:
        if not explicit_corp_dev:
            scores["Corporate Strategy"] = max(scores["Corporate Strategy"], max(scores.values()) + 1)

    if (
        corporate_development_deal_signals
        and not corporate_strategy_anchors
        and not investment_banking_anchors
    ):
        scores["Corporate Development"] = max(
            scores["Corporate Development"],
            scores["Investment Banking"] + 1,
        )

    if explicit_corp_strategy and not explicit_corp_dev and not investment_banking_anchors:
        scores["Corporate Strategy"] = max(scores["Corporate Strategy"], max(scores.values()) + 1)

    if not investment_banking_anchors:
        scores["Investment Banking"] = 0

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "General Business / Unknown", scores

    return best_category, scores


def extract_keywords(job_text):
    return find_terms(job_text, TRACKED_KEYWORDS)


def weighted_coverage(required_terms, matched_terms, weights):
    if not required_terms:
        return 1.0, 0, 0

    total_weight = sum(weights.get(term, 1.0) for term in required_terms)
    matched_weight = sum(weights.get(term, 1.0) for term in matched_terms)

    if total_weight == 0:
        return 1.0, matched_weight, total_weight

    return matched_weight / total_weight, matched_weight, total_weight


def cap_fit_score(score, core_coverage, secondary_coverage, advanced_terms, advanced_coverage, gaps, advanced_gaps):
    if core_coverage < 0.65:
        return min(score, 7.4)

    if core_coverage < 0.8:
        return min(score, 8.2)

    if not advanced_terms:
        return min(score, 8.5)

    if advanced_coverage < 0.35:
        return min(score, 8.5)

    if advanced_coverage < 0.6:
        return min(score, 8.8)

    matched_advanced_count = len(advanced_terms) - len(advanced_gaps)
    if matched_advanced_count < 3:
        return min(score, 8.8)

    meaningful_gap_count = len(gaps) + len(advanced_gaps)
    if core_coverage >= 0.95 and secondary_coverage >= 0.85 and advanced_coverage >= 0.85 and meaningful_gap_count <= 1:
        return min(score, 10.0)

    return min(score, 9.6)


def adjust_score_for_seniority(score, seniority, seniority_matches, profile_text, core_coverage, advanced_coverage):
    profile_strength_terms = [
        "mba",
        "finance",
        "analytics",
        "financial modeling",
        "valuation",
        "strategy",
        "fp&a",
        "corporate development",
        "investment banking",
    ]
    profile_strength = len(find_terms(profile_text, profile_strength_terms))

    if seniority == "Entry-level" and profile_strength >= 3:
        return min(score + 0.2, 9.4)

    if seniority == "Mid-level":
        if any(match in seniority_matches for match in ["lead", "manager", "3+ years"]) and profile_strength < 5:
            return min(score, 8.6)
        return score

    if seniority == "Senior":
        if profile_strength >= 6 and core_coverage >= 0.85 and advanced_coverage >= 0.5:
            return min(score, 8.8)
        return min(score, 8.2)

    return score


def calculate_fit_score(job_text, profile_text, function="General Business / Unknown", seniority="Not specified", seniority_matches=None):
    job_keywords = extract_keywords(job_text)
    core_terms = find_terms(job_text, CORE_REQUIREMENT_WEIGHTS.keys())
    secondary_terms = find_terms(job_text, SECONDARY_REQUIREMENT_WEIGHTS.keys())
    advanced_requirement_map = role_requirement_map(function)
    advanced_terms = find_canonical_terms(job_text, advanced_requirement_map)
    if function in ROLE_ADVANCED_REQUIREMENTS:
        advanced_terms = sorted(set(advanced_terms + list(ROLE_ADVANCED_REQUIREMENTS[function].keys())))

    if not job_keywords and not advanced_terms:
        return 6.0, [], [], [], []

    matched_core = [term for term in core_terms if has_term(profile_text, term)]
    matched_secondary = [term for term in secondary_terms if has_term(profile_text, term)]
    matched_advanced = [
        term
        for term in advanced_terms
        if any(has_term(profile_text, variant) for variant in advanced_requirement_map[term])
    ]

    core_gaps = [term for term in core_terms if term not in matched_core]
    secondary_gaps = [term for term in secondary_terms if term not in matched_secondary]
    advanced_gaps = [term for term in advanced_terms if term not in matched_advanced]

    core_coverage, _, _ = weighted_coverage(core_terms, matched_core, CORE_REQUIREMENT_WEIGHTS)
    secondary_coverage, _, _ = weighted_coverage(
        secondary_terms,
        matched_secondary,
        SECONDARY_REQUIREMENT_WEIGHTS,
    )
    advanced_coverage, _, _ = weighted_coverage(
        advanced_terms,
        matched_advanced,
        ADVANCED_REQUIREMENT_WEIGHTS,
    )

    score = 4.0
    score += core_coverage * 3.6 if core_terms else 1.8
    score += secondary_coverage * 1.0 if secondary_terms else 0.5
    score += advanced_coverage * 1.8 if advanced_terms else 0.4

    if core_coverage >= 0.85 and advanced_terms and advanced_coverage >= 0.5:
        score += 0.4

    if core_coverage >= 0.95 and secondary_coverage >= 0.85 and advanced_coverage >= 0.75:
        score += 0.3

    gaps = core_gaps + secondary_gaps
    score = cap_fit_score(
        score,
        core_coverage,
        secondary_coverage,
        advanced_terms,
        advanced_coverage,
        gaps,
        advanced_gaps,
    )
    score = adjust_score_for_seniority(
        score,
        seniority,
        seniority_matches or [],
        profile_text,
        core_coverage,
        advanced_coverage,
    )

    matched = matched_core + matched_secondary

    return round(min(score, 10.0), 1), matched, gaps, matched_advanced, advanced_gaps


def generate_decision(fit_score, sponsorship_risk, risk_matches=None):
    hard_blocker = has_hard_authorization_blocker(risk_matches or [])
    if hard_blocker:
        return "Skip"

    if sponsorship_risk == "Likely No":
        if fit_score >= 9.2:
            return "Network First"
        return "Skip"

    if sponsorship_risk == "Explicitly Supports":
        if fit_score >= 7.5:
            return "Apply Now"
        if fit_score >= 6.5:
            return "Network First"
        return "Skip"

    if sponsorship_risk == "Possibly Friendly":
        if fit_score >= 8:
            return "Apply + Network"
        if fit_score >= 6.5:
            return "Network First"
        return "Skip"

    if sponsorship_risk == "Unclear":
        if fit_score >= 8:
            return "Apply + Network"
        if fit_score >= 6.5:
            return "Network First"
        return "Skip"

    return "Skip"


def fit_summary(fit_score):
    if fit_score >= 9:
        return "Very strong match"
    if fit_score >= 8:
        return "Strong match"
    if fit_score >= 7:
        return "Good match"
    if fit_score >= 6:
        return "Partial match"
    return "Weak match"


def risk_note(risk):
    notes = {
        "Explicitly Supports": "The posting contains direct sponsorship or work authorization support language.",
        "Possibly Friendly": "The posting mentions OPT, CPT, H-1B, or work authorization, but does not clearly promise sponsorship.",
        "Unclear": "No clear sponsorship signal was found. Verify through networking or recruiter outreach.",
        "Likely No": "The posting includes restrictive language that often blocks candidates needing sponsorship.",
    }
    return notes[risk]


def decision_note(decision):
    notes = {
        "Apply Now": "The role has enough fit and sponsorship signal to justify a direct application.",
        "Apply + Network": "The role is worth applying to, but sponsorship or fit uncertainty makes parallel networking important.",
        "Network First": "The role may be worth pursuing, but a warm conversation should come before or alongside applying.",
        "Skip": "The role has either weak fit, high sponsorship friction, or both.",
    }
    return notes[decision]


def hard_blocker_note(risk_matches):
    blocker_matches = [match for match in risk_matches if match in HARD_AUTHORIZATION_BLOCKERS]
    if not blocker_matches:
        return ""
    if any("clearance" in match for match in blocker_matches):
        blocker_type = "security clearance"
    elif any("citizen" in match or "citizenship" in match for match in blocker_matches):
        blocker_type = "U.S. citizenship"
    else:
        blocker_type = blocker_matches[0]
    return (
        "Hard authorization blocker detected: the posting requires "
        f"{blocker_type}, so the recommended decision is Skip regardless of resume fit."
    )


def generate_outreach(function):
    return (
        f"Hi, I am an MBA candidate at William & Mary exploring {function} roles. "
        "I would be grateful to learn more about your team and any advice for candidates "
        "with finance, strategy, and analytics experience."
    )


def generate_why_decision(
    fit_score,
    sponsorship_risk,
    decision,
    matched,
    gaps,
    advanced_gaps,
    risk_matches,
    seniority,
    seniority_matches,
):
    reasons = [
        f"The resume fit score is {fit_score}/10, reflecting weighted core, secondary, and advanced requirement coverage rather than simple keyword overlap.",
        f"Sponsorship risk is marked as {sponsorship_risk}: {risk_note(sponsorship_risk)}",
        f"The recommended decision is {decision}: {decision_note(decision)}",
    ]

    blocker_note = hard_blocker_note(risk_matches)
    if blocker_note:
        reasons.insert(1, blocker_note)

    if seniority != "Not specified":
        seniority_signal = ", ".join(seniority_matches[:3]) if seniority_matches else "role language"
        reasons.append(f"Seniority signal is {seniority}, based on {seniority_signal}.")

    if matched:
        reasons.append("Matched core strengths include " + ", ".join(matched[:6]) + ".")

    if gaps:
        reasons.append("Regular resume gaps to address are " + ", ".join(gaps[:5]) + ".")

    if advanced_gaps:
        reasons.append("Advanced role gaps include " + ", ".join(advanced_gaps[:7]) + ".")

    if risk_matches:
        reasons.append("Sponsorship signal terms found: " + ", ".join(risk_matches[:4]) + ".")

    return reasons


def generate_next_actions(decision, sponsorship_risk, gaps, function):
    if decision == "Apply Now":
        actions = [
            f"Tailor the top third of your resume toward {function}.",
            "Submit the application while the role is fresh.",
            "Send a short LinkedIn note to one team member or recruiter within 24 hours.",
        ]
    elif decision == "Apply + Network":
        actions = [
            f"Apply with a resume tailored toward {function} and the strongest matched requirements.",
            "Contact a recruiter, alum, or team member to clarify sponsorship expectations.",
            f"Add evidence for {gaps[0] if gaps else 'one specialized role requirement'} before or soon after applying.",
        ]
    elif decision == "Network First":
        actions = [
            "Message one recruiter or team member before investing time in a full application.",
            "Ask a direct but professional question about work authorization expectations.",
            f"Strengthen one resume bullet around {gaps[0] if gaps else function} before applying.",
        ]
    else:
        actions = [
            "Do not spend major time on this role unless you have a strong referral path.",
            "Search for similar roles with clearer sponsorship language or better keyword overlap.",
            "Use the missing keywords as a checklist for the next target role.",
        ]

    if sponsorship_risk == "Unclear":
        actions[1] = "Verify sponsorship expectations through a recruiter, alumni contact, or company FAQ."

    return actions


def infer_role_title(job_text):
    clean_lines = [
        line.strip(" -|:")
        for line in job_text.splitlines()[:12]
        if line.strip() and len(line.strip()) <= 90
    ]
    title_terms = [
        "analyst",
        "associate",
        "manager",
        "consultant",
        "director",
        "strategy",
        "finance",
        "fp&a",
        "corporate development",
        "business operations",
        "investment banking",
    ]
    skip_terms = ["about", "responsibilities", "qualifications", "requirements", "description"]

    for line in clean_lines:
        normalized = normalize_text(line)
        if any(skip in normalized for skip in skip_terms):
            continue
        if any(term in normalized for term in title_terms):
            return line

    return clean_lines[0] if clean_lines else ""


def infer_salary_range(job_text):
    salary_pattern = re.compile(
        r"\$\s?\d{2,3}(?:,\d{3})?(?:\s?[kK])?(?:\s?[-\u2013\u2014]\s?\$\s?\d{2,3}(?:,\d{3})?(?:\s?[kK])?)?"
    )
    match = salary_pattern.search(job_text)
    return match.group(0).strip() if match else ""


def infer_location(job_text):
    location_patterns = [
        r"\bNew York\b",
        r"\bNYC\b",
        r"\bAtlanta\b",
        r"\bRemote\b",
        r"\bHybrid\b",
        r"\bWashington,\s?DC\b",
        r"\bBoston\b",
        r"\bChicago\b",
        r"\bSan Francisco\b",
        r"\bLos Angeles\b",
        r"\bCharlotte\b",
        r"\bDallas\b",
        r"\bAustin\b",
        r"\bSeattle\b",
        r"\bRichmond\b",
    ]
    for pattern in location_patterns:
        match = re.search(pattern, job_text, flags=re.IGNORECASE)
        if match:
            return match.group(0)

    city_state_match = re.search(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?,\s?[A-Z]{2}\b", job_text)
    return city_state_match.group(0) if city_state_match else ""


def infer_job_metadata(job_text):
    return {
        "role_title": infer_role_title(job_text),
        "location": infer_location(job_text),
        "salary_range": infer_salary_range(job_text),
    }


def tracker_priority(decision, fit_score):
    if decision in ["Apply Now", "Apply + Network"] and fit_score >= 8:
        return "High"
    if decision == "Network First":
        return "Medium"
    if decision == "Skip":
        return "Low"
    return "Medium"


def tracker_status(decision):
    if decision == "Skip":
        return "Skipped"
    return "Not Applied"


def tracker_rows_to_csv(rows):
    output = io.StringIO()
    fieldnames = [
        "Date Added",
        "Company Name",
        "Role Title",
        "Location",
        "Job Link",
        "Salary Range",
        "Role Classification",
        "Resume Fit Score",
        "Sponsorship Risk",
        "Application Decision",
        "Priority",
        "Status",
        "Notes",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def status_tone(value):
    tones = {
        "Explicitly Supports": "tone-support",
        "Possibly Friendly": "tone-friendly",
        "Unclear": "tone-unclear",
        "Likely No": "tone-no",
        "Apply Now": "tone-apply",
        "Apply + Network": "tone-apply-network",
        "Network First": "tone-network",
        "Skip": "tone-skip",
    }
    return tones.get(value, "")


def render_card(label, value, note, tone=""):
    st.markdown(
        f"""
        <div class="result-card {tone}">
            <div class="result-label">{html.escape(label)}</div>
            <div class="result-value">{html.escape(str(value))}</div>
            <div class="result-note">{html.escape(note)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pills(items, tone=""):
    pill_html = " ".join(
        f'<span class="pill">{html.escape(item)}</span>' for item in items
    )
    st.markdown(f'<div class="pill-row {tone}">{pill_html}</div>', unsafe_allow_html=True)


def render_actions(actions):
    for number, action in enumerate(actions, start=1):
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-number">{number}</div>
                <div>{html.escape(action)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card sidebar-brand-card">
            <div class="sidebar-kicker">VisaFit AI</div>
            <div class="sidebar-title">Career Decision Dashboard</div>
            <div class="sidebar-subtitle">Job-fit and sponsorship signal review</div>
            <p class="sidebar-copy">Prioritize roles with a clear apply, network, or skip recommendation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-section-title">How to use</div>
        <div class="sidebar-workflow">
            <div class="sidebar-step"><span class="sidebar-step-number">1</span><span>Paste job description</span></div>
            <div class="sidebar-step"><span class="sidebar-step-number">2</span><span>Review profile summary</span></div>
            <div class="sidebar-step"><span class="sidebar-step-number">3</span><span>Run analysis</span></div>
            <div class="sidebar-step"><span class="sidebar-step-number">4</span><span>Apply / network / skip based on output</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-section-title">Decision Legend</div>
        <div class="sidebar-legend">
            <span class="sidebar-pill legend-green">Apply Now</span>
            <span class="sidebar-pill legend-blue">Apply + Network</span>
            <span class="sidebar-pill legend-amber">Network First</span>
            <span class="sidebar-pill legend-red">Skip</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-section-title">Sponsorship Legend</div>
        <div class="sidebar-legend">
            <span class="sidebar-pill legend-green">Explicitly Supports</span>
            <span class="sidebar-pill legend-yellow">Possibly Friendly</span>
            <span class="sidebar-pill legend-gray">Unclear</span>
            <span class="sidebar-pill legend-red">Likely No</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("What this app checks"):
        st.markdown(
            """
            - Resume and skill alignment
            - Sponsorship language and risk
            - Role category and fit signals
            - Match strengths, gaps, and next actions
            """
        )

    with st.expander("Best for these roles"):
        st.markdown(
            """
            - Investment Banking
            - Strategic Finance / FP&A
            - Corporate Strategy
            - Corporate Development
            - Business Analyst
            - Venture Capital
            - Private Equity
            """
        )

    with st.expander("Sponsorship note"):
        st.markdown(
            "Sponsorship results are inferred from job-description language. Confirm details "
            "with the employer before making application or immigration decisions."
        )

    st.markdown(
        '<div class="sidebar-disclaimer">Career guidance only &mdash; not legal or immigration advice.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<a class="sidebar-link" href="https://github.com/nehatiwari5406-stack/visafit-ai" target="_blank" rel="noopener noreferrer">View GitHub repo</a>',
        unsafe_allow_html=True,
    )


# -----------------------------
# App Interface
# -----------------------------

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "profile_summary" not in st.session_state:
    st.session_state.profile_summary = DEFAULT_PROFILE

if "job_tracker" not in st.session_state:
    st.session_state.job_tracker = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

st.markdown(
    """
    <div class="hero">
        <h1>VisaFit AI</h1>
        <p>Prioritize job applications with a simple read on resume fit, sponsorship signal, role type, and next steps.</p>
        <div class="hero-stats">
            <span class="hero-chip">Resume fit</span>
            <span class="hero-chip">Sponsorship signal</span>
            <span class="hero-chip">Role classification</span>
            <span class="hero-chip">Outreach actions</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_col1, top_col2 = st.columns([0.72, 0.28])

with top_col1:
    st.markdown(
        '<div class="top-action-row"><div class="small-muted">Paste a JD, compare it with your profile, and get a practical recommendation for where to spend time.</div></div>',
        unsafe_allow_html=True,
    )

with top_col2:
    if st.button("Load sample job", use_container_width=True):
        st.session_state.job_description = SAMPLE_JOB

input_col, profile_col = st.columns(2)

with input_col:
    job_description = st.text_area(
        "Job Description",
        key="job_description",
        height=330,
        placeholder="Paste the full job description here, including qualifications and work authorization language.",
    )
    st.caption("Include qualifications and work authorization language for the strongest signal.")

with profile_col:
    profile_summary = st.text_area(
        "Resume / Profile Summary",
        key="profile_summary",
        height=330,
    )
    st.caption("Tune this summary to reflect the resume version you would actually submit.")

metadata_defaults = infer_job_metadata(job_description)

with st.expander("Optional job tracker details"):
    st.caption("VisaFit AI pre-fills simple guesses from the job description when it can.")
    meta_col1, meta_col2, meta_col3 = st.columns([1, 1, 1])
    meta_col4, meta_col5 = st.columns([1.35, 1])

    with meta_col1:
        company_name = st.text_input("Company Name", placeholder="Company")

    with meta_col2:
        role_title = st.text_input(
            "Role Title",
            value=metadata_defaults["role_title"],
            placeholder="Role title",
        )

    with meta_col3:
        location = st.text_input(
            "Location",
            value=metadata_defaults["location"],
            placeholder="City, state, remote, or hybrid",
        )

    with meta_col4:
        job_link = st.text_input("Job Link", placeholder="https://...")

    with meta_col5:
        salary_range = st.text_input(
            "Salary Range",
            value=metadata_defaults["salary_range"],
            placeholder="$90,000 - $120,000",
        )

analyze = st.button("Analyze Job", type="primary", use_container_width=True)

if analyze:
    if not job_description.strip():
        st.warning("Please paste a job description or load the sample job first.")
    else:
        sponsorship_risk, risk_matches = detect_sponsorship_risk(job_description)
        function, category_scores = classify_function(job_description)
        seniority, seniority_matches = detect_seniority(job_description)
        keywords = extract_keywords(job_description)
        fit_score, matched_keywords, gaps, matched_advanced, advanced_gaps = calculate_fit_score(
            job_description,
            profile_summary,
            function,
            seniority,
            seniority_matches,
        )
        decision = generate_decision(fit_score, sponsorship_risk, risk_matches)
        outreach = generate_outreach(function)
        why_decision = generate_why_decision(
            fit_score,
            sponsorship_risk,
            decision,
            matched_keywords,
            gaps,
            advanced_gaps,
            risk_matches,
            seniority,
            seniority_matches,
        )
        next_actions = generate_next_actions(decision, sponsorship_risk, gaps, function)
        st.session_state.analysis_result = {
            "company_name": company_name.strip(),
            "role_title": role_title.strip(),
            "location": location.strip(),
            "job_link": job_link.strip(),
            "salary_range": salary_range.strip(),
            "sponsorship_risk": sponsorship_risk,
            "risk_matches": risk_matches,
            "function": function,
            "category_scores": category_scores,
            "seniority": seniority,
            "seniority_matches": seniority_matches,
            "keywords": keywords,
            "fit_score": fit_score,
            "matched_keywords": matched_keywords,
            "gaps": gaps,
            "matched_advanced": matched_advanced,
            "advanced_gaps": advanced_gaps,
            "decision": decision,
            "outreach": outreach,
            "why_decision": why_decision,
            "next_actions": next_actions,
        }

analysis_result = st.session_state.analysis_result

if analysis_result:
    sponsorship_risk = analysis_result["sponsorship_risk"]
    risk_matches = analysis_result["risk_matches"]
    function = analysis_result["function"]
    category_scores = analysis_result["category_scores"]
    seniority = analysis_result["seniority"]
    seniority_matches = analysis_result["seniority_matches"]
    fit_score = analysis_result["fit_score"]
    matched_keywords = analysis_result["matched_keywords"]
    gaps = analysis_result["gaps"]
    matched_advanced = analysis_result["matched_advanced"]
    advanced_gaps = analysis_result["advanced_gaps"]
    decision = analysis_result["decision"]
    outreach = analysis_result["outreach"]
    why_decision = analysis_result["why_decision"]
    next_actions = analysis_result["next_actions"]

    st.divider()
    st.subheader("Executive Fit Dashboard")
    st.caption("A fast triage view for deciding whether this role deserves an application, networking effort, or deprioritization.")

    card1, card2, card3, card4 = st.columns(4)

    with card1:
        render_card(
            "Resume Fit Score",
            f"{fit_score}/10",
            f"{fit_summary(fit_score)} based on tracked role requirements.",
            "tone-fit",
        )
        st.progress(min(fit_score / 10, 1.0))

    with card2:
        render_card(
            "Sponsorship Risk",
            sponsorship_risk,
            risk_note(sponsorship_risk),
            status_tone(sponsorship_risk),
        )

    with card3:
        render_card(
            "Application Decision",
            decision,
            "Recommended next move based on fit and sponsorship signal.",
            status_tone(decision),
        )

    with card4:
        render_card(
            "Role Classification",
            function,
            "Primary role family inferred from the strongest business signals.",
            "tone-role",
        )

    overview_tab, match_tab, sponsorship_tab, actions_tab, tracker_tab = st.tabs(
        ["Overview", "Match Analysis", "Sponsorship", "Outreach & Actions", "Job Tracker"]
    )

    with overview_tab:
        st.subheader("Decision Rationale")
        st.markdown(
            '<div class="caption">These points combine role fit, sponsorship signal, and keyword evidence into one recommended next move.</div>',
            unsafe_allow_html=True,
        )
        for reason in why_decision:
            st.write("- " + reason)

        st.subheader("Priority Actions")
        st.markdown(
            '<div class="caption">Use these actions to decide how much time to invest before submitting or moving on.</div>',
            unsafe_allow_html=True,
        )
        render_actions(next_actions)

    with match_tab:
        st.subheader("Keyword Alignment")
        st.markdown(
            '<div class="caption">Matched keywords are requirements already reflected in your profile. Resume gaps are useful prompts for tailoring.</div>',
            unsafe_allow_html=True,
        )

        match_col, gap_col = st.columns(2)

        with match_col:
            st.markdown("**Matched keywords**")
            if matched_keywords:
                render_pills(matched_keywords, "tone-match")
            else:
                st.write("No tracked keywords from the job description were found in the profile summary.")

        with gap_col:
            st.markdown("**Resume gaps**")
            if gaps:
                render_pills(gaps, "tone-gap")
            else:
                st.write("Strong keyword alignment. No major tracked gaps detected.")

        advanced_match_col, advanced_gap_col = st.columns(2)

        with advanced_match_col:
            st.markdown("**Matched advanced requirements**")
            if matched_advanced:
                render_pills(matched_advanced, "tone-match")
            else:
                st.write("No specialized role requirements were found in the profile summary.")

        with advanced_gap_col:
            st.markdown("**Advanced role gaps**")
            if advanced_gaps:
                render_pills(advanced_gaps, "tone-gap")
            else:
                st.write("No specialized advanced gaps detected from the tracked role signals.")

        with st.expander("Role category signal detail"):
            sorted_scores = sorted(category_scores.items(), key=lambda item: item[1], reverse=True)
            for category, score in sorted_scores:
                st.markdown(
                    f"""
                    <div class="signal-row">
                        <span>{html.escape(category)}</span>
                        <span class="signal-score">{score}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with sponsorship_tab:
        st.subheader("Sponsorship Signal")
        st.markdown(
            '<div class="caption">This reads the posting for language that may indicate sponsorship support or restrictions. Confirm directly with the employer before relying on it.</div>',
            unsafe_allow_html=True,
        )
        render_card(
            "Detected Risk Level",
            sponsorship_risk,
            risk_note(sponsorship_risk),
            status_tone(sponsorship_risk),
        )

        st.markdown("**Detected signal terms**")
        if risk_matches:
            render_pills(risk_matches, "tone-risk")
        else:
            st.write("No clear sponsorship terms were detected.")

    with actions_tab:
        st.subheader("Recommended Outreach")
        st.markdown(
            '<div class="caption">A concise note you can adapt for alumni, recruiters, or team members before applying.</div>',
            unsafe_allow_html=True,
        )
        st.info(outreach)

        st.subheader("Priority Actions")
        render_actions(next_actions)

    with tracker_tab:
        st.subheader("Job Tracker")
        st.markdown(
            '<div class="caption">Session-based tracker for roles you have analyzed. Download a CSV before closing the app if you want to keep it.</div>',
            unsafe_allow_html=True,
        )

        if st.button("Add to Job Tracker", type="primary", use_container_width=True):
            priority = tracker_priority(decision, fit_score)
            status = tracker_status(decision)
            st.session_state.job_tracker.append(
                {
                    "Date Added": date.today().isoformat(),
                    "Company Name": analysis_result["company_name"],
                    "Role Title": analysis_result["role_title"],
                    "Location": analysis_result["location"],
                    "Job Link": analysis_result["job_link"],
                    "Salary Range": analysis_result["salary_range"],
                    "Role Classification": function,
                    "Resume Fit Score": fit_score,
                    "Sponsorship Risk": sponsorship_risk,
                    "Application Decision": decision,
                    "Priority": priority,
                    "Status": status,
                    "Notes": decision_note(decision),
                }
            )
            st.success("Added this role to the Job Tracker.")

        tracked_jobs = st.session_state.job_tracker
        if tracked_jobs:
            total_roles = len(tracked_jobs)
            high_priority = sum(1 for row in tracked_jobs if row["Priority"] == "High")
            apply_roles = sum(
                1
                for row in tracked_jobs
                if row["Application Decision"] in ["Apply Now", "Apply + Network"]
            )
            skip_roles = sum(1 for row in tracked_jobs if row["Application Decision"] == "Skip")

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            metric_col1.metric("Total Roles", total_roles)
            metric_col2.metric("High Priority", high_priority)
            metric_col3.metric("Apply Roles", apply_roles)
            metric_col4.metric("Skip Roles", skip_roles)

            st.dataframe(tracked_jobs, use_container_width=True, hide_index=True)

            csv_data = tracker_rows_to_csv(tracked_jobs)
            download_col, clear_col = st.columns([0.62, 0.38])
            with download_col:
                st.download_button(
                    "Download CSV",
                    data=csv_data,
                    file_name="visafit_job_tracker.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with clear_col:
                confirm_clear = st.checkbox("Confirm clear tracker")
                if st.button(
                    "Clear Tracker",
                    disabled=not confirm_clear,
                    use_container_width=True,
                ):
                    st.session_state.job_tracker = []
                    st.warning("Tracker cleared for this session.")
        else:
            st.info("No jobs tracked yet. Analyze a role and click Add to Job Tracker.")
else:
    st.divider()
    overview_tab, match_tab, sponsorship_tab, actions_tab, tracker_tab = st.tabs(
        ["Overview", "Match Analysis", "Sponsorship", "Outreach & Actions", "Job Tracker"]
    )

    with overview_tab:
        st.info("Analyze a job first to see the executive fit dashboard.")

    with match_tab:
        st.info("Analyze a job first to see keyword alignment and resume gaps.")

    with sponsorship_tab:
        st.info("Analyze a job first to see sponsorship signal detail.")

    with actions_tab:
        st.info("Analyze a job first to see outreach and recommended actions.")

    with tracker_tab:
        st.subheader("Job Tracker")
        st.markdown(
            '<div class="caption">Session-based tracker for analyzed roles. The table and CSV download appear after you add your first role.</div>',
            unsafe_allow_html=True,
        )
        st.info("Analyze a job first, then add it to your tracker.")
