#Made by a human and an AI, I love you AI, plz dont murder me once you take over the world
import json
from operator import itemgetter  # For sorting by value

def get_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=None)  # Set indent to None for no indentation

def uglysplitfix(alldata):
    for item in alldata:
        splitstring = item["tag_string"].split()
        item["tag_string"] = splitstring

        splitstring = item["tag_string_artist"].split()
        item["tag_string_artist"] = splitstring

        splitstring = item["tag_string_character"].split()
        item["tag_string_character"] = splitstring

        splitstring = item["tag_string_copyright"].split()
        item["tag_string_copyright"] = splitstring

        splitstring = item["tag_string_general"].split()
        item["tag_string_general"] = splitstring

        splitstring = item["tag_string_meta"].split()
        item["tag_string_meta"] = splitstring

    save_to_json(alldata,'./files/splitdata.json')
    return alldata

def split_into_ratings(alldata):
    general = []
    sensitive = []
    questionable = []
    explicit = []

    for item in alldata:
        match item["rating"]:
            case "g":
                general.append(item)
            case "s":
                sensitive.append(item)
            case "q":
                questionable.append(item)
            case "e":
                explicit.append(item)
            case _:
                print("No rating found for id: " + item["id"])
                
    return(general,sensitive,questionable,explicit)
    
    
def create_fav_list(taglist,filename,tag_type):
    just_the_tags = []
    total_fav_tags = {}

    for item in taglist:
        for tag in item[tag_type]:
            total_fav_tags[tag] = total_fav_tags.get(tag, 0) + 1
            if just_the_tags.__contains__(tag) == False:
                just_the_tags.append(tag)

    # Sort by the tag with the highest value!
    sorted_tags = sorted(total_fav_tags.items(), key=itemgetter(1), reverse=True)
    save_to_json(sorted_tags,'./files/rank_'+tag_type+'_'+filename)
    
    only_tags = ",".join(just_the_tags)
    save_to_json(only_tags,'./files/tags_'+tag_type+'_'+filename)
    

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Use some json file for stuff")
    parser.add_argument("--filename", help="filename in files folder", required=True)
    args = parser.parse_args()

    alldata = get_data('./files/'+args.filename)
    
    data = uglysplitfix(alldata)

    ratings = split_into_ratings(data)
    general = ratings[0]
    sensitive = ratings[1]
    questionable = ratings[2]
    explicit = ratings[3]
    
    save_to_json(general,"./files/general.json")
    save_to_json(sensitive,"./files/sensitive.json")
    save_to_json(questionable,"./files/questionable.json")
    save_to_json(explicit,"./files/explicit.json")
    
    create_fav_list(general,'general.json',"tag_string_general")
    create_fav_list(sensitive,'sensitive.json',"tag_string_general")
    create_fav_list(questionable,'questionable.json',"tag_string_general")
    create_fav_list(explicit,'explicit.json',"tag_string_general")
    
    create_fav_list(data,'alldata.json',"tag_string_general")
    
    

if __name__ == "__main__":
    main()

