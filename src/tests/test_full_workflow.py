from fastapi.testclient import TestClient
import sys
from pathlib import Path
from datetime import datetime, timezone
import random

grandparent_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(grandparent_dir))

from api import app

client = TestClient(app)

def test_full_workflow():
    response = client.post("/shorten/www.roblox.com")
    print(response)