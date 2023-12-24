// App.js
import React, { useState, useEffect } from 'react';
import StockOrderForm from './components/StockOrderForm';
import api from './services/api';

const App = () => {
  
  const [notification, setNotification] = useState(null);
  const [error, setError] = useState(null);
  const [stockOrder, setStockOrder] = useState({});

  const handleStockOrderSubmit = async (order) => {
    try {
      
      // Call the new endpoint that performs the strategy calculation
      setNotification('Processing your request, please wait...');
      const response = await api.calculateStrategy(order);
      console.log('Response from backend:', response); // Log the response
      
      if (response.error_message) {
        // Handle error from the backend
        setError(response.error_message);
      } else {
        // If successful, update the state with the result
        setStockOrder(response);
        setNotification('Strategy implemented ');
      }

    } catch (error) {
      console.error('Error calculating strategy:', error.message);
      console.error('Error details:', error.response?.data); // Added '?'
      setError('Failed to calculate strategy. Please check the console for more details.');
    }
  };

  return (
    <div>
      {notification && <p>{notification}</p>}
      {error && (
        <div>
          <p>Error: {error}</p>
        </div>
      )}
      {!stockOrder.order_placed ? (
        <StockOrderForm onSubmit={handleStockOrderSubmit} />
      ) : (
        <div>
          {stockOrder.order_placed ? (
            <div>
              <p>Strategy calculated successfully!</p>
              <p>Individual order details:</p>
              {stockOrder.additional_info && (
                <ul>
                  {stockOrder.additional_info.map((orderResponse) => (
                    <li key={orderResponse.order_tag}>
                      Order Tag: {orderResponse.order_tag}, Order ID: {orderResponse.order_id}, Status: {orderResponse.status}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            <div>
              <p>Error calculating strategy:</p>
              <p>{stockOrder.error_message}</p>
              {stockOrder.individual_order_responses && (
                <ul>
                  {stockOrder.individual_order_responses.map((orderResponse) => (
                    <li key={orderResponse.order_tag}>
                      Order Tag: {orderResponse.order_tag}, Error Message: {orderResponse.error_message}, Status: {orderResponse.status}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
