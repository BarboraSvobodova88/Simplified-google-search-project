from app import clean_serpapi_results # importuji metodu z backendu app.py

def test_clean_serpapi_results_basic():
    raw = { # idealni uz vycisteny vstup
        "organic_results": [
            {
                "title": "Test Title",
                "link": "https://example.com",
                "snippet": "Example snippet"
            }
        ]
    }

    result = clean_serpapi_results(raw) # volam funkci na vycisteny vstup aby se neobjevila None, chyba, ci neprejmenovalo to klice
                                        # funkce realne tedy jen "preposila spravne hodnoty"
    assert len(result) == 1 # vystup mi musi vratit prave 1 vysledek, protoze takto definujeme raw vyse
    assert result[0]["title"] == "Test Title"  # Tady ověřim, že funkce yachovala správné hodnoty, 
    assert result[0]["link"] == "https://example.com" # nic nepřejmenovala, nic neodstranila,
    assert result[0]["link"] == "https://example.com" # nic „nepokazila“
    assert result[0]["snippet"] == "Example snippet" # v seznamu slovniku indexuji 1. slovnik ([0]) a v nem hodnotu pod klicem "snippet"

# když SerpAPI nevrátí snippet
def test_clean_results_missing_snippet():
    raw = {
        "organic_results": [
            {
                "title": "Title only",
                "link": "https://link.com"
                # snippet chybí
            }
        ]
    }

    result = clean_serpapi_results(raw)

    assert result[0]["snippet"] is None or result[0]["snippet"] == ""

# test 3: prázdný vstup
def test_clean_results_empty(): # test odolnosti funkce proti prazdnemu vstupu = nespadne do KeyError nebo TypeError
    raw = {}                    # funkce by tedy mela vratit prazdny seznam (=zadne vysledky)
    result = clean_serpapi_results(raw)
    assert result == []