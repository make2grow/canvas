source .env && curl -X POST "${API_URL}/api/v1/courses/81929/quizzes" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "quiz": {
          "title": "Sample Quiz",
          "description": "This is a sample quiz created via API",
          "time_limit": 30,
          "shuffle_answers": true,
          "hide_results": "always",
          "published": true
        }
      }'


