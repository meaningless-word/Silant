import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../hook/useAuth";

import "./Authorize.css";

const Authorize = () => {
  const { signIn, fail } = useAuth();
  const navigate = useNavigate();
  const modalContent = useRef();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    signIn({ username: username, password: password }, () => navigate("/", { replace: true }));
    setError(fail);
  };

  const handleCancel = (e) => {
    if (modalContent.current && !modalContent.current.contains(e.target)) {
      navigate("/");
    }
  };

  return (
    <div className="modal" onClick={handleCancel}>
      <div className="authorize__modal-content" ref={modalContent}>
        <h1>Авторизация</h1>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Логин" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="red-back" type="submit">
            Войти
          </button>
        </form>
        {error && <p>{error}</p>}
      </div>
    </div>
  );
};

export default Authorize;
