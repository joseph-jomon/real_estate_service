Thank you for the clarification! I now understand the distinction you're making between the **`endpoints.py`** (which handles FlowFact API interactions and batch processing) and the **`user_endpoints.py`** (which handles user login and registration with PostgreSQL).

Let’s summarize the correct separation and adjust the files accordingly.

### File Separation:
1. **`endpoints.py`** (FlowFact API interaction and batch processing):
   - This file contains endpoints related to communicating with the FlowFact API, retrieving data, validating images, and sending data for batch processing.
   - These endpoints do **not** interact with PostgreSQL but rather handle the processing tasks related to FlowFact.

2. **`user_endpoints.py`** (User login and interaction with PostgreSQL):
   - This file is responsible for managing user registration, login, and storing session information.
   - It interacts with the **PostgreSQL database** to store user credentials and session information.
   - It allows the user to input their API key, which will be used by the endpoints in `endpoints.py` to interact with the FlowFact API.

### Changes to Consider:

#### 1. **`endpoints.py`** (FlowFact API Interaction)
No database connection (`get_db`) is needed here because it deals directly with the FlowFact API, not the PostgreSQL database. This file should focus on calling the FlowFact API, processing the data, and sending the batches.

Here's the revised version of **`endpoints.py`**:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.services.authentication import authenticate_api_key
from app.services.data_fetch import fetch_real_estate_data
from app.services.image_service import validate_image_links
from app.core.utils import save_to_dataframe
from app.services.batch_processing import send_text_batch, send_image_batch, get_task_status

router = APIRouter()

# FlowFact API key authentication
@router.post("/authenticate/")
async def authenticate(api_key: str):
    token = await authenticate_api_key(api_key)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid API key")
    return {"message": "Authentication successful", "token": token}

# Fetch real estate data from FlowFact API
@router.get("/fetch-data/")
async def fetch_data(token: str = Depends(authenticate_api_key)):
    real_estate_data = await fetch_real_estate_data(token)
    return {"data": real_estate_data}

# Validate image links for real estate objects
@router.post("/validate-images/")
async def validate_images():
    invalid_ids = await validate_image_links()
    return {"invalid_ids": invalid_ids}

# Remove invalid IDs from the dataset
@router.post("/remove-invalid-ids/")
async def remove_invalid_ids():
    df = save_to_dataframe()
    return {"message": "Filtered list saved"}

# Process a batch of text data and send it for vectorization
@router.post("/process-text-batch/")
async def process_text_batch(text_batch: list):
    task_id = await send_text_batch(text_batch)
    return {"task_id": task_id}

# Process a batch of image data and send it for vectorization
@router.post("/process-image-batch/")
async def process_image_batch(image_batch: list):
    task_id = await send_image_batch(image_batch)
    return {"task_id": task_id}

# Check the status of a batch processing task
@router.get("/task-status/{task_id}")
async def task_status(task_id: str):
    status = await get_task_status(task_id)
    return {"status": status}
```

- **No database interaction** (`get_db`) because this file is purely responsible for interacting with the FlowFact API and processing data, not handling user authentication or database operations.

#### 2. **`user_endpoints.py`** (User Registration and Login)
This file interacts with **PostgreSQL** to manage user registration and login. The user inputs the API key here, which can later be used by `endpoints.py` to communicate with the FlowFact API.

Here’s your current **`user_endpoints.py`**, which looks good but should be made fully asynchronous.

Here’s the updated **`user_endpoints.py`** to ensure it is asynchronous:

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import create_user, authenticate_user
from app.database.session import get_db

router = APIRouter()

# User registration endpoint
@router.post("/register/")
async def register_user(username: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, username, email, password)  # Make sure create_user is async
    return {"message": "User registered successfully", "user": user}

# User login endpoint
@router.post("/login/")
async def login_user(username: str, password: str, request: Request, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, username, password)  # Make sure authenticate_user is async
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Store user information in the session
    request.session["user_id"] = user.id
    return {"message": "Login successful"}
```

#### Key Points:
- **Asynchronous Database Handling**: I made the database functions `async` to handle user data efficiently. Ensure that both `create_user` and `authenticate_user` in your service are also asynchronous.
- **Session Management**: This remains the same, storing the user's `user_id` in the session after a successful login.

### Separation of Concerns:
- **`endpoints.py`** is focused purely on **FlowFact API interaction** and **batch processing**. It uses the API key provided by the user but does not interact with the PostgreSQL database.
- **`user_endpoints.py`** is responsible for **user authentication** and **interaction with PostgreSQL** to manage login sessions.

### Final Overview:
- **`endpoints.py`** handles the core business logic related to FlowFact, such as fetching data and processing batches.
- **`user_endpoints.py`** handles user authentication and stores the API key in the session for later use by the FlowFact API endpoints.

This separation ensures that your application is modular, maintainable, and scalable, with each module focusing on a specific responsibility.

Let me know if you need further adjustments or if you want to discuss anything else!