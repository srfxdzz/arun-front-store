
from coinbase_commerce.client import Client

API_KEY = 'c37f6972-5748-4ddc-bcff-35b874dd0023'

def create_payment():
    
    client = Client(api_key=API_KEY)
    
    charge = {
        'name': 'Product Payment',
        'description': 'Payment for a $10 product',
        'pricing_type': 'fixed_price',
        'local_price': {
            'amount': '10.00',  
            'currency': 'USD'
        },
        'redirect_url': 'https://example.com/success',  
        'cancel_url': 'https://example.com/cancel'
    }

    try:
        # Create the payment charge
        charge_result = client.charge.create(**charge)
        # Print the hosted payment URL
        return charge_result['hosted_url']
    except Exception as e:
        return e 


