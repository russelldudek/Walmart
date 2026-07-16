from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(relative_path: str, old: str, new: str) -> None:
    path = ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Expected source pattern not found in {relative_path}: {old[:80]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def table(headers: tuple[str, str], rows: list[tuple[str, str]]) -> str:
    head = f"<tr><th>{headers[0]}</th><th>{headers[1]}</th></tr>"
    body = "".join(f"<tr><td>{left}</td><td>{right}</td></tr>" for left, right in rows)
    return f'<table class="table">{head}{body}</table>'


def section(title: str, body: str) -> str:
    return f'<div class="doc-section"><h2>{title}</h2>{body}</div>'


def phase_box(day: int, outcome: str, actions: list[str]) -> str:
    return (
        '<div class="phase-box">'
        f'<b>What changes by day {day}</b><h3>{outcome}</h3>'
        f'{bullets(actions)}</div>'
    )


def continuation_header() -> str:
    return (
        '<div class="page-two-header"><strong>120-Day Entry Plan</strong>'
        '<span>Russell Dudek | https://russelldudek.github.io/Walmart/</span></div>'
    )


replace_once(
    "styles.css",
    ".decision-rail { background:#fff; color:var(--walmart-bentonville-blue); padding:2rem; }",
    ".decision-rail { position:sticky; top:90px; align-self:start; background:#fff; color:var(--walmart-bentonville-blue); padding:2rem; }",
)
replace_once(
    "styles.css",
    ".doc-company img { width:.72in; height:.36in; object-fit:cover; }",
    ".doc-company img { width:.92in; height:.34in; object-fit:contain; object-position:left center; flex:0 0 auto; }",
)
replace_once(
    "styles.css",
    "  .scenario-panel { position:static; }",
    "  .scenario-panel, .decision-rail { position:static; }",
)
replace_once(
    "scripts/build_artifacts.py",
    "('walmart-wordmark-white-on-true-blue.jpg', 'walmart-wordmark-cropped.jpg', (205, 185, 795, 380))",
    "('walmart-wordmark-white-on-true-blue.jpg', 'walmart-wordmark-cropped.jpg', (155, 145, 845, 420))",
)
replace_once(
    "scripts/build_artifacts.py",
    "('120-day-plan.html', '120-day-plan.pdf', 2)",
    "('120-day-plan.html', '120-day-plan.pdf', 4)",
)
replace_once(
    "scripts/audit_public.py",
    "'120-day-plan.pdf': 2",
    "'120-day-plan.pdf': 4",
)
replace_once(
    "brand-intelligence.md",
    "- Non-destructive crop derivative: `assets/brand/walmart-wordmark-cropped.jpg`",
    "- Non-destructive crop derivative: `assets/brand/walmart-wordmark-cropped.jpg` (retains additional horizontal clear space for document headers)",
)

page1_actions = [
    "Meet CLO staff, Governance leaders, Technology, Finance, Architecture, Privacy, Security, and delivery teams.",
    "Inventory active and proposed AI use cases, spend, dependencies, vendors, controls, and accountable owners.",
    "Map intake, prioritization, approval, exception, escalation, release, monitoring, and retirement decisions.",
    "Shadow representative workflows across Legal, Compliance, Ethics, Investigations, and Security.",
    "Separate prudent review time from avoidable queue time and rework.",
    "Baseline decision latency, evidence completeness, adoption burden, and recurring bottlenecks.",
]
page1_questions = [
    "Where does AI demand enter, and how does it become portfolio work?",
    "Which decisions are enterprise-wide, and which require local legal judgment?",
    "Where are ownership, funding, or release authority ambiguous?",
    "Which controls are repeatedly rebuilt rather than reused?",
    "Where does adoption fail after technical approval?",
    "Which existing mechanisms already work and should be protected?",
]
page1_stakeholders = [
    ("CLO and Governance leadership", "Strategic priorities, risk appetite, decision pain, and executive visibility needs"),
    ("Legal, Compliance, Ethics, Investigations", "Substantive authority, workflow friction, exceptions, and evidence standards"),
    ("Privacy and Security", "Data boundaries, access, logging, monitoring, and escalation expectations"),
    ("Technology and Architecture", "Platforms, dependencies, reusable services, and delivery constraints"),
    ("Finance and business owners", "Investment logic, baselines, value evidence, and operating ownership"),
]

page2_actions = [
    "Co-design the seven-clause Scannable AI Contract with governance, technology, finance, and operating leaders.",
    "Define risk-sensitive stage gates rather than forcing every use case through the same review burden.",
    "Create a portfolio view showing sponsor, owner, value thesis, risk posture, dependencies, evidence, and next decision date.",
    "Clarify who may Fund, Shape, Hold, Stop, release, escalate, or grant an exception.",
    "Align Finance on investment, capacity, and value-realization logic.",
    "Select two contrasting use cases for controlled proof.",
]
contract_rows = [
    ("Outcome", "Which workflow, decision, risk, or obligation improves?"),
    ("Legal basis", "What authority, obligation, policy, or permitted use supports the work?"),
    ("Risk and harm", "What can go wrong, who is affected, and what escalates?"),
    ("Data and security", "What data is necessary, protected, retained, logged, or prohibited?"),
    ("Human authority", "Which decisions remain human and where may automation act?"),
    ("Operating ownership", "Who owns performance, exceptions, adoption, maintenance, and retirement?"),
    ("Evidence and economics", "What proof earns the next investment or triggers a stop?"),
]
decision_rows = [
    ("Intake", "Who qualifies demand and what minimum context is required?"),
    ("Prioritization", "How value, risk, reuse, urgency, and capacity are balanced"),
    ("Release", "Who accepts residual risk and operational readiness"),
    ("Exception", "Who may deviate, for how long, and with what evidence"),
    ("Funding", "What evidence earns additional investment"),
    ("Retirement", "Who stops low-value, obsolete, or unmanaged work"),
]

page3_actions = [
    "Apply the contract to two use cases with different risk, data, and authority profiles.",
    "Test evaluation, logging, monitoring, escalation, fallback, and human-review mechanisms.",
    "Measure decision latency, rework, evidence completeness, and adoption burden.",
    "Run an executive portfolio review that results in a real Fund, Shape, Hold, or Stop decision.",
    "Capture reusable controls, decision templates, architecture patterns, and unresolved exceptions.",
    "Document what the mechanism accelerated, what it protected, and where it created unnecessary burden.",
]
evidence_rows = [
    ("Decision latency", "Time from intake to a named posture, segmented by risk and complexity"),
    ("Control evidence", "Quality of evaluation, logging, monitoring, escalation, and human review"),
    ("Adoption burden", "Training, workarounds, exceptions, role changes, and sustained use"),
    ("Value evidence", "Observed outcome against an agreed baseline and operating cost"),
    ("Exception quality", "Whether exceptions reveal policy, architecture, ownership, or data gaps"),
]

page4_actions = [
    "Publish reusable decision, control, evaluation, and ownership patterns.",
    "Align capacity and talent to the prioritized portfolio roadmap.",
    "Define executive cadence, escalation paths, and portfolio health indicators.",
    "Set value-realization and adoption reviews with Finance and business owners.",
    "Establish a learning backlog: what to standardize, localize, automate, or stop.",
    "Translate unresolved exceptions into policy, platform, data, talent, or operating-model work.",
]
roadmap_rows = [
    ("Portfolio governance", "Single intake, prioritization, posture, ownership, and decision cadence"),
    ("Reusable controls", "Shared evaluation, logging, monitoring, escalation, and evidence patterns"),
    ("Platform and data", "Architecture and data capabilities that reduce duplicated review and delivery work"),
    ("Adoption and talent", "Role clarity, training, change burden, support, and capacity alignment"),
    ("Measurement and learning", "Value realization, decision latency, evidence quality, reuse, and retirement"),
]
cadence_rows = [
    ("Monthly portfolio review", "Fund, Shape, Hold, Stop, remove dependencies, and reallocate capacity"),
    ("Quarterly value review", "Compare realized outcomes with investment, adoption, and operating cost"),
    ("Exception learning review", "Convert recurring exceptions into reusable policy, control, or platform work"),
    ("Talent and capacity review", "Match specialist expertise and delivery capacity to the highest-value portfolio needs"),
]

header = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Russell Dudek - Walmart 120-Day Entry Plan</title>'
    '<link rel="stylesheet" href="styles.css"></head><body class="document-body">'
    '<div class="document-actions no-print"><a href="resume.html">View Resume</a>'
    '<a href="cover-letter.html">View Cover Letter</a><a href="index.html">Candidate Vision</a>'
    '<a class="primary" href="docs/120-day-plan.pdf" download>Download PDF</a></div>'
    '<main class="document-stack">'
)
first_header = (
    '<div class="doc-header"><div><div class="doc-name">Russell Dudek</div>'
    '<div class="doc-identity">120-Day Entry Plan</div></div>'
    '<div class="doc-contact">Pittsburgh, Pennsylvania | 412.287.8640<br>'
    '<a href="mailto:russelldudek@gmail.com">russelldudek@gmail.com</a> | '
    '<a href="https://www.linkedin.com/in/russelldudek">linkedin.com/in/russelldudek</a><br>'
    '<a href="https://russelldudek.github.io/Walmart/">https://russelldudek.github.io/Walmart/</a>'
    '</div></div><div class="doc-company"><img src="assets/brand/walmart-wordmark-cropped.jpg" alt="Walmart">'
    '<span>Independent candidate vision for Walmart</span></div>'
)

