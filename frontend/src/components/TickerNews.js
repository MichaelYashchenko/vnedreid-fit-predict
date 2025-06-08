// src/components/TickerNews.js

import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import InterpretationModal from './InterpretationModal';

const SentimentIndicator = ({ sentiment, score }) => {
  // ... (код без изменений)
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
  // ... (код без изменений)
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('ru-RU', options);
};


// --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА PROPS ---
const TickerNews = ({ tickers, startDate, endDate, source, sortOrder, filterSentiments, popularityThreshold, onDataLoaded }) => {
// --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА PROPS ---
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [interpretingItem, setInterpretingItem] = useState(null);
  const [isInterpreting, setIsInterpreting] = useState(false);
  const [interpretationError, setInterpretationError] = useState(null);
  const [interpretationResult, setInterpretationResult] = useState('');

  useEffect(() => {
    if (!tickers || tickers.length === 0) { setNews([]); return; }
    const fetchNews = async () => {
      setLoading(true);
      setError(null);
      const tickersParam = tickers.join(',');
      const apiUrl = 'http://127.0.0.1:5000';
      try {
        const response = await fetch(`${apiUrl}/get_ticker_news?tickers=${tickersParam}&date_start=${startDate}&date_end=${endDate}&source=${source}`);
        if (!response.ok) throw new Error('Ошибка сети или сервера при загрузке новостей');
        const data = await response.json();
        setNews(data);
        onDataLoaded(data); // <--- ВЫЗЫВАЕМ CALLBACK ЗДЕСЬ
      } catch (err) {
        setError(err.message);
        onDataLoaded([]); // <--- Сбрасываем в случае ошибки
      } finally {
        setLoading(false);
      }
    };
    fetchNews();
  }, [tickers, startDate, endDate, source, onDataLoaded]); // Добавляем onDataLoaded в зависимости

  const displayedNews = useMemo(() => {
    let processedNews = [...news];

    // --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА ФИЛЬТРАЦИИ ---
    processedNews = processedNews.filter(item => 
      filterSentiments.includes(item.news_sentiment) &&
      (item.duplicates || 0) >= popularityThreshold
    );
    // --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА ФИЛЬТРАЦИИ ---

    const sentimentOrder = { positive: 1, neutral: 2, negative: 3 };
    switch (sortOrder) {
      case 'popularity_desc':
        processedNews.sort((a, b) => (b.duplicates || 0) - (a.duplicates || 0));
        break;
      case 'alphabetical_asc':
        processedNews.sort((a, b) => a.news_title.localeCompare(b.news_title));
        break;
      case 'sentiment':
        processedNews.sort((a, b) => (sentimentOrder[a.news_sentiment] || 99) - (sentimentOrder[b.news_sentiment] || 99));
        break;
      case 'date_desc':
      default:
        processedNews.sort((a, b) => new Date(b.news_date) - new Date(a.news_date));
        break;
    }

    return processedNews;
  }, [news, sortOrder, filterSentiments, popularityThreshold]); // Обновляем зависимости

  // ... (остальной код компонента handleInterpretClick и JSX остается без изменений) ...

  const handleInterpretClick = async (newsItem) => {
    setInterpretingItem(newsItem);
    setIsInterpreting(true);
    setInterpretationError(null);
    setInterpretationResult('');
    const apiUrl = 'http://127.0.0.1:5000';

    try {
      const response = await fetch(`${apiUrl}/interpret_news`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          news_text: newsItem.news_summary,
          sentiment: newsItem.news_sentiment,
          sentiment_score: newsItem.news_sentiment_score,
          ticker: newsItem.ticker,
        }),
      });
      if (!response.ok) throw new Error('Не удалось получить ответ от LLM.');
      const data = await response.json();
      setInterpretationResult(data.interpretation);
    } catch (err) {
      setInterpretationError(err.message);
    } finally {
      setIsInterpreting(false);
    }
  };

  const closeInterpretationModal = () => {
    setInterpretingItem(null);
  };

  if (loading) return <p className="status-message">Загрузка новостей...</p>;
  if (error) return <p className="status-message error-message">Ошибка: {error}</p>;
  if (!tickers || tickers.length === 0) return <p className="status-message">Введите тикер для поиска новостей.</p>;
  if (displayedNews.length === 0 && !loading) return <p className="status-message">Нет новостей для выбранных параметров.</p>;

  return (
    <>
      <div className="news-list">
        {displayedNews.map((item) => (
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
              {item.duplicates > 0 && (
                <div className="popularity-indicator" title={`Эта новость встретилась ${item.duplicates} раз в разных источниках`}>
                  🔥 <span className="popularity-text">Популярность: <strong>{item.duplicates}</strong></span>
                </div>
              )}
            </div>
            <footer className="news-footer">
              <div>
                <span>Источник: <strong>{item.source}</strong></span>
                <span style={{ marginLeft: '1rem' }}>{formatDate(item.news_date)}</span>
              </div>
              <button
                className="interpret-button"
                onClick={() => handleInterpretClick(item)}
                disabled={isInterpreting && interpretingItem?.id === item.id}
              >
                Интерпретировать
              </button>
            </footer>
          </article>
        ))}
      </div>
      
      <InterpretationModal
        newsTitle={interpretingItem?.news_title}
        loading={isInterpreting}
        error={interpretationError}
        interpretation={interpretationResult}
        onClose={closeInterpretationModal}
      />
    </>
  );
};
export default TickerNews;