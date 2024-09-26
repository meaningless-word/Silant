import React, { useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../../Shared/api.jsx";
import Cell from "../../../Shared/Cell/Cell.jsx";
import FilterPanel from "../FilterPanel/FilterPanel.jsx";
import Details from "./Details/Details.jsx";
import "./SharedInfo.css";

const SharedInfo = () => {
  const [data, setData] = useState([]);
  const [isEmpty, setIsEmpty] = useState(false);
  const [detailMe, setDetailMe] = useState();

  const [filter, setFilter] = useState({
    serial: "",
    tec: "",
    eng: "",
    trm: "",
    lda: "",
    sta: "",
  });

  const fetchData = async () => {
    try {
      const query = Object.entries(filter)
        .map((x) => (x[1] ? x.join("=") : ""))
        .reduce((acc, cur) => (cur ? `${acc}${acc ? "&" : ""}${cur}` : acc));

      const response = await axios.get(`${API_URL}machines/${query ? "?" + query : ""}`);
      setData(response.data);
      setIsEmpty(response.data.length === 0);
    } catch (error) {
      console.error("Error fetching machines data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [filter]);

  const handleSearch = () => {
    setFilter({ ...filter, serial: document.getElementById("searcher").value });
  };

  const handleSelect = (e) => {
    let element = e.target;
    while (element && element.tagName != "TR") {
      element = element.parentElement;
    }
    setDetailMe(element.id.split("-")[1]);
  };

  return (
    <div className="shared-info">
      <h1>Проверьте комплектацию и технические характеристики техники Силант</h1>
      <div className="shared-info__search-panel">
        <input id="searcher" type="text" placeholder="Заводской номер" />
        <button className="red-back" onClick={handleSearch}>
          Поиск
        </button>
      </div>

      <FilterPanel filter={filter} setFilter={setFilter} />

      <h3>Информация о комплектации и технических характеристиках Вашей техники</h3>
      <div className="shared-info__table-container">
        <table className="shared-info__table">
          <thead>
            <tr>
              <th></th>
              <th>техника</th>
              <th>двигатель</th>
              <th>трансмиссия</th>
              <th>ведущий мост</th>
              <th>управляемый мост</th>
            </tr>
          </thead>
          <tbody>
            {data.map((machine) => (
              <tr id={"machine-" + machine.id} key={machine.id} onClick={handleSelect}>
                <th>
                  <Cell model="модель" serial="серийный №" />
                </th>
                <td>
                  <Cell model={machine.model_name} serial={machine.serial} />
                </td>
                <td>
                  <Cell model={machine.engine_model_name} serial={machine.engine_serial} />
                </td>
                <td>
                  <Cell model={machine.transmission_model_name} serial={machine.transmission_serial} />
                </td>
                <td>
                  <Cell model={machine.leading_axle_model_name} serial={machine.leading_axle_serial} />
                </td>
                <td>
                  <Cell model={machine.steerable_axle_model_name} serial={machine.steerable_axle_serial} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {isEmpty && <h3>Данных о машине с таким заводским номером нет в системе.</h3>}
      {detailMe && <Details id={detailMe} setId={setDetailMe} />}
    </div>
  );
};

export default SharedInfo;
