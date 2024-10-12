The current HTML files you've shared (**`base.html`** and **`dashboard.html`**) primarily handle the API key submission and data fetching, but they do not yet address the **user registration** and **login** functionality. Let me walk you through what needs to be added to handle **user login** and **registration** effectively.

### Changes Needed:
1. **User Registration and Login Page**: We need a dedicated **login** and **registration** page for first-time users. This page should allow users to:
   - Register with their username, email, and password (for new users).
   - Log in with their username and password (for returning users).
   - Once logged in, users should be able to enter their API key to interact with the FlowFact API.

2. **Redirect and Session Handling**: After logging in, users should be redirected to the **API key submission form** (e.g., on **`base.html`**) where they can submit their FlowFact API key.

### Updated Template Structure:

1. **New Login and Registration Page**: This will handle user registration and login functionality.
2. **Modification to the API Key Form (base.html)**: To handle users who are already logged in and need to submit their FlowFact API key.

---

### 1. **`login.html`** (New Login and Registration Page)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login or Register</title>
    <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
            max-width: 400px;
            margin: 0 auto;
        }
        label {
            font-size: 1.2em;
        }
        input[type="text"], input[type="password"] {
            padding: 10px;
            margin: 10px 0;
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        footer {
            margin-top: 30px;
            text-align: center;
            color: #777;
        }
    </style>
</head>
<body>
    <h1>Login or Register</h1>

    <form id="login-form" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        
        <button type="submit">Login</button>
    </form>

    <form id="register-form" method="POST" style="margin-top: 40px;">
        <h2>New User? Register Here</h2>
        
        <label for="username-register">Username:</label>
        <input type="text" id="username-register" name="username" required>
        
        <label for="email-register">Email:</label>
        <input type="text" id="email-register" name="email" required>

        <label for="password-register">Password:</label>
        <input type="password" id="password-register" name="password" required>

        <button type="submit">Register</button>
    </form>

    <!-- Pyscript or JavaScript code to handle login and registration -->
    <py-script src="{{ url_for('static', filename='pyscript_auth.js') }}"></py-script>

    <footer>
        <p>Real Estate API Service</p>
    </footer>
</body>
</html>
```

### Key Features:
- **Login Form**: This allows users to log in with their username and password. Once logged in, the user will be redirected to the **API key submission page** (e.g., **`base.html`**).
- **Registration Form**: New users can register with a username, email, and password.
- **PyScript/JavaScript**: The form submissions are handled by **PyScript** (via `pyscript_auth.js`) or a similar mechanism to authenticate and register users asynchronously.

---

### 2. **Updated `pyscript_auth.js`** (New PyScript for Handling Login/Registration)

```python
from pyscript import Element
import httpx

# Function to handle user login
async def login(event):
    event.preventDefault()

    username = Element("username").value
    password = Element("password").value
    response_message = Element("response-message")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post('/login/', data={'username': username, 'password': password})
            if response.status_code == 200:
                window.location.href = '/api-key-page'  # Redirect to API key page after successful login
            else:
                response_message.write("Invalid login credentials.")
    except Exception as e:
        response_message.write(f"Error: {str(e)}")

# Function to handle user registration
async def register(event):
    event.preventDefault()

    username = Element("username-register").value
    email = Element("email-register").value
    password = Element("password-register").value
    response_message = Element("response-message")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post('/register/', data={'username': username, 'email': email, 'password': password})
            if response.status_code == 200:
                response_message.write("Registration successful! You can now log in.")
            else:
                response_message.write("Error during registration.")
    except Exception as e:
        response_message.write(f"Error: {str(e)}")

# Attach event listeners
Element("login-form").element.onsubmit = login
Element("register-form").element.onsubmit = register
```

### Key Features:
- **Login Handling**: The login form submits the user’s username and password to the `/login/` endpoint, which authenticates the user. On success, the user is redirected to the page for submitting their API key (e.g., **`base.html`**).
- **Registration Handling**: New users can register by submitting their username, email, and password to the `/register/` endpoint. On success, they are prompted to log in.
- **Redirect on Success**: After a successful login, the user is redirected to the **API key submission page**.

---

### 3. **API Key Form (Updated `base.html`)**:
We already updated **`base.html`** to allow users to submit their API key after logging in, so no further changes are needed here. Once the user logs in, they will be redirected to the **API key submission form**.

### 4. **Routing and Session Management**:
Ensure your backend correctly handles:
- **User session management**: After login, the user session should be created, and the user can proceed to the **API key submission**.
- **Redirection to the API key page**: After login, ensure the user is redirected to the correct page for API key submission.

### Summary of Additions:
1. **`login.html`**: A new login and registration page for handling user authentication.
2. **`pyscript_auth.js`**: New PyScript file to handle the login and registration processes.
3. **Redirect Flow**: Users are redirected to the **API key submission** form after login.

This setup provides a smooth flow for user authentication and API key submission, while being aligned with the backend structure you have in place.

Let me know if you need further refinement!