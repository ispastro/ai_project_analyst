# AI Project Analyst

An AI-powered pipeline that turns a rough, unstructured project brief into a complete, structured project analysis — automatically generating key points, functional requirements, user stories, a recommended tech stack, and a delivery timeline.

Built as an agentic workflow using **LangGraph**, orchestrating multiple LLM-driven steps that each build on the output of the last.

---

## What It Does

Given nothing more than a plain-text project description (the kind a client might paste into a Slack message or an Upwork brief), the pipeline runs it through five sequential analysis stages:

1. **Key Points Extraction** — Distills the raw input into core problem statement, features, target users, constraints, and risks.
2. **Functional Requirements** — Converts key points into clear, testable "the system shall..." requirements.
3. **User Stories** — Generates role-based user stories (customer, admin, driver, etc.) tied to the requirements.
4. **Tech Stack Recommendation** — Suggests a frontend, backend, database, hosting, and supporting services, with reasoning for each choice.
5. **Timeline Estimation** — Produces a phased delivery plan (e.g. MVP vs. post-launch) that respects any stated deadline or team constraints.

Each stage feeds its output into the next, so the final result is coherent and grounded in the original brief — not five disconnected LLM calls.

---

## How It Works

The pipeline is built as a directed graph using **LangGraph**, where each node is a discrete analysis step:

```
raw_text
   │
   ▼
extract_key_points
   │
   ▼
generate_requirements
   │
   ▼
generate_user_stories
   │
   ▼
suggest_tech_stack
   │
   ▼
estimate_timeline
```

State (key points, requirements, tech stack, etc.) is passed between nodes via a shared `ProjectState` object, so later steps have full context from everything generated before them.

The LLM calls are wrapped with automatic **retry-with-backoff** logic, so transient rate limits or timeouts don't crash the pipeline — it waits and retries before giving up.

### Tech Used

| Component        | Choice                          |
|-------------------|----------------------------------|
| Orchestration      | LangGraph                       |
| LLM interface       | LangChain (`ChatOpenAI`-compatible client) |
| LLM provider         | Groq (`llama-3.3-70b-versatile`) |
| Config/env           | `python-dotenv`                 |
| Package management   | `uv`                             |

---

## Project Structure

```
AI_project_Analyst/
├── main.py                  # Entry point — runs the pipeline
├── pipeline/
│   ├── graph.py              # Defines the LangGraph workflow
│   ├── nodes.py               # Each analysis step (LLM calls + prompts)
│   └── state.py                # Shared state schema
├── prompts/
│   └── templates.py             # Prompt templates for each stage
├── .env                          # API keys (not committed)
├── pyproject.toml
└── uv.lock
```

---

## Setup

**1. Clone and install dependencies**

```bash
git clone <repo-url>
cd AI_project_Analyst
uv sync
```

**2. Add your API key**

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com/keys](https://console.groq.com/keys).

**3. Run the pipeline**

```bash
uv run main.py
```

By default, `main.py` runs against a sample project brief defined in the script. Swap in your own `raw_text` to analyze a different project.

---

## Sample Output

**Input:** A grocery delivery app brief — multi-store browsing, real-time inventory, scheduled delivery, driver notifications, live tracking, 3–4 month timeline, small team with no in-house developers.

**Output (abridged):**

```
--- KEY POINTS ---
Core problem: building a mobile-first grocery delivery platform
Key features: browse multiple stores, real-time inventory, scheduled
delivery windows, driver notifications, payment support, live order
tracking, push notifications, store owner dashboard
Constraints: 3-4 month timeline, small team, no in-house developers

--- FUNCTIONAL REQUIREMENTS ---
1. The system shall allow users to browse products from a minimum
   of 5 different stores on initial launch.
2. The system shall provide real-time inventory updates, refreshing
   data at least every 15 minutes.
   ...

--- USER STORIES ---
As a customer, I want to browse products from multiple stores,
so that I can compare prices and find the best deals.
   ...

--- TECH STACK ---
Frontend: React Native
Backend: Node.js with Express
Database: MongoDB
Hosting: AWS
Key Services: Firebase Cloud Messaging, Stripe
   ...

--- TIMELINE ---
MVP / Phase 1 — 16 weeks (core features)
Phase 2 (Post-Launch) — 8 weeks (dashboard, push notifications)
```

The full pipeline runs end-to-end in well under a minute.

---

## Why This Approach

Client briefs are often informal, incomplete, or high-level. This tool bridges that gap by turning a loose description into the structured documentation a dev team actually needs to start building — requirements, stories, stack, and timeline — without manual back-and-forth, and in a fraction of the time it would take to do by hand.

---

## Possible Extensions

- Export results directly to Markdown/PDF/Notion for client-ready deliverables
- Add a RAG layer to ground suggestions in a company's existing tech standards or past projects
- Swap in different LLMs per stage (e.g. a stronger model for requirements, faster model for user stories)
- Wrap in a simple web UI for non-technical client use