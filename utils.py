import json
from . import constants as consts
def update_token(sesh,file_name=None):
    """
Sets token for the session object used to make all the api calls.

 Assumes you have the token in your working directory, alternatively you can supply a path to your token with the file_name parameter.
"""
    if file_name == None:
        file_name = 'config.json'
    config = json.load(open(file_name,'rb'))
    token_response = sesh.post(consts.TOKEN_ENDPOINT,
                               data= {'client_id': config["ClientId"],
                                      'client_secret': config["ClientSecret"],
                                      'scope': 'icdapi_access',
                                      'grant_type': 'client_credentials'},
                               verify=True).json()
    token = token_response['access_token']
    sesh.headers.update({'Authorization':  'Bearer '+ token,
                         'Accept': 'application/json',
                         'API-Version':'v2',
                         'Accept-Language': 'en'})

def check_for_string(value, name):
    """Checks that value has type str. name is the identifier of value"""
    return _check_for_type(value, name, str)

def check_for_bool(value, name):
    """Checks that value has type bool. name is the identifier of value"""
    return _check_for_type(value, name, bool)


def _check_for_type(value, name, type_):
    """Factory function to check for types"""
    if not isinstance(value, type_):
        raise ValueError(f'Expected {name} in {type_.__name__} format you passed:',type(value))
    return True
