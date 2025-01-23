import React, { useState } from "react";
import CreateUserForm from "../components/CreateUserForm";
import UserList from "../components/UserList";

const UsersPage = () => {
  const [refresh, setRefresh] = useState(false);

  const handleUserCreated = () => {
    setRefresh(!refresh); // Trigger refresh of the user list
  };

  return (
    <div>
      <h1>Users Management</h1>
      <CreateUserForm onUserCreated={handleUserCreated} />
      <UserList key={refresh} />
    </div>
  );
};

export default UsersPage;
