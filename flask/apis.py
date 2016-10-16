from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key="Ybgxn8fAjGVLNvjh-DGnrg",
    consumer_secret="HS8MmSHy7yYis_dkiJhyd5Kk6pI",
    token="xXQ3qCZr9vkRKZ-nqmem3w0bOORK_s5w",
    token_secret="4soDIWMkyD83RbWdl8SgcvtOdAk"
)


client = Client(auth)

params = {
    'term': 'food',
    'lang': 'fr'
}

res = client.search('San Francisco', **params)

