import requests
import re


REVIEWS_COUNT = 500
REVIEWS_PER_REQUEST = 20


game_IDs = {
    "AAA": {
        "KINGDOM_COME_DELIVERANCE": "379430",
        "ASSASSINS_CREED_ODYSSEY": "812140",
        "FAR_CRY_5 ": "552520",
        "ARTIFACT ": "583950",
        "DARKSIDERS_III ": "606280",
        "SHADOW_OF_THE_TOMB_RAIDER ": "750920",
        "PATHFINDER_KINGMAKER ": "640820",
        "PILLARS_OF_ETERNITY_II_DEADFIRE ": "560130",
        "BATTLETECH": "637090",
        "MONSTER_HUNTER_WORLD ": "582010 ",
    },
    
    "indie": {
        "RIMWORLD": "294100",
        "DUSK": "519860",
        "DEAD_CELLS" : "588650",
        "RETURN_OF_THE_OBRA_DINN" : "653530",
        "GRIS" : "683320",
        "JUST_SHAPES_BEATS" : "531510",
        "THE_FOREST" : "242760",
        "NEKOPARA_EXTRA" : "899970",
        "EPIC_BATTLE_FANTASY_5" : "432350",
        "ZUP_X" : "508900"
    }
}


def review_to_words(review):
    """
    input : a string "review"
    filters out anything else than pure words
    output: a string list of words in that review
    """
    words = []
    review = re.sub(r'[^\w\s]', '', review)
    review = re.sub(r"\n", " ",     review)
    review.replace('☐', '', 1)
    review = review.lower()
    for word in review.split(' '):
        if word != '':
            words.append(word)
    return words


def response_to_words(jarr):
    """
    input : array called "reviews" in the json of the Steam API response
    output: a string list of words in user reviews of the Steam API response
    """
    all_words = []
    for jelem in jarr:
        rev = jelem['review']
        for word in review_to_words(rev):
            all_words.append(word)
    return all_words


def main():
    for game_type in game_IDs:
        for game_name in game_IDs[game_type]:
            game_id = game_IDs[game_type][game_name]
            print(f'Processing game ID {game_id}... ')
            words_count = {}  # dictionary: word -> count
            api_cursor = '*' 
            for revs_idx in range(0, REVIEWS_COUNT, REVIEWS_PER_REQUEST):
                api_url = "https://store.steampowered.com/appreviews/" + game_id + "?json=1&cursor=" + api_cursor
                response = requests.get(api_url)
                try:
                    jres = response.json()
                    api_cursor = jres['cursor'].replace('+', '')  # Steam API...
                    words = response_to_words(jres['reviews'])
                    for word in words:
                        if word not in words_count:
                            words_count[word] = 0
                        words_count[word] += 1
                except:
                    print(f'Failed fetching reviews {revs_idx}-{revs_idx + 20}. ({api_url})')
            sorted_words_count = sorted(words_count.items(), key=lambda x: x[1], reverse=True)
            path = './out/' + game_type + '_' + game_id + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(sorted_words_count))


if __name__ == '__main__':
    main()
