import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";

import "./App.css";
import "./fonts/fonts.css";

import { AuthProvider } from "./hoc/AuthProvider.jsx";
import Header from "./components/Header/Header.jsx";
import Main from "./components/Main/Main.jsx";
import Authorize from "./components/Main/Authorize/Authorize.jsx";
import Footer from "./components/Footer/Footer.jsx";

function App() {
  const [tabIndex, setTabIndex] = useState(0);

  return (
    <AuthProvider>
      <Header />
      <Routes>
        <Route path="/" element={<Main tabIndex={tabIndex} setTabIndex={setTabIndex} />} />
        <Route path="/login" element={<Authorize />} />
      </Routes>
      <Footer />
    </AuthProvider>
  );
}

export default App;
