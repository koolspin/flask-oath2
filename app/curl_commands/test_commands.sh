#!/usr/bin/env bash
curl -X POST -d "client_id=google_assistant&redirect_uri=https%3A%2F%2Foauth-redirect.googleusercontent.com%2Fr%2F12345678&state=foo_bar&response_type=token" http://localhost:8086/oauth/implicit

http://localhost:8086/oauth/implicit?client_id=google_assistant&redirect_uri=https%3A%2F%2Foauth-redirect.googleusercontent.com%2Fr%2F12345678&state=foo_bar&response_type=token
