#Made by a human and an AI, I love you AI, plz dont murder me once you take over the world
import requests
import json
import time

def get_data(api_url, page, limit):
    params = {"limit": limit, "page": page}  # Base parameters

    url = f"{api_url}"  # Start with base URL

    if params:  # Add parameters if any
        url += "&".join([f"{k}={v}" for k, v in params.items()])

    print(url)
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    return response.json()

def save_to_json(data, filename):

    with open(filename, 'w') as f:
        json.dump(data, f, indent=None)  # Set indent to None for no indentation

def main():
    """Parses command-line arguments and runs the script."""
    #Example:
    # https://danbooru.donmai.us/posts.json?login=USERNAME&api_key=APIKEY&tags=fav:USERNAME&limit=2&page=1
    # https://danbooru.donmai.us/posts.json?tags=fav:albert&limit=2&page=1
    # python getalldata.py --username NAME --pages 24 --limit 200 --yourusername NAME --apikey KEY
    
    import argparse
    parser = argparse.ArgumentParser(description="Extract and count tags from an API")
    parser.add_argument("--username", help="The username to use with the API", required=True)
    parser.add_argument("--pages", type=int, help="The number of pages to fetch", required=True)
    parser.add_argument("--limit", type=int, help="Max 200", required=True)
    parser.add_argument("--yourusername", help="Only needed if you have an API key (optional)", required=False)
    parser.add_argument("--apikey", help="The API key for authentication (optional)", required=False)
    args = parser.parse_args()

    base_url = "https://danbooru.donmai.us/posts.json?"  # Base URL

    # Construct API URL including username and API key if provided
    api_url = f"{base_url}"
    if args.apikey:
        api_url += f"login={args.yourusername}"
        api_url += f"&api_key={args.apikey}" + "&"

    all_data = []

    for page in range(1, args.pages + 1):
        page_data = get_data(api_url, page, args.limit)

        # Break if nothing is returned because that means... theres nothing left?
        if page_data.count == 0:
            break

        all_data.extend(page_data)

        #you can do more calls than this if youre gold or platinum but eh... No rush for me, check here for info: https://danbooru.donmai.us/wiki_pages/help%3Ausers
        time.sleep(1)

    # for item in all_data:
    #     tags = item["tags"]
    #     for tag in tags:
    #         total_fav_tags[tag] = total_fav_tags.get(tag, 0) + 1
    #         if just_the_tags.__contains__(tag) == False:
    #             just_the_tags.append(tag)

    # Sort by the tag with the highest value!
    # sorted_tags = sorted(total_fav_tags.items(), key=itemgetter(1), reverse=True)

    save_to_json(all_data, "allyourdata.json")
    # print("Total fav tags saved to total_fav_tags.json")

if __name__ == "__main__":
    main()
