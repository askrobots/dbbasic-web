"""User API - demonstrates hierarchical routing

This file handles:
- /user → list all users
- /user/123 → get user 123
- /user/123/posts → get posts for user 123
"""
import json
from dbbasic_web.responses import json as json_response, text


def handle(request):
    """Route based on path_parts"""
    path_parts = request["path_parts"]
    method = request["method"]

    # /user
    if len(path_parts) == 1:
        if method == "GET":
            return list_users(request)
        elif method == "POST":
            return create_user(request)

    # /user/{id}
    elif len(path_parts) == 2:
        user_id = path_parts[1]
        if method == "GET":
            return get_user(user_id)
        elif method == "PUT":
            return update_user(user_id, request)
        elif method == "DELETE":
            return delete_user(user_id)

    # /user/{id}/posts
    elif len(path_parts) == 3 and path_parts[2] == "posts":
        user_id = path_parts[1]
        return get_user_posts(user_id)

    return text("Not Found", 404)


def list_users(request):
    """List all users"""
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]
    return json_response(json.dumps({"users": users}))


def get_user(user_id: str):
    """Get a single user"""
    # In a real app, fetch from database
    user = {"id": int(user_id), "name": f"User {user_id}", "email": f"user{user_id}@example.com"}
    return json_response(json.dumps({"user": user}))


def create_user(request):
    """Create a new user"""
    # In a real app, parse body and save to database
    return json_response(json.dumps({"status": "created", "id": 999}), status=201)


def update_user(user_id: str, request):
    """Update a user"""
    return json_response(json.dumps({"status": "updated", "id": int(user_id)}))


def delete_user(user_id: str):
    """Delete a user"""
    return json_response(json.dumps({"status": "deleted", "id": int(user_id)}))


def get_user_posts(user_id: str):
    """Get posts for a user"""
    posts = [
        {"id": 1, "user_id": int(user_id), "title": "First post"},
        {"id": 2, "user_id": int(user_id), "title": "Second post"},
    ]
    return json_response(json.dumps({"posts": posts}))
