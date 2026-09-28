import sqlite3
from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
def validate_sql_query(query: str) -> bool:
    query_upper = query.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False
    return True

def execute_query(query: str):
    if not validate_sql_query(query):
        return "Error: Security violation. Dangerous SQL keywords detected."
    
    conn = sqlite3.connect("file:olist.db?mode=ro", uri=True)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

class AgentState(TypedDict):
    question: str
    sql_query: str
    query_result: str
    final_answer: str

def query_executor_node(state: AgentState):
    query = state["sql_query"]
    result = execute_query(query)
    return {"query_result": str(result)}

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0, max_tokens=200)

def sql_generator_node(state: AgentState):
    question = state["question"]
    prompt = f"""Write a single SQLite query for table 'orders' to answer: {question}.
Columns available in 'orders': order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date.
Return ONLY the raw SQL query, with no markdown or backticks."""
    response = llm.invoke(prompt)
    query_text = response.content[0]["text"] if isinstance(response.content, list) else response.content
    return {"sql_query": query_text.strip()}

def response_generator_node(state: AgentState):
    question = state["question"]
    result = state["query_result"]
    prompt = f"Answer the user's question: '{question}' based on this database result: {result}. Keep it concise and factual."
    response = llm.invoke(prompt)
    answer_text = response.content[0]["text"] if isinstance(response.content, list) else response.content
    return {"final_answer": answer_text.strip()}

workflow = StateGraph(AgentState)

workflow.add_node("sql_generator", sql_generator_node)
workflow.add_node("query_executor", query_executor_node)
workflow.add_node("response_generator", response_generator_node)

workflow.add_edge(START, "sql_generator")
workflow.add_edge("sql_generator", "query_executor")
workflow.add_edge("query_executor", "response_generator")
workflow.add_edge("response_generator", END)

agent_app = workflow.compile()

initial_state = {
    "question": "How many orders are canceled?",
    "sql_query": "",
    "query_result": "",
    "final_answer": ""
}

final_output = agent_app.invoke(initial_state)

print("\n--- FINAL AGENT WORKFLOW RESULT ---")
print("Generated SQL:", final_output["sql_query"])
print("Query Result:", final_output["query_result"])
print("Final Answer:", final_output["final_answer"])
