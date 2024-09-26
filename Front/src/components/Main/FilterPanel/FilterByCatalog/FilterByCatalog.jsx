import React, { useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../../../Shared/api.jsx";
import "./FilterByCatalog.css";

const FilterByCatalog = ({ caption, category, store, changer, visible }) => {
  const [catalog, setCatalog] = useState([]);

  const fetchCatalog = async () => {
    try {
      const response = await axios.get(`${API_URL}catalogs/${category}/`);
      setCatalog(response.data);
    } catch (error) {
      console.error(`Error fetching catalog ${caption} data:`, error);
    }
  };

  const handlerChange = (e) => {
    changer({ ...store, [category]: e.target.value });
  };

  useEffect(() => {
    fetchCatalog();
  }, []);

  return (
    <label className={visible ? "filter-by__label" : "filter-by__label--hidden"}>
      <p>{caption}</p>
      <select name={category} volume={store.tec} onChange={handlerChange}>
        <option value="">Все</option>
        {catalog.map((item) => (
          <option key={item.id} value={item.id}>
            {item.name}
          </option>
        ))}
      </select>
    </label>
  );
};

export default FilterByCatalog;
