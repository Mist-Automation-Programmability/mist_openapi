#!/bin/sh
ts=`date "+%s"`
echo "backuping src"
cp ./mist.openapi.yml ./mist.openapi.yml.$ts.bak

echo "removing spotlight entries"
python3 ./a0_remove_xtags.py
sleep 1

echo "processing files"
python3 ./a1_process.py
#mv ./mist.openapi_reordered.yml ./mist.openapi.yml
sleep 1

echo "yaml to postman conversion"
rm ../mist.postman.*
openapi2postmanv2 -s ../mist.openapi.yml -o ../mist.postman.json -p -O enableOptionalParameters=false,includeAuthInfoInExample=false
sleep 1

echo "Postman post-process"
python3 ./a2_postman_postprocess.py
sleep 1

echo "Adding custom tags"
python3 ./a3_doc_xtags.py
sleep 1

./generate_toc.sh -a