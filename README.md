# Real-Time Options Pricing & Arbitrage Dashboard 🚀

A powerful web application for real-time options pricing, Greeks calculation, and arbitrage opportunities visualization. Built with FastAPI and React.

## Features ✨

- **Real-time Options Pricing**: Calculate option prices using the Black-Scholes model
- **Greeks Calculation**: View Delta, Gamma, Theta, Vega, and Rho in real-time
- **Heat Map Visualization**: Interactive heat maps for call and put options
- **P&L Tracking**: Monitor your profits and losses with purchase price inputs
- **Live Updates**: WebSocket-based real-time data streaming
- **Modern UI**: Clean, responsive interface built with React and styled-components

## Tech Stack 🛠️

### Backend

- Python 3.8+
- FastAPI
- WebSocket
- NumPy
- SciPy

### Frontend

- React
- styled-components
- Chart.js
- react-grid-heatmap
- WebSocket client

## Project Structure 📁

```
blackscholesOptionPricer/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   └── test_main.py      # Backend tests
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── public/
    │   ├── index.html
    │   └── manifest.json
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.js
    │   │   ├── HeatMap.js
    │   │   └── Navbar.js
    │   ├── App.js
    │   ├── index.js
    │   └── index.css
    └── package.json          # Node.js dependencies
```

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## Usage 📊

1. **Access the Dashboard**

   - Backend API: `http://localhost:8000`
   - Frontend Dashboard: `http://localhost:3000`

2. **Calculate Option Prices**

   - Enter the required parameters:
     - Spot Price
     - Strike Price
     - Time to Maturity (in years)
     - Risk-free Rate
     - Volatility
   - Click "Calculate" to see the results

3. **View Heat Maps**

   - The dashboard automatically displays heat maps for:
     - Call Options
     - Put Options
   - Colors indicate P&L (green for profit, red for loss)

4. **Track P&L**
   - Enter your purchase prices for call and put options
   - View real-time P&L updates in the results section

## API Endpoints 🔌

### REST API

- `POST /api/calculate`: Calculate option prices
- `GET /api/heatmap`: Get heat map data
- `GET /api/history`: Get calculation history

### WebSocket

- `ws://localhost:8000/ws`: Real-time market data stream

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Black-Scholes model implementation
- FastAPI for the robust backend
- React for the beautiful frontend
- Chart.js for data visualization
