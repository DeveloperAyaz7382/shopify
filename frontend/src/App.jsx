import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import UsersPage from "./pages/UsersPage";

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/users" element={<UsersPage />} />
    </Routes>
  </Router>
);

export default App;
