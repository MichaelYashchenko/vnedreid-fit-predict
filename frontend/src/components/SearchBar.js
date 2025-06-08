import React from 'react';

const SearchBar = ({ setStartDate, setEndDate, setSource, initialStartDate, initialEndDate }) => {
  return (
    <div className="search-bar">
      <label htmlFor="start-date">Дата начала</label>
      <input id="start-date" type="date" defaultValue={initialStartDate} onChange={(e) => setStartDate(e.target.value)} />
      <label htmlFor="end-date">Дата окончания</label>
      <input id="end-date" type="date" defaultValue={initialEndDate} onChange={(e) => setEndDate(e.target.value)} />
      <label htmlFor="source-input">Источник</label>
      <input id="source-input" type="text" onChange={(e) => setSource(e.target.value)} placeholder="Например, РБК" />
    </div>
  );
};
export default SearchBar;