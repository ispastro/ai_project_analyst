import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import RateLimitError
from pipeline.state import ProjectState
from prompts.templates import (
    EXTRACT_KEY_POINTS_PROMPT,
    FUNCTIONAL_REQUIREMENTS_PROMPT,
    USER_STORIES_PROMPT,
    TECH_STACK_PROMPT,
    TIMELINE_PROMPT,
)

load_dotenv()

llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    timeout=60,
)


def invoke_with_retry(prompt, max_retries=5, base_wait=10):
    """Call the LLM, retrying on 429 rate limits with backoff."""
    for attempt in range(1, max_retries + 1):
        try:
            return llm.invoke(prompt)
        except RateLimitError as e:
            wait = base_wait * attempt
            try:
                wait = e.response.json()["error"]["metadata"].get("retry_after_seconds", wait)
            except Exception:
                pass
            print(f"   ⚠ Rate limited (attempt {attempt}/{max_retries}), waiting {wait:.0f}s...")
            time.sleep(wait)
    raise RuntimeError("Exceeded max retries due to repeated rate limiting.")


def extract_key_points(state: ProjectState) -> ProjectState:
    print("→ Extracting key points...")
    prompt = EXTRACT_KEY_POINTS_PROMPT.format(raw_text=state["raw_text"])
    response = invoke_with_retry(prompt)
    return {"key_points": response.content}


def generate_requirements(state: ProjectState) -> ProjectState:
    print("→ Generating functional requirements...")
    prompt = FUNCTIONAL_REQUIREMENTS_PROMPT.format(key_points=state["key_points"])
    response = invoke_with_retry(prompt)
    return {"functional_requirements": response.content}


def generate_user_stories(state: ProjectState) -> ProjectState:
    print("→ Generating user stories...")
    prompt = USER_STORIES_PROMPT.format(
        key_points=state["key_points"],
        functional_requirements=state["functional_requirements"],
    )
    response = invoke_with_retry(prompt)
    return {"user_stories": response.content}


def suggest_tech_stack(state: ProjectState) -> ProjectState:
    print("→ Suggesting tech stack...")
    prompt = TECH_STACK_PROMPT.format(
        key_points=state["key_points"],
        functional_requirements=state["functional_requirements"],
    )
    response = invoke_with_retry(prompt)
    return {"tech_stack": response.content}


def estimate_timeline(state: ProjectState) -> ProjectState:
    print("→ Estimating timeline...")
    prompt = TIMELINE_PROMPT.format(
        key_points=state["key_points"],
        raw_text=state["raw_text"][:3000],
        functional_requirements=state["functional_requirements"],
        tech_stack=state["tech_stack"],
    )
    response = invoke_with_retry(prompt)
    return {"timeline": response.content}