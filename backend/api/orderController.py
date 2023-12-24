# orderController.py
from pya3 import TransactionType, OrderType, ProductType

def place_general_order(alice, instrument, quantity, action):
    print("Received arguments:", alice, instrument, quantity, action)
    try:
        response = alice.place_order(
            transaction_type=TransactionType.Buy if action.lower() == 'buy' else TransactionType.Sell,
            instrument=instrument,
            quantity=quantity,
            order_type=OrderType.Market,
            product_type=ProductType.Intraday,
            price=0.0,
            trigger_price=None,
            stop_loss=None,
            square_off=None,
            trailing_sl=None,
            is_amo=False,
            order_tag='order1'
        )

        # Check 'stat' value in the response
        if response.get('stat') == 'Ok':
            order_id = response.get('NOrdNo', '')
            print(f"Order placed successfully. Order ID: {order_id}")
            return order_id
        else:
            error_message = response.get('emsg', 'Unknown error')
            raise Exception(f"Error placing order: {error_message}")
    except Exception as e:
        print(f"Error placing order: {e}")
        # Re-raise the exception to propagate it
        raise e
