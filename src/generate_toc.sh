FILTER_FILE="./.filters"
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

rm -rf ./spec/components/*
mkdir ./spec/components/parameters
mkdir ./spec/components/responses
mkdir ./spec/components/schemas

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
        cp -r ./content/api/$new_filter $ROOT_FOLDER/content/api/
        cp -r ./spec/$new_filter $ROOT_FOLDER/spec/
    done
}


echo "removing old folders"
ROOT_FOLDER="../../API/mistapi_portal/src"
CONTENT_FOLDER="$ROOT_FOLDER/content/api"
SPEC_FOLDER="$ROOT_FOLDER/spec"

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
cp -r ./spec/components $ROOT_FOLDER/spec/
copy_files
