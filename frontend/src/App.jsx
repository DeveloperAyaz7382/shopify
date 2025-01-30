import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import UsersPage from "./pages/UsersPage";
import ProductVariants from "./components/ProductVariants";


const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/users" element={<UsersPage />} />
      <Route path="/variants" element={<ProductVariants />} />
    </Routes>
  </Router>
);

export default App;
