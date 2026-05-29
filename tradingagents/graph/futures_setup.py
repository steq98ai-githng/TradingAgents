from typing import Any, Dict
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from tradingagents.agents import *
from tradingagents.agents.utils.agent_states import FuturesAgentState

class FuturesGraphSetup:
    def __init__(self, quick_thinking_llm, deep_thinking_llm, tool_nodes):
        self.quick_thinking_llm = quick_thinking_llm
        self.deep_thinking_llm = deep_thinking_llm
        self.tool_nodes = tool_nodes

    def setup_graph(self):
        workflow = StateGraph(FuturesAgentState)

        # Nodes
        workflow.add_node("Market Analyst", create_market_analyst(self.quick_thinking_llm))
        workflow.add_node("News Analyst", create_news_analyst(self.quick_thinking_llm))
        workflow.add_node("Gemini Assistant", create_gemini_futures_assistant(self.quick_thinking_llm))
        workflow.add_node("Trader", create_trader(self.quick_thinking_llm))
        workflow.add_node("Topstep Risk Manager", create_topstep_risk_manager(self.quick_thinking_llm))

        # Edges
        workflow.add_edge(START, "Market Analyst")
        workflow.add_edge("Market Analyst", "News Analyst")
        workflow.add_edge("News Analyst", "Gemini Assistant")
        workflow.add_edge("Gemini Assistant", "Trader")
        workflow.add_edge("Trader", "Topstep Risk Manager")
        workflow.add_edge("Topstep Risk Manager", END)

        return workflow
