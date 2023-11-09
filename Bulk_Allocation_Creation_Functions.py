import datetime
import requests

class direct_allocation_req_class:
  def __init__(self):
    self.reporter_account_id=""
    self.summary=""
    self.project_name_code =""
    self.project_name = ""
    self.resource_account_id = ""
    self.alloc_percent=""
    self.alloc_start=""
    self.alloc_end=""
    self.bill_type=""
    self.allocation_check=""
    self.special_app=""
    self.estimation_attched=""
    self.description=""
    self.is_extra_resource="" ## 18/05/23 Change

def rest_Post_Issue_Create_for_Direct_Allocation_Req_SD(ticket_obj):

    ## -- 18/05/23 Change ---------------------------
    if ticket_obj.is_extra_resource == "Yes":    
         ticket_obj.is_extra_resource = "13466"
    elif ticket_obj.is_extra_resource == "No":
         ticket_obj.is_extra_resource = "13467"
    else:
         ticket_obj.is_extra_resource =""
    ## -- 18/05/23 Change ---------------------------

    #ticket_summary = " [ Bulk Allocation Req ] | " + ticket_obj.summary
    
    json_data = {
        "fields": {
            "project": {"key": "JRT"},
			"reporter": {"accountId": ticket_obj.reporter_account_id},
			"customfield_10021": "jrt/5e0f9480-80fa-44c3-bf54-4f90f4938620",
			"issuetype": {"name":"Resource Allocation"},
			"summary": ticket_obj.summary,
			"customfield_10987": ticket_obj.project_name_code,
			"customfield_11009": ticket_obj.project_name,
			"customfield_10968": {"accountId": ticket_obj.resource_account_id},
			"customfield_11014": ticket_obj.alloc_percent,
			"customfield_11015": ticket_obj.alloc_start,
			"customfield_11016": ticket_obj.alloc_end,
			"customfield_11021": {"value":ticket_obj.bill_type},
			"customfield_11018": {"value":ticket_obj.allocation_check},
			"customfield_11019": {"value":ticket_obj.special_app},
			"customfield_11020": {"value":ticket_obj.estimation_attched},
            "customfield_11144": {"id": ticket_obj.is_extra_resource},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": ticket_obj.description,
                                "type": "text"
                            }
                        ]
                    }
                ]
            }
        }
    }

    endpoint = "https://aifel.atlassian.net/rest/api/3/issue"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA=="  #Gobi's Token
    
    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    r = requests.post(url=endpoint, headers=header_values,json=json_data, timeout=10)

    if r.status_code == 201:
        response = r.json()
        returned_ticket_no = response ['key']
    else:
        returned_ticket_no = "Issue Creating Jira Allocation_Request_Ticket_<<RestCallERROR>>_" + str(r.status_code) + "---" + str(r.json())

    return returned_ticket_no


def get_months_difference_betw_dates(start_date, end_date):
    """Calculate the number of months between two dates"""
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if end_date.day >= start_date.day:
        months += 1
    return months


def rest_get_validations_api_call(jql,req_fields):

    endpoint = "https://aifel.atlassian.net/rest/api/3/search?"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA==" # Nuwanee's Tkn Changed to Gobi's one

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': jql,'fields': req_fields}

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)

    if r.status_code == 200:
        response = r.json()
        #record_count = response['total']
                                       
    else:
        response  = "_RestCallERROR_ --> " + str(r.status_code)
        #record_count = "_RestCallERROR_ --> " + str(r.status_code)

    #return r.status_code, response,record_count
    return r.status_code, response


def validate_record_main_function(all_start,all_end,proj_code,resour_email):
    get_months_diff = get_months_difference_betw_dates (all_start,all_end)
    print ("Records range in months --> " + str(get_months_diff))

    valid_status = ""
    returned_account_id =""
    returned_allocated_hours=""
    
    # 1- Check 6 Months duration validity ------------------
    if get_months_diff > 6:
        valid_status = valid_status + " | " + "Error : Allocation exceeds 6 Months period"
              

    # 2- Check Project card is available --------------------------------
    jql = "project = JRT AND issuetype = 'RM Project Creation' AND status not in (Discontinued, Completed) AND 'JRT_Project Code[Short text]' ~ " + str(proj_code)
    req_fields= "customfield_10988"
    get_proj_card_detail_status_code, get_proj_card_detail_response_json = rest_get_validations_api_call (jql,req_fields)
        
    if get_proj_card_detail_status_code == 200:
             if get_proj_card_detail_response_json['total'] == 0:
                  valid_status = valid_status + " | "  + "Error : No Project card available" 
    else:
        valid_status = valid_status + " | "  + "Error REST Calling project_card_details_check ! " + str(get_proj_card_detail_response_json)
        
        
    # 3- Check Resource card is availble --------------------------
    #jql = "project = JRT AND issuetype = 'RM Resource Creation' AND status = Active AND 'JRT_Resource Email[Short text]' ~ " + "'" + str(resour_email) + "'"
    jql = "project = JRT AND issuetype = 'RM Resource Creation' AND status = Active AND 'JRT_Resource Email[Short text]' ~ " + "'" + str(resour_email) + "'" + " AND 'JRT_Employment Date[Date]' <= " +  all_start  ## 30/06/2023 Changed the Jql to check the resource allocation_start_date validation also in the query 
    req_fields= "customfield_10968,customfield_10978"
    get_resrce_card_detail_status_code, get_resrce_card_detail_response_json = rest_get_validations_api_call (jql,req_fields)

    if get_resrce_card_detail_status_code == 200:
             if get_resrce_card_detail_response_json['total'] == 1:
                  returned_account_id = get_resrce_card_detail_response_json['issues'][0]['fields']['customfield_10968']['accountId']
                  returned_allocated_hours = get_resrce_card_detail_response_json['issues'][0]['fields']['customfield_10978']
             else: 
                  valid_status = valid_status + " | "  + "Error : No Resource card available"
    else:
        valid_status = valid_status + " | "  + "Error REST Calling resource_card_details_check ! " + str(get_resrce_card_detail_response_json)
                    
     
    ## -- Final set value for valid_statue ---------------------
    if valid_status  =="":
         valid_status = "Valid"

    return valid_status,returned_account_id,returned_allocated_hours



