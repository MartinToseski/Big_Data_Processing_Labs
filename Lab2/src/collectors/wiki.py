import requests

def get_wikipedia_title(wikidata_id):
    try:
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
        data = requests.get(url).json()
        entity = data["entities"][wikidata_id]

        sitelinks = entity.get("sitelinks", {})
        if "enwiki" in sitelinks:
            return sitelinks["enwiki"]["title"]
    except:
        return None

    return None


def get_description_length(title):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        data = requests.get(url).json()
        return len(data.get("extract", ""))
    except:
        return 0


def enrich(tags):
    wikidata_id = tags.get("wikidata") or tags.get("brand:wikidata")

    if not wikidata_id:
        return None, 0

    title = get_wikipedia_title(wikidata_id)

    if not title:
        return None, 0

    desc_len = get_description_length(title)

    return wikidata_id, desc_len