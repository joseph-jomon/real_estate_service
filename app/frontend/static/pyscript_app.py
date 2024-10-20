from js import document, JSON  # This is the updated way to access the DOM in PyScript
from pyscript import fetch  # Fetch is still available directly from pyscript

async def submit_form(event):
    event.preventDefault()  # Prevent the form from refreshing the page

    # Get elements for interacting with the DOM using js.document
    api_key = document.querySelector("#api-key").value
    print(f"API Key: {api_key}")  # Debugging: Print the API Key to console
    response_message = document.querySelector("#response-message")
    progress_section = document.querySelector("#progress-section")
    progress_bar = document.querySelector("#progress-bar")

    # Reset progress bar and clear previous message
    progress_bar.value = 0
    response_message.innerHTML = ""

    try:
        # Send a POST request with JSON body
        response = await fetch("/flowfact/authenticate/",  
                               method="POST", 
                               headers={"Content-Type": "application/json"},
                               body=JSON.stringify({"api_key": api_key}))  # Ensure API key is properly sent as JSON
        print(f"Response Status: {response.status}")  # Debugging: Print the status of the response

        if response.ok:
            response_message.innerHTML = "API Key authenticated successfully!"
            progress_section.style.display = "block"
            # Proceed to fetch data
            await fetch_data(progress_bar)
        else:
            response_message.innerHTML = f"Error authenticating API key: {response.status}"

    except Exception as e:
        response_message.innerHTML = f"Error: {str(e)}"
        print(f"This is the thrown Error: {str(e)}")



async def fetch_data(progress_bar):
    try:
        # Fetch data from FlowFact API
        response = await fetch("/flowfact/fetch-data/")

        if response.ok:
            progress_bar.value = 50
            # Start image validation after data is fetched
            invalid_ids_response = await fetch("/flowfact/validate-images/", method="POST")
            invalid_ids = await invalid_ids_response.json()

            progress_bar.value = 100
            document.querySelector("#response-message").innerHTML = f"Data fetch and validation complete. Invalid IDs: {len(invalid_ids)}"
        else:
            document.querySelector("#response-message").innerHTML = f"Error fetching data: {response.status}"

    except Exception as e:
        document.querySelector("#response-message").innerHTML = f"Error: {str(e)}"
