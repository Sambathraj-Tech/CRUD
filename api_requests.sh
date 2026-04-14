## ============================================================
## Sample API Requests — cURL Cheatsheet
## Base URL: http://localhost:8000/api/v1
## Swagger UI: http://localhost:8000/docs
## ============================================================

BASE="http://localhost:8000/api/v1"


# ==============================================================
# USERS
# ==============================================================

## --- CREATE user ---
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "full_name": "Alice Smith"
  }' | python3 -m json.tool

## --- LIST users (page 1, 10 per page) ---
curl -s "$BASE/users/?skip=0&limit=10" | python3 -m json.tool

## --- GET single user ---
curl -s "$BASE/users/1" | python3 -m json.tool

## --- UPDATE user (partial) ---
curl -s -X PATCH "$BASE/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alice Johnson",
    "is_active": false
  }' | python3 -m json.tool

## --- DELETE user ---
curl -s -X DELETE "$BASE/users/1" -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 204


# ==============================================================
# TASKS
# ==============================================================

## --- CREATE task for user 1 ---
curl -s -X POST "$BASE/users/1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }' | python3 -m json.tool

## --- LIST tasks for user 1 ---
curl -s "$BASE/users/1/tasks?skip=0&limit=10" | python3 -m json.tool

## --- LIST all tasks ---
curl -s "$BASE/tasks/?skip=0&limit=10" | python3 -m json.tool

## --- GET single task ---
curl -s "$BASE/tasks/1" | python3 -m json.tool

## --- MARK task complete ---
curl -s -X PATCH "$BASE/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}' | python3 -m json.tool

## --- UPDATE task title ---
curl -s -X PATCH "$BASE/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and snacks"}' | python3 -m json.tool

## --- DELETE task ---
curl -s -X DELETE "$BASE/tasks/1" -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 204


# ==============================================================
# HEALTH CHECK
# ==============================================================
curl -s "http://localhost:8000/health" | python3 -m json.tool
# Expected: {"status": "ok", "app": "FastAPI CRUD App"}


# ==============================================================
# ERROR CASES (to verify validation works)
# ==============================================================

## Duplicate username → 400
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "new@example.com"}' | python3 -m json.tool

## User not found → 404
curl -s "$BASE/users/9999" | python3 -m json.tool

## Create task for non-existent user → 404
curl -s -X POST "$BASE/users/9999/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Ghost task"}' | python3 -m json.tool