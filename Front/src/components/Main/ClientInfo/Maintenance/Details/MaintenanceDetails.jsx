import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

import { API_URL } from "../../../../../Shared/api.jsx";
import { useAuth } from "../../../../../hook/useAuth.jsx";
import Bit from "../../../../../Shared/Bit/Bit.jsx";

import "./MaintenanceDetails.css";
import toLeft from "../../../../../Shared/images/to-left.svg";
import toRight from "../../../../../Shared/images/to-right.svg";

const MaintenanceDetails = ({ id, setId }) => {
  const modalContentRef = useRef();
  const bannerRef = useRef();
  const { token } = useAuth();

  const [data, setData] = useState({});
  const [maintenance_type, setMaintenanceType] = useState({});
  const [service_company, setServiceCompany] = useState({});

  const fetchData = () => {
    axios
      .get(`${API_URL}maintenances/${id}`, {
        headers: {
          Authorization: `Bearer ${token.access}`,
        },
      })
      .then((response) => {
        return response.data;
      })
      .then((data) => {
        setData(data);
        setMaintenanceType(data.maintenance_type);
        setServiceCompany(data.service_company ?? {});
      })
      .catch((error) => console.error("Error fetching maintenance detailed data:", error));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlerCancel = (e) => {
    if (modalContentRef.current && !modalContentRef.current.contains(e.target)) {
      setId();
    }
  };

  const handlerScrollPrev = () => {
    if (bannerRef.current) {
      const boxElement = document.getElementsByClassName("bit-box")[0];
      bannerRef.current.scrollLeft -= bannerRef.current.clientWidth / Math.floor(bannerRef.current.clientWidth / boxElement.clientWidth) - 2;
    }
  };

  const handlerScrollNext = () => {
    if (bannerRef.current) {
      const boxElement = document.getElementsByClassName("bit-box")[0];
      bannerRef.current.scrollLeft += bannerRef.current.clientWidth / Math.floor(bannerRef.current.clientWidth / boxElement.clientWidth) - 2;
    }
  };

  return (
    <div className="modal" onClick={handlerCancel}>
      <div className="maintenance-details__modal-content" ref={modalContentRef}>
        <div className="client-info__details-container" key={id}>
          <button className="client-info__button" onClick={handlerScrollPrev}>
            <img src={toLeft} alt="<" />
          </button>
          <div className="client-info__details-slider" ref={bannerRef}>
            <Bit title="техника" model={data.machine_model} serial={data.machine_serial} description={data.machine_description} />
            <Bit title="вид ТО" nameless={maintenance_type.name} description={maintenance_type.description} />
            <Bit title="дата проведения ТО" nameless={data.maintenance_date} />
            <Bit title="наработка, м/час" nameless={data.engine_hours} />
            <Bit title="№ заказ-наряда" nameless={data.order_number} />
            <Bit title="дата заказ-наряда" nameless={data.order_date} />
            <Bit title="сервисная компания" nameless={service_company.company_name ?? "самостоятельно"} />
          </div>
          <button className="client-info__button" onClick={handlerScrollNext}>
            <img src={toRight} alt=">" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default MaintenanceDetails;
