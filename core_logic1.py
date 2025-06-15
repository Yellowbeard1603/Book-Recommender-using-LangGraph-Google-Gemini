# === Standard Library Imports ===

import os
import re
import ast
import requests
from typing import TypedDict, List, Dict, Any

# === LangGraph & LangChain Imports ===
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, END
import google.generativeai as genai

# === Global LLM Instance (injected from Streamlit/app.py) ===
llm1 = None

def set_llm(model):
    """
    Sets the global llm1 variable to the given LLM model instance.
    This is used to inject the model from outside (e.g., Streamlit UI).
    """
    global llm1
    llm1 = model


# === Shared State Object ===
class BookState(TypedDict, total=False):
    user_query: str
    plan: List[Dict[str, Any]]
    current_step: int
    done: bool
    books: List[Dict[str, Any]]
    filtered_books: List[Dict[str, Any]]
    top_book: Dict[str, Any]
    presentation: List[str]
    
# === Planning Agent ===
def plan_agent(user_query: str) -> list:
    """
    Uses the injected LLM (llm1) to break down a user query
    into an ordered list of 3 high-level tasks.
    """
    global llm1
    if llm1 is None:
        raise ValueError("LLM is not initialized. Please set llm1 before calling plan_agent().")

    prompt = (
        "You are an AI workflow planner.\n"
        "Given a user's request, break it down into an ordered list of steps.\n"
        "Each step should be a dictionary with a single 'task' key, and only include extra keys if absolutely required for that specific step.\n"
        "Do NOT add redundant references (like 'book': 'found_book') if there's clearly only one book or one main object in the workflow.\n"
        "Example:\n"
        "[\n"
        "  {'task': 'Query a book database or API for science fiction books.'},\n"
        "  {'task': 'Filter the results to identify books with high ratings.'},\n"
        "  {'task': 'Present the book with the highest overall score based on the ranking criteria as the suggested best science fiction book.'}\n"
        "]\n"
        "Output your response strictly as a Python list of dictionaries.\n"
        f'User request: "{user_query}"\n'
        "Tasks:"
    )
    response = llm1.invoke(prompt)
    plan_str = response.content.strip()

    match = re.search(r'\[.*\]', plan_str, re.DOTALL)
    if match:
        plan_str = match.group(0)
    try:
        plan = ast.literal_eval(plan_str)
        assert isinstance(plan, list)
        return plan
    except Exception as e:
        print("Could not parse LLM response. Got:", plan_str)
        raise e
    
# === Book Data Fetcher ===
def fetch_books(subject, max_results=10):
    """
    Queries Google Books API to retrieve books for a specific subject/genre.
    Returns a list of book metadata dictionaries.
    """
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"subject:{subject}",
        "maxResults": max_results,
        "printType": "books",
        "orderBy": "relevance"
    }
    response = requests.get(url, params=params)
    data = response.json()
    items = data.get("items", [])
    if not items:
        return []

    books = []
    for book in items:
        info = book.get("volumeInfo", {})
        snippet = book.get("searchInfo", {}).get("textSnippet", "No review snippet found.")
        books.append({
            "title": info.get("title", "N/A"),
            "authors": info.get("authors", ["N/A"]),
            "description": info.get("description", "No summary found."),
            "averageRating": info.get("averageRating", 0),
            "ratingsCount": info.get("ratingsCount", 0),
            "publishedDate": info.get("publishedDate", ""),
            "categories": info.get("categories", []),
            "snippet": snippet,
            "infoLink": info.get("infoLink", ""),
        })
    return books

