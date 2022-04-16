#!/bin/sh

ROOT_DIR=/usr/share/nginx/html

# Replace env vars in JavaScript files
echo "Replacing env constants in JS"

for file in $ROOT_DIR/js/*.js* $ROOT_DIR/index.html;
do
  echo "Processing $file ...";

  sed -i 's|VUE_APP_NLU_SERVICE_URL_VALUE|'${VUE_APP_NLU_SERVICE_URL}'|g' $file 
  sed -i 's|VUE_APP_NLU_PATH_VALUE|'${VUE_APP_NLU_PATH}'|g' $file
  sed -i 's|VUE_APP_NLU_ENTRIES_PAGE_SIZE_VALUE|'${VUE_APP_NLU_ENTRIES_PAGE_SIZE}'|g' $file
  sed -i 's|PUBLIC_PATH_VALUE|'${PUBLIC_PATH}'|g' $file

done
echo "Starting Nginx"
nginx -g 'daemon off;'