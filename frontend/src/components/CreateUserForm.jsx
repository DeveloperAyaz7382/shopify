import React, { useState } from "react";
import { createUser } from "../api/users";
import { Form, Input, Select, Button, message } from "antd";

const { Option } = Select;

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

  const handleChange = (value, key) => {
    setFormData((prevData) => ({ ...prevData, [key]: value }));
  };

  const handleSubmit = async (values) => {
    setError(null);
    try {
      const newUser = await createUser(values);
      message.success("User created successfully!");
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
      message.error("Failed to create user");
    }
  };

  return (
    <div>
      <h2>Create New User</h2>
      <Form
        name="createUserForm"
        onFinish={handleSubmit}
        initialValues={formData}
        layout="vertical"
      >
        <Form.Item
          label="First Name"
          name="first_name"
          rules={[{ required: true, message: "First name is required" }]}
        >
          <Input
            value={formData.first_name}
            onChange={(e) => handleChange(e.target.value, "first_name")}
          />
        </Form.Item>

        <Form.Item label="Last Name" name="last_name">
          <Input
            value={formData.last_name}
            onChange={(e) => handleChange(e.target.value, "last_name")}
          />
        </Form.Item>

        <Form.Item
          label="Email"
          name="email"
          rules={[{ required: true, message: "Please input a valid email!" }]}
        >
          <Input
            type="email"
            value={formData.email}
            onChange={(e) => handleChange(e.target.value, "email")}
          />
        </Form.Item>

        <Form.Item label="Phone" name="phone">
          <Input
            value={formData.phone}
            onChange={(e) => handleChange(e.target.value, "phone")}
          />
        </Form.Item>

        <Form.Item
          label="Password"
          name="password"
          rules={[{ required: true, message: "Password is required" }]}
        >
          <Input.Password
            value={formData.password}
            onChange={(e) => handleChange(e.target.value, "password")}
          />
        </Form.Item>

        <Form.Item label="Role" name="role">
          <Select
            value={formData.role}
            onChange={(value) => handleChange(value, "role")}
          >
            <Option value="Customer">Customer</Option>
            <Option value="Admin">Admin</Option>
            <Option value="Supplier">Supplier</Option>
            <Option value="Staff">Staff</Option>
          </Select>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            Create User
          </Button>
        </Form.Item>
      </Form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default CreateUserForm;
