import React, { useState } from "react";
import { createUser } from "../api/users";

const CreateUserForm = ({ onUserCreated }) => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
    role: "Customer",
  });

  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const newUser = await createUser(formData);
      setSuccess(true);
      setFormData({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        role: "Customer",
      });
      if (onUserCreated) onUserCreated(newUser); // Notify parent component
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create user");
    }
  };

  return (
    <div>
      <h2>Create New User</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>First Name:</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Phone:</label>
          <input
            type="text"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Role:</label>
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
          >
            <option value="Customer">Customer</option>
            <option value="Admin">Admin</option>
            <option value="Supplier">Supplier</option>
            <option value="Staff">Staff</option>
          </select>
        </div>
        <button type="submit">Create User</button>
      </form>

      {success && <p style={{ color: "green" }}>User created successfully!</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default CreateUserForm;
