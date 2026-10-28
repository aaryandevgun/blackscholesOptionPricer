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

# ---------------------------------------------------------------------------
# Correctness checks on the pricing math
# ---------------------------------------------------------------------------

def _params(option_type, S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2):
    return OptionParams(
        spot_price=S,
        strike_price=K,
        time_to_maturity=T,
        risk_free_rate=r,
        volatility=sigma,
        option_type=option_type,
    )


def _price(option_type, **kw):
    return black_scholes(_params(option_type, **kw)).price


def test_reference_prices():
    # Textbook values for S=K=100, T=1, r=5%, sigma=20%
    assert black_scholes(_params("call")).price == pytest.approx(10.4506, abs=1e-4)
    assert black_scholes(_params("put")).price == pytest.approx(5.5735, abs=1e-4)


@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100, 100, 1.0, 0.05, 0.2),
    (80, 100, 0.25, 0.03, 0.35),
    (130, 100, 2.0, 0.01, 0.15),
])
def test_put_call_parity(S, K, T, r, sigma):
    import math
    kw = dict(S=S, K=K, T=T, r=r, sigma=sigma)
    lhs = _price("call", **kw) - _price("put", **kw)
    rhs = S - K * math.exp(-r * T)
    assert lhs == pytest.approx(rhs, abs=1e-10)


@pytest.mark.parametrize("option_type", ["call", "put"])
@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100, 100, 1.0, 0.05, 0.2),
    (80, 100, 0.25, 0.03, 0.35),
    (130, 100, 2.0, 0.01, 0.15),
])
def test_greeks_match_finite_differences(option_type, S, K, T, r, sigma):
    kw = dict(S=S, K=K, T=T, r=r, sigma=sigma)
    g = black_scholes(_params(option_type, **kw))
    h = 1e-4

    def bump(name, dh):
        k = dict(kw)
        k[name] += dh
        return _price(option_type, **k)

    delta = (bump("S", h) - bump("S", -h)) / (2 * h)
    gamma = (bump("S", h) - 2 * _price(option_type, **kw) + bump("S", -h)) / h**2
    vega = (bump("sigma", h) - bump("sigma", -h)) / (2 * h)
    rho = (bump("r", h) - bump("r", -h)) / (2 * h)
    # Theta is the derivative w.r.t. calendar time, i.e. -dV/dT
    theta = -(bump("T", h) - bump("T", -h)) / (2 * h)

    assert g.delta == pytest.approx(delta, rel=1e-5, abs=1e-6)
    assert g.gamma == pytest.approx(gamma, rel=1e-3, abs=1e-5)
    assert g.vega == pytest.approx(vega, rel=1e-5, abs=1e-6)
    assert g.rho == pytest.approx(rho, rel=1e-5, abs=1e-6)
    assert g.theta == pytest.approx(theta, rel=1e-5, abs=1e-6)


def test_put_rho_negative_and_call_rho_positive():
    assert black_scholes(_params("call")).rho > 0
    assert black_scholes(_params("put")).rho < 0


def test_deep_itm_put_can_have_positive_theta():
    # Deep ITM European put with meaningful rates gains value as time passes
    g = black_scholes(_params("put", S=50, K=100, T=1.0, r=0.10, sigma=0.2))
    assert g.theta > 0


@pytest.mark.parametrize("field", ["spot_price", "strike_price", "time_to_maturity", "volatility"])
def test_nonpositive_inputs_rejected(field):
    body = {
        "spot_price": 100,
        "strike_price": 100,
        "time_to_maturity": 1.0,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
        "option_type": "call",
    }
    body[field] = 0
    assert client.post("/pricing", json=body).status_code == 422
