// src/pages/HomePage.js

import React, { useState } from 'react';
import TickerInput from '../components/TickerInput';
import SearchBar from '../components/SearchBar';
import TickerNews from '../components/TickerNews';
import UserPortfolio from '../components/UserPortfolio';
import NewsControls from '../components/NewsControls';

const HomePage = () => {
  const [selectedTickers, setSelectedTickers] = useState(['SBER', 'YNDX']);
  const [startDate, setStartDate] = useState('2024-09-01');
  const [endDate, setEndDate] = useState('2025-03-30');
  const [source, setSource] = useState('');

  const [sortOrder, setSortOrder] = useState('date_desc');
  const [filterSentiments, setFilterSentiments] = useState(['positive', 'neutral', 'negative']);
  
  // --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА ---
  const [popularityThreshold, setPopularityThreshold] = useState(0);
  const [maxPopularity, setMaxPopularity] = useState(10); // Начальное значение по умолчанию

  // Callback для получения данных из дочернего компонента
  const handleDataLoaded = (news) => {
    if (!news || news.length === 0) {
      setMaxPopularity(10); // Сброс, если нет новостей
      return;
    }
    // Находим максимальное значение 'duplicates' в загруженных новостях
    const max = Math.max(...news.map(n => n.duplicates || 0));
    // Устанавливаем его как максимум для слайдера, но не меньше 10
    setMaxPopularity(max > 0 ? max : 10);
  };
  // --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА ---

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
      setPortfolio([]);
      const response = await fetch(`http://127.0.0.1:5000/get_user_portfolio?token=${token}`);
      if (!response.ok) throw new Error('Ошибка сети при загрузке портфеля.');
      const data = await response.json();
      if (data.length === 0) setPortfolioError('Портфель не найден или пуст для данного токена.');
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
        <TickerInput selectedTickers={selectedTickers} onTickerAdd={addTicker} onTickerRemove={removeTicker} />
        <hr className="divider" />
        <SearchBar setStartDate={setStartDate} setEndDate={setEndDate} setSource={setSource} initialStartDate={startDate} initialEndDate={endDate} />
        <hr className="divider" />
        <UserPortfolio portfolioTickers={portfolio} selectedTickers={selectedTickers} onTickerClick={addTicker} loading={portfolioLoading} error={portfolioError} onFetchPortfolio={fetchPortfolioByToken} />
      </aside>
      <main className="main-content">
        <NewsControls
          sortOrder={sortOrder}
          onSortChange={setSortOrder}
          filterSentiments={filterSentiments}
          onSentimentChange={setFilterSentiments}
          // --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА ---
          popularityThreshold={popularityThreshold}
          onPopularityChange={setPopularityThreshold}
          maxPopularity={maxPopularity}
          // --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА ---
        />
        <TickerNews
          tickers={selectedTickers}
          startDate={startDate}
          endDate={endDate}
          source={source}
          sortOrder={sortOrder}
          filterSentiments={filterSentiments}
          // --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА ---
          popularityThreshold={popularityThreshold}
          onDataLoaded={handleDataLoaded} // Передаем callback
          // --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА ---
        />
      </main>
    </div>
  );
};

export default HomePage;