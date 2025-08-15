# Docker Setup for AgriSaarthi

This document explains how to run the AgriSaarthi FastAPI service using Docker.

## Prerequisites

- Docker and Docker Compose installed
- Environment variables configured (see `env.example`)

## Quick Start

### 1. Set up environment variables

Copy the example environment file and fill in your API keys:

```bash
cp env.example .env
# Edit .env with your actual API keys
```

Required environment variables:

- `GOOGLE_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: Your Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Your Qdrant Cloud API key
- `TAVILY_API_KEY`: Your Tavily Search API key

### 2. Run the service

#### Development mode (with hot reload):

```bash
docker-compose --profile dev up --build
```

#### Production mode:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

#### Basic mode (just the API):

```bash
docker-compose up --build
```

## Docker Compose Files

- **`docker-compose.yml`**: Base configuration for the API service
- **`docker-compose.override.yml`**: Development overrides (hot reload, volume mounts)
- **`docker-compose.prod.yml`**: Production configuration with nginx reverse proxy

## Services

### AgriSaarthi API (`agrisathi-api`)

- **Port**: 8000
- **Health Check**: `/` endpoint
- **Features**: FastAPI service with MCP server

## Development Workflow

1. **Start development environment**:

   ```bash
   docker-compose --profile dev up --build
   ```

2. **Make code changes** - they will automatically reload

3. **View logs**:

   ```bash
   docker-compose logs -f agrisathi-api
   ```

4. **Stop services**:
   ```bash
   docker-compose down
   ```

## Production Deployment

1. **Deploy the service**:

   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

2. **Monitor health**:
   ```bash
   docker-compose ps
   curl http://localhost:8000/
   ```

## Docker Commands

### Build images

```bash
docker-compose build
```

### View running containers

```bash
docker-compose ps
```

### View logs

```bash
docker-compose logs -f [service-name]
```

### Execute commands in container

```bash
docker-compose exec agrisathi-api bash
```

### Clean up

```bash
docker-compose down -v --remove-orphans
docker system prune -f
```

## Troubleshooting

### Common Issues

1. **Port already in use**:

   ```bash
   # Check what's using port 8000
   lsof -i :8000
   # Kill the process or change port in docker-compose.yml
   ```

2. **Environment variables not loaded**:

   - Ensure `.env` file exists and has correct format
   - Check variable names match those in `docker-compose.yml`

3. **Build failures**:

   ```bash
   # Clean build cache
   docker-compose build --no-cache
   ```

4. **Permission issues**:
   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER ./volumes
   ```

### Health Checks

The service includes health checks that can be monitored:

```bash
# Check container health
docker inspect agrisathi-api | grep Health -A 10

# Test API endpoint
curl http://localhost:8000/
```

## Performance Tuning

### For Production

1. **Resource limits** - Add to docker-compose.yml:

   ```yaml
   deploy:
     resources:
       limits:
         memory: 2G
         cpus: "1.0"
   ```

2. **Volume optimization** - Use named volumes for persistent data

### For Development

1. **Hot reload** - Already configured in `docker-compose.override.yml`
2. **Volume mounts** - Source code changes reflect immediately
3. **Debug mode** - Add `PYTHONUNBUFFERED=1` for better logging

## Security Considerations

- Non-root user in containers
- Environment variables for sensitive data
- Rate limiting in nginx
- Health checks for monitoring
- Network isolation with custom bridge network

## Monitoring

### Logs

```bash
# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs -f agrisathi-api
```

### Metrics

- Health check endpoint: `/health`
- API status: `/`
- Container metrics: `docker stats`

## Backup and Recovery

### Data persistence

```bash
# Backup volumes
docker run --rm -v agrisathi_agrisathi-data:/data -v $(pwd):/backup alpine tar czf /backup/agrisathi-data.tar.gz -C /data .

# Restore volumes
docker run --rm -v agrisathi_agrisathi-data:/data -v $(pwd):/backup alpine tar xzf /backup/agrisathi-data.tar.gz -C /data
```

### Configuration backup

```bash
# Backup configuration files
tar czf config-backup.tar.gz docker-compose*.yml .env
```
