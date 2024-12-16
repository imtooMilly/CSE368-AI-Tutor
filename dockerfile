# Stage 1: Build React app
FROM node:16 AS build

# Set the working directory for the React app
WORKDIR /app/client

# Install dependencies
COPY client/package.json client/package-lock.json ./
RUN npm install

# Build the React app
COPY client/ ./
RUN npm run build

# Stage 2: Set up Flask backend and serve the React app
FROM python:3.10-slim

# Set the working directory for the Flask app
WORKDIR /app

# Install dependencies for the Flask app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy the backend app code
COPY backend/ ./

# Copy the React build from the build stage
COPY --from=build /app/client/build /app/client/build

# Expose Flask app port
EXPOSE 5000

# Start the Flask app (assuming app.py is the entry point for Flask)
CMD ["python", "app.py"]