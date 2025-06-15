# 📚 Book Recommender using LangGraph + Google Gemini

An interactive book recommendation system built using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and Google Gemini (Generative AI). This system breaks down natural language queries into actionable steps, retrieves real-time book data from the Google Books API, ranks them, and recommends the top results to the user — all via a simple Streamlit interface.

---

## 🚀 Features

- 🔍 Understands free-form user queries like “Suggest the best horror book”
- 🧠 Plans tasks dynamically using agentic workflows with Gemini
- 📚 Fetches real book data using Google Books API
- ⭐ Filters and ranks by ratings
- 🧾 Presents the top recommended titles
- 💬 Interactive UI with [Streamlit](https://streamlit.io)
- 🔐 Accepts user-provided API key at runtime — no hardcoding needed

---

## 🧰 Tech Stack

| Layer       | Tool                         |
|-------------|------------------------------|
| 🖥️ UI        | Streamlit                    |
| 🧠 Planner   | Gemini via LangChain         |
| ⚙️ Workflow  | LangGraph                    |
| 📚 Data API  | Google Books API             |
| 💻 Language  | Python                       |

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/book-recommender.git
cd book-recommender
```

### 2. Install Dependencies

Make sure you have Python 3.9 or higher installed.

Then install all required packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Get a Google Generative AI API Key

- Visit: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Generate your free API key and copy it

---

### 4. Run the Application

Launch the Streamlit app with the following command:

```bash
streamlit run app1.py
```

When the app opens in your browser:

  🔐 Paste your Google API key into the input field

  💬 Enter your book request (e.g. “Suggest the best mystery book”)

  ✅ View your top recommendations instantly

---

## ✅ Task Coverage & Evaluation

This project was built as part of an assignment to implement an agentic workflow using LangGraph. Below is a self-evaluation of how it meets the stated requirements:

| **Task Requirement**                                      | **Our Implementation**                                                                         | ✅ Status    |
|-----------------------------------------------------------|------------------------------------------------------------------------------------------------|-------------|
| **Use LangGraph**                                         | ✔ Used `StateGraph` from `langgraph.graph` with planner and executor nodes                     | ✅           |
| **Use a PlanAgent to split user query into sub-tasks**    | ✔ `plan_agent(user_query)` uses Gemini model to generate a structured task plan                | ✅           |
| **Iteratively refine and solve tasks using ToolAgent**    | ✔ `tool_node` + `dynamic_tool_agent()` handle task-by-task execution with context updates      | ✅           |
| **Implement feedback loops / reflection for reliability** | ⚠️ Basic iterative execution is implemented; **no advanced reflection or retry logic** present | ⚠️ Partial  |
| **Use any LLM and tools of your choice**                  | ✔ Used Google Gemini + Google Books API                                                        | ✅           |
| **LangGraph integration for task & tool management**      | ✔ Full task-tool separation via planner and executor in LangGraph                              | ✅           |
| **Modularity and code readability**                       | ✔ Modular functions like `fetch_books`, `tool_agent`, `plan_node` are all well-scoped          | ✅           |
| **Documentation**                                         | ✔ Full inline documentation and markdown README provided                                       | ✅           |
| **Video explanation**                                     | ✔ [Available here](#video-demo-link)                                                           | ✅           |
| **Hosted Solution**                                       | ✔                                                                                              | ✅           |

---

