// components/StockOrderForm.js
import React,{useState} from "react";
const StockOrderForm = ({ onSubmit }) => {
  const [orderData, setOrderData] = useState({
    optionContract: 'BANKNIFTY',
    expiryDate: '',
    currentATM: '',
    premiumDifference: '',
    quantity: '1',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setOrderData((prevOrderData) => ({ ...prevOrderData, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(orderData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Option Contract:
        <select name="optionContract" value={orderData.optionContract} onChange={handleChange}>
          <option value="BANKNIFTY">BANKNIFTY</option>
          <option value="NIFTY">NIFTY</option>
        </select>
      </label>
      <br />

      <label>
        Expiry Date:
        <input
          type="text"
          name="expiryDate"
          value={orderData.expiryDate}
          onChange={handleChange}
          placeholder="YYYY-MM-DD"
        />
      </label>
      <br />

      <label>
        Current ATM:
        <input
          type="text"
          name="currentATM"
          value={orderData.currentATM}
          onChange={handleChange}
          placeholder="e.g., 21400"
        />
      </label>
      <br />

      <label>
        Premium Difference:
        <input
          type="number"
          name="premiumDifference"
          value={orderData.premiumDifference}
          onChange={handleChange}
          placeholder="e.g., 50"
        />
      </label>
      <br />

      <label>
        Quantity:
        <input
          type="number"
          name="quantity"
          value={orderData.quantity}
          onChange={handleChange}
          placeholder="e.g., 10"
        />
      </label>
      <br />

      <button type="submit">Place Order</button>
    </form>
  );
};

export default StockOrderForm;
