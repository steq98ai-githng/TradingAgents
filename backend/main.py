from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
import asyncio
from typing import List
from backend.database import AsyncSessionLocal, MNQCandle, init_db
from sqlalchemy import select
from datetime import datetime
from tradingagents.graph.trading_graph import FuturesTradingGraph
from tradingagents.default_config import DEFAULT_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Futures Trader Support System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global graph instance
graph = FuturesTradingGraph(config=DEFAULT_CONFIG)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/candles")
async def get_candles(symbol: str = "MNQ", limit: int = 100):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(MNQCandle)
            .where(MNQCandle.symbol == symbol)
            .order_by(MNQCandle.timestamp.desc())
            .limit(limit)
        )
        candles = result.scalars().all()
        return [{"time": c.timestamp.isoformat(), "open": c.open, "high": c.high, "low": c.low, "close": c.close} for c in candles]

@app.post("/api/webhook/tradingview")
async def tradingview_webhook(payload: dict = Body(...)):
    logger.info(f"Received TradingView Webhook: {payload}")
    await manager.broadcast(json.dumps({"type": "WEBHOOK", "data": payload}))
    return {"status": "received"}

@app.post("/api/analyze")
async def trigger_analysis(ticker: str = "MNQ", date: str = None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Run the agent graph
    result = graph.propagate_futures(ticker, date)

    # Extract reports
    analysis_data = {
        "type": "SIGNAL",
        "ticker": ticker,
        "date": date,
        "market_report": result.get("market_report"),
        "futures_report": result.get("futures_assistant_report"),
        "risk_report": result.get("risk_management_report"),
        "risk_status": result.get("risk_status"),
        "trader_plan": result.get("trader_investment_plan")
    }

    await manager.broadcast(json.dumps(analysis_data))
    return analysis_data

@app.post("/api/order/confirm")
async def confirm_order(order: dict = Body(...)):
    logger.info(f"Order confirmed by user: {order}")
    return {"status": "success", "order_id": "sim-12345"}

@app.websocket("/ws/market")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming commands if any
    except WebSocketDisconnect:
        manager.disconnect(websocket)
