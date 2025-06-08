// src/components/NewsModal.js

import React from 'react';
import './NewsModal.css';

// Добавляем 'position' в принимаемые props
const NewsModal = ({ newsItem, position, onClose }) => {
  if (!newsItem || !position) return null;

  const handleBackdropClick = (e) => {
    // В режиме тултипа фон не нужен, но оставим логику для закрытия
    if (e.target.classList.contains('modal-backdrop-tooltip')) {
      onClose();
    }
  };

  // Стиль для позиционирования
  const modalStyle = {
    // Добавляем небольшое смещение, чтобы тултип не перекрывал курсор
    top: `${position.top - 20}px`,
    left: `${position.left + 20}px`,
  };

  // --- НАЧАЛО НОВОГО КОДА ---
  // Создаем дополнительный класс на основе тональности новости
  const sentimentClass = newsItem.news_sentiment
    ? `modal-content-tooltip--${newsItem.news_sentiment}`
    : '';
  // --- КОНЕЦ НОВОГО КОДА ---

  return (
    // Используем другой класс для фона, чтобы не было затемнения
    <div className="modal-backdrop-tooltip" onClick={handleBackdropClick}>
      {/* Добавляем динамический класс для окрашивания рамки */}
      <div className={`modal-content-tooltip ${sentimentClass}`} style={modalStyle}>
        <h3>{newsItem.news_title}</h3>
        <p>{newsItem.news_summary}</p>
        <div className="modal-footer">
          {/* --- НАЧАЛО ОБНОВЛЕННОГО БЛОКА --- */}
          <div className="modal-meta-info">
            <span>Источник: <strong>{newsItem.source}</strong></span>
            {newsItem.duplicates > 0 && (
              <div className="popularity-indicator" title={`Новость встретилась ${newsItem.duplicates} раз`}>
                🔥 {newsItem.duplicates}
              </div>
            )}
          </div>
          {/* --- КОНЕЦ ОБНОВЛЕННОГО БЛОКА --- */}
          <a href={newsItem.url} target="_blank" rel="noopener noreferrer">Читать полностью</a>
        </div>
      </div>
    </div>
  );
};

export default NewsModal;