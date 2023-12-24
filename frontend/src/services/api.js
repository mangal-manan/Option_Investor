// services/api.js
const BASE_URL = process.env.REACT_APP_BACKEND_URL; // Update with your backend URL

const api = {
  // async submitUserCredentials(credentials) {
  //   // Call the backend endpoint for submitting user credentials
  //   const response = await fetch(`${BASE_URL}/submit_user_credentials`, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(credentials),
  //   });

  //   if (!response.ok) {
  //     throw new Error('Failed to submit user credentials');
  //   }

  //   return response.json();
  // },

  async calculateStrategy(order) {
    // Call the backend endpoint for calculating strategy
    const response = await fetch(`${BASE_URL}/calculate_strategy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(order),
    });

    if (!response.ok) {
      throw new Error('Failed to calculate strategy');
    }

    return response.json();
  },

  
  // async placeStockOrder(order) {
  //   // Call the backend endpoint for placing a stock order
  //   const response = await fetch(`${BASE_URL}/place_stock_order`, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(order),
  //   });

  //   if (!response.ok) {
  //     throw new Error('Failed to place stock order');
  //   }

  //   return response.json();
  // },
};

export default api;
