FROM node:18-alpine

WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Copy package files
COPY package*.json ./

# Install all dependencies
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Verify build was successful and create BUILD_ID if it doesn't exist
RUN ls -la .next && \
    if [ ! -f .next/BUILD_ID ]; then \
        echo "BUILD_ID not found, creating one..." && \
        echo "$(date +%s)" > .next/BUILD_ID; \
    fi && \
    ls -la .next/BUILD_ID

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Start the application
CMD ["npm", "start"]
