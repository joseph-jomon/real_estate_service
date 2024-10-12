from pyscript import Element
import httpx

async def submit_form(event):
    event.preventDefault()  # Prevent the form from refreshing the page
    
    api_key = Element("api-key").value
    response_message = Element("response-message")
    progress_section = Element("progress-section")
    progress_bar = Element("progress-bar")

    # Reset progress bar and message
    progress_bar.value = 0
    response_message.clear()

    try:
        # Authenticate user's API key (adjusted to match the new API structure)
        async with httpx.AsyncClient() as client:
            response = await client.post('/login/', data={'api_key': api_key})  # Assuming login is where the API key is set
            if response.status_code == 200:
                response_message.write("API Key authenticated successfully!")
                
                # Start fetching data after successful authentication
                progress_section.show()
                await fetch_data(client, progress_bar)
            else:
                response_message.write(f"Error authenticating API key: {response.status_code}")
    
    except Exception as e:
        response_message.write(f"Error: {str(e)}")

async def fetch_data(client, progress_bar):
    try:
        # Fetch data from FlowFact API
        response = await client.get('/fetch-data/')
        if response.status_code == 200:
            data = response.json().get("data", [])
            progress_bar.value = 50
            
            # Start image validation after fetching data
            invalid_ids_response = await client.post('/validate-images/')
            invalid_ids = invalid_ids_response.json().get("invalid_ids", [])
            
            progress_bar.value = 100
            Element("response-message").write(f"Data fetch and validation complete. Invalid IDs: {len(invalid_ids)}")
        else:
            Element("response-message").write(f"Error fetching data: {response.status_code}")

    except Exception as e:
        Element("response-message").write(f"Error: {str(e)}")

# Attach the event listener to the form
Element("api-key-form").element.onsubmit = submit_form
