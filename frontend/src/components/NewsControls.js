// src/components/NewsControls.js

import React from 'react';
import './NewsControls.css';

const NewsControls = ({
  sortOrder,
  onSortChange,
  filterSentiments,
  onSentimentChange,
  // --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА ---
  popularityThreshold,
  onPopularityChange,
  maxPopularity,
  // --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА ---
}) => {
  const sentimentOptions = [
    { value: 'positive', label: 'Положительные' },
    { value: 'neutral', label: 'Нейтральные' },
    { value: 'negative', label: 'Отрицательные' },
  ];

  const handleSentimentCheckbox = (e) => {
    const { value, checked } = e.target;
    const newSentiments = checked
      ? [...filterSentiments, value]
      : filterSentiments.filter((s) => s !== value);
    onSentimentChange(newSentiments);
  };

  return (
    <div className="news-controls-container">
      <div className="control-group">
        <label htmlFor="sort-select">Сортировать по:</label>
        <select id="sort-select" value={sortOrder} onChange={(e) => onSortChange(e.target.value)}>
          <option value="date_desc">Дате (сначала новые)</option>
          <option value="popularity_desc">Популярности</option>
          <option value="alphabetical_asc">Алфавиту (А-Я)</option>
          <option value="sentiment">Тональности</option>
        </select>
      </div>

      <div className="control-group">
        <label>Фильтр по тональности:</label>
        <div className="checkbox-group">
          {sentimentOptions.map((opt) => (
            <div key={opt.value} className="checkbox-item">
              <input type="checkbox" id={`sentiment-${opt.value}`} value={opt.value} checked={filterSentiments.includes(opt.value)} onChange={handleSentimentCheckbox} />
              <label htmlFor={`sentiment-${opt.value}`}>{opt.label}</label>
            </div>
          ))}
        </div>
      </div>
      
      {/* --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА --- */}
      <div className="control-group slider-group">
        <label htmlFor="popularity-slider">Популярность (от {popularityThreshold})</label>
        <div className="slider-container">
          <input
            type="range"
            id="popularity-slider"
            min="0"
            max={maxPopularity}
            value={popularityThreshold}
            onChange={(e) => onPopularityChange(Number(e.target.value))}
          />
          <span className="slider-value">{popularityThreshold}</span>
        </div>
      </div>
      {/* --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА --- */}
    </div>
  );
};

export default NewsControls;