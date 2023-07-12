#!/bin/bash

RAND=$((1 + $RANDOM % 100))

curl -X POST http://localhost:5000/api/timeline_post -d "name=Charlie$RAND&email=charlie$RAND@example.com&content=Testing $RAND" 

CURLRESULT=$(curl -s http://localhost:5000/api/timeline_post | jq -r ".timeline_posts | .[] | select(.name == \"Charlie$RAND\") | select(.email == \"charlie$RAND@example.com\") | select(.content == \"Testing $RAND\")")

if [[ -z $CURLRESULT ]]
then
    echo "Fail"
else
    echo "All good"
fi
