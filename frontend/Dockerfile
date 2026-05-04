# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy manifests first for layer caching
COPY package.json ./

# Install with legacy peer deps; then force-hoist ajv@8 so react-scripts
# webpack chain resolves it correctly on Node 20
RUN npm install --legacy-peer-deps && \
    npm install --save-dev ajv@^8.17.1 --legacy-peer-deps

COPY . .

ARG REACT_APP_API_URL=http://localhost:8000
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.25-alpine

# Copy built assets
COPY --from=builder /app/build /usr/share/nginx/html

# Nginx config with SPA routing and CORS proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -qO- http://localhost:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
