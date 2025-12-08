# API Documentation

Complete API documentation for the Snake Game Backend.

## Base URL

```
http://localhost:8000  # Development
https://api.yourdomain.com  # Production
```

## Authentication

Currently, the API does not require authentication. Future versions may include API keys or OAuth.

## Response Format

### Success Response

```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `SCORE_INVALID` | 400 | Score out of valid range |
| `USERNAME_INVALID` | 400 | Username doesn't meet requirements |
| `DUPLICATE_SUBMISSION` | 409 | Same score submitted recently |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `NOT_FOUND` | 404 | Resource not found |
| `SERVER_ERROR` | 500 | Internal server error |
| `DATABASE_ERROR` | 500 | Database operation failed |

## Endpoints

### Health Check

#### GET /health

Basic health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

#### GET /health/db

Database health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "db_connected": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Leaderboard

#### GET /api/v1/leaderboard

Get leaderboard entries with pagination and filtering.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Number of results (1-100) |
| `offset` | integer | 0 | Offset for pagination |
| `mode` | string | null | Filter by game mode: `walls` or `walls-through` |
| `sort` | string | `score` | Sort order: `score` or `date` |

**Example Request:**
```bash
GET /api/v1/leaderboard?limit=20&offset=0&mode=walls&sort=score
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "username": "PLAYER1",
      "score": 250,
      "mode": "walls",
      "date": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

#### POST /api/v1/leaderboard

Submit a new score to the leaderboard.

**Request Body:**
```json
{
  "username": "PLAYER1",
  "score": 250,
  "mode": "walls"
}
```

**Validation Rules:**
- `username`: 2-20 characters, alphanumeric and underscores only
- `score`: 0-999999
- `mode`: `walls` or `walls-through`

**Response:**
```json
{
  "id": 1,
  "username": "PLAYER1",
  "score": 250,
  "mode": "walls",
  "date": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400`: Validation error (invalid data)
- `409`: Duplicate submission (same score submitted recently)
- `429`: Rate limit exceeded

#### GET /api/v1/leaderboard/{username}

Get scores for a specific user.

**Path Parameters:**
- `username`: Username to get scores for

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Number of results (1-100) |
| `offset` | integer | 0 | Offset for pagination |
| `mode` | string | null | Filter by game mode |

**Example Request:**
```bash
GET /api/v1/leaderboard/PLAYER1?limit=10&offset=0&mode=walls
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "username": "PLAYER1",
      "score": 250,
      "mode": "walls",
      "date": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 5,
    "limit": 10,
    "offset": 0,
    "has_more": false
  }
}
```

**Error Responses:**
- `404`: User not found or no scores

#### GET /api/v1/leaderboard/stats/summary

Get aggregate statistics.

**Response:**
```json
{
  "total_players": 50,
  "total_scores": 250,
  "average_score": 150.5,
  "top_score": 500
}
```

## Rate Limiting

- Score submissions: 60 requests per minute per IP/user
- Other endpoints: No rate limiting (may be added in future)

## Examples

### Submit a Score

```bash
curl -X POST http://localhost:8000/api/v1/leaderboard \
  -H "Content-Type: application/json" \
  -d '{
    "username": "PLAYER1",
    "score": 250,
    "mode": "walls"
  }'
```

### Get Top 10 Scores

```bash
curl http://localhost:8000/api/v1/leaderboard?limit=10&sort=score
```

### Get User Scores

```bash
curl http://localhost:8000/api/v1/leaderboard/PLAYER1
```

## Interactive Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation with the ability to test endpoints directly.

## Versioning

The API is versioned using URL paths (`/api/v1/...`). Future versions will use `/api/v2/...` etc.

Breaking changes will only occur in new API versions. Current version (`v1`) will remain stable.

