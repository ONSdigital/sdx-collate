# sdx-collate

The SDX-collate service is responsible for processing and packaging all business survey comments that have been
extracted and stored by sdx-survey.

## Process

The collate microservice is triggered daily at 06:00 via kubernetes CronJob. Reading from Google Datastore, all comments 
stored **prior to the current date** will be decrypted, added to an in-memory Excel file (xml) and sent to sdx-deliver via
HTTP: `POST` request: `deliver/comments`

## Getting started
Install requirements:
```shell
$ make build
```

Testing:
ensure you have installed all requirements with above `make build` command then:
```shell
$ make test
```

Running:
ensure you have installed all requirements with above `make build` command then:
```shell
$ make start
```

## GCP

#### Datastore
Collate reads comments out of GCP Datastore under the **'Comments'** entity.

| Attribute       | Description                  | Example
|-----------------|------------------------------|----------------
| key (name/id)   | Transaction ID (tx_id)       | `name=09bd7d53-6f16-4efa-a9c0-ea6c35976062`
| created         | Date and time comment stored | `yyyy-mm-dd HH:MM:SS.ss`
| encrypted_data  | Encrypted JSON               |  
| period          | Period from survey JSON      | `period: 201904`
| survey_id       | Survey ID                    | `survey_id: 017`

#### Secret Manager
Decrypt comment key is managed by Google Secret Manager. A single API call is made on program startup
and stored in `DECRYPT_COMMENT_KEY`. The default value is the test key.

## Configuration
| Environment Variable    | Description
|-------------------------|------------------------------------
| PROJECT_ID              | Name of project
| DECRYPT_COMMENT_KEY     | Key used to decrypt comments
| DELIVER_SERVICE_URL     | URL of ``sdx-deliver`` service
| DATASTORE_CLIENT        | Datastore Client for Reading comments out of GCP

## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.