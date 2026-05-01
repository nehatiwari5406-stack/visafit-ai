import html
import re

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
        background: #fbfdff;
        border-right: 1px solid #e7edf5;
        box-shadow: inset -1px 0 0 rgba(148, 163, 184, 0.08);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.35rem;
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
        box-shadow: 0 8px 18px rgba(29, 78, 216, 0.16);
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1e40af, #03685f);
        border-color: #1e40af;
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
        "investment banking",
        "m&a",
        "mergers",
        "acquisitions",
        "valuation",
        "pitchbook",
        "financial modeling",
        "deal execution",
    ],
    "Corporate Development": [
        "corporate development",
        "strategic acquisitions",
        "m&a strategy",
        "partnerships",
        "due diligence",
        "integration planning",
    ],
    "Strategic Finance / FP&A": [
        "fp&a",
        "financial planning",
        "forecasting",
        "budgeting",
        "variance analysis",
        "strategic finance",
        "annual planning",
    ],
    "Corporate Strategy": [
        "corporate strategy",
        "growth strategy",
        "market strategy",
        "strategic initiatives",
        "new market",
        "competitive analysis",
    ],
    "Business Analytics": [
        "sql",
        "tableau",
        "power bi",
        "dashboard",
        "data analysis",
        "analytics",
        "kpi",
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

FINANCE_INTENT_TERMS = [
    "strategic finance",
    "fp&a",
    "financial planning",
    "forecasting",
    "budgeting",
    "variance analysis",
    "financial modeling",
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

TRACKED_KEYWORDS = [
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
    "stakeholder management",
    "cross-functional",
    "presentation",
    "analytics",
    "executive communication",
]


# -----------------------------
# Helper Functions
# -----------------------------

def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_terms(text, terms):
    normalized = normalize_text(text)
    return [term for term in terms if term in normalized]


def detect_sponsorship_risk(job_text):
    explicit_support_terms = [
        "visa sponsorship available",
        "sponsorship available",
        "h-1b sponsorship",
        "h1b sponsorship",
        "will sponsor",
        "support h-1b",
        "supports opt",
        "supports cpt",
        "work authorization support",
        "requiring current or future work authorization support are welcome",
    ]

    likely_no_terms = [
        "no sponsorship",
        "will not sponsor",
        "does not sponsor",
        "not sponsor",
        "without sponsorship",
        "sponsorship is not available",
        "must be authorized to work in the united states without sponsorship",
        "must be authorized to work in the us without sponsorship",
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
        "international students",
        "work authorization",
        "e-verify",
        "stem opt",
    ]

    explicit_matches = find_terms(job_text, explicit_support_terms)
    likely_no_matches = find_terms(job_text, likely_no_terms)
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

    finance_signals = find_terms(job_text, FINANCE_INTENT_TERMS)
    analytics_tool_signals = find_terms(job_text, ANALYTICS_TOOL_TERMS)

    if finance_signals:
        scores["Strategic Finance / FP&A"] += min(len(finance_signals), 4)

    if finance_signals and analytics_tool_signals:
        scores["Business Analytics"] = max(
            0,
            scores["Business Analytics"] - min(len(analytics_tool_signals), 3),
        )

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "General Business / Unknown", scores

    return best_category, scores


def extract_keywords(job_text):
    return find_terms(job_text, TRACKED_KEYWORDS)


def calculate_fit_score(job_text, profile_text):
    job_keywords = extract_keywords(job_text)
    profile = normalize_text(profile_text)

    if not job_keywords:
        return 6.0, [], []

    matched = [keyword for keyword in job_keywords if keyword in profile]
    gaps = [keyword for keyword in job_keywords if keyword not in profile]
    score = 5 + (len(matched) / len(job_keywords)) * 5

    return round(score, 1), matched, gaps


def generate_decision(fit_score, sponsorship_risk):
    if sponsorship_risk == "Likely No":
        if fit_score >= 8.5:
            return "Network First"
        return "Skip"

    if sponsorship_risk == "Explicitly Supports":
        if fit_score >= 7:
            return "Apply Now"
        return "Network First"

    if sponsorship_risk == "Possibly Friendly":
        if fit_score >= 8:
            return "Apply Now"
        if fit_score >= 6.5:
            return "Network First"
        return "Skip"

    if fit_score >= 8.5:
        return "Apply Now"

    if fit_score >= 6.5:
        return "Network First"

    return "Skip"


def fit_summary(fit_score):
    if fit_score >= 8.5:
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
        "Network First": "The role may be worth pursuing, but a warm conversation should come before or alongside applying.",
        "Skip": "The role has either weak fit, high sponsorship friction, or both.",
    }
    return notes[decision]


def generate_outreach(function):
    return (
        f"Hi, I am an MBA candidate at William & Mary exploring {function} roles. "
        "I would be grateful to learn more about your team and any advice for candidates "
        "with finance, strategy, and analytics experience."
    )


def generate_why_decision(fit_score, sponsorship_risk, decision, matched, gaps, risk_matches):
    reasons = [
        f"The resume fit score is {fit_score}/10, which indicates a {fit_summary(fit_score).lower()}.",
        f"Sponsorship risk is marked as {sponsorship_risk}: {risk_note(sponsorship_risk)}",
        f"The recommended decision is {decision}: {decision_note(decision)}",
    ]

    if matched:
        reasons.append("Matched strengths include " + ", ".join(matched[:6]) + ".")

    if gaps:
        reasons.append("The biggest resume gaps to address are " + ", ".join(gaps[:5]) + ".")

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


def status_tone(value):
    tones = {
        "Explicitly Supports": "tone-support",
        "Possibly Friendly": "tone-friendly",
        "Unclear": "tone-unclear",
        "Likely No": "tone-no",
        "Apply Now": "tone-apply",
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
    st.title("VisaFit AI")
    st.caption("Executive job-fit dashboard")

    st.subheader("Focus")
    st.write(
        "International MBA students and early-career professionals deciding which roles "
        "deserve an application, a networking push, or a quick pass."
    )

    st.subheader("Workflow")
    st.write(
        "Paste a job description, review or edit the profile summary, then run the analysis. "
        "Use the decision, gaps, and next actions to prioritize your search queue."
    )

    st.subheader("Disclaimer")
    st.warning(
        "This is career guidance, not legal or immigration advice. Confirm work authorization "
        "questions with qualified professionals or the employer."
    )


# -----------------------------
# App Interface
# -----------------------------

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "profile_summary" not in st.session_state:
    st.session_state.profile_summary = DEFAULT_PROFILE

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

analyze = st.button("Analyze Job", type="primary", use_container_width=True)

if analyze:
    if not job_description.strip():
        st.warning("Please paste a job description or load the sample job first.")
    else:
        sponsorship_risk, risk_matches = detect_sponsorship_risk(job_description)
        function, category_scores = classify_function(job_description)
        keywords = extract_keywords(job_description)
        fit_score, matched_keywords, gaps = calculate_fit_score(job_description, profile_summary)
        decision = generate_decision(fit_score, sponsorship_risk)
        outreach = generate_outreach(function)
        why_decision = generate_why_decision(
            fit_score,
            sponsorship_risk,
            decision,
            matched_keywords,
            gaps,
            risk_matches,
        )
        next_actions = generate_next_actions(decision, sponsorship_risk, gaps, function)

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

        overview_tab, match_tab, sponsorship_tab, actions_tab = st.tabs(
            ["Overview", "Match Analysis", "Sponsorship", "Outreach & Actions"]
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
