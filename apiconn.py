import requests
from decouple import config


def getapidata():
    url = "https://data.brreg.no/enhetsregisteret/api/enheter?size="+config('AMOUNT_OF_ENTRIES')
    r = requests.get(url)
    data = r.json()
    return data
