import requests

def prestep_1_ta_get_token():
    url = "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/oauth2/token"
    headers = {
        "Content-Type": "application/JSON"
    }
    data = {
        "client_id":"5e263ba0-8ed6-4dbe-b52e-6b14ab15ba04",
        #"client_secret":,
        "grant_type": "client_credentials",
        "resource": "https://tSAPWSAADApp",
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    set_environment_variable("var_TA_Access_Token", response_data.get("access_token"))

    # Test logic
    if response_data.get("token_type") != "Bearer":
        print("Test Automation Access token was not returned! Can't move forward.")
    else:
        print("Test Automation access token was retrieved successfully.")

token = prestep_1_ta_get_token()
print(token)
