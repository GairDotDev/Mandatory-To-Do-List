#!/bin/bash

# Simple script to run the todo app locally

set -e

echo "🚀 Starting Todo App..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

# Use docker compose (newer) or docker-compose (older)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "📦 Building and starting services..."
$DOCKER_COMPOSE up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if services are healthy
echo "🔍 Checking service health..."

# Check API health
if curl -f http://localhost:8080/healthz > /dev/null 2>&1; then
    echo "✅ API is healthy"
else
    echo "⚠️  API health check failed (may still be starting)"
fi

# Check Frontend
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️  Frontend health check failed (may still be starting)"
fi

echo ""
echo "🎉 Todo App is starting!"
echo ""
echo "📍 Services:"
echo "   - Frontend: http://localhost:3001"
echo "   - API: http://localhost:8080"
echo "   - API Health: http://localhost:8080/healthz"
echo "   - API Readiness: http://localhost:8080/readyz"
echo ""
echo "📝 To view logs:"
echo "   $DOCKER_COMPOSE logs -f"
echo ""
echo "🛑 To stop:"
echo "   $DOCKER_COMPOSE down"
echo ""

