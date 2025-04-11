from fastapi.testclient import TestClient
from main import app, black_scholes, OptionParams
import pytest

client = TestClient(app)

def test_black_scholes_call():
    params = OptionParams(
        spot_price=100,
        strike_price=100,
        time_to_maturity=1.0,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="call"
    )
    result = black_scholes(params)
    assert result.price > 0
    assert -1 <= result.delta <= 1
    assert result.gamma > 0
    assert result.vega > 0

def test_black_scholes_put():
    params = OptionParams(
        spot_price=100,
        strike_price=100,
        time_to_maturity=1.0,
        risk_free_rate=0.05,
        volatility=0.2,
        option_type="put"
    )
    result = black_scholes(params)
    assert result.price > 0
    assert -1 <= result.delta <= 0
    assert result.gamma > 0
    assert result.vega > 0

def test_pricing_endpoint():
    response = client.post(
        "/pricing",
        json={
            "spot_price": 100,
            "strike_price": 100,
            "time_to_maturity": 1.0,
            "risk_free_rate": 0.05,
            "volatility": 0.2,
            "option_type": "call"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "price" in data
    assert "delta" in data
    assert "gamma" in data
    assert "theta" in data
    assert "vega" in data
    assert "rho" in data

def test_invalid_option_type():
    response = client.post(
        "/pricing",
        json={
            "spot_price": 100,
            "strike_price": 100,
            "time_to_maturity": 1.0,
            "risk_free_rate": 0.05,
            "volatility": 0.2,
            "option_type": "invalid"
        }
    )
    assert response.status_code == 422  # Validation error 