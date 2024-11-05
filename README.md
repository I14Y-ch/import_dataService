# POST a DataService using swagger.json on I14Y

This project contains a Python script `POST_DataService.py` that posts a DataService using the metadata extracted from a Swagger/OpenAPI JSON file and a python script `PUT_DataService.py` that updates the posted DataService. The scripts read the `swagger.json`, processe it to create the appropriate metadata format, and then send it to a I14Y API endpoint.

Currently, the endpoint to POST a DataService on I14Y is not publicly available. It is expected to be made accessible in the coming months for automated use. If you need access immediately, please reach out to the [I14Y team](mailto:i14y@bfs.admin.ch); they can provide you with the appropriate publisher ID required to run the script.

## Prerequisites

Before using this script, ensure that you have the following:

- The `requests` library. You can install it via pip if you haven't done so:

  ```bash
  pip install requests

## Usage
### 1. Set Up the Script:
- Update the following variables in the script:
    - `token`: Set your authorization token (To find the authorization token: log in to the internal area of the platform, click on the user symbol in the upper righ corner and then on “Copy access token”).
    - `id_publisher_i14y`: Set the correct publisher ID.
    - `swagger_file_path`: Update this to point to your swagger.json file.

### 2. Post the DataService:

If you run the script will automatically post the generated metadata to the specified API endpoint (PROD or ABN) and print the response status. 

## Update the DataService on I14Y
If you need to update the DataService you can run the script `PUT_DataService.py`. First you need to set up the script: 
    - `token`: Set your authorization token (To find the authorization token: log in to the internal area of the platform, click on the user symbol in the upper righ corner and then on “Copy access token”).
    - `id_publisher_i14y`: Set the correct publisher ID.
    - `swagger_file_path`: Update this to point to your swagger.json file.
    - `id_object`: state the id of the object that you need to update. *Note: the Id can be derived from the I14Y web interface in the URL of the page dedicated to the specific DataService: https://input.i14y-a.admin.ch/dataservices/{Id}*
    
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

## Example of swagger.json structure: 
``` 
{
  "openapi": "3.0.1",
  "info": {
    "title": "Esempio API",
    "description": "Technical description displayed in the swagger page.", 
    "version": "1.0.1",
    "contact": {
      "email": "example@email.com", 
      "name": "contact name"
    },
    "x-metadata": {
      "title": {
        "de": "string",
        "en": "API name",
        "fr": "string",
        "it": "string",
        "rm": "string"
    },
    "description": {
      "de": "string",
      "en": "Business description of the API for non-technical users",
      "fr": "string",
      "it": "string",
      "rm": "string"
    },
    "accessRights": {
        "code": "PUBLIC"
      },
    "endpointDescription": [
      {
        "url": "https://endpointDescription.ch/",
        "label": {
          "de": "string",
          "en": "string",
          "fr": "string",
          "it": "string",
          "rm": "string"
        }
      }
    ],
    "endpointUrl": [
      {
        "url": "https://endpointUrl.ch/",
        "label": {
          "de": "string",
          "en": "string",
          "fr": "string",
          "it": "string",
          "rm": "string"
        }
      }
    ],
    "contactPoint":  [ {
        "address": {
          "de": "string",
          "en": "string",
          "fr": "string",
          "it": "string",
          "rm": "string"
        },
        "email": "string",
        "organizationName": {
          "de": "string",
          "en": "string",
          "fr": "string",
          "it": "string",
          "rm": "string"
        },
        "note": {
          "de": "string",
          "en": "string",
          "fr": "string",
          "it": "string",
          "rm": "string"
        },
        "telephoneNumber": "string"
      }
    ],
      "conformsTo": [
        {
          "uri": "https://conformsto.ch/",
          "label": {
            "de": "string",
            "en": "string",
            "fr": "string",
            "it": "string",
            "rm": "string"
          }
        }
      ],
      
        "keyword": [
          {
            "de": "string",
            "en": "string",
            "fr": "string",
            "it": "string",
            "rm": "string"
          }
        ],
      "landingPage": [   {
        "url": "https://landingPage.ch/",
        "label": {
          "de": "string",
          "en": "Label for the landing page",
          "fr": "string",
          "it": "string",
          "rm": "string"
        }
      },    {
        "url": "https://landingPage1.ch/",
        "label": {
          "de": "string",
          "en": "Label for the landing page",
          "fr": "string",
          "it": "string",
          "rm": "string"
        }
      }],

      "license": {"code": "terms_by"},
      "theme": {"code": ["121", "119"]},
      "versionNotes":{
        "de": "string",
        "en": "These are some version notes",
        "fr": "string",
        "it": "string",
        "rm": "string"
      }, 

      "documentation": [
        {
          "url": "https://documentations.ch/",
          "label": {
            "de": "string",
            "en": "string",
            "fr": "string",
            "it": "string",
            "rm": "string"
          }
        }
      ]
    }
  },
  "paths": {
    "/api/catalogs/{catalogId}/dcat/exports/rdf": {
      "get": {
        "tags": [
          "Catalogs"
        ],
        "summary": "GET DCAT catalog in RDF format.",
        "description": "Retrieves DCAT catalog by catalog id in RDF format.",
        "parameters":
...
``` 

## Example of swagger.json in different languages:

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
    "endpointDescription": [
      {
        "url": "https://endpointDescription.ch/",
        "label": {
          "de": "Endpunkt-Label",
          "en": "Endpoint label",
          "fr": "Nom du endpoint",
          "it": "Nome dell'endpoint"
        }
      }
    ],
    "endpointUrl": [
      {
        "url": "https://endpointUrl.ch/",
        "label": {
          "de": "Endpunkt url Label",
          "en": "EndpointUrl label",
          "fr": "Nom du endpointUrl",
          "it": "Nome dell'endpointUrl"
        }
      }
    ],
    "contactPoint": [
      {
        "address": {
          "de": "Hauptstrasse 1, Beispielstadt, Deutschland",
          "en": "1 Main Street, Sample City, Germany",
          "fr": "1 Rue Principale, Ville Exemple, Allemagne",
          "it": "Via Principale 1, Città di Esempio, Germania"
        },
        "email": "kontakt@beispiel.com",
        "organizationName": {
          "de": "Beispiel",
          "en": "Example",
          "fr": "Exemple",
          "it": "Esempio"
        },
        "note": {
          "de": "Kontaktieren Sie uns für weitere Informationen.",
          "en": "Contact us for more information.",
          "fr": "Contactez-nous pour plus d'informations.",
          "it": "Contattaci per ulteriori informazioni."
        }
      }
    ],    
      "conformsTo": [
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
      
      "keyword": [
        {
          "de": "Stichwort",
          "en": "keyword",
          "fr": "mot-clé",
          "it": "parola chiave"
        }
      ],        
      "landingPage": [   {
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

      "theme": {"code": ["121", "119"]},

      "versionNotes": {
        "de": "Dies sind einige Versionshinweise",
        "en": "These are some version notes",
        "fr": "Voici quelques notes de version",
        "it": "Queste sono alcune note di versione"
      },      

      "documentation": [
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



