from environs import Env
import requests


def get_access_token(client_secret, client_id):
    url = 'https://api.moltin.com/oauth/access_token'
    data = {'grant_type': 'client_credentials',
            'client_secret': client_secret, 'client_id': client_id}
    response = requests.post(url, data=data)
    response.raise_for_status()
    access_token = response.json().get('access_token')
    return access_token


def get_products(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.moltin.com/pcm/products',
                            headers=headers)
    response.raise_for_status()
    raw_products = response.json().get('data')
    response = requests.get('https://api.moltin.com/v2/inventories',
                            headers=headers)
    response.raise_for_status()
    inventories = response.json().get('data')
    return raw_products, inventories


def create_customer(token):
    headers = {
        "Authorization": token,
    }
    payload = {
        "data": {
            "name": "Riko Starkoni",
            "password": "password",
            "email": "lol_email@mail.com",
            "type": "customer",
        }
    }
    response = requests.post(
        "https://api.moltin.com/v2/customers",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()


def create_cart(token, cart_name, cart_id):
    headers = {
        "Authorization": token,
    }
    payload = {
        "data": {
            "name": f"{cart_name}",
            "id": f"{cart_id}",
            "description": "How much is the fish?"
        }
    }
    response = requests.post(
        "https://api.moltin.com/v2/carts",
        json=payload,
        headers=headers
        )
    response.raise_for_status()
    return response.json()


def get_cart(token, cart_id):
    headers = {
        "Authorization": token,
    }
    response = requests.get(
        f"https://api.moltin.com/v2/carts/{cart_id}",
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def add_product_to_cart(token, product, cart_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    json_data = {
        "data": {
            "type": "custom_item",
            "name": product["attributes"]["name"],
            'sku': product["attributes"]["sku"],
            'description': product["attributes"]["description"],
            'quantity': 1,
            'price': {
                'amount': 3,
            },
        },
    }
    response = requests.post(
        f"https://api.moltin.com/v2/carts/{cart_id}/items",
        headers=headers,
        json=json_data
    )
    response.raise_for_status()
    return response.json()


def get_cart_items(token, cart_id):
    headers = {
        "Authorization": token,
    }
    response = requests.get(
        f"https://api.moltin.com/v2/carts/{cart_id}/items",
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    env = Env()
    env.read_env()
    store_id = env.str('STORE_ID')
    client_id = env.str('CLIENT_ID')
    client_secret = env.str('CLIENT_SECRET')
    access_token = get_access_token(client_secret, client_id)
    raw_products, inventories = get_products(access_token)
    # create_customer(access_token)
    cart_name = "Fish"
    cart_id = "101"
    product = raw_products[0]
    # create_cart(access_token, cart_name, cart_id)
    get_cart(access_token, cart_id)
    add_product_to_cart(access_token, product, 'Fish')


if __name__ == "__main__":      
    main()
