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
