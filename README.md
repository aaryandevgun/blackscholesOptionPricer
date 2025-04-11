# Real-Time Options Pricing & Arbitrage Dashboard

A full-stack web application that provides real-time options pricing using the Black-Scholes model, P&L visualization, and arbitrage opportunity detection through an interactive dashboard.

## Features

- Real-time options pricing using the Black-Scholes model
- Calculation of option Greeks (Delta, Gamma, Theta, Vega, Rho)
- Interactive heat maps showing P&L across different spot prices and volatilities
- Purchase price tracking and P&L calculation
- WebSocket-based real-time data streaming
- MySQL database storage of all calculations
- Modern, responsive UI with styled components
- REST API endpoints for manual price calculations
- Comprehensive test suite for the pricing engine

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application and Black-Scholes implementation
│   │   ├── database.py       # Database configuration
│   │   ├── models.py         # Database models
│   │   └── test_main.py      # Test suite for the backend
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # Backend-specific documentation
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.js # Main dashboard component
│   │   │   └── HeatMap.js   # Heat map visualization component
│   │   ├── App.js          # Main application component
│   │   └── index.js        # Entry point
│   ├── package.json        # Node.js dependencies
│   └── README.md           # Frontend-specific documentation
└── README.md               # Project overview
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- MySQL 8.0+

## Installation

### Database Setup

1. Create a MySQL database:

```sql
CREATE DATABASE options_pricing;
```

2. Configure database connection:
   - Create a `.env` file in the backend directory
   - Add your database credentials:
   ```
   DATABASE_URL=mysql://username:password@localhost/options_pricing
   ```

### Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Backend

1. Start the FastAPI server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

The backend will be available at `http://localhost:8000`

### Frontend

1. Start the React development server:
   ```bash
   cd frontend
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Features in Detail

### Option Pricing

- Input current asset price, strike price, time to maturity, volatility, and risk-free rate
- Calculate theoretical option prices using the Black-Scholes model
- View option Greeks and their values

### Heat Map Visualization

- Visualize P&L across different spot prices and volatilities
- Green indicates positive P&L, red indicates negative P&L
- Separate heat maps for call and put options
- Interactive grid showing P&L values

### Purchase Price Tracking

- Input purchase prices for call and put options
- Automatic P&L calculation based on current market conditions
- Real-time updates of P&L values

### Database Storage

- All calculations are stored in MySQL database
- Historical data tracking
- Input parameters and results are saved for future reference

## API Documentation

Once the backend is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /pricing` - Calculate option price and Greeks
- `POST /heatmap` - Generate heat map data
- `GET /history` - Retrieve calculation history
- `WS /ws` - WebSocket endpoint for real-time data

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Black-Scholes model implementation based on the original paper by Fischer Black and Myron Scholes
- FastAPI for the backend framework
- React and Chart.js for the frontend visualization
- MySQL for data persistence
