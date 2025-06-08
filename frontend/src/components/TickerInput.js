import React, { useState } from 'react';
import './TickerInput.css';

const TickerInput = ({ selectedTickers, onTickerAdd, onTickerRemove }) => {
  const [inputValue, setInputValue] = useState('');
  const handleInputChange = (e) => setInputValue(e.target.value.toUpperCase());
  const handleAddTicker = () => {
    if (inputValue && !selectedTickers.includes(inputValue)) {
      onTickerAdd(inputValue);
      setInputValue('');
    }
  };
  const handleKeyDown = (e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddTicker(); } };
  return (
    <div className="ticker-input-container">
      <label htmlFor="ticker-input">Тикеры для поиска</label>
      <div className="input-area">
        <input id="ticker-input" type="text" value={inputValue} onChange={handleInputChange} onKeyDown={handleKeyDown} placeholder="Например, GAZP"/>
        <button onClick={handleAddTicker}>Добавить</button>
      </div>
      <div className="ticker-tags">
        {selectedTickers.map((ticker) => (
          <div key={ticker} className="ticker-tag">
            {ticker}
            <button className="remove-tag-btn" onClick={() => onTickerRemove(ticker)} title={`Удалить ${ticker}`}>×</button>
          </div>
        ))}
      </div>
    </div>
  );
};
export default TickerInput;