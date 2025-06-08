// src/components/InterpretationModal.js
import React from 'react';
import './InterpretationModal.css';

const InterpretationModal = ({ newsTitle, loading, error, interpretation, onClose }) => {
  if (!newsTitle) return null;

  const handleBackdropClick = (e) => {
    if (e.target.classList.contains('interpretation-modal-backdrop')) {
      onClose();
    }
  };

  return (
    <div className="interpretation-modal-backdrop" onClick={handleBackdropClick}>
      <div className="interpretation-modal-content">
        <button className="interpretation-modal-close-btn" onClick={onClose}>×</button>
        <h3>Интерпретация новости</h3>
        <p className="interpretation-modal-subtitle">{newsTitle}</p>
        
        <div className="interpretation-modal-body">
          {loading && <p className="status-message">Загрузка интерпретации от LLM...</p>}
          {error && <p className="status-message error-message">{error}</p>}
          {!loading && !error && interpretation && (
            <p>{interpretation}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default InterpretationModal;