page1 = (
    '<section class="sheet">' + first_header +
    '<h1 class="doc-title">Earn the right to standardize.</h1>'
    '<p class="doc-subtitle">A tactical-empathy-first entry plan for Global Governance Digital Strategy.</p>'
    '<div class="brief-callout"><h2>Days 1-30 - Listen and map</h2>'
    '<p>Build a shared, evidence-based view of decisions, work, authority, and friction before proposing a new governance mechanism.</p></div>'
    '<div class="doc-grid-2"><div>' +
    section("Primary outcome", phase_box(30, "Leadership has one map of the current portfolio and the decisions that govern it.", page1_actions)) +
    section("Questions to answer", bullets(page1_questions)) +
    '</div><aside>' + section("Stakeholder listening map", table(("Stakeholder", "What to learn"), page1_stakeholders)) +
    section("Discovery artifacts", bullets(["Decision-rights map", "Stakeholder topology", "Portfolio and spend inventory", "Use-case risk segmentation", "Workflow friction and rework map", "Control reuse map", "Adoption burden map", "Baseline scorecard"])) +
    section("Early trust signals", "<p>Clear listening notes, visible follow-through, transparent assumptions, disciplined meeting load, and removal of one avoidable operating friction without weakening a necessary control.</p>") +
    '</aside></div><div class="doc-footer"><span>120-Day Entry Plan | Russell Dudek</span><span>1 / 4</span></div></section>'
)

