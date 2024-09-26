import React, { useState, useEffect } from "react";
import axios from "axios";

import { ACC_URL } from "../../../../Shared/api.jsx";
import { useAuth } from "../../../../hook/useAuth.jsx";
import "./FilterByUser.css";

const FilterByCatalog = ({ caption, category, store, changer, visible }) => {
  const { isAuthenticated, token } = useAuth();
  const [catalog, setCatalog] = useState([]);

  const fetchCatalog = async () => {
    try {
      const response = await axios.get(`${ACC_URL}users/?role=${category}`, {
        headers: {
          Authorization: `Bearer ${token.access}`,
        },
      });
      setCatalog(response.data);
    } catch (error) {
      console.error(`Error fetching users of ${caption} role:`, error);
    }
  };

  const handlerChange = (e) => {
    changer({ ...store, [category]: e.target.value });
  };

  useEffect(() => {
    fetchCatalog();
  }, []);

  return (
    <label className={visible ? "filter-by-user__label" : "filter-by-user__label--hidden"}>
      <p>{caption}</p>
      <select name={category} volume={store.id} onChange={handlerChange}>
        <option value="">Все</option>
        {catalog.map((item) => (
          <option key={item.id} value={item.id}>
            {item.company_name}
          </option>
        ))}
      </select>
    </label>
  );
};

export default FilterByCatalog;
