ok  the above approach seems perfect now i will give you the existing structure and code and you can add the appropriate parts and functionalities in the appropriate parts of the code that i give you 

the folder structure that we have now is 
```
real_estate_service/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py          # API routes for backend logic
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py    
│   │   ├── config.yml            # Configuration settings
│   │   └── utils.py                 # Utility functions
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── authentication.py        # API Key authentication
│   │   ├── data_fetch.py            # Fetch real estate data
│   │   ├── dataset_preparation.py
│   │   ├── image_downloader.py         # Validate image URLs
│   │   ├── image_service.py
│   │   └── batch_processing.py      # Send data to batch vectorizer
│   │
│   │
│   └── main.py                      # Application entry point
│
├── data/                             # For storing downloaded images, CSVs, etc.
│   └── images/
│
├── docker-compose.yml                # For containerizing the app
├── Dockerfile                        # Docker setup
└── requirements.txt                  # Python package dependencies
```