import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import HeatMap from './HeatMap';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const DashboardContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
`;

const FormContainer = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const ChartContainer = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const Select = styled.select`
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const Button = styled.button`
  width: 100%;
  padding: 0.75rem;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;

  &:hover {
    background-color: #34495e;
  }
`;

const ResultsContainer = styled.div`
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
`;

const Dashboard = () => {
  const [formData, setFormData] = useState({
    spot_price: 100,
    strike_price: 100,
    time_to_maturity: 1.0,
    risk_free_rate: 0.05,
    volatility: 0.2,
    option_type: 'call',
    call_purchase_price: '',
    put_purchase_price: ''
  });

  const [priceData, setPriceData] = useState({
    price: 0,
    delta: 0,
    gamma: 0,
    theta: 0,
    vega: 0,
    rho: 0,
    call_pnl: 0,
    put_pnl: 0
  });

  const [heatMapData, setHeatMapData] = useState(null);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Option Price',
        data: [],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  });

  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws');

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPriceData(data.pricing);
      
      setChartData(prev => ({
        labels: [...prev.labels, new Date().toLocaleTimeString()],
        datasets: [{
          ...prev.datasets[0],
          data: [...prev.datasets[0].data, data.pricing.price]
        }]
      }));
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Calculate option price
      const response = await axios.post('http://localhost:8000/pricing', formData);
      setPriceData(response.data);

      // Get heat map data
      const heatMapResponse = await axios.post('http://localhost:8000/heatmap', formData);
      setHeatMapData(heatMapResponse.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Real-Time Option Price'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return (
    <DashboardContainer>
      <FormContainer>
        <form onSubmit={handleSubmit}>
          <FormGroup>
            <Label>Spot Price</Label>
            <Input
              type="number"
              name="spot_price"
              value={formData.spot_price}
              onChange={handleInputChange}
              step="0.01"
            />
          </FormGroup>
          <FormGroup>
            <Label>Strike Price</Label>
            <Input
              type="number"
              name="strike_price"
              value={formData.strike_price}
              onChange={handleInputChange}
              step="0.01"
            />
          </FormGroup>
          <FormGroup>
            <Label>Time to Maturity (years)</Label>
            <Input
              type="number"
              name="time_to_maturity"
              value={formData.time_to_maturity}
              onChange={handleInputChange}
              step="0.1"
            />
          </FormGroup>
          <FormGroup>
            <Label>Risk-Free Rate</Label>
            <Input
              type="number"
              name="risk_free_rate"
              value={formData.risk_free_rate}
              onChange={handleInputChange}
              step="0.01"
            />
          </FormGroup>
          <FormGroup>
            <Label>Volatility</Label>
            <Input
              type="number"
              name="volatility"
              value={formData.volatility}
              onChange={handleInputChange}
              step="0.01"
            />
          </FormGroup>
          <FormGroup>
            <Label>Option Type</Label>
            <Select
              name="option_type"
              value={formData.option_type}
              onChange={handleInputChange}
            >
              <option value="call">Call</option>
              <option value="put">Put</option>
            </Select>
          </FormGroup>
          <FormGroup>
            <Label>Call Purchase Price</Label>
            <Input
              type="number"
              name="call_purchase_price"
              value={formData.call_purchase_price}
              onChange={handleInputChange}
              step="0.01"
            />
          </FormGroup>
          <FormGroup>
            <Label>Put Purchase Price</Label>
            <Input
              type="number"
              name="put_purchase_price"
              value={formData.put_purchase_price}
              onChange={handleInputChange}
              step="0.01"
            />
          </FormGroup>
          <Button type="submit">Calculate Price</Button>
        </form>

        <ResultsContainer>
          <h3>Option Greeks</h3>
          <p>Price: {priceData.price.toFixed(4)}</p>
          <p>Delta: {priceData.delta.toFixed(4)}</p>
          <p>Gamma: {priceData.gamma.toFixed(4)}</p>
          <p>Theta: {priceData.theta.toFixed(4)}</p>
          <p>Vega: {priceData.vega.toFixed(4)}</p>
          <p>Rho: {priceData.rho.toFixed(4)}</p>
          {priceData.call_pnl !== null && (
            <p>Call P&L: {priceData.call_pnl.toFixed(4)}</p>
          )}
          {priceData.put_pnl !== null && (
            <p>Put P&L: {priceData.put_pnl.toFixed(4)}</p>
          )}
        </ResultsContainer>
      </FormContainer>

      <ChartContainer>
        <Line data={chartData} options={chartOptions} />
        {heatMapData && (
          <>
            <HeatMap data={heatMapData} title="Call Option P&L Heat Map" />
            <HeatMap data={heatMapData} title="Put Option P&L Heat Map" />
          </>
        )}
      </ChartContainer>
    </DashboardContainer>
  );
};

export default Dashboard; 