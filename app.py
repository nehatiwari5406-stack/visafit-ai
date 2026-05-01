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
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }
    .hero {
        border: 1px solid #d7dde8;
        border-radius: 8px;
        padding: 1.25rem 1.35rem;
        background: #f8fafc;
        margin-bottom: 1.25rem;
    }
    .hero h1 {
        margin: 0 0 0.35rem 0;
        font-size: 2.25rem;
        line-height: 1.15;
        letter-spacing: 0;
    }
    .hero p {
        margin: 0;
        color: #475569;
        font-size: 1rem;
    }
    .result-card {
        border: 1px solid #d7dde8;
        border-radius: 8px;
        padding: 1rem;
        min-height: 126px;
        background: #ffffff;
    }
    .result-label {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.4rem;
    }
    .result-value {
        color: #0f172a;
        font-size: 1.45rem;
        font-weight: 750;
        line-height: 1.2;
        margin-bottom: 0.45rem;
    }
    .result-note {
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.35;
    }
    .pill {
        display: inline-block;
        border-radius: 999px;
        padding: 0.22rem 0.6rem;
        background: #eef2f7;
        color: #263244;
        font-size: 0.86rem;
        border: 1px solid #d7dde8;
    }
    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem 0.45rem;
        margin: 0.35rem 0 0.85rem 0;
    }
    .small-muted {
        color: #64748b;
        font-size: 0.9rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
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


def render_card(label, value, note):
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">{label}</div>
            <div class="result-value">{value}</div>
            <div class="result-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pills(items):
    pill_html = " ".join(
        f'<span class="pill">{html.escape(item)}</span>' for item in items
    )
    st.markdown(f'<div class="pill-row">{pill_html}</div>', unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.title("VisaFit AI")
    st.caption("Job fit and sponsorship risk analyzer")

    st.subheader("Who this helps")
    st.write(
        "International MBA students and early-career professionals deciding which roles "
        "deserve an application, networking effort, or quick pass."
    )

    st.subheader("How to use it")
    st.write(
        "Paste a job description, review or edit the profile summary, then run the analysis. "
        "Use the decision, gaps, and next actions to prioritize your search."
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
    </div>
    """,
    unsafe_allow_html=True,
)

top_col1, top_col2 = st.columns([0.72, 0.28])

with top_col1:
    st.markdown(
        '<div class="small-muted">Paste a JD, compare it with your profile, and get a practical application recommendation.</div>',
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

with profile_col:
    profile_summary = st.text_area(
        "Resume / Profile Summary",
        key="profile_summary",
        height=330,
    )

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

        card1, card2, card3, card4 = st.columns(4)

        with card1:
            render_card(
                "Resume Fit Score",
                f"{fit_score}/10",
                f"{fit_summary(fit_score)} based on tracked role requirements.",
            )
            st.progress(min(fit_score / 10, 1.0))

        with card2:
            render_card(
                "Sponsorship Risk",
                sponsorship_risk,
                risk_note(sponsorship_risk),
            )

        with card3:
            render_card(
                "Application Decision",
                decision,
                "Recommended next move based on fit and sponsorship signal.",
            )

        with card4:
            render_card(
                "Role Classification",
                function,
                "Primary role family inferred from the strongest business signals.",
            )

        st.subheader("Decision Rationale")
        for reason in why_decision:
            st.write("- " + reason)

        st.subheader("Priority Actions")
        for number, action in enumerate(next_actions, start=1):
            st.write(f"{number}. {action}")

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            st.subheader("Keyword Alignment")
            if matched_keywords:
                st.markdown("Matched keywords")
                render_pills(matched_keywords)
            else:
                st.write("No tracked keywords from the job description were found in the profile summary.")

            if gaps:
                st.markdown("Resume gaps")
                render_pills(gaps)
            else:
                st.write("Strong keyword alignment. No major tracked gaps detected.")

        with detail_col2:
            st.subheader("Sponsorship Signals")
            if risk_matches:
                render_pills(risk_matches)
            else:
                st.write("No clear sponsorship terms were detected.")

            st.subheader("Recommended Outreach")
            st.info(outreach)

        with st.expander("Role category signal detail"):
            sorted_scores = sorted(category_scores.items(), key=lambda item: item[1], reverse=True)
            for category, score in sorted_scores:
                st.write(f"{category}: {score}")
