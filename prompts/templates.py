EXTRACT_KEY_POINTS_PROMPT = """You are a senior business analyst.
Read the project document below and extract the most important information into clean bullet points.

Cover:
- The core problem being solved
- Key features requested
- Target users
- Any constraints (budget, timeline, team size)
- Any concerns or risks raised

Be concise. Use bullet points only. No preamble.

DOCUMENT:
{raw_text}
"""

FUNCTIONAL_REQUIREMENTS_PROMPT = """You are a senior business analyst.
Based on the key points below, write a numbered list of clear functional requirements.

Rules:
- Each requirement starts with "The system shall..."
- Be specific and measurable where possible
- Cover every feature and concern mentioned in the key points
- No preamble, no explanation, just the numbered list

KEY POINTS:
{key_points}
"""

USER_STORIES_PROMPT = """You are a senior product manager.
Based on the key points and functional requirements below, write user stories.

Format each story exactly as:
As a [user type], I want [goal], so that [reason].

Rules:
- Cover all major user types (customer, admin, etc.)
- One story per line
- No preamble, no numbering, no extra commentary

KEY POINTS:
{key_points}

FUNCTIONAL REQUIREMENTS:
{functional_requirements}
"""

TECH_STACK_PROMPT = """You are a senior software architect.
Based on the project key points and functional requirements below, recommend a tech stack.

Format:
**Frontend:** [choice] — [one sentence justification]
**Backend:** [choice] — [one sentence justification]
**Database:** [choice] — [one sentence justification]
**Hosting:** [choice] — [one sentence justification]
**Key Services:** [choice] — [one sentence justification]

Rules:
- Justify each choice based on the actual project needs
- Prioritize cost-effectiveness and scalability
- No preamble

KEY POINTS:
{key_points}

FUNCTIONAL REQUIREMENTS:
{functional_requirements}
"""

TIMELINE_PROMPT = """You are an experienced project manager.
Before writing the timeline, scan the key points and raw text for any stated timeline constraints or MVP-first preferences.

If a timeline constraint IS found:
- Start with one sentence explaining your reasoning
- Then produce TWO sections:

**MVP / Phase 1 — [duration]**
Scope: [what's included and excluded]
- [phase]: [duration] — [description]

**Phase 2 (Post-Launch) — [duration]**
Scope: [remaining features]
- [phase]: [duration] — [description]

If NO constraint is found, produce the standard five phases:
**Phase 1 — Planning & Discovery:** [duration] — [description]
**Phase 2 — Design & Architecture:** [duration] — [description]
**Phase 3 — Development:** [duration] — [description]
**Phase 4 — Testing & QA:** [duration] — [description]
**Phase 5 — Deployment & Launch:** [duration] — [description]

Rules:
- Durations in weeks
- Base estimates on actual scope
- No extra commentary

KEY POINTS:
{key_points}

RAW TEXT:
{raw_text}

FUNCTIONAL REQUIREMENTS:
{functional_requirements}

TECH STACK:
{tech_stack}
"""