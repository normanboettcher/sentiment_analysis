#!/bin/sh

# Dynamically generate env.js file using container env variables
cat <<EOF > /usr/share/nginx/html/env.js
window.ENV = {
  VITE_MODEL_API_HOST: "${VITE_MODEL_API_HOST}",
  VITE_MODEL_API_PORT: "${VITE_MODEL_API_PORT}"
};
EOF

# Start nginx
nginx -g 'daemon off;'
