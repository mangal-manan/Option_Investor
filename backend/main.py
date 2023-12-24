# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.orderController import place_general_order
from api.strategy_calculation import calculate_strategy
from pya3 import * # Import the broker's SDK
from pya3.alicebluepy import Aliceblue
import os
from dotenv import load_dotenv

app = FastAPI()

# CORS configuration
origins = [os.getenv("FRONTEND_URL", "http://localhost:3000")]    # need to update while deploying
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get sensitive information from environment variables
load_dotenv()  # Load variables from .env file
userID = os.getenv("ALICEBLUE_USER_ID")
apiKey = os.getenv("ALICEBLUE_API_KEY")

# Initialize the AliceBlue object with your user ID and API key
alice = Aliceblue(user_id=userID, api_key=apiKey)
alice.get_session_id() # Get Session ID

class StockOrder(BaseModel):
    optionContract: str # BANKNIFTY/NIFTY
    expiryDate: str # YYYY-MM-DD
    currentATM: str 
    premiumDifference: int
    quantity: int

@app.post("/calculate_strategy")
def calculate_strategy_endpoint(order: StockOrder):
    try:
        # Pass the input data and Alice object to the strategy calculation function
        response = calculate_strategy(alice, order)
        
        # Check the response and perform further actions
        if response.get('order_placed'):
            # If order placed successfully, you can return a success message or additional information
            return {"order_placed": 1 ,"message": "Strategy processed successfully", "additional_info": response.get('individual_order_responses')}
        else:
            # If an error occurred, return an appropriate response
            raise HTTPException(status_code=500, detail=response.get('error_message', 'Failed to process strategy'))

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Failed to place stock order")

# @app.post("/place_stock_order")
# def place_stock_order(order: StockOrder):
#     try:
#         # Log the received order for debugging purposes
#         print("Received order:", order.dict())
        
#         # Get instrument details
#         instrument = alice.get_instrument_for_fno(
#             exch="NFO",
#             symbol=order.symbol,
#             expiry_date=order.expiry_date,
#             is_fut=order.is_fut,
#             strike=order.strike,
#             is_CE=order.is_CE
#         )

#         # Log instrument details
#         print("Instrument details:", instrument)

#         # Place stock order using the orderController
#         order_id=final_place_stock_order(alice, instrument, order.quantity, order.action)
        
#         # For testing purposes, returning the received order as response
#         # Return the order ID to the client
#         return {"message": "Order placed successfully", "order_id": order_id}
    
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail="Failed to place stock order")


    if __name__ == "__main__":
        import uvicorn

        # Run the application with uvicorn in synchronous mode
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")