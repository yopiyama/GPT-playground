#!/bin/sh

curl -s https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY" | jq .data[].id | sort | jq
