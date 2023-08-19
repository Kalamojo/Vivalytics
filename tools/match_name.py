from fuzzywuzzy import process
import difflib


def find_entity(search_query, names):
    # Check for exact match
    exact_match = next((name for name in names if name.split()[-1].lower() == search_query.lower()), None)
    print(exact_match)
    if exact_match:
       return [(exact_match, 100)]
    else:
        closest_matches = process.extract(search_query, names)
        closest_matches = [match for match in closest_matches if match[1] == closest_matches[0][1]]
        return closest_matches

def find_entity2(search_query, names):
    closest_matches = difflib.get_close_matches(search_query, names)
    return closest_matches