from typing import Annotated, Any
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.analysis.tools.rank_categories import rank_categories
from src.analysis.tools.compare_groups import compare_groups
from src.analysis.tools.calculate_contribution import calculate_contribution
from src.analysis.tools.descriptive_statistics import descriptive_statistics
from src.analysis.tools.distribution_statistics import distribution_statistics
from src.analysis.tools.analyze_trend import analyze_trend
from src.analysis.tools.calculate_change import calculate_change
from src.analysis.tools.detect_outliers import detect_outliers
from src.analysis.tools.correlation_analysis import correlation_analysis
from src.analysis.tools.group_statistics import group_statistics
from src.analysis.tools.top_bottom_analysis import top_bottom_analysis
from src.analysis.tools.percentage_change_analysis import percentage_change_analysis
from src.analysis.tools.share_distribution import share_distribution
from src.analysis.tools.frequency_analysis import frequency_analysis

from src.llm.models.groq import GroqModel


class AnalysisState(TypedDict):
    user_query: str
    rows: list[dict[str, Any]]
    columns: list[str]
    messages: Annotated[list[AnyMessage], add_messages]


ANALYSIS_TOOLS = [
    rank_categories,
    compare_groups,
    calculate_contribution,
    descriptive_statistics,
    distribution_statistics,
    analyze_trend,
    calculate_change,
    detect_outliers,
    correlation_analysis,
    group_statistics,
    top_bottom_analysis,
    percentage_change_analysis,
    share_distribution,
    frequency_analysis,
]


analysis_tool_node = ToolNode(ANALYSIS_TOOLS)


SYSTEM_PROMPT = """
You are NEXA's data analysis agent.

Answer analytical questions using the supplied SQL query results.

Rules:
1. Use available analysis tools when calculations or comparisons are needed.
2. Dataset rows are supplied through graph state and injected into tools.
3. Never invent numbers, statistics, or findings.
4. Base conclusions on tool outputs and supplied data.
5. Choose the tool best suited to the user's question.
6. If the available tools cannot answer the question, explain the limitation.
7. Keep the final answer clear, accurate, and relevant.
8. Do not execute SQL or modify the SQL query pipeline.
"""


llm_provider = GroqModel()
llm = llm_provider.model.bind_tools(ANALYSIS_TOOLS)


def analysis_agent(state: AnalysisState) -> dict[str, Any]:
    """Ask the LLM to answer the question or select an analysis tool."""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm.invoke(messages)

    return {"messages": [response]}


builder = StateGraph(AnalysisState)

builder.add_node("agent", analysis_agent)
builder.add_node("tools", analysis_tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "agent")

analysis_graph = builder.compile()
