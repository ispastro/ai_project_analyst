import os
from dotenv import load_dotenv
from pipeline.graph import build_graph

load_dotenv()

test_input = """
Project: FreshCart - Grocery Delivery App
We want to build a mobile-first grocery delivery platform.
Key features: browse multiple stores, real-time inventory, 
scheduled delivery windows, driver notifications, store owner dashboard,
payment support, live order tracking, push notifications.
Client wants to launch MVP within 3-4 months.
Small team, no in-house developers.
"""

graph = build_graph()

print("Running pipeline...\n")
result = graph.invoke({"raw_text": test_input})

print("\n--- KEY POINTS ---")
print(result["key_points"])
print("\n--- FUNCTIONAL REQUIREMENTS ---")
print(result["functional_requirements"])
print("\n--- USER STORIES ---")
print(result["user_stories"])
print("\n--- TECH STACK ---")
print(result["tech_stack"])
print("\n--- TIMELINE ---")
print(result["timeline"])