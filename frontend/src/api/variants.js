import axios from "axios";

const API_URL = 'http://127.0.0.1:8000'; // FastAPI backend URL

// ✅ Fetch all product variants
export const fetchVariants = async () => {
  const response = await axios.get(`${API_URL}/variants`);
  return response.data;
};

// ✅ Create a new product variant
export const createVariant = async (variant) => {
  const response = await axios.post(`${API_URL}/variants`, variant);
  return response.data;
};

// ✅ Delete a product variant
export const deleteVariant = async (id) => {
  await axios.delete(`${API_URL}/${id}`);
};
