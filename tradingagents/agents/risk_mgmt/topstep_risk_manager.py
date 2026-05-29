from tradingagents.agents.utils.agent_utils import get_language_instruction

def create_topstep_risk_manager(llm):
    def risk_manager_node(state):
        # Topstep 50k Account Rules
        DLL_LIMIT = 1000.0  # Daily Loss Limit
        MLL_LIMIT = 2000.0  # Max Loss Limit (Trailing Drawdown usually, but simplified here)

        # In a real system, these would come from the account balance service
        current_daily_pnl = state.get("current_daily_pnl", 0.0)
        current_max_drawdown = state.get("current_max_drawdown", 0.0)

        trader_plan = state.get("trader_investment_plan", "No plan yet.")

        prompt = f"""You are the Topstep Risk Manager. Your job is to enforce the following rules for the 50k Trading Combine:
1. Daily Loss Limit (DLL): -${DLL_LIMIT}
2. Maximum Loss Limit (MLL): -${MLL_LIMIT}

Current Account Status:
- Daily PnL: ${current_daily_pnl}
- Current Max Drawdown: ${current_max_drawdown}

Trader's Proposed Action:
{trader_plan}

Your Tasks:
1. Calculate if the proposed trade risks breaching the DLL or MLL.
2. Provide a 'Risk Status' (GREEN/YELLOW/RED).
3. If RED, strictly advise against the trade.
4. If YELLOW, suggest reducing position size.

Respond with a 'Topstep Risk Report'.
""" + get_language_instruction()

        response = llm.invoke(prompt)

        return {
            "messages": [response],
            "risk_management_report": response.content,
            "risk_status": "RED" if current_daily_pnl <= -DLL_LIMIT else "GREEN"
        }

    return risk_manager_node
