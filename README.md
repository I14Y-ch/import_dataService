# Import a dataService using swagger.json on I14Y

This project provides two Python scripts to manage DataService metadata on I14Y:
- `import_dataService.py`: Posts a new DataService using metadata from a Swagger/OpenAPI JSON file.
- `update_dataService.py`: Updates an existing DataService on I14Y.

These scripts process `swagger.json` files, structure the metadata for I14Y, and send it to the API endpoint.

## Features
The script can import two different type of swagger documentation: 

- **[Standard OpenAPI](https://swagger.io/specification/)-compliant Swagger file with minimal metadata**: After import, the Local Data Steward will need to validate the entry and add translations, optional metadata, and other fields beyond the OpenAPI standard to meet [I14Y’s complete documentation requirements](https://github.com/I14Y-ch/POST_DataService?tab=readme-ov-file#metadata-properties). You can find an example [here](https://github.com/I14Y-ch/POST_DataService?tab=readme-ov-file#example-of-a-standard-openapi-compliant-swagger-file-with-minimal-metadata).
- **Fully detailed Swagger file that follows I14Y’s documentation guidelines**: It includes multilingual metadata and all required details, enabling the entry to be used immediately with minimal or no additional setup by the Local Data Steward. This approach ensures full compliance with I14Y’s API documentation standards, promoting consistency and quality across API documentations. You can find an example [here](https://github.com/I14Y-ch/POST_DataService?tab=readme-ov-file#example-of-a-fully-detailed-swagger-file-that-follows-i14ys-documentation-guidelines).
  
Note: The I14Y POST DataService endpoint is currently restricted but expected to be publicly available soon. For early access, contact the [I14Y team](mailto:i14y@bfs.admin.ch) for a publisher ID.


## API Publication Guidelines for I14Y

Which APIs must be documented in I14Y?
- Publish only APIs accessible to external users or applications.
- Avoid internal-only APIs (e.g., frontend-specific APIs).
  
Languages for publication:
- Initially, APIs can be documented in one language.
- Over time, Local Data Stewards should complete entries in French, German, and Italian (English is optional).

## Prerequisites

- Python 3.8+
- pip package manager

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd import_rdf_datasets
```

2. (Optional but recommended) Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
   - Edit `src/config.py` with your I14Y API token, organization ID and right file format ("xml" or "ttl")

## Usage
### 1. Script Setup:

Update the following variables in the script:
- `token`: Authorization token (To find the authorization token: log in to the internal area of the platform, click on the user symbol in the upper righ corner and then on “Copy access token”).
- `id_publisher_i14y`: Your assigned publisher ID.
- `swagger_file_path`: Path to your `swagger.json` file.
  
If needed:
- `language_tag`: Language of OpenAPI-specified informations (e.g., de, fr, it, en). You may leave this out if following I14Y’s documentation guidelines, as multilingual metadata should already be included.
- `url_api_root`: If the endpointUrl is not declared in x-metadata, you MUST specify the API url root.
- `url_swagger`: If the endpointDescription is not declared in x-metadata, you CAN specify the swagger webpage url (recommended).
      
Default Access Rights: If not specified, access rights default to non-public. Validation by a Local Data Steward is required to finalize the access level and entry status. 

### 2. Posting a DataService:

Run `POST_DataService.py` to submit the metadata to the I14Y API endpoint (PROD or ABN). The script returns the response status. After import, missing details or translations can be added as needed.

## Updating a DataService

To update an existing DataService, use `UPDATE_DataService.py`. Configure: 
- `token`: Set your authorization token (To find the authorization token: log in to the internal area of the platform, click on the user symbol in the upper righ corner and then on “Copy access token”).
- `id_publisher_i14y`: Set the correct publisher ID.
- `swagger_file_path`: Path to your `swagger.json` file.
- `id_object`: ID of the DataService to update. *Note: the Id can be derived from the I14Y web interface in the URL of the page dedicated to the specific DataService: https://input.i14y-a.admin.ch/dataservices/{Id}*
  
If needed:
- `language_tag`: Language of OpenAPI-specified informations (e.g., de, fr, it, en). You may leave this out if following I14Y’s documentation guidelines, as multilingual metadata should already be included.
- `url_api_root`: If you need to change the endpointUrl. 
- `url_swagger`: If the endpointDescription is not yet declared, you CAN specify the swagger webpage url (recommended).

## Metadata Properties
The metadata includes several properties, some of which are mandatory for successful posting. Below is a table detailing each property, whether it is mandatory, and what can be stated inside the property. More information regarding the properties and the standards used can be found [here](https://i14y-ch.github.io/handbook/de/6_anhang/eingabefelder/).

| Property | Description | Value range | Requirement level | 
| ----| ---- | ---- | ---- | 
| __title__ | The entry title is short but makes the electronic interface easy to find. It should be written in the relevant language. The title can include letters, special characters, numbers, or a date. | string | mandatory |
| __description__ | A free-text description of the API in the relevant language, ideally containing all terms likely to be searched. Paragraphs are allowed, but text formatting is not. It's recommended to provide descriptions in multiple languages. | string | mandatory | 
| __accessRights__ | Specify if the data accessed via the API is free and public ("Public"), can be used under specific conditions ("Restricted"), or is exclusively available to your organization ("Non-public"). Options are from an [EU Vocabulary](http://publications.europa.eu/resource/authority/access-right). | string (to be chosen from:  [PUBLIC, NON_PUBLIC, CONFIDENTIAL, RESTRICTED](http://publications.europa.eu/resource/authority/access-right)) | mandatory | 
| __endpointUrl__ | The root location or primary endpoint of the service (a Web-resolvable IRI). If the label is specified, the platform will display the linked label; otherwise, the full internet address is shown. For APIs with multiple endpoints, consider linking to the documentation page (e.g., Swagger). Multiple endpoints can be documented on the platform. | url: resource [mandatory] / label: string [optional] | mandatory | 
| __publisher__ | The organisation that commissioned or maintains the data collection is listed as the publisher. You need to set the correct publisher id in the script before running it.  | id: string [mandatory] | mandatory |
| __endpointDescription__ | Links to the descriptions or documentation for individual endpoints, in the same order as in the "endpointUrl" section. | url: resource [mandatory] / label: string [optional] | recommended |
| __license__ | Choose the license under which the data accessed via the interface is available. If not defined, choose "unknown." This field must be filled out if metadata is published on Opendata.swiss. The license options are based on [Open Government Data licenses](https://dcat-ap.ch/vocabulary/licenses/20210623.html). | string to be chosen from: [terms_open, terms_by, terms_ask, terms_by_ask](https://dcat-ap.ch/vocabulary/licenses/20210623.html) | recommended/mandatory | 
| __Contact: name__ | Enter the name of the organization (e.g., the office, section, or municipality). Both the name and address of the contact point can be multilingual. Multiple contact points can be entered. | string | recommended | 
| __Contact: email__ | Enter the organization’s email address, which should be permanently monitored. | string | recommended |
| __Contact: x-adress__ | Enter the organization's address, ideally as street name followed by house number, with further details like PO Box (if applicable) on the next line, and finally postal code and location. | string | recommended | 
| __Contact: x-note__ | Additional or clarifying information about the contact point can be entered here. | string | recommended | 
| __Contact: x-telephone__ | Enter a contact phone number for questions regarding the data offer, in the format +41 XXX XX XX. | string | recommended | 
| __Keyword__ | Keywords can be entered here to make the entry more easily searchable. This field is particularly for terms found in the [Termdat database](https://termdat.admin.ch) des Bundes verzeichnet sind.  | string | recommended | 
| __theme__ | Specify the thematic areas from which data is provided. These entries serve as the basis for filters on the I14Y interoperability platform. The list is a [concept available on the I14Y platform](https://www.i14y.admin.ch/de/concepts/08da58dc-4dc8-f9cb-b6f2-7d16b3fa0cde/description) and it's based on ([eCH-0122](https://www.ech.ch/de/ech/ech-0122/1.0)). | code: string to be chosen from [i14y themes](https://www.i14y.admin.ch/en/concepts/08da58dc-4dc8-f9cb-b6f2-7d16b3fa0cde/content) [mandatory] / name: optional | optional | 
| __landingPage__ | Enter the link to a webpage on your organization's site where the API is described in detail. | url: resource [mandatory] / label: string [optional] | optional |
| __conformsTo__ | Enter legal bases for the data offer. Include a link to relevant documents on  [Fedlex](https://www.fedlex.admin.ch) or another online resource containing the relevant text. Add a link if the data offer complies with a standard. | url: resource [mandatory] / label: string [optional] | optional | 
| __externalDocs__ | Enter any additional documents directly related to the offer, such as a manual or background text. | url: resource [mandatory] / x-name : string [optional] | optional | 
| __version__ | Enter the version number of the data collection. | string | optional |
| __versionNotes__ | Enter additional information about the version here. | string | optional | 

## Example of a Standard OpenAPI-compliant Swagger file with minimal metadata: 

In this case some mandatory information are not specified in the swagger documentation, therfore you need to define the following variables in order to import the API in I14Y: 
- `language_tag`: en
- `url_api_root`: API url root, for example: "https://api.example.com"
- `url_swagger`: Swagger webpage url, for example: "https://api.example.com/v1/swagger"

The accessRights are by default set to NON_PUBLIC, Validation by a Local Data Steward is required to finalize the access level and entry status. 
``` 
{
  "openapi": "3.0.1",
  "info": {
      "title": "API name shown in the swagger page",
      "description": "Description displayed in the swagger page.", 
      "version": "1.0.0",
      "contact": {
        "email": "example@email.com", 
        "name": "contact name shown in the swagger page"
      }
  },
  "externalDocs": {
    "description": "Find more info here", 
    "url": "https://example.com"
  },
  "paths": {
...
``` 

## Example of a fully detailed Swagger file that follows I14Y’s documentation guidelines

The documentation enables a comprehensive view of the Swagger API while also allowing the direct import of metadata into I14Y. By using the custom `x-metadata{}` property, you can specify all mandatory fields in multiple languages, as well as any recommended or optional fields as needed.

This is a complete example. While it's not required to define every property, it is recommended to include as much detail as possible.


``` 
{
  "openapi": "3.0.1",
  "info": {
    "title": "API name shown in the swagger page",
    "description": "Technical description displayed in the swagger page.", 
    "version": "1.0.0",
    "contact": {
      "email": "example@email.com", 
      "name": "contact name shown in the swagger page"
    },
    "x-metadata": {
      "title": {
        "de": "API-Name1",
        "en": "API name",
        "fr": "Nom de l'API",
        "it": "Nome dell'API"
    },
    "description": {
      "de": "Beschreibung der API für nicht-technische Benutzer",
      "en": "Business description of the API for non-technical users",
      "fr": "Description métier de l'API pour les utilisateurs non techniques",
      "it": "Descrizione dell'API per utenti non tecnici"
    },
    "accessRights": {
        "code": "PUBLIC"
      },
    "endpointDescription": [                               -> you can add multiple endpointDescription
       {
        "url": "https://api.example.com/v1/swagger",
        "label": {
          "de": "Swagger webpage",
          "en": "Swagger webpage",
          "fr": "Swagger webpage",
          "it": "Swagger webpage"
        }
      }
      {
        "url": "https://endpointDescription.ch/",
        "label": {
            "de": "Swagger Dokumentation",
            "en": "API Documentation",
            "fr": "Documentation API",
            "it": "Documentazione API"
        }
      }
    ],
    "endpointUrl": [                             -> you can add multiple endpointUrl
      {
        "url": "https://endpointUrl.ch/",
        "label": {
          "de": "Endpunkt-URL-Root",
          "en": "Endpoint URL root",
          "fr": "Racine de l'URL de l'endpoint",
          "it": "Radice dell'URL dell'endpoint"
        }
      }
    ],
    "contactPoint": [                            -> you can add multiple contactPoint
      {
        "address": {
          "de": "Hauptstrasse 1, Beispielstadt, Deutschland",
          "en": "1 Main Street, Sample City, Germany",
          "fr": "1 Rue Principale, Ville Exemple, Allemagne",
          "it": "Via Principale 1, Città di Esempio, Germania"
        },
        "telWorkVoice": "0910000000 -> telephone number"
        "emailInternet": "kontakt@beispiel.com",
        "fn": {
          "de": "Name der Organisation",
          "en": "Organization name",
          "fr": "Nom de l'organization",
          "it": "Nome dell'organizzazione"
        },
        "note": {
          "de": "Kontaktieren Sie uns für weitere Informationen.",
          "en": "Contact us for more information.",
          "fr": "Contactez-nous pour plus d'informations.",
          "it": "Contattaci per ulteriori informazioni."
        }
      }
    ],    
      "conformsTo": [                              -> you can add multiple conformsTo
        {
          "url": "https://conformsto.ch/",
          "label": {
            "de": "label",
            "en": "label",
            "fr": "label",
            "it": "label"
          }
        }
      ],
      
      "keyword": [                                -> you can add multiple keywords
        {
          "de": "Stichwort",
          "en": "keyword",
          "fr": "mot-clé",
          "it": "parola chiave"
        }
      ],        
      "landingPage": [   {                         -> you can add multiple landingPage
        "url": "https://landingPage.ch/",
        "label": {
          "de": "label",
          "en": "label",
          "fr": "label",
          "it": "label"
        }
      },    {
        "url": "https://landingPage1.ch/",
        "label": {
          "de": "label",
          "en": "label",
          "fr": "label",
          "it": "label"
        }
      }],

      "license": {"code": "terms_by"},

      "theme": {"code": ["121", "119"]},                 -> you can add multiple themes

      "versionNotes": {
        "de": "Dies sind einige Versionshinweise",
        "en": "These are some version notes",
        "fr": "Voici quelques notes de version",
        "it": "Queste sono alcune note di versione"
      },      

      "documentation": [                                -> you can add multiple doumentations 
        {
          "url": "https://documentations.ch",
          "label": {
            "de": "label",
            "en": "label",
            "fr": "label",
            "it": "label"
          }
        }
      ]
    }
  },


## File Structure

```
import_rdf_datasets/
├── data/
│   └── swagger.json
├── src/
│   ├── config.py
│   ├── update_dataService.py
│   ├── import_dataService.py
├── requirements.txt
└── README.md
```

## Contributing

Please ensure any pull requests or contributions adhere to the following guidelines:
- Keep the code simple and well-documented
- Follow PEP 8 style guidelines
- Include appropriate error handling
- Test thoroughly before submitting

