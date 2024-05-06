#!/bin/sh

echo "backuping src"
cp ./mist.openapi.yml ./mist.openapi.yml.bck

echo "removing spotlight entries"
python3 ./a0_remove_xtags.py

echo "processing files"
python3 ./a1_process.py
#mv ./mist.openapi_reordered.yml ./mist.openapi.yml

echo "yaml to postman conversion"
rm ../mist.postman.*
openapi2postmanv2 -s ../mist.openapi.yml -o ../mist.postman.json -p -O enableOptionalParameters=false,includeAuthInfoInExample=false

echo "Postman post-process"
python3 ./a2_postman_postprocess.py

echo "Adding custom tags"
python3 ./a3_doc_xtags.py

./generate_toc.sh -a