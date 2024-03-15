OUT_FOLDER="../src"
FILTER_FILE="./.filters"
PORTAL_FOLDER="../../API/mistapi_portal/src"
CONTENT_FOLDER="$PORTAL_FOLDER/content/api"
SPEC_FOLDER="$PORTAL_FOLDER/spec"
REGEN=0
if echo $@ | grep -q "^-a$"
then 
    REGEN=1
fi
if [ $REGEN -eq 1 ]
then 
    echo "python3 ./0_tag_grp1.py"
    python3 ./0_tag_grp1.py
    echo "python3 ./0_tag_grp2.py"
    python3 ./0_tag_grp2.py
    echo "python3 ./0_tag_grp3.py"
    python3 ./0_tag_grp3.py
fi

rm -rf $OUT_FOLDER/spec/components/*
mkdir $OUT_FOLDER/spec/components/parameters
mkdir $OUT_FOLDER/spec/components/responses
mkdir $OUT_FOLDER/spec/components/schemas

echo "python3 ./1_components.py"
python3 ./1_components.py
echo "python3 ./1_tag_spec.py"
python3 ./1_tag_spec.py
echo "python3 ./2_tag_toc.py"
python3 ./2_tag_toc.py

FILTERS=`cat $FILTER_FILE | cut -d"=" -f2 | cut -d"#" -f1`
copy_files(){
    local IFS=,
    for filter in $FILTERS
    do 
        new_filter=`echo "$filter" | tr '[:upper:]' '[:lower:]'`
        echo "$new_filter"
        cp -r $OUT_FOLDER/content/api/$new_filter $PORTAL_FOLDER/content/api/
        cp -r $OUT_FOLDER/spec/$new_filter $PORTAL_FOLDER/spec/
    done
}


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
cp -r $OUT_FOLDER/spec/components $PORTAL_FOLDER/spec/
copy_files
