"""Simple hello API endpoint - demonstrates basic routing"""
import json
from dbbasic_web.responses import json as json_response


def handle(request):
    """Handle /hello and /hello?name=World"""
    name = request.get("query", {}).get("name", "world")
    body = json.dumps({"message": f"Hello, {name}!", "path": request["path"]})
    return json_response(body)
