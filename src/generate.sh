#!/bin/sh

echo "processing files"
python3 ./process.py
#mv ./mist.openapi_reordered.yml ./mist.openapi.yml

echo "yaml to postman conversion"
rm ../mist.postman.*
openapi2postmanv2 -s ../mist.openapi.yml -o ../mist.postman.json -p -O enableOptionalParameters=false,includeAuthInfoInExample=false

echo "Postman post-process"
python3 ./postman_postprocess.py
