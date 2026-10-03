#!/usr/bin/env bash
set -e

# Define working directory
WORKDIR="/home/azureuser/app"
mkdir -p \$WORKDIR
cd \$WORKDIR

# 1. Write the production environment file (.env.prod) using Key Vault data
cat <<EOF > .env.prod
NODE_ENV=production
FRONTEND_URL=${frontend-url}
JWT_SECRET=${jwt-secret}
OSU_CLIENT_SECRET=${osu-client-secret}
DATABASE_URL=${database-url}
EOF

# 2. Write the Nginx proxy configuration
cat <<'EOF' > nginx.conf
events { worker_connections 1024; }
http {
    server {
        listen 80;
        server_name _;

        # Route /backend/ to the backend API container
        location /backend/ {
            proxy_pass http://backend:8000/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
        }

        # Route everything else to the frontend container
        location / {
            proxy_pass http://frontend:3000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
        }
    }
}
EOF

# 3. Write out the production Docker Compose file
cat <<'EOF' > docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend

  frontend:
    image: xenozite/osu-similarity-frontend:latest
    restart: unless-stopped
    environment:
      INTERNAL_API_URL: http://backend:8000
    depends_on:
      - backend

  backend:
    image: xenozite/osu-similarity-backend:latest
    restart: unless-stopped
    env_file: .env.prod
EOF

# 4. Pull fresh images and run the production stack
# (Since Docker is already baked into your Packer image, this works instantly)
docker compose pull
docker compose up -d
