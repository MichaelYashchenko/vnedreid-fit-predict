// src/components/UserPortfolio.js

import React, { useState } from 'react';
import './UserPortfolio.css';

const UserPortfolio = ({ portfolioTickers, selectedTickers, onTickerClick, loading, error, onFetchPortfolio }) => {
  const [tokenInput, setTokenInput] = useState('');

  const handleFetchClick = () => {
    onFetchPortfolio(tokenInput);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleFetchClick();
    }
  };

  return (
    <div className="user-portfolio-container">
      <h4>Ваш портфель</h4>
      <div className="portfolio-input-area">
        <input
          type="text"
          value={tokenInput}
          onChange={(e) => setTokenInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Введите токен..."
          disabled={loading}
        />
        <button onClick={handleFetchClick} disabled={loading}>
          {loading ? '...' : 'Найти'}
        </button>
      </div>

      {error && <p className="status-message-small error-message-small">{error}</p>}
      
      {portfolioTickers.length > 0 && (
        <div className="portfolio-tags">
          {portfolioTickers.map((item) => {
            const isSelected = selectedTickers.includes(item.ticker);
            return (
              <button
                key={item.ticker}
                className="portfolio-tag"
                onClick={() => onTickerClick(item.ticker)}
                disabled={isSelected}
                title={isSelected ? `${item.ticker} уже добавлен` : `Добавить ${item.ticker}`}
              >
                {item.ticker}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default UserPortfolio;