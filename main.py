import requests
import json
import time

def get_data(api_url, page):
    """Fetches JSON data from the specified API URL with pagination.

    Args:
        api_url (str): The base URL of the API endpoint.
        page (int): The page number for pagination (if applicable).

    Returns:
        list: A list of dictionaries containing extracted tags.
    """

    url = f"{api_url}&page={page}"  # Append page number to URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    data = response.json()  # Assuming the response is valid JSON

    # Extract and split tag_string from each object
    processed_data = []
    for item in data:
        if "tag_string" in item:  # Check if "tag_string" exists
            tags = item["tag_string"].split()  # Split tags using whitespace
            processed_data.append({"tags": tags})  # Store extracted tags

    return processed_data

def save_to_json(data, filename):
    """Saves the provided data to a JSON file.

    Args:
        data (list): A list of dictionaries containing extracted tags.
        filename (str): The name of the output JSON file.
    """

    with open(filename, 'w') as f:
        json.dump(data, f, indent=None)  # Indent for readability

if __name__ == '__main__':
    # ... (API URL and num_pages)

    all_data = []
    total_fav_tags = {}  # Initialize the dictionary for total fav tags

    for page in range(1, num_pages + 1):
        page_data = get_data(api_url, page)
        all_data.extend(page_data)
        time.sleep(1)

    for item in all_data:
        tags = item["tags"]  # Access the "tags" list
        for tag in tags:
            total_fav_tags[tag] = total_fav_tags.get(tag, 0) + 1  # Count tag occurrences

    # Save the total fav tags dictionary to JSON
    save_to_json(total_fav_tags, "total_fav_tags.json")
    print("Total fav tags saved to total_fav_tags.json")
