cd ../v2
API_KEY="xxx"
TUPLES=(
"mist.openapi.authentication.yml:64f1b7559486b90f72e7ff61"
"mist.openapi.self.yml:64f205c97abb41004c7b9770"
"mist.openapi.configuration.msps.yml:64f1b784c6ef6405f85e08f0"
"mist.openapi.configuration.orgs.yml:64f1b7b2b1ffa8006806a4ac"
"mist.openapi.configuration.sites.yml:64f1b7eed96e550030c432c0"
"mist.openapi.monitor.msps.yml:64f1b86bbbe2e30fe7f6b43a"
"mist.openapi.constants.yml:64f1b8346a8126006f8bc478"
"mist.openapi.monitor.orgs.yml:64f1b88e121282116e61d350"
"mist.openapi.monitor.sites.yml:64f1b8f0e48bd10076ac1874"
"mist.openapi.installer.yml:64f1b853c87585002ac7983c"
"mist.openapi.webhook.yml:64f1b953fe07ee004338c17b"
)


for i in ${TUPLES[@]}
do
    FILE=`echo $i | cut -d":" -f1`
    ID=`echo $i | cut -d":" -f2`
    echo " -- $FILE -- $ID --"
    rdme openapi \
    --key=$API_KEY \
    --id=$ID $FILE
done


