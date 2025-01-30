import { useEffect, useState } from "react";
import { fetchVariants, createVariant, deleteVariant } from "../api/variants";
import { Form, Input, Button, Checkbox, Spin, message, List } from "antd";
import { LoadingOutlined } from "@ant-design/icons";

const ProductVariants = () => {
  const [variants, setVariants] = useState([]);
  const [newVariant, setNewVariant] = useState({
    name: "",
    sku: "",
    weight: 0,
    price: 0,
    options: {
      additionalProp1: "",
      additionalProp2: "",
      additionalProp3: "",
    },
    continue_selling: false,
    image_id: 0,
    quantity: 0,
    product_id: 1,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ✅ Fetch product variants from API
  useEffect(() => {
    setLoading(true);
    fetchVariants()
      .then((data) => {
        setVariants(data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to fetch variants");
        setLoading(false);
      });
  }, []);

  // ✅ Handle input changes
  const handleChange = (e) => {
    if (e.target.name.startsWith("options.")) {
      const optionKey = e.target.name.split(".")[1];
      setNewVariant({
        ...newVariant,
        options: { ...newVariant.options, [optionKey]: e.target.value },
      });
    } else {
      setNewVariant({ ...newVariant, [e.target.name]: e.target.value });
    }
  };

  // ✅ Handle form submission
  const handleSubmit = async (values) => {
    setLoading(true);
    setError("");
    try {
      const createdVariant = await createVariant(values);
      setVariants([...variants, createdVariant]); // Add new variant to list
      message.success("Variant added successfully!");
    } catch (err) {
      setError("Failed to create variant");
      message.error("Error creating variant");
    }
    setLoading(false);
  };

  // ✅ Handle delete
  const handleDelete = async (id) => {
    setLoading(true);
    setError("");
    try {
      await deleteVariant(id);
      setVariants(variants.filter((variant) => variant.id !== id));
      message.success("Variant deleted successfully!");
    } catch (err) {
      setError("Failed to delete variant");
      message.error("Error deleting variant");
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Product Variants</h2>

      {/* Display loading/error message */}
      {loading && <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Form to create a new variant */}
      <Form
        name="newVariant"
        onFinish={handleSubmit}
        initialValues={newVariant}
        layout="vertical"
        style={{ maxWidth: 600, margin: "0 auto" }}
      >
        <Form.Item
          label="Name"
          name="name"
          rules={[{ required: true, message: "Please input the name!" }]}
        >
          <Input onChange={handleChange} />
        </Form.Item>
        <Form.Item
          label="SKU"
          name="sku"
          rules={[{ required: true, message: "Please input the SKU!" }]}
        >
          <Input onChange={handleChange} />
        </Form.Item>
        <Form.Item
          label="Weight"
          name="weight"
          rules={[{ required: true, message: "Please input the weight!" }]}
        >
          <Input type="number" onChange={handleChange} />
        </Form.Item>
        <Form.Item
          label="Price"
          name="price"
          rules={[{ required: true, message: "Please input the price!" }]}
        >
          <Input type="number" onChange={handleChange} />
        </Form.Item>
        <Form.Item
          label="Quantity"
          name="quantity"
          rules={[{ required: true, message: "Please input the quantity!" }]}
        >
          <Input type="number" onChange={handleChange} />
        </Form.Item>
        <Form.Item label="Image ID" name="image_id">
          <Input type="number" onChange={handleChange} />
        </Form.Item>
        <Form.Item label="Continue Selling" name="continue_selling" valuePropName="checked">
          <Checkbox onChange={() => setNewVariant({ ...newVariant, continue_selling: !newVariant.continue_selling })}>
            Continue Selling
          </Checkbox>
        </Form.Item>
        {/* Options Inputs */}
        <Form.Item label="Additional Prop 1" name="options.additionalProp1">
          <Input onChange={handleChange} />
        </Form.Item>
        <Form.Item label="Additional Prop 2" name="options.additionalProp2">
          <Input onChange={handleChange} />
        </Form.Item>
        <Form.Item label="Additional Prop 3" name="options.additionalProp3">
          <Input onChange={handleChange} />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Add Variant
          </Button>
        </Form.Item>
      </Form>

      {/* List of product variants */}
      <List
        bordered
        dataSource={variants}
        renderItem={(variant) => (
          <List.Item
            actions={[
              <Button
                type="danger"
                onClick={() => handleDelete(variant.id)}
                loading={loading}
              >
                Delete
              </Button>,
            ]}
          >
            <List.Item.Meta
              title={variant.name}
              description={`Price: $${variant.price} | SKU: ${variant.sku}`}
            />
          </List.Item>
        )}
      />
    </div>
  );
};

export default ProductVariants;
