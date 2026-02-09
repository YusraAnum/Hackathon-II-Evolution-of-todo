# Use official Node runtime as base image
FROM node:18-alpine AS builder

# Set working directory in the container
WORKDIR /app

# Copy package files
COPY phase-3/frontend_todo_app/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application code
COPY phase-3/frontend_todo_app/ .

# Build the Next.js application
RUN npm run build

# Production stage
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY phase-3/frontend_todo_app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy the built application from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./next.config.js
COPY --from=builder /app/node_modules ./node_modules

# Expose port 3000
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]