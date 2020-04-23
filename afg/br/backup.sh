#!/bin/sh

# Exit script in case of error
set -e

echo "-----------------------------------------------------"
echo "STARTING BACKUP $(date)"
echo "-----------------------------------------------------"

if [ "$1" != "" ]; then
    BKP_FOLDER_NAME="$1"
else
    BKP_FOLDER_NAME="data/backup_restore"
fi

cd /home/geosolutions/venv/afg

./manage.sh backup -f -c afg/br/settings_afg.ini --backup-dir /$BKP_FOLDER_NAME/

BKP_FILE_LATEST=$(find /$BKP_FOLDER_NAME/*.zip -type f -exec stat -c '%Y %n' {} \; | sort -nr | awk 'NR==1,NR==1 {print $2}')
BKP_FILE_NAME=$(echo $BKP_FILE_LATEST | tail -n 1 | grep -oP -m 1 "\/$BKP_FOLDER_NAME\/\K.*" | sed 's|.zip||')

sed -i 's~$~ /'"$BKP_FOLDER_NAME"'/'"$BKP_FILE_NAME"'.zip~g' /$BKP_FOLDER_NAME/$BKP_FILE_NAME.md5

echo "-----------------------------------------------------"
cat /$BKP_FOLDER_NAME/$BKP_FILE_NAME.md5
echo "\n"
echo "-----------------------------------------------------"
