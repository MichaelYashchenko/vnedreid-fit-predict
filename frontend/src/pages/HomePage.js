// src/pages/HomePage.js

import React, { useState } from 'react';
import TickerInput from '../components/TickerInput';
import SearchBar from '../components/SearchBar';
import TickerNews from '../components/TickerNews';
import UserPortfolio from '../components/UserPortfolio';

const HomePage = () => {
  const [selectedTickers, setSelectedTickers] = useState(['SBER', 'YNDX']);
  const [startDate, setStartDate] = useState('2024-09-01');
  const [endDate, setEndDate] = useState('2025-03-30');
  const [source, setSource] = useState('');

  const [portfolio, setPortfolio] = useState([]);
  const [portfolioLoading, setPortfolioLoading] = useState(false);
  const [portfolioError, setPortfolioError] = useState(null);

  const fetchPortfolioByToken = async (token) => {
    if (!token) {
      setPortfolioError('Пожалуйста, введите токен пользователя.');
      setPortfolio([]);
      return;
    }
    try {
      setPortfolioLoading(true);
      setPortfolioError(null);
      setPortfolio([]); // Очищаем старый портфель перед новым запросом
      const response = await fetch(`http://127.0.0.1:8000/news/get_user_portfolio?token=${token}`);
      if (!response.ok) {
        throw new Error('Ошибка сети при загрузке портфеля.');
      }
      const data = await response.json();
      if (data.length === 0) {
        setPortfolioError('Портфель не найден или пуст для данного токена.');
      }
      setPortfolio(data);
    } catch (err) {
      setPortfolioError(err.message);
    } finally {
      setPortfolioLoading(false);
    }
  };


  const addTicker = (ticker) => {
    if (ticker && !selectedTickers.includes(ticker)) {
      setSelectedTickers([...selectedTickers, ticker]);
    }
  };

  const removeTicker = (tickerToRemove) => {
    setSelectedTickers(selectedTickers.filter(ticker => ticker !== tickerToRemove));
  };

  return (
    <div className="container">
      <aside className="sidebar-container">
        <TickerInput
          selectedTickers={selectedTickers}
          onTickerAdd={addTicker}
          onTickerRemove={removeTicker}
        />
        <hr className="divider" />
        <SearchBar
          setStartDate={setStartDate}
          setEndDate={setEndDate}
          setSource={setSource}
          initialStartDate={startDate}
          initialEndDate={endDate}
        />
        <hr className="divider" />
        <UserPortfolio
          portfolioTickers={portfolio}
          selectedTickers={selectedTickers}
          onTickerClick={addTicker}
          loading={portfolioLoading}
          error={portfolioError}
          onFetchPortfolio={fetchPortfolioByToken}
        />
      </aside>
      <main className="main-content">
        <TickerNews
          tickers={selectedTickers}
          startDate={startDate}
          endDate={endDate}
          source={source}
        />
      </main>
    </div>
  );
};

export default HomePage;