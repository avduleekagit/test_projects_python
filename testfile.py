import requests
import os
from openpyxl import Workbook
import datetime
import pandas as pd
import logging
from datetime import datetime, timedelta

# Get the current time & one hour earlier
current_time = datetime.now()
one_hour_earlier = current_time - timedelta(hours=1)
two_days_earlier = current_time - timedelta(hours=48)
current_time_formatted = current_time.strftime('%Y-%m-%d %H:%M')
one_hour_earlier_formatted = one_hour_earlier.strftime('%Y-%m-%d %H:%M')
two_days_earlier_formatted = two_days_earlier.strftime('%Y-%m-%d %H:%M')

max_record_count=100
start_at=0
projectcode = ""
allocation_project_code = ""

# Get updated allocations
def get_updated_allocations(max_results,last_run):

    jql= "project = JRT AND issuetype = 'Resource Allocation' AND updated >= '"+ str(last_run).rstrip(':00') + "' AND 'JRT_Project Type[Dropdown]' in ('Resource Aug','Ring Fenced') order by created DESC"
    print(jql)
    endpoint=f"https://aifel.atlassian.net/rest/api/3/search?startAt={start_at}"
    token="Basic amlyYUFkbWluc0BheGlhdGFkaWdpdGFsbGFicy5jb206QVRBVFQzeEZmR0YwRUdiekNIQW1iSHZfUXc2VzNiNXdidjdISjlxeEhHSWlmbUFVdFNYZWlYcl9CZ3pMSXNOX3hScUc4dUtjdy00ajk0UG1YNFVhbTNtZTBZdnVPa1FOSGFyMnFCQ1NUQUFLV3FVNTJKQ2hDOUlud2stQ2dXMTlzNUZxM0g5Ujd2NUQtc1U1YnRfd3NoR29JODduN2pJeEhxTkVYbGpaOGFTcE0tQ3NHUHpYbjJBPTY5QjM4MEY0" # Jira Admin's token

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': jql,'fields': 'key,customfield_10987,customfield_10989', 'maxResults' : max_results }

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)
        
    if r.status_code == 200:
        response_updated_resources = r.json() 
        
    else:
        response_updated_resources  = {"issues": []}
    
    return r.status_code, response_updated_resources
    
        
# Get respective project cards
def get_project_cards(max_results, alloc_project_code):

    jql=f"project = JRT AND issuetype = 'RM Project Creation' AND status in ('Active - Presale', 'Active - Warranty', Active-Materialized) AND 'JRT_Project Type[Dropdown]' in ('Resource Aug','Ring Fenced') AND 'JRT_Project Code[Short text]' ~ '{alloc_project_code}' ORDER BY updated ASC"
    endpoint="https://aifel.atlassian.net/rest/api/3/search?"
    token="Basic ZHVsZWVrYS5yb3NoaW5pZUBheGlhdGFkaWdpdGFsbGFicy5jb206SVJPSW1kV3lHeE5QRHFBdVJmQlZCMkQ3" #Roshinie's token

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': jql,'fields': 'key,customfield_10987', 'maxResults' : max_results}

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)
            
    if r.status_code == 200:
        response = r.json()
                                            
    else:
        response  = "Error fetching project cards --> " + str(r.status_code)

    return r.status_code, response

# Get allocations incorporated with selected project card
def get_allocations(max_results,project_code):

    jql=f"project= JRT AND issuetype = 'Resource Allocation' AND status = 'Demand Approved' AND 'JRT_Project Code[Short text]' ~ {project_code} AND 'JRT_Allocation Start Date[Date]' <= now() AND 'JRT_Confirmed End Date / Released Date[Date]' >= now() AND ('JRT_Extra Resource[Dropdown]' is EMPTY OR 'JRT_Extra Resource[Dropdown]' = No) order by created desc"
    endpoint="https://aifel.atlassian.net/rest/api/3/search?"
    token="Basic ZHVsZWVrYS5yb3NoaW5pZUBheGlhdGFkaWdpdGFsbGFicy5jb206SVJPSW1kV3lHeE5QRHFBdVJmQlZCMkQ3" #Roshinie's token

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': jql,'fields': 'key,customfield_10971,customfield_11014', 'maxResults' : max_results }

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)
    
    if r.status_code == 200:
        response_resources = r.json()
                                       
    else:
        response_resources  = "Error fetching allocations --> " + str(r.status_code)
    
    return r.status_code, response_resources

