# Application Startup Guide

This document provides comprehensive instructions on how to start, run, and stop the **not-another-list-app** application using Docker Compose.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Services Overview](#services-overview)
- [Starting the Application](#starting-the-application)
- [Verifying the Application](#verifying-the-application)
- [Accessing the Application](#accessing-the-application)
- [Running Tests](#running-tests)
- [Stopping the Application](#stopping-the-application)
- [Viewing Logs](#viewing-logs)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)

## Prerequisites

Before you can run this application, ensure you have the following installed on your macOS system:

- **Docker Desktop** (includes Docker Engine and Docker Compose)
  - Download from: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
  - Verify installation: `docker --version` and `docker-compose --version`

## Quick Start

For the impatient developer, here's the one-liner to build and start everything:

```bash
docker-compose up --build -d natl_backend_api db frontend
```

Then verify all services are running:

```bash
docker-compose ps
```

Open your browser to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8081

## Services Overview

The application consists of four main services defined in `docker-compose.yml`:

| Service | Port | Description | Dependencies |
|---------|------|-------------|--------------|
| `natl_backend_api` | 8081 | Python FastAPI backend | `db` |
| `db` | 3306 | MySQL database | None |
| `frontend` | 3000 | React web interface | None |
| `test` | N/A | Test runner container | `db`, `natl_backend_api` |

**Environment Configuration:**
- Backend deployment mode: `compose` (set automatically via `docker-compose.yml`)
- MySQL root password: `developer`
- Test API URL: `http://natl_backend_api:8081/api`

## Starting the Application

### Option 1: Build and Start Everything (Recommended)

This builds all images and starts the backend, database, and frontend services in the background:

```bash
docker-compose up --build -d natl_backend_api db frontend
```

**What this does:**
- Rebuilds all service images from their Dockerfiles
- Starts the MySQL database (`db`)
- Waits for DB to be ready (depends_on)
- Starts the backend API (`natl_backend_api`)
- Starts the frontend (`frontend`)
- Runs all services in detached mode (`-d`)

### Option 2: Start Without Rebuilding

If images are already built, start faster without rebuilding:

```bash
docker-compose up -d natl_backend_api db frontend
```

### Option 3: Start and Follow Logs in Terminal

To start services and watch logs in real-time (useful for debugging):

```bash
docker-compose up natl_backend_api db frontend
```

Press `Ctrl+C` to stop (services keep running; use `docker-compose down` to stop them).

### Option 4: Build Only (Without Starting)

To just build images without starting services:

```bash
docker-compose build --parallel
```

## Verifying the Application

After starting, verify all services are running and healthy:

```bash
# List running containers and their status
docker-compose ps

# Expected output (or similar):
# NAME                 COMMAND                  SERVICE             STATUS              PORTS
# natl_backend_api     "python -m uvicorn..." natl_backend_api    Up (healthy)        0.0.0.0:8081->8081/tcp
# db                   "docker-entrypoint..."  db                 Up (healthy)        0.0.0.0:3306->3306/tcp
# frontend             "npm start"             frontend           Up                  0.0.0.0:3000->3000/tcp
```

### Health Checks

- **Backend API health**: `curl http://localhost:8081/api` or visit in browser
- **Database connection**: Check backend logs for successful DB connection
- **Frontend**: Should load without 404 errors at http://localhost:3000

## Accessing the Application

Once all services are running:

### Frontend (Web UI)
- **URL**: http://localhost:3000
- Access the React application and interact with the list/task management interface

### Backend API
- **Base URL**: http://localhost:8081
- **API Endpoints**: http://localhost:8081/api
- Check available endpoints and documentation via FastAPI docs (if enabled)

### Database (MySQL)
- **Host**: `localhost` (when accessing from your machine)
- **Port**: `3306`
- **Root Username**: `root`
- **Root Password**: `developer`

Connect via MySQL client:
```bash
mysql -h localhost -u root -p
# Enter password: developer
```

Or use a GUI tool like MySQL Workbench or TablePlus pointing to `localhost:3306`.

## Running Tests

### Run Tests (Full Suite)

To run the complete test suite inside the test container:

```bash
docker-compose run --rm test
```

**What this does:**
- Builds the test image if not already built
- Runs the test container with access to the running backend and database
- Automatically removes the container after tests complete (`--rm`)
- Returns the container's exit code (0 = pass, non-zero = fail)

### Run Tests and Keep Container Running

If you want to inspect the test container or see full output:

```bash
docker-compose up --build test
```

Then stop with:
```bash
docker-compose stop test
```

### Run Tests with Specific Output

For verbose test output:

```bash
docker-compose run --rm test python -m pytest -v
```

(Adjust the command based on your test framework; check `tests/Dockerfile` for details.)

## Stopping the Application

### Stop All Services (Keep Containers)

Stops running containers but preserves them:

```bash
docker-compose stop
```

You can restart with `docker-compose start`.

### Stop and Remove All Containers

Stops and removes containers, networks, and volumes (more thorough cleanup):

```bash
docker-compose down
```

### Stop and Remove Everything Including Volumes

**Use with caution** — this deletes database data:

```bash
docker-compose down -v
```

Use this when you want a completely fresh start.

### Stop a Single Service

Stop just one service while keeping others running:

```bash
docker-compose stop natl_backend_api
```

Restart it:
```bash
docker-compose start natl_backend_api
```

## Viewing Logs

### View All Logs

Show logs from all services:

```bash
docker-compose logs
```

### Follow Logs (Real-Time)

Watch logs as they're generated (useful for debugging):

```bash
docker-compose logs -f
```

### View Logs for a Specific Service

Watch just the backend logs:

```bash
docker-compose logs -f natl_backend_api
```

Other services: `db`, `frontend`, `test`

### View Last N Lines

Show only the last 50 lines:

```bash
docker-compose logs --tail=50
```

### View Logs from a Specific Time Period

Logs since 5 minutes ago:

```bash
docker-compose logs --since 5m
```

## Troubleshooting

### Issue: "Docker daemon is not running"

**Solution**: Start Docker Desktop and wait for it to be ready.

```bash
# Verify Docker is running
docker ps
```

### Issue: "Port already in use (e.g., 3000 or 8081)"

**Cause**: Another application is using the port.

**Solution**: Either stop the other application or change the port in `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Host port 3001 → Container port 3000
```

Then rebuild and restart:
```bash
docker-compose up --build -d
```

### Issue: Backend can't connect to database

**Cause**: Database container not fully initialized, or backend started before DB was ready.

**Solution**: Check database logs and wait a moment:

```bash
docker-compose logs -f db
# Wait 5-10 seconds for MySQL to initialize
docker-compose restart natl_backend_api
```

### Issue: Frontend shows "Cannot connect to API"

**Cause**: Backend container not running or API endpoint incorrect.

**Solution**: 
1. Verify backend is running: `docker-compose ps natl_backend_api`
2. Check backend logs: `docker-compose logs -f natl_backend_api`
3. Verify frontend is using correct API URL (check React code in `natl-frontend/src/config/`)

### Issue: Database persistence not working (data lost after restart)

**Cause**: Docker volumes not properly configured or removed.

**Solution**: Ensure you use `docker-compose stop` instead of `docker-compose down -v`. If data is already lost:

```bash
# Start fresh (warning: deletes data)
docker-compose down -v
docker-compose up --build -d natl_backend_api db frontend
```

### Issue: "Cannot read property 'X' of undefined" in frontend

**Cause**: API not returning expected data structure.

**Solution**: 
1. Verify backend is running: `docker-compose ps`
2. Check backend logs for errors: `docker-compose logs -f natl_backend_api`
3. Test API manually: `curl http://localhost:8081/api`

### Issue: Container keeps restarting or exiting

**Cause**: Application error or health check failure.

**Solution**: Check logs immediately after restart:

```bash
docker-compose logs --tail=100 natl_backend_api
```

Look for stack traces or error messages. Common issues:
- Missing environment variables
- Database connection timeout
- Port binding conflicts

## Development Workflow

### Typical Local Development Session

1. **Start the app:**
   ```bash
   docker-compose up --build -d natl_backend_api db frontend
   ```

2. **Verify it's running:**
   ```bash
   docker-compose ps
   ```

3. **Access in browser:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8081

4. **Watch logs while testing:**
   ```bash
   docker-compose logs -f natl_backend_api
   ```

5. **Run tests:**
   ```bash
   docker-compose run --rm test
   ```

6. **Stop when done:**
   ```bash
   docker-compose down
   ```

### Making Changes and Rebuilding

**If you modify backend code:**
```bash
docker-compose up --build -d natl_backend_api
```

**If you modify frontend code:**
```bash
docker-compose up --build -d frontend
```

**If you modify database schema:**
```bash
docker-compose down -v
docker-compose up --build -d natl_backend_api db frontend
```

**If you modify tests:**
```bash
docker-compose run --rm test
```

### Hot Reload / Development Mode

Check if services support hot reload by examining their Dockerfiles:
- **Backend** (`backend/Dockerfile`): May use `--reload` flag in uvicorn
- **Frontend** (`natl-frontend/Dockerfile`): React typically watches for changes
- If hot reload is configured, changes to source files may automatically reload without rebuild

If hot reload is not working, rebuild the affected service.

## Additional Resources

- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **Backend Repository**: `backend/` folder
- **Frontend Repository**: `natl-frontend/` folder
- **Tests**: `tests/` folder
- **CI/CD Pipeline**: `.github/workflows/ci.yml`

## Notes

- All services run in the same Docker network, allowing inter-service communication via service names (e.g., `natl_backend_api:8081`).
- Database credentials are hardcoded in `docker-compose.yml` for development; do not use in production.
- Volumes are automatically created and managed by Docker Compose; they persist between container restarts unless explicitly removed.
- The frontend and backend are built independently; ensure both are running for the full application to function.
