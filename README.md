# MedAssist

MedAssist is a project designed to offer support to community health workers in early stage detection and management of sickle cell disease. It is a digital platform that promotes deeper thinking, practical learning, empathy, understanding, user agency, and a collaborative community culture.

## Table of Contents

- [Tech Used](#tech-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Tech Used

- Python
- Flask
- Docker
- BeautifulSoup
- Llama Index
- ChromaDB
- Langchain

## Prerequisites

- Python 3.11
- Docker
- Knowledge of Flask and Docker

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Build the Docker image using the Dockerfile provided

```bash
docker build -t medAssist .
```

4. Run the Docker container

```bash
docker run -p 5000:5000 medAssist
```

## Usage

The application exposes a POST endpoint at `/chat` which accepts a JSON payload with `user_input` and `chat_history` fields.

Example request:

```python
import requests
import json

reqUrl = "http://127.0.0.1:5000/chat"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json"
}

payload = json.dumps({
  "user_input":"What is the state of Sickle cell anaemia in Kenya?",
  "chat_history":[
    "Hello",
    "Hi there! How can I assist you today?",
    "Hello! My name is Mueni. I am a Community Health Worker AI assistant here to assist you with any health-related questions or concerns you may have. How can I assist you today?"

    ]
})

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)
```

## Dependencies

The project has several dependencies which are listed in the `requirements.txt` file. These can be installed using pip:

```bash
pip install -r requirements.txt
```

## Project Structure

The project has the following structure:

```
medAssist-chw/
┣ storage/
┃ ┣ bjh0146-0675.pdf
┃ ┣ CHV_handbook_PDF-F.pdf
┃ ┣ Decreased Hepcidin Levels Are Associated_GOLD VoR.pdf
┃ ┣ MedAssist - Demo.pptx
┃ ┣ MOH-514-LOG-BOOK_DEC-8.xls
┃ ┗ NATIONAL-GUIDELINES-FOR-CONTROL-AND-MANAGEMENT-OF-SICKLE-CELL-DISEASE-IN-KENYA-.pdf
┣ .env
┣ .gitignore
┣ .gitmodules
┣ api.py
┣ Dockerfile
┣ loader.py
┣ orchestrator.py
┣ README.md
┣ requirements.txt
┗ start.sh
```

## Contributing

Contributions are welcome. Please fork the repository and create a pull request with your changes.

## License

MIT License
