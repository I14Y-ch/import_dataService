# POST a DataService using swagger.json

This project contains a Python script that posts a DataService using the metadata extracted from a Swagger/OpenAPI JSON file. The script reads the `swagger.json`, processes it to create the appropriate metadata format, and then sends it to a I14Y API endpoint.

## Prerequisites

Before using this script, ensure that you have the following:

- The `requests` library. You can install it via pip if you haven't done so:

  ```bash
  pip install requests

## Usage
### 1. Set Up the Script:
- Update the following variables in the script:
    - `token`: Set your authorization token (To find the authorization token: log in to the internal area of the platform, click on the user symbol in the upper righ corner and then on “Copy access token”).
    - `language_tag`: Specify the language that you have use in your swagger.json for the documentation, one of the following: fr, de, it, en, rm.
    - `id_publisher_i14y`: Set the correct publisher ID.
    - `swagger_file_path`: Update this to point to your swagger.json file.

### 2. Post the DataService:

If you run the script will automatically post the generated metadata to the specified API endpoint and print the response status. 

## Metadata Properties
The metadata includes several properties, some of which are mandatory for successful posting. Below is a table detailing each property, whether it is mandatory, and what can be stated inside the property. More information regarding the properties and the standards used can be found [here](https://i14y-ch.github.io/handbook/de/6_anhang/eingabefelder/).

| Property | Description | Value range | Requirement level | 
| ----| ---- | ---- | ---- | 
| __title__ | The entry title is short but makes the electronic interface easy to find. It should be written in the relevant language. The title can include letters, special characters, numbers, or a date. | string | mandatory |
| __description__ | A free-text description of the API in the relevant language, ideally containing all terms likely to be searched. Paragraphs are allowed, but text formatting is not. It's recommended to provide descriptions in multiple languages. | string | mandatory | 
| __accessRights__ | Specify if the data accessed via the API is free and public ("Public"), can be used under specific conditions ("Restricted"), or is exclusively available to your organization ("Non-public"). Options are from an [EU Vocabulary](http://publications.europa.eu/resource/authority/access-right). | string (to be chosen from:  [PUBLIC, NON_PUBLIC, CONFIDENTIAL, RESTRICTED](http://publications.europa.eu/resource/authority/access-right)) | mandatory | 
| __endpointUrl__ | The internet address and title of the API’s primary endpoint. If the title is specified, the platform will display the linked title; otherwise, the full internet address is shown. For APIs with multiple endpoints, consider linking to the documentation page (e.g., Swagger). Multiple endpoints can be documented on the platform. | url: resource [mandatory] / label: string [optional] | mandatory | 
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

## Example of swagger.json: 
``` 
{
  "openapi": "3.0.1",
  "info": {
    "title": "API name",
    "description": "Technical description displayed in the swagger page.", 
    "version": "1.0.0",
    "contact": {
      "email": "example@email.com", 
      "name": "contact name", 
      "x-address": "contact addess",
      "x-telephone": "0910000000",
      "x-note": "This is a note to add to the contact point information"
    },
    "x-metadata": {
      "accessRights": {
        "code": "PUBLIC"
      },
      "conformsTo": [
        {
          "uri": "https://conformsto.ch/",
          "label":  "Label for information about conformance"
        }, 
        {
          "uri": "https://conformsto.ch/",
          "label":  "Label for information about conformance"
        }],
      "description": "Business description of the API for non-technical users",
      "endpointDescription": [{
        "uri": "https://endpointdescription.ch/",
        "label":  "Label for the endpoint description"
      }, 
      {"uri": "https://endpointdescription.ch/",
      "label":  "Label for the endpoint description"}],
      "endpointUrl": [{
        "uri": "https://endpointurl.ch/",
        "label":  "Label for the endpoint url"
        },
        {"uri": "https://endpointurl.ch/",
        "label":  "Label for the endpoint url"
        }],
      "keyword": [
        "keyword1", "keyword2"
      ],
      "landingPage": [{
        "uri": "https://landingpage.ch/",
        "label":  "Label for the landing page"
      }, {"uri": "https://landingpage.ch/",
      "label":  "Label for the landing page"}],

      "license": {"code": "terms_by"},
      "theme": {"code": ["121", "119"]},
      "versionNotes": "These are some version notes"
    }
  },
  "externalDocs": {
    "x-name": "name", 
    "description": "Find more info regarding docs here",
    "url": "https://example.com"
  }, 
  "paths": {
    "/api/catalogs/{catalogId}/dcat/exports/rdf": {
      "get": {
        "tags": [
          "Catalogs"
        ],
        "summary": "GET DCAT catalog in RDF format.",
        "description": "Retrieves DCAT catalog by catalog id in RDF format.",
        "parameters": ...




