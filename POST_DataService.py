from requests import Session
from requests.auth import HTTPBasicAuth
from requests import get, post, put, delete
import json

token= " " #state the correct token
headers = {'Authorization': token, 'Content-Type': 'application/json'}
language_tag = "en" #state the correct language used for documentation (fr, de, it, en, rm)
id_publisher = " " #state the correct publisher id 


# Paths to the files
swagger_file_path = 'openapi.json'
output_file_path = 'metadata.json'


url = "https://dcat-a.app.cfap02.atlantica.admin.ch/api/Dataservice" #endpoint URL
# Load the swagger.json file
with open(swagger_file_path, 'r', encoding='utf-8') as file:
    swagger_data = json.load(file)


def replace_uri_with_href(data):
    if isinstance(data, dict):
        return {('href' if k == 'uri' else k): replace_uri_with_href(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_uri_with_href(item) for item in data]
    else:
        return data
      
#######################################
# Metadata mapping from swagger.json to i14y
#######################################

# Initialize metadata dictionary
metadata = {}

metadata = swagger_data.get("info", {}).get("x-metadata", {})

# Title and version from `info`
metadata['title'] = {language_tag: swagger_data.get("info", {}).get("title", "")}
metadata['version'] = swagger_data.get("info", {}).get("version", "")
metadata['publisher'] = {"id": id_publisher}
metadata['description'] = { language_tag: swagger_data.get("info", {}).get("x-metadata", {}).get("description", "")}
metadata['versionNotes'] = { language_tag: swagger_data.get("info", {}).get("x-metadata", {}).get("versionNotes", "")}

# ContactPoint
contact_data = swagger_data.get("info", {}).get("contact", [])
metadata["contactPoint"] = [
    {
        "fn": {"de": contact.get("name", "")},
        "emailInternet": contact.get("email", ""),
        "adrWork": {"it": contact.get("x-address", "")},
        "telWorkVoice": contact.get("x-telephone", ""),
        "note": {"it": contact.get("x-note", "")},
        "child": "Organization",
        "org": {}
    } for contact in (contact_data if isinstance(contact_data, list) else [contact_data])
]

# Documentation
documentation_data = swagger_data.get("externalDocs", [])
metadata['documentation'] = [
    {
        "href": doc.get("url", ""),
        "label": {"it": doc.get("x-name", "")}
    } for doc in (documentation_data if isinstance(documentation_data, list) else [documentation_data])
]

# ConformsTo
conforms_to_data = swagger_data.get("info", {}).get("x-metadata", {}).get("conformsTo", [])
metadata['conformsTo'] = [
    {
        "label": {language_tag: item.get("label", "")},
        "href": item.get("uri", "")
    } for item in (conforms_to_data if isinstance(conforms_to_data, list) else [conforms_to_data])
]

# LandingPage
landing_page_data = swagger_data.get("info", {}).get("x-metadata", {}).get("landingPage", [])
metadata['landingPage'] = [
    {
        "label": {language_tag: page.get("label", "")},
        "href": page.get("uri", "")
    } for page in (landing_page_data if isinstance(landing_page_data, list) else [landing_page_data])
]

# EndpointDescription
endpoint_description_data = swagger_data.get("info", {}).get("x-metadata", {}).get("endpointDescription", [])
metadata['endpointDescription'] = [
    {
        "label": {language_tag: endpoint.get("label", "")},
        "href": endpoint.get("uri", "")
    } for endpoint in (endpoint_description_data if isinstance(endpoint_description_data, list) else [endpoint_description_data])
]

# EndpointUrl
endpoint_url_data = swagger_data.get("info", {}).get("x-metadata", {}).get("endpointUrl", [])
metadata['endpointUrl'] = [
    {
        "label": {language_tag: endpoint.get("label", "")},
        "href": endpoint.get("uri", "")
    } for endpoint in (endpoint_url_data if isinstance(endpoint_url_data, list) else [endpoint_url_data])
]

# Keywords
keywords_data = swagger_data.get("info", {}).get("x-metadata", {}).get("keyword", [])
metadata['keyword'] = [
    {

            language_tag : keyword,

     
    } for keyword in (keywords_data if isinstance(keywords_data, list) else [keywords_data])
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

# Save the result to metadata.json
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(metadata, output_file, indent=4, ensure_ascii=False)

print(f"Metadata extracted and saved to {output_file_path}.")

#######################################
# POST API metdata on i14y
#######################################

file_path = 'metadata.json' #state the right file name here
with open(file_path, 'r') as file:
    json_data = file.read()

response = post(url, headers=headers, data = json_data, verify = False)
if response.status_code == 201:
    print(f'DataService posted correctly. Status-Code: {response.status_code}')
    print(f'Concept Id: {response.content}')
else:
    print(f"Error: {response.status_code} - {response.text}")
