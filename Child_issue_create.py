import requests
import logging
import math
import datetime


##############################
class parent_ticket_class:
  def __init__(self):
    self.key =""
    self.resource_name = ""
    self.project_name = ""
    self.project_name_code =""
    self.resource_email=""
    self.alloc_start=""
    self.alloc_end=""
    self.confirmed_end=""
    self.hou_per_day=""
    self.alloc_percent=""
    self.bill_type=""
    self.country_code=""
    self.proj_status_type=""
    #self.resolution=""
    self.resource_prev_name=""
    self.resource_first_last_name=""
    self.resource_practice=""
    self.project_dyn_code=""
    self.reporter=""
    ## -- - -  Added for 'Change' Ticket details
    self.orig_tkt_id_for_change=""
    ## --- 19/05/23 CR -- added new field JRT_Extra_Resource
    self.is_extra_resource=""
    ## --- 23/06/23 Fix -- get JRT_Over Allocation details
    self.is_over_allocation=""


################################################################
def rest_get_Parent_Details(parent_ticket_key):

    parent_ticket_obj = parent_ticket_class()

    endpoint = "https://aifel.atlassian.net/rest/api/3/issue/" + parent_ticket_key
    token = "Basic ZHVsZWVrYS5yb3NoaW5pZUBheGlhdGFkaWdpdGFsbGFicy5jb206SVJPSW1kV3lHeE5QRHFBdVJmQlZCMkQ3"  # Roshinie's Token
    
    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'fields': "customfield_10987,customfield_11011,customfield_10988,customfield_10971,customfield_11015,customfield_11016,customfield_11012,customfield_11024,customfield_11014,customfield_11021,customfield_10976,customfield_11006,resolution,customfield_10969,customfield_10970,customfield_10975,customfield_10987,reporter,customfield_11008,customfield_11144,customfield_11018"}
    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)

    if r.status_code == 200:
        response = r.json()
        if len(response) > 0:
            parent_ticket_obj.key = response ['key']
            #parent_ticket_obj.resource_name = response ['fields']['customfield_11011']['emailAddress']
            parent_ticket_obj.resource_name = response ['fields']['customfield_11011']['accountId']
            parent_ticket_obj.project_name = response ['fields']['customfield_10988']['name']
            parent_ticket_obj.project_name_code = response ['fields']['customfield_10988']['key']
            parent_ticket_obj.resource_email = response ['fields']['customfield_10971']
            parent_ticket_obj.alloc_start = response ['fields']['customfield_11015']
            parent_ticket_obj.alloc_end = response ['fields']['customfield_11016']
            parent_ticket_obj.confirmed_end = response ['fields']['customfield_11012']
            parent_ticket_obj.hou_per_day = response ['fields']['customfield_11024']
            parent_ticket_obj.alloc_percent = response ['fields']['customfield_11014']
            parent_ticket_obj.bill_type = response ['fields']['customfield_11021']['value']
            parent_ticket_obj.country_code = response ['fields']['customfield_10976']['value']
            parent_ticket_obj.proj_status_type = response ['fields']['customfield_11006']['value']
            #parent_ticket_obj.resolution = response ['fields']['resolution']['name']
            parent_ticket_obj.resource_prev_name = response ['fields']['customfield_10969']
            parent_ticket_obj.resource_first_last_name = response ['fields']['customfield_10970']
            parent_ticket_obj.resource_practice = response ['fields']['customfield_10975']['value']
            parent_ticket_obj.project_dyn_code = response ['fields']['customfield_10987']
            #parent_ticket_obj.reporter = response ['fields']['reporter']['emailAddress']
            parent_ticket_obj.reporter = response ['fields']['reporter']['accountId']
            #---- To add 'Change' Ticket details
            parent_ticket_obj.orig_tkt_id_for_change = response ['fields']['customfield_11008']
            # -- 18/05/23 CR - added field JRT_Extra Resource
            if response ['fields']['customfield_11144'] is not None:
                parent_ticket_obj.is_extra_resource = response ['fields']['customfield_11144']['id']
            else:
                parent_ticket_obj.is_extra_resource = ""
            # -- 23/06/23 Fix - get details of JRT_Over Allocation
            parent_ticket_obj.is_over_allocation = response ['fields']['customfield_11018']['value']

        else:
            returned_project_code = "user not available"
    else:
        returned_project_code = "_RestCallERROR_" + str(r.status_code)

    return parent_ticket_obj

