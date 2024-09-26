import React, { useRef, useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../../../Shared/api.jsx";
import Bit from "../../../../Shared/Bit/Bit.jsx";
import "./Details.css";
import toLeft from "../../../../Shared/images/to-left.svg";
import toRight from "../../../../Shared/images/to-right.svg";

const Details = ({ id, setId }) => {
  const modalContentRef = useRef();
  const bannerRef = useRef();

  const [data, setData] = useState({});
  const [model, setModel] = useState({});
  const [engine, setEngine] = useState({});
  const [transmission, setTransmission] = useState({});
  const [leading, setLeading] = useState({});
  const [steerable, setSteerable] = useState({});

  const fetchData = () => {
    axios
      .get(`${API_URL}machines/${id}`)
      .then((response) => {
        return response.data;
      })
      .then((data) => {
        setData(data);
        setModel(data.model);
        setEngine(data.engine_model);
        setTransmission(data.transmission_model);
        setLeading(data.leading_axle_model);
        setSteerable(data.steerable_axle_model);
      })
      .catch((error) => console.error("Error fetching machines data by id:", error));
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
      <div className="details__modal-content" ref={modalContentRef}>
        <div className="client-info__details-container" key={id}>
          <button className="client-info__button" onClick={handlerScrollPrev}>
            <img src={toLeft} alt="<" />
          </button>
          <div className="client-info__details-slider" ref={bannerRef}>
            <Bit title="техника" model={model.name} serial={data.serial} description={model.description} />
            <Bit title="двигатель" model={engine.name} serial={data.engine_serial} description={engine.description} />
            <Bit title="трансмиссия" model={transmission.name} serial={data.transmission_serial} description={transmission.description} />
            <Bit title="ведущий мост" model={leading.name} serial={data.leading_axle_serial} description={leading.description} />
            <Bit title="управляемый мост" model={steerable.name} serial={data.steerable_axle_serial} description={steerable.description} />
          </div>
          <button className="client-info__button" onClick={handlerScrollNext}>
            <img src={toRight} alt=">" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Details;