page2 = (
    '<section class="sheet">' + continuation_header() +
    '<h1 class="doc-title">Days 31-60 - Make decisions visible</h1>'
    '<p class="doc-subtitle">Co-design the minimum portfolio contract and decision architecture with the people who own the consequences.</p>'
    '<div class="doc-grid-2"><div>' +
    section("Primary outcome", phase_box(60, "Material AI work is visible in one portfolio view with explicit ownership and a defined next decision.", page2_actions)) +
    section("Minimum decision contract", table(("Clause", "Question made explicit"), contract_rows)) +
    '</div><aside>' + section("Decision rights to clarify", table(("Decision", "Required clarity"), decision_rows)) +
    section("Controlled-proof pair", '<div class="evidence-chip"><b>Use case A - lower-risk, high-adoption potential</b><p>Tests whether the contract accelerates a useful workflow without adding unnecessary governance load.</p></div><div class="evidence-chip"><b>Use case B - sensitive data or authority boundary</b><p>Tests whether the mechanism exposes ambiguity early enough to reshape or hold the work responsibly.</p></div>') +
    section("Exit condition", "<p>The mechanism is ready for proof when each use case has a named sponsor, accountable operating owner, explicit human decision boundary, evidence plan, and next decision date.</p>") +
    '</aside></div><div class="doc-footer"><span>120-Day Entry Plan | Make decisions visible</span><span>2 / 4</span></div></section>'
)

