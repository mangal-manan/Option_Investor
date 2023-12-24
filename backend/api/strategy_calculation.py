# strategy_calculation.py
from pya3.alicebluepy import Aliceblue
from pya3 import TransactionType, OrderType, ProductType

def calculate_strategy(alice, order):
    try:
        # Calculate PEotmStrike and CEotmStrike
        PEotmStrike = str(int(order.currentATM) + order.premiumDifference)
        CEotmStrike = str(int(order.currentATM) - order.premiumDifference)

        # Define individual orders within the basket order
        basket_order = [
            {
                "instrument": alice.get_instrument_for_fno(
                    exch="NFO",
                    symbol=order.optionContract,
                    expiry_date=order.expiryDate,
                    is_fut=False,
                    strike=float(order.currentATM),
                    is_CE=True
                ),
                "order_type": OrderType.Market,
                "quantity": order.quantity,
                "transaction_type": TransactionType.Sell,
                "product_type": ProductType.Intraday,
                "order_tag": "Sell_CE"
            },
            {
                "instrument": alice.get_instrument_for_fno(
                    exch="NFO",
                    symbol=order.optionContract,
                    expiry_date=order.expiryDate,
                    is_fut=False,
                    strike=float(order.currentATM),
                    is_CE=False
                ),
                "order_type": OrderType.Market,
                "quantity": order.quantity,
                "transaction_type": TransactionType.Sell,
                "product_type": ProductType.Intraday,
                "order_tag": "Sell_PE"
            },
            {
                "instrument": alice.get_instrument_for_fno(
                    exch="NFO",
                    symbol=order.optionContract,
                    expiry_date=order.expiryDate,
                    is_fut=False,
                    strike=float(PEotmStrike),
                    is_CE=False
                ),
                "order_type": OrderType.Market,
                "quantity": order.quantity,
                "transaction_type": TransactionType.Buy,
                "product_type": ProductType.Intraday,
                "order_tag": "Buy_PE"
            },
            {
                "instrument": alice.get_instrument_for_fno(
                    exch="NFO",
                    symbol=order.optionContract,
                    expiry_date=order.expiryDate,
                    is_fut=False,
                    strike=float(CEotmStrike),
                    is_CE=True
                ),
                "order_type": OrderType.Market,
                "quantity": order.quantity,
                "transaction_type": TransactionType.Buy,
                "product_type": ProductType.Intraday,
                "order_tag": "Buy_CE"
            },
        ]

        # Place the basket order
        basket_order_response = alice.place_basket_order(basket_order)
        
        # Check the basket order response and extract individual order details or errors
        individual_order_responses = []
        for i, response in enumerate(basket_order_response):
            if response.get('stat') == 'Ok':
                individual_order_responses.append({
                    'order_tag': basket_order[i]['order_tag'],
                    'order_id': response.get('NOrdNo'),
                    'status': 'Success'
                })
            else:
                individual_order_responses.append({
                    'order_tag': basket_order[i]['order_tag'],
                    'error_message': response.get('emsg'),
                    'status': 'Error'
                })

        print(individual_order_responses)
        # Check if all individual orders were successful
        if all(response['status'] == 'Success' for response in individual_order_responses):
            # If all individual orders are successful, return a success response with individual order details
            return {
                'order_placed': True,
                'individual_order_responses': individual_order_responses,
            }
        else:
            # If any individual order fails, return an error response with individual order details
            return {
                'order_placed': False,
                'individual_order_responses': individual_order_responses,
                'error_message': 'Failed to place one or more individual orders'
            }

    except Exception as e:
        print("Error calculating strategy:", e)
        # If an error occurs during strategy calculation, return an error response
        return {'error_message': 'Failed to calculate strategy'}
