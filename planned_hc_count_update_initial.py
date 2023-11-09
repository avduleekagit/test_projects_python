import requests
import os
from openpyxl import Workbook
import datetime
import pandas as pd

max_record_count=100
start_at=0
projectcode = ""
allocation_id = ""
allocation_percentage = 0.0

# Retrieve active RA & RF project cards
def get_project_cards(max_results):

    jql="project = JRT AND issuetype = 'RM Project Creation' AND status in ('Active - Presale', 'Active - Warranty', Active-Materialized) AND 'JRT_Project Type[Dropdown]' in ('Resource Aug','Ring Fenced') ORDER BY updated ASC"
    endpoint="https://aifel.atlassian.net/rest/api/3/search?"
    token="Basic amlyYUFkbWluc0BheGlhdGFkaWdpdGFsbGFicy5jb206QVRBVFQzeEZmR0YwRUdiekNIQW1iSHZfUXc2VzNiNXdidjdISjlxeEhHSWlmbUFVdFNYZWlYcl9CZ3pMSXNOX3hScUc4dUtjdy00ajk0UG1YNFVhbTNtZTBZdnVPa1FOSGFyMnFCQ1NUQUFLV3FVNTJKQ2hDOUlud2stQ2dXMTlzNUZxM0g5Ujd2NUQtc1U1YnRfd3NoR29JODduN2pJeEhxTkVYbGpaOGFTcE0tQ3NHUHpYbjJBPTY5QjM4MEY0" # Jira Admin's token

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}
    input_params = {'jql': jql,'fields': 'key,customfield_10987', 'maxResults' : max_results, 'startAt': start_at}

    r = requests.get(url=endpoint, headers=header_values,params=input_params, timeout=10)
            
    if r.status_code == 200:
        response = r.json()
                                            
    else:
        response  = "Error fetching project cards --> " + str(r.status_code)

    return r.status_code, response

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

    # Create an Excel workbook and add data to a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["Project Card ID", "Project Code", "Head Count","Project Card Update Status"])

    response_code,resulted_project_cards = get_project_cards(max_record_count)

    if response_code == 200:
        
        if resulted_project_cards['total'] > 0:
            
            for project_card in resulted_project_cards['issues']:
                ticket_id = project_card['key']
                projectcode = project_card['fields']['customfield_10987']
                print("Project Card: ",ticket_id," ===>> ",projectcode)

                response_code_allocations,resulted_allocations = get_allocations(max_record_count, projectcode)

                if response_code_allocations == 200:

                    allocations = []

                    for allocation in resulted_allocations['issues']:
                        allocation_id = allocation['key']
                        resource_email = allocation['fields']['customfield_10971']
                        allocation_percentage = float(allocation['fields']['customfield_11014'])
                        print(allocation_id,"----",allocation_percentage)
                        allocations.append(allocation_percentage)

                    # Calculate the sum of allocation_percentage values
                    total_allocation_percentage = sum(allocations)
                    print("Sum of Allocation Percentages: ", total_allocation_percentage)

                    # Divide the total_allocation_percentage by 100
                    head_count = total_allocation_percentage / 100

                    # Print the head count
                    print("Head Count:", head_count)        

                else:
                    print(f"Error fetching allocations for project code: {projectcode}")

                # Update project card
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

    # Specify the file path
    save_directory = "D:\\Script_Outputs\\Project Cards\\"

    # Save the workbook as an Excel file
    file_name = "Initial Planned Head Count Update - " + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx"
            
    # Create the full file path by joining the directory and file name
    full_file_path = os.path.join(save_directory, file_name)

    workbook.save(full_file_path)