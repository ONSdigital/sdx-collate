# sdx-collate

The SDX-collate service is responsible for processing and packaging all business survey comments that have been
extracted and stored by sdx-survey.

## Getting Started

### Prerequisites

- Python 3.13
- UV (a command line tool for managing Python environments)
- make

### Installing Python 3.13

If you don't have Python 3.13 installed, you can install it via brew:

```bash
brew install python@3.13
```

### Install UV:
   - This project uses UV for dependency management. Ensure it is installed on your system.
   - If UV is not installed, you can install it using:
```bash

curl -LsSf https://astral.sh/uv/install.sh | sh

OR 

brew install uv
```
- Use the official UV installation guide for other installation methods: https://docs.astral.sh/uv/getting-started/installation/
- Verify the installation by using the following command:
```bash
uv --version
```

### Install dependencies

This command will install all the dependencies required for the project, including development dependencies:

```bash
uv sync
```

If you ever need to update the dependencies, you can run:

```bash
uv sync --upgrade
```

## Running the service

```bash
uv run run.py
```

## Linting

```bash
make lint
```

## Formatting

```bash
make format
```

## Tests

```bash
make test
```

## License

Copyright © 2024, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.

## GCP

#### Datastore
Collate reads comments out of GCP Datastore under the **'{survey_id}_{period}'** kind.

| Attribute       | Description                  | Example                                      |
|-----------------|------------------------------|----------------                              |
| key (name/id)   | Transaction ID (tx_id)       | `name=09bd7d53-6f16-4efa-a9c0-ea6c35976062`  |
| created         | Date and time comment stored | `yyyy-mm-dd, HH:MM:SS.ss`                    |
| encrypted_data  | Encrypted JSON               | `gAAAAABgOR2_QLs62GL7DFp0Fr_DwRatIQlWK...`   |

#### Secret Manager
`sdx-comment-key` is managed by Google Secret Manager. A single API call is made on program startup
and stored in `DECRYPT_COMMENT_KEY`. The default value is the test key.

## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.