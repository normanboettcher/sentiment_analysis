#!/bin/sh

# Dynamically generate env.js file using container env variables
cat <<EOF > /usr/share/nginx/html/env.js
window.ENV = {
  VITE_MODEL_API_URL: "${VITE_MODEL_API_URL}"
};
EOF

# Start nginx
nginx -g 'daemon off;'
