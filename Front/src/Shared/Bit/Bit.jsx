import React from "react";
import "./Bit.css";

const Bit = ({ title, model, serial, nameless, description }) => {
  return (
    <div className="bit-box">
      <div className="bit-box__header">{title}</div>
      {model ? (
        <div className="bit-box__model">
          <span>модель</span>
          <span>{model}</span>
        </div>
      ) : null}
      {serial ? (
        <div className="bit-box__model">
          <span>серийный №</span>
          <span>{serial}</span>
        </div>
      ) : null}
      {nameless ? <div className="bit-box__nameless">{nameless}</div> : null}
      {description ? <div className={"bit-box__text display-linebreak"}>{description}</div> : null}
    </div>
  );
};

export default Bit;
