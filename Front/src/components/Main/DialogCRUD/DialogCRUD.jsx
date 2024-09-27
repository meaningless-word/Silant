import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

import { API_URL } from "../../../Shared/api.jsx";
import { useAuth } from "../../../hook/useAuth.jsx";
import "./DialogCRUD.css";

const DialogCRUD = ({ param, setParam }) => {
  const { token } = useAuth();
  const [data, setData] = useState({});

  const modalContentRef = useRef();

  const handlerCancel = (e) => {
    if (modalContentRef.current && !modalContentRef.current.contains(e.target)) {
      setParam();
    }
  };

  return (
    <div className="modal" onClick={handlerCancel}>
      <div className="dialog-crud__modal-content" ref={modalContentRef}></div>
    </div>
  );
};

export default DialogCRUD;
