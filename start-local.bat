@echo off
REM Simple script to run the todo app locally on Windows

echo Starting Todo App...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if Docker Compose is available
docker compose version >nul 2>&1
if errorlevel 1 (
    docker-compose version >nul 2>&1
    if errorlevel 1 (
        echo Docker Compose is not installed. Please install Docker Compose.
        exit /b 1
    )
    set DOCKER_COMPOSE=docker-compose
) else (
    set DOCKER_COMPOSE=docker compose
)

echo Building and starting services...
%DOCKER_COMPOSE% up --build -d

echo Waiting for services to be ready...
timeout /t 5 /nobreak >nul

echo Checking service health...

REM Check API health
curl -f http://localhost:8080/healthz >nul 2>&1
if errorlevel 1 (
    echo API health check failed (may still be starting)
) else (
    echo API is healthy
)

REM Check Frontend
curl -f http://localhost:3001 >nul 2>&1
if errorlevel 1 (
    echo Frontend health check failed (may still be starting)
) else (
    echo Frontend is healthy
)

echo.
echo Todo App is starting!
echo.
echo Services:
echo    - Frontend: http://localhost:3001
echo    - API: http://localhost:8080
echo    - API Health: http://localhost:8080/healthz
echo    - API Readiness: http://localhost:8080/readyz
echo.
echo To view logs:
echo    %DOCKER_COMPOSE% logs -f
echo.
echo To stop:
echo    %DOCKER_COMPOSE% down
echo.

