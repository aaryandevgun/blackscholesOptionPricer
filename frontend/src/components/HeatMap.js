import React from 'react';
import styled from 'styled-components';
import { HeatMapGrid } from 'react-grid-heatmap';

const HeatMapContainer = styled.div`
  margin-top: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h3`
  margin-bottom: 1rem;
  color: #2c3e50;
`;

const HeatMap = ({ data, title }) => {
  if (!data) return null;

  const xLabels = data.spot_prices.map(price => price.toFixed(2));
  const yLabels = data.volatilities.map(vol => vol.toFixed(2));

  const getColor = (value) => {
    if (value === 0) return '#ffffff';
    const intensity = Math.min(Math.abs(value) * 2, 1);
    return value > 0 
      ? `rgba(0, 255, 0, ${intensity})`
      : `rgba(255, 0, 0, ${intensity})`;
  };

  return (
    <HeatMapContainer>
      <Title>{title}</Title>
      <HeatMapGrid
        data={data.call_pnl}
        xLabels={xLabels}
        yLabels={yLabels}
        cellStyle={(_x, _y, ratio) => ({
          background: getColor(ratio),
          fontSize: '11px',
          color: '#000',
          width: '30px',
          height: '30px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        })}
        cellHeight="30px"
        xLabelsPos="bottom"
        xLabelsStyle={() => ({
          fontSize: '10px',
          textTransform: 'uppercase',
        })}
        yLabelsStyle={() => ({
          fontSize: '10px',
          textTransform: 'uppercase',
        })}
      />
    </HeatMapContainer>
  );
};

export default HeatMap; 