page3 = (
    '<section class="sheet">' + continuation_header() +
    '<h1 class="doc-title">Days 61-90 - Run controlled proof</h1>'
    '<p class="doc-subtitle">Test whether the operating mechanism improves real decisions - not whether it produces more documentation.</p>'
    '<div class="doc-grid-2"><div>' +
    section("Primary outcome", phase_box(90, "Two contrasting use cases produce evidence about decision quality, control sufficiency, adoption burden, and value.", page3_actions)) +
    section("Evidence plan", table(("Category", "Evidence sought"), evidence_rows)) +
    '</div><aside>' + section("Test sequence", '<div class="evidence-chip"><b>Before release</b><p>Confirm the decision contract, evidence threshold, human authority, fallback, owner, and monitoring plan.</p></div><div class="evidence-chip"><b>During controlled use</b><p>Observe real workflow behavior, exceptions, data handling, review load, and user workarounds.</p></div><div class="evidence-chip"><b>After evidence review</b><p>Change funding, design, control, release, ownership, or retirement based on what was learned.</p></div>') +
    section("Executive portfolio review output", bullets(["Named posture and rationale", "Accountable owner", "Next evidence requirement", "Human decision boundary", "Control or architecture dependency", "Funding or capacity implication", "Next decision date"])) +
    section("Failure modes to surface", bullets(["Approval without operating ownership", "Strong demo with weak adoption path", "Control burden disproportionate to risk", "Automation crossing an unclear human-authority boundary", "Value claim without a defensible baseline"])) +
    section("Exit condition", "<p>Evidence has changed at least one material portfolio decision and the review has identified which elements should be reused, revised, localized, or stopped.</p>") +
    '</aside></div><div class="doc-footer"><span>120-Day Entry Plan | Run controlled proof</span><span>3 / 4</span></div></section>'
)

page4 = (
    '<section class="sheet">' + continuation_header() +
    '<h1 class="doc-title">Days 91-120 - Scale the mechanism</h1>'
    '<p class="doc-subtitle">Turn proven decisions, controls, and operating practices into a two-quarter roadmap without flattening legitimate local judgment.</p>'
    '<div class="doc-grid-2"><div>' +
    section("Primary outcome", phase_box(120, "Leadership has a prioritized roadmap tied to value, trust, talent, capacity, and reusable governance capabilities.", page4_actions)) +
    section("Two-quarter roadmap workstreams", table(("Workstream", "Roadmap intent"), roadmap_rows)) +
    '</div><aside>' + section("Executive cadence", table(("Cadence", "Purpose"), cadence_rows)) +
    section("120-day deliverables", bullets(["Governance portfolio view", "Scannable AI Contract", "Risk-sensitive stage gates and decision-rights map", "Executive scorecard and review cadence", "Reusable control and evaluation library", "Two-quarter roadmap", "Learning backlog and retirement candidates"])) +
    section("Success at day 120", "<p>Leadership can see the portfolio, understand the next decision for every material initiative, distinguish value from activity, preserve substantive governance authority, and scale expertise through a small number of trusted operating mechanisms.</p>") +
    section("Continuing questions", bullets(["Did evidence change funding, design, release, ownership, or retirement?", "Which controls became reusable enterprise capabilities?", "Where does global consistency still conflict with local judgment?", "Which work should stop to release capacity?"])) +
    '</aside></div><div class="doc-footer"><span>120-Day Entry Plan | Scale the mechanism</span><span>4 / 4</span></div></section>'
)

(ROOT / "120-day-plan.html").write_text(header + page1 + page2 + page3 + page4 + "</main></body></html>", encoding="utf-8")
print("Applied campaign corrections.")
