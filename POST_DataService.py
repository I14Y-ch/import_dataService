from requests import Session
from requests.auth import HTTPBasicAuth
from requests import get, post, put, delete
import json

token = ""
headers = {'Authorization': token, 'Content-Type': 'application/json'}
id_publisher_i14y = "b9b7ad7e-27b5-41da-a8b3-dce6197ce51e" #state the correct publisher id 


# Paths to the files
swagger_file_path = 'C:/Users/U80877014/Documents/openapi.json'


url = "https://dcat-a.app.cfap02.atlantica.admin.ch/api/Dataservice" #ABNHAME
# url = "https://dcat.app.cfap02.atlantica.admin.ch/api/Dataservice" #PRODUCTION

def replace_uri_with_href(data):
    if isinstance(data, dict):
        return {('href' if k == 'url' else k): replace_uri_with_href(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_uri_with_href(item) for item in data]
    else:
        return data

# Load the swagger.json file
with open(swagger_file_path, 'r', encoding='utf-8') as file:
    swagger_data = json.load(file)

# Initialize metadata dictionary
metadata = {}

metadata = swagger_data.get("info", {}).get("x-metadata", {})


metadata['publisher'] = {"id": id_publisher_i14y}
metadata['version'] = swagger_data.get("info", {}).get("version", "")


# ContactPoint
contact_data = swagger_data.get("info", {}).get("x-metadata", {}).get("contactPoint", [])
metadata["contactPoint"] = [
    {
        "fn": contact.get("organizationName", {}),
        "emailInternet": contact.get("email", ""),
        "adrWork": contact.get("address", {}),
        "telWorkVoice": contact.get("telephoneNumber", ""),
        "note": contact.get("note", {}),
        "child": "Organization",
        "org": {}
    } for contact in (contact_data if isinstance(contact_data, list) else [contact_data])
]

# Theme - assuming placeholder names for each code
theme_codes = swagger_data.get("info", {}).get("x-metadata", {}).get("theme", {}).get("code", [])
metadata['theme'] = [
    {
        "code": code,
   
    } for code in (theme_codes if isinstance(theme_codes, list) else [theme_codes])
]

# Apply uri-to-href replacement on the whole metadata structure
metadata = replace_uri_with_href(metadata)


output_file_path = 'metadata.json' #state the right file name and path here
with open(output_file_path, 'w', encoding='utf-8') as output_file:
   json.dump(metadata, output_file, indent=4, ensure_ascii=False)

print(f"Metadata extracted and saved to {output_file_path}.")
 
with open(output_file_path, 'r') as file:
        json_data = file.read()
    
#######################################
# POST API metdata on i14y
#######################################

# Convert metadata to JSON and send as request payload
#json_data = json.dumps(metadata, ensure_ascii=False, indent=4)

response = post(url, headers=headers, data=json_data, verify=False)
if response.status_code == 201:
    print(f'DataService posted correctly. Status-Code: {response.status_code}')
    response_json = response.json()
    print(f'DataService ID: {response_json["id"]}')
    print(f'Response content: {response.content}')
else:
    print(f"Error: {response.status_code} - {response.text}")
