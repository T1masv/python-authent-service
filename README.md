# Python Authentication Service

## Description
This Python-based project provides a simple authentication service, making it easier to integrate secure authentication into various applications.

## Installation
To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```
### Usage
To start the service, execute:

```bash
python app/main.py
```
### Running Tests
Execute the following to run tests:

```bash
python -m unittest
```
### Docker Support
To build and run the Docker container:

```bash
docker build -t python-auth-service .
docker run -p 5000:5000 python-auth-service
```

License
This project is licensed under the MIT License - see the LICENSE file for details.