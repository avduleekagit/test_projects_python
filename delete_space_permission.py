import pip._vendor.requests 
import json
from openpyxl import Workbook

start_val = 0
confluence_user_group_ids = []   
while True:

    # url_get = "https://aifel.atlassian.net/wiki/rest/api/space/?expand=permissions&type=personal"
    url_get = f"https://aifel.atlassian.net/wiki/rest/api/space/?start={start_val}&limit=50&expand=permissions&type=personal"

    token = "Basic dGhhcnVrYS5oZXJhdGhAYXhpYXRhZGlnaXRhbGxhYnMuY29tOkFUQVRUM3hGZkdGMERjRXhWOVBrM2Rtejh0ZXdXem13Um9rNEhlUjlDdFAyQkJYa3ZTU2VBRUZyZFV3XzNNVzdHWW9CZ2Vob09FY2VjYmprcUhVUGdsSlR0VXl4dzVQTDRieGpncjFqT294eXFLV2RnN0t2Qm5TZFJkT0tINHc0bXc2VmJxQkc0N04yWjhlT3lHaWQ3VDdxVW5SUHFiRE9LVnp1LVoyUS1BTEJvVDJxWUpfdFhEcz1FQTQyMzMxQg=="

    header_values = {'Content-Type': "application/json",'Accept': "application/json",'Authorization':token}

    response = pip._vendor.requests.request(
    "GET",
    url_get,
    headers=header_values,
    )

    start_val += 50  
    # json -> python list
    data_list = json.loads(response.text)

    space_list = data_list["results"]
    
    if data_list["size"] == 0:
        break
    
    for index in space_list:
        grp_list = index["permissions"]
        for permission in grp_list:
            subjects = permission.get("subjects", {})
            group_results = subjects.get("group", {}).get("results", [])
        
        # Check if the permission is related to the "confluence-users" group
            for group_info in group_results:
                if group_info.get("name") == "confluence-users":
                    confluence_user_group_ids.append({"space_key":index["key"], "id_value":permission["id"]})
                                  

print("Confluence User Group IDs:", confluence_user_group_ids)

# Create an Excel workbook and add data to a worksheet
workbook = Workbook()
worksheet = workbook.active
worksheet.append(["Space Key", "ID Value"])

for item in confluence_user_group_ids:
    worksheet.append([item["space_key"], item["id_value"]])

# Save the workbook as an Excel file
excel_file_path = "confluence_user_group_ids2.xlsx"
workbook.save(excel_file_path)
 
def deletePermission(space_key_val, id_val):
    url_delete = "https://aifel.atlassian.net/wiki/rest/api/space/{space_key_val}/permission/{id_val}"
    
    response_delete = pip._vendor.requests.request(
    "DELETE",
    url_delete,
    headers=header_values,)
    
    print(json.loads(response_delete.text))
    
# for delete_index in confluence_user_group_ids:
    # deletePermission(delete_index["space_key"], delete_index["id_value"])