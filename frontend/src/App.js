// App.js

import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TickerPage from './pages/TickerPage';
import HowItWorksPage from './pages/HowItWorksPage'; // <-- Импорт новой страницы
import './App.css'; 

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <Link to="/" className="header-link">
            <h1>Новостной Т-Терминал</h1>
          </Link>
          {/* --- НАЧАЛО НОВОГО КОДА --- */}
          <Link to="/how-it-works" className="how-it-works-link">
            Как это работает?
          </Link>
          {/* --- КОНЕЦ НОВОГО КОДА --- */}
        </header>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/ticker/:tickerSymbol" element={<TickerPage />} />
          <Route path="/how-it-works" element={<HowItWorksPage />} /> {/* <-- Новый маршрут */}
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;