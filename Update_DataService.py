from requests import Session
from requests.auth import HTTPBasicAuth
from requests import put
import json


url = "https://dcat-a.app.cfap02.atlantica.admin.ch/api/Dataservice" #ABNHAME
# url = "https://dcat.app.cfap02.atlantica.admin.ch/api/Dataservice" #PRODUCTION

#######################################
# Variables you need to define 
#######################################

token = ""
id_publisher = ""  # Specify the publisher ID
swagger_file_path = 'swagger.json' #specify the correct file path
id_object = "" #state the id of the object that you need to update

#if needed
url_swagger = "" #specify the Swagger webpage url if you need to change it or it has not been specfied before
url_api_root = "" #specify the API url root if you need to change it
language_tag = ""  # Specify the correct language (fr, de, it, en)

#######################################
# Logic to handle metadata
#######################################

headers = {'Authorization': token, 'Content-Type': 'application/json'}

with open(swagger_file_path, 'r', encoding='utf-8') as file:
    swagger_data = json.load(file)

metadata = {}
x_metadata = swagger_data.get("info", {}).get("x-metadata", {})
if x_metadata:
    metadata.update(x_metadata)

metadata['id'] = id_object
metadata['publisher'] = {"id": id_publisher}
metadata['version'] = swagger_data.get("info", {}).get("version", "")

# Handling based on availability in x-metadata: if in x-metadata take that, if not take 

if "title" in x_metadata:
    metadata['title'] = x_metadata["title"]
else:
    metadata['title'] = {language_tag: swagger_data.get("info", {}).get("title", "")}

if "description" in x_metadata:
    metadata['description'] = x_metadata["description"]
else:
    metadata['description'] = {language_tag: swagger_data.get("info", {}).get("description", "")}


if not x_metadata.get("accessRights"): 
    metadata["accessRights"] =  {
        "code": "NON_PUBLIC"
    }

if "endpointUrl" not in metadata:
    metadata["endpointUrl"] = [
      {
        "href": url_api_root,
        "label": {
          "de": "Endpunkt-URL-Root",
          "en": "Endpoint URL root",
          "fr": "Racine de l'URL de l'endpoint",
          "it": "Radice dell'URL dell'endpoint"
        }
      }
    ]

    
if "endpointDescription" not in metadata and url_swagger:
    metadata["endpointDescription"] =  {
        "href": url_swagger,
        "label": {
            "de": "Swagger Dokumentation",
            "en": "API Documentation",
            "fr": "Documentation API",
            "it": "Documentazione API"
        }
      },


contact_data = x_metadata.get("contactPoint") if "contactPoint" in x_metadata else swagger_data.get("info", {}).get("contact", [])
if contact_data:
    metadata["contactPoint"] = [
        {
            "fn": contact.get("fn", {}) if "contactPoint" in x_metadata else {language_tag: contact.get("name", "")},
            "emailInternet": contact.get("emailInternet", "") if "contactPoint" in x_metadata else contact.get("email", ""),
            "adrWork": contact.get("adrWork", {}) if "contactPoint" in x_metadata else {language_tag: contact.get("x-address", "")},
            "telWorkVoice": contact.get("telephoneNumber", "") if "contactPoint" in x_metadata else contact.get("x-telephone", ""),
            "note": contact.get("note", {}) if "contactPoint" in x_metadata else {language_tag: contact.get("x-note", "")},
            "child": "Organization",
            "org": {}
        } for contact in (contact_data if isinstance(contact_data, list) else [contact_data])
    ]


documentation_data = x_metadata.get("documentation") if "documentation" in x_metadata else swagger_data.get("externalDocs", [])
if documentation_data:
    metadata['documentation'] = [
        {
            "href": doc.get("url", ""),
            "label": {"it": doc.get("description", "")}
        } for doc in (documentation_data if isinstance(documentation_data, list) else [documentation_data])
    ]



theme_codes = swagger_data.get("info", {}).get("x-metadata", {}).get("theme", {}).get("code", [])
metadata['theme'] = [
    {
        "code": code
    } for code in (theme_codes if isinstance(theme_codes, list) else [theme_codes])
]

# Function to replace 'url' with 'href'
def replace_uri_with_href(data):
    if isinstance(data, dict):
        return {('href' if k == 'url' else k): replace_uri_with_href(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_uri_with_href(item) for item in data]
    else:
        return data

metadata = replace_uri_with_href(metadata)

# Save metadata to JSON file
output_file_path = 'metadata.json' #state the right file name and path here

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(metadata, output_file, indent=4, ensure_ascii=False)
print(f"Metadata extracted and saved to {output_file_path}.")
with open(output_file_path, 'r') as file:
    json_data = file.read()

#If you don't want to create a new file metadata.json: uncomment the following line
#json_data = json.dumps(metadata, ensure_ascii=False, indent=4)

#######################################
# Update API metdata on i14y
#######################################


response = put(url, headers=headers, data=json_data, verify=False)
if response.status_code == 204:
    print(f'DataService updated correctly. Status-Code: {response.status_code}')
else:
    print(f"Error: {response.status_code} - {response.text}")
