OUT_FOLDER="../src"
FILTER_FILE="./.filters"
PORTAL_FOLDER="../../mistapi-portal/src"
CONTENT_FOLDER="$PORTAL_FOLDER/content/api"
SPEC_FOLDER="$PORTAL_FOLDER/spec"

mkdir -p $OUT_FOLDER/spec
echo "python3 ./d0_matic.py"
python3 ./d0_matic.py
echo "python3 ./d1_matic_toc.py"
python3 ./d1_matic_toc.py

# FILTERS=`cat $FILTER_FILE | cut -d"=" -f2 | cut -d"#" -f1`
# copy_files(){
#     local IFS=,
#     for filter in $FILTERS
#     do 
#         new_filter=`echo "$filter" | tr '[:upper:]' '[:lower:]'`
#         echo "$new_filter"
#         cp -r $OUT_FOLDER/content/api/$new_filter $PORTAL_FOLDER/content/api/
#         cp -r $OUT_FOLDER/spec/api/$new_filter $PORTAL_FOLDER/spec/api/
#     done
# }


echo "removing old folders"
for i in `ls -F $CONTENT_FOLDER`
do 
    if echo $i | grep -q "/$"
        then rm -rf $CONTENT_FOLDER/$i
    fi
done

for i in `ls -F $SPEC_FOLDER`
do
    if echo $i | grep -q "/$"
        then rm -rf $SPEC_FOLDER/$i
    fi
done

echo "copying new folders"
cp -r $OUT_FOLDER/spec/* $PORTAL_FOLDER/../spec_in/
cp -r $OUT_FOLDER/content/api/* $PORTAL_FOLDER/content/api/
rm -rf $OUT_FOLDER
