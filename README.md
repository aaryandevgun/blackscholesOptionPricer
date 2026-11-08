# Black-Scholes Option Pricer

A Black-Scholes pricer for European calls and puts, with all five Greeks, a P&L heat map over spot and volatility, and a small React dashboard on top of a FastAPI backend.

## What it does

- Prices European calls and puts with the closed-form Black-Scholes formula (no dividends).
- Computes delta, gamma, theta, vega, and rho analytically.
- Given a purchase price, computes P&L and shows it as a heat map over a 20 x 20 grid of spot prices (50% to 150% of the current spot) and volatilities (10% to 50%).
- Streams a live-updating price chart over a WebSocket. The market data in this stream is **simulated** (random spot, volatility, and maturity values generated once per second), not a real feed.

## Validation

The pricing math is tested in `backend/app/test_main.py`:

- **Reference values:** at S = K = 100, T = 1, r = 5%, σ = 20%, the call prices at 10.4506 and the put at 5.5735, matching the textbook values.
- **Put-call parity:** C − P = S − K·e^(−rT) holds to 1e-10 across three parameter sets.
- **Greeks vs. finite differences:** every analytic Greek, for both calls and puts, is checked against a central-difference approximation from bumping the relevant input.
- **Sign checks:** call rho is positive, put rho is negative, and a deep in-the-money put with high rates has positive theta.
- **Input validation:** zero or negative spot, strike, maturity, or volatility, and option types other than `call`/`put`, are rejected with HTTP 422.

Run the tests from `backend/app`:

```bash
cd backend/app
pytest
```

## Conventions

| Input | Units |
|---|---|
| `time_to_maturity` | years |
| `risk_free_rate` | annual, continuously compounded (0.05 = 5%) |
| `volatility` | annualized (0.2 = 20%) |

The Greeks use the standard analytic form with no rescaling:

| Greek | Units |
|---|---|
| theta | change in price per **year** of calendar time (divide by 365 for per day) |
| vega | change in price per 1.00 change in volatility (divide by 100 for per vol point) |
| rho | change in price per 1.00 change in the rate (divide by 100 for per 1%) |

## API

| Method | Path | Body | Returns |
|---|---|---|---|
| `POST` | `/pricing` | option parameters | price, Greeks, and P&L if a purchase price was given |
| `POST` | `/heatmap` | option parameters | call/put prices and P&L over the spot × volatility grid |
| `WS` | `/ws` | n/a | one simulated market tick plus its pricing per second |

Example request body:

```json
{
  "spot_price": 100,
  "strike_price": 100,
  "time_to_maturity": 1.0,
  "risk_free_rate": 0.05,
  "volatility": 0.2,
  "option_type": "call",
  "call_purchase_price": 9.5
}
```

`call_purchase_price` and `put_purchase_price` are optional. Without one, the P&L fields come back `null` from `/pricing` and as zeros in the `/heatmap` grid.

## Running it locally

Requires Python 3.9+ and Node.js 14+.

Backend (serves on `http://localhost:8000`):

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (serves on `http://localhost:3000`):

```bash
cd frontend
npm install
npm start
```

## Stack

- **Backend:** Python, FastAPI, NumPy, SciPy, Pydantic, pytest
- **Frontend:** React, styled-components, Chart.js (react-chartjs-2), react-grid-heatmap, axios

## Project structure

```
backend/
  app/
    main.py         # pricing, Greeks, heat map, API and WebSocket endpoints
    test_main.py    # API tests and pricing-math validation
  requirements.txt
frontend/
  src/
    components/
      Dashboard.js  # input form, Greeks display, live chart
      HeatMap.js    # P&L heat map
      Navbar.js
    App.js
    index.js
```

## Limitations

- European options only, with no dividends.
- Volatility is an input. The pricer does not compute implied volatility.
- The live stream uses simulated data, not a market feed.
