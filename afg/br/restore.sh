#! /bin/bash

echo "-----------------------------------------------------"
echo "STARTING RESTORE $(date)"
echo "-----------------------------------------------------"

if [ "$1" != "" ]; then
    BKP_FOLDER_NAME="$1"
else
    BKP_FOLDER_NAME="data/backup_restore"
fi

if [ -z "$SOURCE_URL" ] || [ -z "$TARGET_URL" ]
then
    echo "-----------------------------------------------------"
    echo "ERROR: SOURCE_URL and TARGET_URL environment variables not set"
    echo " e.g.: SOURCE_URL=https://disasterrisk.af TARGET_URL=https://stage1.disasterrisk.af"
    echo "-----------------------------------------------------"
    exit 1
else
    echo "$SOURCE_URL --> $TARGET_URL"
fi

cd /home/geosolutions/venv/afg

BKP_FILE_LATEST=$(find /$BKP_FOLDER_NAME/*.zip -type f -exec stat -c '%Y %n' {} \; | sort -nr | awk 'NR==1,NR==1 {print $2}')
BKP_FILE_NAME=$(echo $BKP_FILE_LATEST | tail -n 1 | grep -oP -m 1 "\/$BKP_FOLDER_NAME\/\K.*" | sed 's|.zip||')

if md5sum -c /$BKP_FOLDER_NAME/$BKP_FILE_NAME.md5; then
    # The MD5 sum matched
    ./manage.sh restore -f --backup-file /$BKP_FOLDER_NAME/$BKP_FILE_NAME.zip
    if [ "$?" != 0 ]
    then
        echo "-----------------------------------------------------"
        echo "ERROR: Could not successfully restore file /$BKP_FOLDER_NAME/$BKP_FILE_NAME.zip"
        echo "-----------------------------------------------------"
        exit 1
    else
        ./manage.sh migrate_baseurl -f --source-address=$SOURCE_URL --target-address=$TARGET_URL
        ./manage.sh set_all_layers_metadata -d -i
    fi
else
    # The MD5 sum didn't match
    echo "-----------------------------------------------------"
    echo "ERROR: The MD5 sum didn't match"
    echo "-----------------------------------------------------"
    exit 1
fi

echo "-----------------------------------------------------"
echo "FINISHED RESTORE $(date)"
echo "-----------------------------------------------------"
