import requests
import json
import time

def get_data(api_url, username, api_key, page):
    """Fetches JSON data from the specified API URL with pagination.

    Args:
        api_url (str): The base URL of the API endpoint.
        username (str): The username to use for authentication.
        api_key (str): The API key for authentication.
        page (int): The page number for pagination (if applicable).

    Returns:
        list: A list of dictionaries containing extracted tags.
    """

    params = {"limit": 2, "page": page}  # Base parameters

    if api_key:  # Add authentication parameters if api_key is provided
        params["login"] = username
        params["api_key"] = api_key

    url = f"{api_url}"  # Start with base URL
    if params:  # Add parameters if any
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

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
    """Saves the provided data to a JSON file without indentation.

    Args:
        data (list or dict): The data to save.
        filename (str): The name of the output JSON file.
    """

    with open(filename, 'w') as f:
        json.dump(data, f, indent=None)  # Set indent to None for no indentation

def main():
    """Parses command-line arguments and runs the script."""

    import argparse

    parser = argparse.ArgumentParser(description="Extract and count tags from an API")
    parser.add_argument("username", help="The username to use with the API")
    parser.add_argument("pages", type=int, help="The number of pages to fetch")
    parser.add_argument("api_key", help="The API key for authentication (optional)")
    args = parser.parse_args()

    api_url = "https://danbooru.donmai.us/posts.json"  # Base URL

    all_data = []
    total_fav_tags = {}

    for page in range(1, args.pages + 1):
        page_data = get_data(api_url, args.username, args.api_key, page)
        all_data.extend(page_data)
        time.sleep(1)

    for item in all_data:
        tags = item["tags"]
        for tag in tags:
            total_fav_tags[tag] = total_fav_tags.get(tag, 0) + 1

    save_to_json(total_fav_tags, "total_fav_tags.json")
    print("Total fav tags saved to total_fav_tags.json")

if __name__ == "__main__":
    main()
