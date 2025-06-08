import React from 'react';

const Sidebar = ({ tickers, selectedTicker, setTicker }) => {
  return (
    <div className="sidebar">
      <h3>Выбор тикера</h3>
      {/* Делаем компонент "управляемым" */}
      <select value={selectedTicker} onChange={(e) => setTicker(e.target.value)}>
        {tickers.map((ticker) => (
          <option key={ticker} value={ticker}>
            {ticker}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Sidebar;