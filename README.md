# Introduction 
Mindly.ai turns your study materials into clear mind maps. Using Azure AI, it extracts key concepts and shows how they connect. Upload your documents, and get instant, customizable mind maps to enhance your learning.

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Flask Project Installation Guide

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7+
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository

First, clone the project repository from GitHub:

```bash
git clone https://MSPL-AI2024s@dev.azure.com/MSPL-AI2024s/Project%20D/_git/Project%20D
```
### 2. Install Dependecies

Run the following command to install dependecies:

```bash
pip install -r requirements.txt
```
### 3. Copy `.env.example` to `.env`

You can copy it manually or run the following command to copy `.env.example` to `.env`:

```bash
copy .env.example .env 
```
### 4. Fill in .env variables
### 4. Run the project

Run project by running ./run.py or run the following command:
```bash
py run.py
```

# Code Architecture
  ```plaintext
  ├── app/
  │   ├── blueprints/   # each one represents related functionalities
  │   ├── static/       # project static files
  │   ├── templates/    # flask templtes
  │   ├── __init__.py      # initialize `flask` app, wrap falsk app and register blueprints
  │   ├── config.py        # initialize config variables
  │   ├── connectors.py    # contains functions that handles connecting to AI services process
  │   ├── dataBaseConnection.py    # contains connection to mongodb process
  │   ├── decorators.py    # contains usefull decorators
  │   ├── forms.py         # 
  │   ├── helpers.py       # define helper functions 
  │   ├── injectors.py     # define injecting function to global flask templates 
  │   ├── models.py        # 
  │   ├── validators.py    # contains validation function and decorators 
  ├── examples/  # directory that contains some testing pdf files
  ├── run.py     # run this file to start running project
  └── README.md  # Project documentation
```

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)