import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import D3PriceChart from '../components/D3PriceChart';
import NewsModal from '../components/NewsModal';

const TickerPage = () => {
  const { tickerSymbol } = useParams();
  const [priceData, setPriceData] = useState([]);
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeNews, setActiveNews] = useState({ item: null, position: null });

  const getInitialDateRange = () => {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - 1);
    return {
      start: startDate.toISOString().split('T')[0],
      end: endDate.toISOString().split('T')[0],
    };
  };

  const [dateRange, setDateRange] = useState(getInitialDateRange);
  const [formDates, setFormDates] = useState(dateRange);

  useEffect(() => {
    const controller = new AbortController();
    const { signal } = controller;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      setActiveNews({ item: null, position: null });
      const apiUrl = 'http://127.0.0.1:5000';
      
      try {
        const [pricesResponse, newsResponse] = await Promise.all([
          fetch(`${apiUrl}/get_ticker_prices?ticker=${tickerSymbol}&date_start=${dateRange.start}&date_end=${dateRange.end}`, { signal }),
          fetch(`${apiUrl}/get_ticker_news?tickers=${tickerSymbol}&date_start=${dateRange.start}&date_end=${dateRange.end}`, { signal })
        ]);

        if (!pricesResponse.ok || !newsResponse.ok) {
          throw new Error('Не удалось загрузить данные. Проверьте работу сервера.');
        }
        const prices = await pricesResponse.json();
        const news = await newsResponse.json();
        setPriceData(prices);
        setNewsData(news);
      } catch (err) {
        if (err.name !== 'AbortError') setError(err.message);
      } finally {
        if (!signal.aborted) setLoading(false);
      }
    };
    fetchData();
    
    return () => {
      controller.abort();
    };
  }, [tickerSymbol, dateRange]);

  const handleDateChange = (e) => {
    const { name, value } = e.target;
    setFormDates(prev => ({ ...prev, [name]: value }));
  };

  const handleBuildChart = () => {
    setDateRange(formDates);
  };

  const handleMarkerHover = (newsItem, pos) => {
    const position = { top: pos.top - 10, left: pos.left + 20 };
    setActiveNews({ item: newsItem, position });
  };

  const handleMarkerLeave = () => {
    setActiveNews({ item: null, position: null });
  };
  
  return (
    <div className="container" style={{flexDirection: 'column', alignItems: 'stretch'}}>
      <Link to="/" className="back-link">← Назад к списку новостей</Link>
      
      <div className="chart-container">
        <h3>Динамика цены {tickerSymbol}</h3>

        <div className="date-range-controls">
          <input type="date" name="start" value={formDates.start} onChange={handleDateChange} />
          <input type="date" name="end" value={formDates.end} onChange={handleDateChange} />
          <button onClick={handleBuildChart} disabled={loading}>
            {loading ? 'Загрузка...' : 'Построить'}
          </button>
        </div>

        {loading && <p className="status-message">Загрузка данных графика...</p>}
        {error && <p className="status-message error-message">{error}</p>}
        {!loading && !error && priceData.length > 0 && (
          <D3PriceChart 
            prices={priceData}
            news={newsData}
            onMarkerHover={handleMarkerHover}
            onMarkerLeave={handleMarkerLeave}
          />
        )}
        {!loading && !error && priceData.length === 0 && (
           <p className="status-message">Нет данных о ценах для отображения графика.</p>
        )}
      </div>

      <NewsModal 
        newsItem={activeNews.item} 
        position={activeNews.position}
        onClose={handleMarkerLeave}
      />
    </div>
  );
};

export default TickerPage;