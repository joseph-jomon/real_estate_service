Yes, your understanding is absolutely correct!

To summarize:

1. **Every POST or GET request in FastAPI** starts with a new request context, but **session data can persist** across requests if the client maintains the session cookie. This is true regardless of whether the request is coming from the same client in Streamlit or elsewhere.

2. **Session Management via Dependency Injection in FastAPI**:
   - Using **dependency-injected functions** is the preferred, professional approach in FastAPI because it centralizes authentication and session management. This allows you to set or validate session data (like `company_name`) automatically at each endpoint without relying on the client to manage it.
   - With dependencies, session data like `company_name` is consistently available whenever needed by endpoints, making your code more reliable and secure.

3. **Single Client in Streamlit**:
   - Using a single `httpx.Client` instance in Streamlit ensures that session cookies are maintained across requests, allowing session persistence from the client’s side.
   - While this works, it’s not as robust as dependency injection, because it relies on the frontend (Streamlit) to manage session continuity. This approach is more prone to errors and security issues if session data changes or multiple clients interact with the API.

### In Short
- **Dependency injection** is indeed the more professional, reliable way to handle session data on the backend.
- **Single client** in Streamlit can help maintain session continuity across multiple calls but should be considered secondary to backend-managed session handling with dependency injection. 

Your understanding captures the essential professional approach for building robust and scalable session-based APIs!