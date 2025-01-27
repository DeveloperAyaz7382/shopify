import axios from "axios";

const API_BASE_URL = 'http://127.0.0.1:8000';

export const fetchUsers = async () => {
  const response = await axios.get(`${API_BASE_URL}/users`);
  return response.data;
};

export const createUser = async (user) => {
  const response = await axios.post(`${API_BASE_URL}/users`, user);
  return response.data;
};


export const updateUser = async (userId, user) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/${userId}`, user);
    return response.data;
  } catch (error) {
    console.error(`Error updating user with ID ${userId}:`, error.message);
    throw error;
  }
};


export const deleteUser = async (userId) => {
  await axios.delete(`${API_BASE_URL}/users/${userId}`);
};
