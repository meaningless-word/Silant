import React from "react";
import "./Cell.css";

const Cell = ({ model, serial }) => {
  return (
    <div className="cell-container">
      <div>{model}</div>
      <div>{serial}</div>
    </div>
  );
};

export default Cell;
