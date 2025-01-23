import React, { useEffect, useState } from "react";
import { fetchUsers, deleteUser } from "../api/users";

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch((err) => console.error("Error:", err));
  }, []);

  const handleDelete = async (userId) => {
    try {
      await deleteUser(userId);
      setUsers(users.filter((user) => user.id !== userId));
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.first_name} {user.last_name} ({user.email})
            <button onClick={() => handleDelete(user.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
