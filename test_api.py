from app import app
import json

def test_api_missing_query(): # testuji, ze API vrací 400 pokud chybí query
    client = app.test_client()

    response = client.post( #Flask test client vytvori falesny HTTP POST request
        "/api/search",
        data=json.dumps({}),           # prázdné tělo
        content_type="application/json"
    )  # Flask framework: vytvoří kontext requestu, zavolá interně tvoji funkci api_search(),
    # zachytí její návratovou hodnotu, převede ji na HTTP response, vrátí to zpět do testu
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
