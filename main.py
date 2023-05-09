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


def main() -> None:
    env = Env()
    env.read_env()
    store_id = env.str('STORE_ID')
    client_id = env.str('CLIENT_ID')
    client_secret = env.str('CLIENT_SECRET')
    access_token = get_access_token(client_secret, client_id)
    print(access_token)
    raw_products, inventories = get_products(access_token)
    print(raw_products, inventories)


if __name__ == "__main__":
    main()
