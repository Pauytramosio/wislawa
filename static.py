import json
def static() -> dict:
    with open("static.json", 'r') as f:
        return json.load(f)

static: dict = static()