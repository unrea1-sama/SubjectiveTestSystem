# Subjective Test System
## Introduction
This is a simple subjective test system which can host your subjective tests for TTS.
It supports three types of subjective tests: ABX, MOS, CMOS.

## Requirement
```python
django
django-bootstrap4
```

## Usage

Clone this repository. Run the following commands to configure:
```
python manage.py makemigrations User Management
python manage.py migrate
python manage.py createsuperuser
```
Run ``python3 manage.py runserver`` to start the system on ``127.0.0.1:8000``.
Open ``127.0.0.1:8000/management/login`` and login with username and password provided before.
Then you can upload your tests into the system.

Users can login to system from ``127.0.0.1:8000/user/login``.
The account for a user is created automatically when they login for the first time.

## Upload Format
Each subjective test should be compressed as a single zip file which contains a json file named ```test.json``` and samples for subjective test.

The json file is a list containing several questions and each question contains several samples for users to judge.

An example json file:
```json
[
    {
        "type": "ABX",
        "text": "this is a test text.",
        "samples": [
            {
                "path": "samples/test1.wav",
                "type": "G",
                "text": "this is the text for test1.wav",
                "score": true,
                "file_type": "audio"
            },
            {
                "path": "samples/test2.wav",
                "type": "G",
                "text": "this is the text for test2.wav",
                "score": false,
                "file_type": "audio"
            },
            {
                "path": "samples/test3.wav",
                "type": "P",
                "text": "this is the text for test3.wav",
                "score": true,
                "file_type": "audio"
            }
        ]
    },
    {
        "type": "MOS",
        "text": "this is a test text.",
        "samples": [
            {
                "path": "samples/test1.wav",
                "type": "G",
                "text": "this is the text for test1.wav",
                "score": true,
                "file_type": "audio"
            },
            {
                "path": "samples/test2.wav",
                "type": "G",
                "text": "this is the text for test2.wav",
                "score": false,
                "file_type": "audio"
            },
            {
                "path": "samples/test3.wav",
                "type": "P",
                "text": "this is the text for test3.wav",
                "score": true,
                "file_type": "audio"
            }
        ]
    },
    {
        "type": "CMOS",
        "text": "this is a test text.",
        "samples": [
            {
                "path": "samples/test1.wav",
                "type": "G",
                "text": "this is the text for test1.wav",
                "score": false,
                "file_type": "audio"
            },
            {
                "path": "samples/test2.wav",
                "type": "P",
                "text": "this is the text for test2.wav",
                "score": true,
                "file_type": "audio"
            },
            {
                "path": "samples/test3.wav",
                "type": "P",
                "text": "this is the text for test3.wav",
                "score": true,
                "file_type": "audio"
            }
        ]
    }
]
```
