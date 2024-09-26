import React, { useState, useRef } from "react";

import "./FilterByString.css";

const FilterByString = ({ caption, category, store, changer, visible }) => {
  const inputValue = useRef();

  const handleSearch = (e) => {
    changer({ ...store, [category]: inputValue.current.value });
  };

  return (
    <div className={visible ? "filter-by-string__container" : "filter-by-string__container--hidden"}>
      <input type="text" placeholder={caption} ref={inputValue} />
      <button className="red-back" onClick={handleSearch}>
        применить
      </button>
    </div>
  );
};

export default FilterByString;
