from langgraph.graph import StateGraph
from typing import TypedDict

from services.classifier.agent import classify_query
from services.retriever.rag import retrieve_docs
from services.responder.agent import generate_response


class GraphState(TypedDict):
    query: str
    intent: str
    docs: list
    response: str


# 🔹 Nodes

def classifier_node(state: GraphState):
    state["intent"] = classify_query(state["query"])
    return state


def retriever_node(state: GraphState):
    state["docs"] = retrieve_docs(state["query"])
    return state


def responder_node(state: GraphState):
    state["response"] = generate_response(
        state["query"],
        state["docs"]
    )
    return state


# 🔹 Build Graph

builder = StateGraph(GraphState)

builder.add_node("classifier", classifier_node)
builder.add_node("retriever", retriever_node)
builder.add_node("responder", responder_node)

builder.set_entry_point("classifier")

builder.add_edge("classifier", "retriever")
builder.add_edge("retriever", "responder")

graph = builder.compile()