################################################################

def rest_Post_Issue_Create(obj,task_num,task_date):

    parent_tkt_obj = obj
    ticket_summary = "Daily Task " + str(task_num) + " of " + parent_tkt_obj.resource_email + " | " + parent_tkt_obj.project_name

    json_data = {
        "fields": {
            "project": {"key": "JRT"},
            "parent":
            {
                "key": parent_tkt_obj.key
            },
            "summary": ticket_summary,
            "issuetype": {"name": "Daily Allocation"},
            "resolution": {"name": "Done"},
            "reporter": {"accountId": "62d8f9d710c44eb6e321c13f"},
            "customfield_11030": task_date,
            "customfield_11011": {"accountId": parent_tkt_obj.resource_name},
            "customfield_10988": {"key": parent_tkt_obj.project_name_code},
            "customfield_10971": parent_tkt_obj.resource_email,
            "customfield_11015": parent_tkt_obj.alloc_start,
            "customfield_11016": parent_tkt_obj.alloc_end,
            "customfield_11012": parent_tkt_obj.confirmed_end,
            "customfield_11024": parent_tkt_obj.hou_per_day,
            "customfield_11014": parent_tkt_obj.alloc_percent,
            "customfield_11021": {"value": parent_tkt_obj.bill_type},
            "customfield_11008": parent_tkt_obj.key,
            "customfield_10976": {"value": parent_tkt_obj.country_code},
            "customfield_11006": {"value": parent_tkt_obj.proj_status_type},
            "customfield_10969": parent_tkt_obj.resource_prev_name,
            "customfield_10970": parent_tkt_obj.resource_first_last_name,
            "customfield_10975": {"value": parent_tkt_obj.resource_practice},
            "customfield_10987": parent_tkt_obj.project_dyn_code,
            "customfield_11144": {"id": parent_tkt_obj.is_extra_resource},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": "",
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
        returned_ticket_no = "Issue Creating Jira sub task_<<RestCallERROR>>_" + str(r.status_code) + "---" + str(r.json())

    return returned_ticket_no

###############################################################

##########   ---------For Change Allocations ------- #####################################

def rest_get__jql_result_Loop(input_jql,input_custom_fields, pagination_startAt):

    endpoint = "https://aifel.atlassian.net/rest/api/3/search?"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA==" # Nuwanee's Tkn changed to Gobi's

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': input_jql,'fields': input_custom_fields, 'maxResults' : 100, 'startAt': pagination_startAt}

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)

    if r.status_code == 200:
        response = r.json()
                                       
    else:
        response  = "_RestCallERROR_ --> " + str(r.status_code)

    return r.status_code, response

def rest_get_full_jql_result(inp_jql,inp_custom_fields):

    # Logger configurations -------------
    file_name = "Function_Execution_Log_" + str (datetime.date.strftime(datetime.datetime.now(), "%Y-%m-%d__%H-%M-%S"))
    logger_file_path = "D:\\Script_Outputs\\" + str(file_name) + ".txt"
    logging.basicConfig(filename=logger_file_path,
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filemode='a', level=logging.INFO)
    logger = logging.getLogger()
    # Logger configurations ------------

    ## --- Declare Empty JSON
    json_full_result = []
    
    rest_status_code, rest_payload  = rest_get__jql_result_Loop(inp_jql,inp_custom_fields, 0)

    if rest_status_code == 200:
        record_count = rest_payload['total']
        if record_count > 0:
                loop_count = math.ceil( record_count / 100 ) + 1    ## To execute the for loop accordingly ie ( For 1 to 1) stops at 1 itself
                record_no = 0
                logger.info( "rest_get_full_jql_result_________" + str(inp_jql) + " - loop count is " + str(loop_count) + " for total records - " + str(record_count))
                for i in range(1, loop_count):
                    logger.info("rest_get_full_jql_result_________" + ": -> -> ->  processing loop " + str(i) + " of " + str(record_count) + " records" + " ---> starting with " + str(record_no))
                    rest_status_code, rest_payload  = rest_get__jql_result_Loop(inp_jql,inp_custom_fields, record_no)
                    
                    for issue in rest_payload['issues']:
                        key = issue['key']
                        json_full_result.append(key)
                                                
                    #Increase record count by 100 for next page in loop
                    record_no = record_no + 100
               

                # Finally - print full json_result    
                logger.info("rest_get_full_jql_result_________" + str(json_full_result))
            
            
        else:
             logger.info("No Records Found")
                  
    else:
        logger.info("rest_get_full_jql_result_________" + "_RestCallERROR_ --> " + str(rest_status_code))

    return json_full_result

def rest_Post_Issue_Transisiton(ticket_key,trans_id):

    json_data = {
        "transition": {
            "id": trans_id
        }
    }

    endpoint = "https://aifel.atlassian.net/rest/api/3/issue/" + str(ticket_key) + "/transitions"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA=="  #Gobi's Token
    
    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    r = requests.post(url=endpoint, headers=header_values,json=json_data, timeout=10)

    if r.status_code == 204:
        returned_response = "Transitioned"
    else:
        returned_response = "Erron when transitioning the Issue_" + str(ticket_key) + "_<<RestCallERROR>>_" + str(r.status_code) + "---" + str(r.json())

    return returned_response

def rest_Post_Issue_AddComment(ticket_key,comment):

    json_data = {
        "body": {
            "content": [
                {
                    "content": [
                        {
                            "text": comment,
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        }
    }

    endpoint = "https://aifel.atlassian.net/rest/api/3/issue/" + str(ticket_key) + "/comment"
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA=="  #Gobi's Token
    
    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    r = requests.post(url=endpoint, headers=header_values,json=json_data, timeout=10)

    if r.status_code == 201:
        returned_response = "CommentAdded"
    else:
        returned_response = "Erron when adding comment_" + str(ticket_key) + "_<<RestCallERROR>>_" + str(r.status_code) + "---" + str(r.json())

    return returned_response

def rest_PUT_Issue_Edit_for_transChange(ticket_key,value):

    json_data = {
        "fields": {
            "customfield_11046": {
                "value": value
            }
        }
    }

    endpoint = "https://aifel.atlassian.net/rest/api/3/issue/" + str(ticket_key)
    token = "Basic bmFkZXNhcGlsbGFpLmdvYmlhbmFudGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOmpJWXQ0cnhPeFdtMU81VWdQZ2lkODM2MA=="  #Gobi's Token
    
    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    r = requests.put(url=endpoint, headers=header_values,json=json_data, timeout=10)

    if r.status_code == 204:
        returned_response = "Updated"
    else:
        returned_response = "Erron when updating the Issue_" + str(ticket_key) + "_<<RestCallERROR>>_" + str(r.status_code) + "---" + str(r.json())

    return returned_response

##########   -----For Change Allocations ----------- #####################################

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   call_parent = rest_get_Parent_Details('JRT-1567')
   print(call_parent.resource_name)
   print(call_parent.project_name)
   print(call_parent.project_name_code)
   print(call_parent.resource_email)
   print(call_parent.alloc_start)
   print(call_parent.alloc_end)
   print(call_parent.confirmed_end)
   print(call_parent.hou_per_day)
   print(call_parent.alloc_percent)
   print(call_parent.bill_type)
   print(call_parent.country_code)
   print(call_parent.proj_status_type)
   #print(call_parent.resolution)
   print(call_parent.resource_prev_name)
   print(call_parent.resource_first_last_name)
   print(call_parent.resource_practice)
   print(call_parent.project_dyn_code)
   print(call_parent.reporter)
   print(call_parent.key)

   print("-----------------")
   #call_create_sub_task = rest_Post_Issue_Create(call_parent, 98, '2023-01-14')
   #print(call_create_sub_task)
