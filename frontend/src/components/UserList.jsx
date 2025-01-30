import React, { useEffect, useState } from "react";
import { Table, Button, Popconfirm, message, Modal, Form, Input, Select } from "antd";
import { fetchUsers, deleteUser, updateUser } from "../api/users";

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch((err) => console.error("Error:", err));
  }, []);

  const handleDelete = async (userId) => {
    try {
      await deleteUser(userId);
      setUsers(users.filter((user) => user.id !== userId));
      message.success("User deleted successfully!");
    } catch (error) {
      console.error("Error deleting user:", error);
      message.error("Failed to delete user.");
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    form.setFieldsValue(user);
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setEditingUser(null);
  };

  const handleSave = async () => {
    try {
      const updatedUser = await updateUser(editingUser.id, form.getFieldsValue());
      setUsers(users.map((user) => (user.id === updatedUser.id ? updatedUser : user)));
      setIsModalVisible(false);
      setEditingUser(null);
      message.success("User updated successfully!");
    } catch (error) {
      console.error("Error updating user:", error);
      message.error("Failed to update user.");
    }
  };

  const columns = [
    {
      title: "First Name",
      dataIndex: "first_name",
      key: "first_name",
    },
    {
      title: "Last Name",
      dataIndex: "last_name",
      key: "last_name",
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "phone",
      dataIndex: "phone",
      key: "phone",
    },
    {
      title: "Actions",
      key: "actions",
      render: (_, user) => (
        <>
          <Button onClick={() => handleEdit(user)} style={{ marginRight: 8 }}>
            Edit
          </Button>
          <Popconfirm
            title="Are you sure to delete this user?"
            onConfirm={() => handleDelete(user.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button danger>Delete</Button>
          </Popconfirm>
        </>
      ),
    },
  ];

  return (
    <div>
      <h2>Users</h2>
      <Table
        dataSource={users}
        columns={columns}
        rowKey="id"
        pagination={false}
        bordered
      />
      <Modal
        title="Edit User"
        visible={isModalVisible}
        onOk={handleSave}
        onCancel={handleCancel}
        okText="Save"
        cancelText="Cancel"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="first_name"
            label="First Name"
            rules={[{ required: true, message: "Please input the first name!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="last_name"
            label="Last Name"
            rules={[{ required: true, message: "Please input the last name!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, message: "Please input the email!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="phone"
            label="Phone"
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="role"
            label="Role"
            rules={[{ required: true, message: "Please select the role!" }]}
          >
            <Select>
              <Select.Option value="Customer">Customer</Select.Option>
              <Select.Option value="Admin">Admin</Select.Option>
              <Select.Option value="Supplier">Supplier</Select.Option>
              <Select.Option value="Staff">Staff</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserList;
