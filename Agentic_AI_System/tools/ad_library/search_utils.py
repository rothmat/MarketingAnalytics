from typing import List

# Mapping of initiatives to known search terms and synonyms
INITIATIVE_KEYWORDS = {
    "10-millionen-schweiz": [
        "10-Millionen-Schweiz",
        "keine 10 Millionen",
        "Masseneinwanderung",
    ],
    "13. ahv-rente": [
        "13. AHV-Rente",
        "AHV+",
        "für ein besseres Leben im Alter",
    ],
    "umweltverantwortungsinitiative": [
        "Umweltverantwortungsinitiative",
        "Verantwortung Umwelt",
        "UV-Initiative",
    ],
}


def expand_search_terms(query: str) -> List[str]:
    """Return a list of search terms based on the provided query.

    The query is compared to known initiatives. If a match is found,
    the corresponding synonyms are returned; otherwise the query
    itself is used.
    """
    q = query.lower()
    for key, terms in INITIATIVE_KEYWORDS.items():
        if key in q or any(t.lower() in q for t in terms):
            return list(set(terms))
    return [query]
