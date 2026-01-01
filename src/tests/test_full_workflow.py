from fastapi.testclient import TestClient
from fastapi import status
import sys
from pathlib import Path

grandparent_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(grandparent_dir))

from api import app

client = TestClient(app)

def test_full_workflow():
    response = client.post("/shorten/www.roblox.com")
    assert response.status_code == status.HTTP_201_CREATED
    short = response.json()["short_url"]
    print(short)
    response = client.get("/shorten/" + short, follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://www.roblox.com"
    response = client.get("/shorten/" + short + "/stats")
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    print(response)
    response = client.put("/shorten/" + short, json = {"url": "www.gutenberg.org"})
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    print(response)
    response = client.delete("/shorten/" + short)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    print("Deleted the entry for " + short)