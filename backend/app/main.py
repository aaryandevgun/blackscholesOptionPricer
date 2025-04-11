from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from scipy.stats import norm
import asyncio
import json
from typing import List, Optional, Dict
import random
import time

app = FastAPI(title="Options Pricing API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class OptionParams(BaseModel):
    spot_price: float
    strike_price: float
    time_to_maturity: float  # in years
    risk_free_rate: float
    volatility: float
    option_type: str  # "call" or "put"
    call_purchase_price: Optional[float] = None
    put_purchase_price: Optional[float] = None

class OptionPrice(BaseModel):
    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    call_pnl: Optional[float] = None
    put_pnl: Optional[float] = None

class HeatMapData(BaseModel):
    spot_prices: List[float]
    volatilities: List[float]
    call_values: List[List[float]]
    put_values: List[List[float]]
    call_pnl: List[List[float]]
    put_pnl: List[List[float]]

# Black-Scholes implementation
def black_scholes(params: OptionParams) -> OptionPrice:
    S = params.spot_price
    K = params.strike_price
    T = params.time_to_maturity
    r = params.risk_free_rate
    sigma = params.volatility
    option_type = params.option_type.lower()

    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    else:  # put
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1

    # Calculate Greeks
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
             r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2))
    vega = S * np.sqrt(T) * norm.pdf(d1)
    rho = K * T * np.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2)

    # Calculate P&L if purchase prices are provided
    call_pnl = None
    put_pnl = None
    if params.call_purchase_price is not None:
        call_pnl = price - params.call_purchase_price if option_type == "call" else None
    if params.put_purchase_price is not None:
        put_pnl = price - params.put_purchase_price if option_type == "put" else None

    return OptionPrice(
        price=float(price),
        delta=float(delta),
        gamma=float(gamma),
        theta=float(theta),
        vega=float(vega),
        rho=float(rho),
        call_pnl=call_pnl,
        put_pnl=put_pnl
    )

# Generate heat map data
def generate_heat_map_data(params: OptionParams) -> HeatMapData:
    # Generate ranges for spot prices and volatilities
    spot_range = np.linspace(params.spot_price * 0.5, params.spot_price * 1.5, 20)
    vol_range = np.linspace(0.1, 0.5, 20)
    
    call_values = []
    put_values = []
    call_pnl = []
    put_pnl = []
    
    for vol in vol_range:
        call_row = []
        put_row = []
        call_pnl_row = []
        put_pnl_row = []
        
        for spot in spot_range:
            # Calculate call option
            call_params = OptionParams(
                spot_price=spot,
                strike_price=params.strike_price,
                time_to_maturity=params.time_to_maturity,
                risk_free_rate=params.risk_free_rate,
                volatility=vol,
                option_type="call",
                call_purchase_price=params.call_purchase_price
            )
            call_result = black_scholes(call_params)
            call_row.append(call_result.price)
            call_pnl_row.append(call_result.call_pnl if call_result.call_pnl is not None else 0)
            
            # Calculate put option
            put_params = OptionParams(
                spot_price=spot,
                strike_price=params.strike_price,
                time_to_maturity=params.time_to_maturity,
                risk_free_rate=params.risk_free_rate,
                volatility=vol,
                option_type="put",
                put_purchase_price=params.put_purchase_price
            )
            put_result = black_scholes(put_params)
            put_row.append(put_result.price)
            put_pnl_row.append(put_result.put_pnl if put_result.put_pnl is not None else 0)
        
        call_values.append(call_row)
        put_values.append(put_row)
        call_pnl.append(call_pnl_row)
        put_pnl.append(put_pnl_row)
    
    return HeatMapData(
        spot_prices=spot_range.tolist(),
        volatilities=vol_range.tolist(),
        call_values=call_values,
        put_values=put_values,
        call_pnl=call_pnl,
        put_pnl=put_pnl
    )

# Mock market data generator
async def generate_market_data():
    while True:
        yield {
            "timestamp": time.time(),
            "spot_price": random.uniform(90, 110),
            "strike_price": 100,
            "time_to_maturity": random.uniform(0.1, 1.0),
            "risk_free_rate": 0.05,
            "volatility": random.uniform(0.1, 0.4),
            "option_type": random.choice(["call", "put"])
        }
        await asyncio.sleep(1)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# REST API endpoints
@app.post("/pricing", response_model=OptionPrice)
async def calculate_option_price(params: OptionParams):
    return black_scholes(params)

@app.post("/heatmap", response_model=HeatMapData)
async def get_heat_map_data(params: OptionParams):
    return generate_heat_map_data(params)

# WebSocket endpoint for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        async for market_data in generate_market_data():
            params = OptionParams(**market_data)
            price_data = black_scholes(params)
            await websocket.send_json({
                "market_data": market_data,
                "pricing": price_data.dict()
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 