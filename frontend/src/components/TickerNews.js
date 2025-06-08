// src/components/TickerNews.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const SentimentIndicator = ({ sentiment, score }) => {
  const sentimentInfo = {
    positive: { text: 'Положительная', className: 'sentiment-positive' },
    negative: { text: 'Отрицательная', className: 'sentiment-negative' },
    neutral: { text: 'Нейтральная', className: 'sentiment-neutral' },
  };
  const currentSentiment = sentimentInfo[sentiment] || sentimentInfo.neutral;
  const confidence = score ? Math.round(score * 100) : 0;
  return (
    <div className="sentiment-indicator">
      <div className="sentiment-label">
        <div className={`sentiment-color-box ${currentSentiment.className}`}></div>
        <span>{currentSentiment.text}</span>
      </div>
      <div className="sentiment-score">Уверенность: {confidence}%</div>
    </div>
  );
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('ru-RU', options);
};

const TickerNews = ({ tickers, startDate, endDate, source }) => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  useEffect(() => {
    if (!tickers || tickers.length === 0) { setNews([]); return; }
    const fetchNews = async () => {
      setLoading(true);
      setError(null);
      const tickersParam = tickers.join(',');
      const apiUrl = 'http://127.0.0.1:8000';
      try {
        const response = await fetch(`${apiUrl}/news/get_ticker_news?tickers=${tickersParam}&date_start=${startDate}&date_end=${endDate}&source_type=${source}`);
        if (!response.ok) throw new Error('Ошибка сети или сервера при загрузке новостей');
        const data = await response.json();
        setNews(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchNews();
  }, [tickers, startDate, endDate, source]);

  if (loading) return <p className="status-message">Загрузка новостей...</p>;
  if (error) return <p className="status-message error-message">Ошибка: {error}</p>;
  if (!tickers || tickers.length === 0) return <p className="status-message">Введите тикер для поиска новостей.</p>;
  if (news.length === 0 && !loading) return <p className="status-message">Нет новостей для выбранных параметров.</p>;

  return (
    <div className="news-list">
      {news.map((item) => (
        <article key={item.id} className="news-item">
          <header className="news-header">
            <a href={item.url} target="_blank" rel="noopener noreferrer" className="news-title-link"><h3>{item.news_title}</h3></a>
            <SentimentIndicator sentiment={item.news_sentiment} score={item.news_sentiment_score} />
          </header>
          <p className="news-summary">{item.news_summary}</p>
          <div className="news-meta">
            <Link to={`/ticker/${item.ticker}`} className="ticker-news-tag">{item.ticker}</Link>
            <div className="news-tags-container">
              {item.news_tags && item.news_tags.map((tag, index) => (<span key={index} className="news-tag">{tag}</span>))}
            </div>
            {/* --- НАЧАЛО НОВОГО КОДА --- */}
            {item.duplicates > 0 && (
              <div className="popularity-indicator" title={`Эта новость встретилась ${item.duplicates} раз в разных источниках`}>
                🔥 <span className="popularity-text">Популярность: <strong>{item.duplicates}</strong></span>
              </div>
            )}
            {/* --- КОНЕЦ НОВОГО КОДА --- */}
          </div>
          <footer className="news-footer">
            <span>Источник: <strong>{item.source}</strong></span>
            <span className="news-date">{formatDate(item.news_date)}</span>
          </footer>
        </article>
      ))}
    </div>
  );
};
export default TickerNews;