# === Genre Extractor ===
def extract_subject_from_query(query: str) -> str:
    """
    Parses the user query to determine the genre/subject of interest.
    Falls back to 'fiction' if no known subject matches.
    """
    # Map of canonical subject → list of possible phrases
    subject_keywords = {
        "science fiction": ["science fiction", "sci-fi", "sci fi"],
        "fantasy": ["fantasy"],
        "thriller": ["thriller", "suspense"],
        "romance": ["romance", "love story", "romantic"],
        "mystery": ["mystery", "detective", "whodunit"],
        "non-fiction": ["non-fiction", "nonfiction", "real story"],
        "history": ["history", "historical"],
        "horror": ["horror", "scary", "ghost"],
        "biography": ["biography", "life of", "memoir"],
        "self-help": ["self-help", "motivation", "inspirational"],
        "young adult": ["young adult", "ya"],
        "poetry": ["poetry", "poems"],
        "philosophy": ["philosophy", "thinking", "ethics"],
        "comedy": ["comedy", "funny", "humor"],
        "drama": ["drama"],
        "historical fiction": ["historical fiction", "period drama"]
    }

    # Clean and lowercase the query
    query_clean = re.sub(r'[^\w\s]', '', query.lower())

    for subject, keywords in subject_keywords.items():
        for phrase in keywords:
            if phrase in query_clean:
                return subject

    # Log if nothing found
    print("[WARN] No genre matched in query → Falling back to 'fiction'")
    return "fiction"
    

# === Planner Node (LangGraph) ===
def plan_node(state: BookState) -> BookState:
    """
    LangGraph node that generates a task plan using the LLM.
    """
    plan = plan_agent(state.get("user_query", ""))
    return {
        **state,
        "plan": plan,
        "current_step": 0,
        "done": False
    }

# === Tool Executor Node (LangGraph) ===
def dynamic_tool_agent(task_dict: Dict[str, Any], state: BookState) -> (Any, BookState):
    """
    Executes a single task step from the plan based on task keywords.
    Updates state accordingly.
    """
    
    task = task_dict["task"].lower()

    # Extract subject from user query
    user_query = state.get("user_query", "")
    subject = extract_subject_from_query(user_query)
    print(f"[DEBUG] Extracted subject: {subject}")

    # Step 1: Fetch books
    if "query" in task or "search" in task or "find books" in task:
        books = fetch_books(subject=subject)
        state["books"] = [{"title": b["title"], "authors": b["authors"], "averageRating": b.get("averageRating", 0)} for b in books]
        return books, state

    # Step 2: Filter and sort by rating
    elif "filter" in task or "rating" in task or "top rated" in task:
        books = state.get("books", [])
        filtered = sorted(books, key=lambda b: b.get("averageRating", 0), reverse=True)
        state["filtered_books"] = [{"title": b["title"], "authors": b["authors"]} for b in filtered]
        return filtered, state

    # Step 3: Present top 2
    elif "present" in task or "suggest" in task or "recommend" in task:
        filtered = state.get("filtered_books", [])
        state["presentation"] = [b["title"] for b in filtered[:5]] if filtered else []
        state["top_book"] = filtered[0] if filtered else {}
        return state["presentation"], state

    else:
        return None, state


# === Node Wrapper (LangGraph) ===
def tool_node(state: BookState) -> BookState:
    """
    LangGraph node that runs one task at a time using dynamic_tool_agent.
    Increments step and marks 'done' when plan is complete.
    """
    plan = state["plan"]
    current_step = state["current_step"]

    if current_step >= len(plan):
        return {**state, "done": True}

    task = plan[current_step]
    _, updated_state = dynamic_tool_agent(task, state)
    updated_state["current_step"] = current_step + 1
    updated_state["done"] = updated_state["current_step"] >= len(plan)

    return updated_state

from langgraph.graph import StateGraph, END

# === LangGraph Workflow Definition ===
graph = StateGraph(BookState)
graph.add_node("planner", plan_node)
graph.add_node("executor", tool_node)

graph.add_edge("planner", "executor")
graph.add_conditional_edges("executor", lambda s: END if s.get("done") else "executor")
graph.set_entry_point("planner")

# Final compiled LangGraph app
app = graph.compile()

