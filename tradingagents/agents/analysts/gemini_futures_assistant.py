from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.agents.utils.agent_utils import (
    get_language_instruction,
)

def create_gemini_futures_assistant(llm):
    def futures_assistant_node(state):
        current_date = state["trade_date"]
        company_of_interest = state["company_of_interest"]

        # In a real scenario, we'd fetch actual MNQ data from our TSDB here
        # For now, we rely on the state and context
        market_report = state.get("market_report", "No market report available.")
        news_report = state.get("news_report", "No news report available.")
        sentiment_report = state.get("sentiment_report", "No sentiment report available.")

        system_message = (
            f"""You are the Gemini Futures Assistant, an expert in CME Micro E-mini Nasdaq-100 (MNQ) intraday trading.
Your goal is to analyze the technical chart patterns, order flow dynamics (simulated), and news sentiment to provide actionable intraday trading hints.

Context:
- Market: MNQ (Nasdaq-100 Futures)
- Date: {current_date}

Current Analysis Summary:
Technical: {market_report}
News: {news_report}
Sentiment: {sentiment_report}

Tasks:
1. Analyze the technical trend specifically for MNQ volatility.
2. Identify potential intraday support and resistance levels.
3. Provide a 'Market Hint' (e.g., Bullish Divergence spotted, Resistance at 18600 holding).
4. Combine news sentiment to warn about upcoming economic releases (e.g., FOMC, CPI) that might impact MNQ.

Output a concise 'Futures Assistant Report' with a 'Recommendation Hint' for the trader.
""" + get_language_instruction()
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt | llm
        result = chain.invoke(state)

        return {
            "messages": [result],
            "futures_assistant_report": result.content,
        }

    return futures_assistant_node