def rest_PUT_Issue_Edit(ticket_key,head_count):

    json_data = {
    "fields": {
        "customfield_10999": head_count
            }
    }

    endpoint = "https://aifel.atlassian.net/rest/api/3/issue/" + str(ticket_key)
    token = "Basic amlyYUFkbWluc0BheGlhdGFkaWdpdGFsbGFicy5jb206QVRBVFQzeEZmR0YwRUdiekNIQW1iSHZfUXc2VzNiNXdidjdISjlxeEhHSWlmbUFVdFNYZWlYcl9CZ3pMSXNOX3hScUc4dUtjdy00ajk0UG1YNFVhbTNtZTBZdnVPa1FOSGFyMnFCQ1NUQUFLV3FVNTJKQ2hDOUlud2stQ2dXMTlzNUZxM0g5Ujd2NUQtc1U1YnRfd3NoR29JODduN2pJeEhxTkVYbGpaOGFTcE0tQ3NHUHpYbjJBPTY5QjM4MEY0"  #Jira Admin's Token
    
    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    r = requests.put(url=endpoint, headers=header_values,json=json_data, timeout=10)

    if r.status_code == 204:
        returned_response = "Updated"
    else:
        returned_response = "Error when updating the Issue_" + str(ticket_key) + "_<<RestCallERROR>>_" + str(r.status_code) + "---" + str(r.json())

    return returned_response

if __name__ == "__main__":
    
    # Get the previous run time
    try:
        with open('last_run_time_log.log', 'r') as log_file:
            lines = log_file.readlines()
            if lines:
                last_run_time_str = lines[-1].split(' - ')[0]
                last_run_time = datetime.strptime(last_run_time_str, '%Y-%m-%d %H:%M')
            else:
                last_run_time = two_days_earlier_formatted

    except Exception as e:
        print(f"---------->>> Error fetching last run time ---------->>> {e} <<<----------")
        last_run_time = two_days_earlier_formatted

    # Create an Excel and add headings
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["Project Card ID", "Project Code", "Head Count", "Project Card Update Status"])
    
    dfs = []

    while True:

        r_code,resulted_updated_allocations = get_updated_allocations(max_record_count,last_run_time)

        if r_code == 200:

            if resulted_updated_allocations['total'] > 0:

                for updated_allocation in resulted_updated_allocations['issues']:
                    updated_allocation_id = updated_allocation['key']
                    allocation_project_code = updated_allocation['fields']['customfield_10987']
                    project_type = updated_allocation['fields']['customfield_10989']['value']
                    print("Updated Allocation: ", updated_allocation_id, "--->>",allocation_project_code,"--->>",project_type)

                    data = {'Project Code': [allocation_project_code]}
                    current_df = pd.DataFrame(data)

                    dfs.append(current_df)

        start_at += max_record_count 

        allocation_list = resulted_updated_allocations.get("issues", [])
    
        if not allocation_list:
            break
    
    try:

        df = pd.concat(dfs, ignore_index=True)
        unique_df = df.drop_duplicates(subset=['Project Code'])
        print("Unique Project Cards: ",unique_df)

        for index, row in unique_df.iterrows():

            project_code = row['Project Code']

            response_code,resulted_project_cards = get_project_cards(max_record_count,project_code)

            if response_code == 200:
                
                if resulted_project_cards['total'] > 0:
                    
                    for project_card in resulted_project_cards['issues']:
                        ticket_id = project_card['key']
                        projectcode = project_card['fields']['customfield_10987']
                        print("Project Card: ",ticket_id,"--->>",projectcode)
                        
                        response_code_allocations, resulted_allocations = get_allocations(max_record_count, project_code)
                        
                        if response_code_allocations == 200:

                            allocations = []

                            for allocation in resulted_allocations['issues']:
                                resource_email = allocation['fields']['customfield_10971']
                                allocation_percentage = float(allocation['fields']['customfield_11014'])

                                allocations.append(allocation_percentage)

                            # Calculate the head count
                            total_allocation_percentage = sum(allocations)
                            print("Sum of Allocation Percentages: ", total_allocation_percentage)
                            head_count = total_allocation_percentage / 100
                            print("Head Count:", head_count)

                        else:
                            print(f"Error fetching allocations for project code: {project_code}")
                        
                        # Call rest_PUT_Issue_Edit function to update the project card
                        update_response = rest_PUT_Issue_Edit(ticket_id, head_count)
                        print(f"{update_response}")
                        
                        # Append data to the log file -- USE THIS WHEN UPDATE
                        worksheet.append([ticket_id, projectcode, head_count, update_response])

                        # Append data to the log file -- USE THIS ONLY FOR LOGGING
                        # worksheet.append([ticket_id, projectcode, head_count, "Not updated yet"])    

                else:
                    return_response = "No Project Cards found to process"

            else:
                return_response = resulted_project_cards
                print(return_response)
    
    except Exception as e:
        print('---------->>> No allocations were updated after ',last_run_time, ' [Error:' , str(e),']')

    # output file
    save_directory = "D:\\Script_Outputs\\Project Cards\\"
    file_name = "Planned HC Count Update - " + str(current_time.strftime("%Y%m%d_%H%M%S")) + ".xlsx"                   
    full_file_path = os.path.join(save_directory, file_name)
    workbook.save(full_file_path)

    # last run time logger
    logging.basicConfig(filename='last_run_time_log.log', level=logging.INFO, format='%(message)s - %(asctime)s - %(levelname)s', datefmt='%Y-%m-%d %H:%M')
    logging.info(f'{one_hour_earlier_formatted} - one hour earlier')