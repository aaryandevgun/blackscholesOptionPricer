import React from 'react';
import styled from 'styled-components';

const Nav = styled.nav`
  background-color: #2c3e50;
  padding: 1rem 2rem;
  color: white;
`;

const NavTitle = styled.h1`
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
`;

const Navbar = () => {
  return (
    <Nav>
      <NavTitle>Real-Time Options Pricing & Arbitrage Dashboard</NavTitle>
    </Nav>
  );
};

export default Navbar; 