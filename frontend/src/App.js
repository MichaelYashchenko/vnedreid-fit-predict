import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TickerPage from './pages/TickerPage';
import './App.css'; 

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <Link to="/" className="header-link">
            <h1>Новостной Т-Терминал</h1>
          </Link>
        </header>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/ticker/:tickerSymbol" element={<TickerPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;