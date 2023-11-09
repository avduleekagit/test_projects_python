import requests
import logging


def rest_get_UserStatus_Check(inp_account_id):

    endpoint = "https://aifel.atlassian.net/rest/api/3/user?"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA==" # Gobi's Tkn

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'accountId': inp_account_id,'fields': "active"}

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)

    if r.status_code == 200:
        response = r.json()
        user_status = response['active']
        if user_status is True:
            returned_user_status = "Proceed"
        else:
            returned_user_status = "User profile not in active state, Hence Rejected --->>> " + str(user_status)                               
    else:
        returned_user_status  = "_RestCallERROR_ --> " + str(r.status_code)

    return returned_user_status

### ----------------------------------------------------------------

def rest_get_user_validations_jql_call(jql,req_fields):

    endpoint = "https://aifel.atlassian.net/rest/api/3/search?"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA==" # Gobi's Tkn

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': jql,'fields': req_fields}

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)

    if r.status_code == 200:
        response = r.json()
        #record_count = response['total']
                                       
    else:
        response  = "_RestCallERROR_ --> " + str(r.status_code)

    return r.status_code, response

# - - - - ---------------------------------------------------------------

########=============================================================

if __name__ == "__main__":
    user_state = rest_get_UserStatus_Check("618b506997825300687c951e")
    print(user_state)

## Deactivate : 618b506997825300687c951e
## Active : 5d898ebc6e35df0c499748bc