# IDCFSS Production Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying IDCFSS (Intelligent Data Cleaning & Feature Selection System) to a production environment.

## Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.9+
- Git
- 2GB+ RAM for optimal performance
- 10GB+ disk space

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### 1. Clone Repository
```bash
git clone <repository-url>
cd idcfss
```

#### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your production settings
nano .env
```

#### 3. Build & Run with Docker Compose
```bash
docker-compose build
docker-compose up -d
```

#### 4. Verify Deployment
```bash
curl http://localhost:8000/health
```

#### 5. View Logs
```bash
docker-compose logs -f idcfss-api
```

---

### Option 2: Manual Deployment (Linux/macOS)

#### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Configure Environment
```bash
cp .env.example .env
export $(cat .env | xargs)  # Load environment variables
```

#### 3. Run Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 4. Access Frontend
- Open `http://localhost:8000` in your browser

---

### Option 3: Cloud Deployment (Vercel/Heroku)

#### Vercel Deployment
1. Push code to GitHub
2. Connect repository to Vercel
3. Configure build settings:
   - Framework: None
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`
4. Deploy

#### Heroku Deployment
```bash
heroku create idcfss-app
git push heroku main
```

---

## Production Configuration

### Environment Variables (from .env.example)

| Variable | Default | Description |
|----------|---------|-------------|
| ENVIRONMENT | production | deployment environment |
| LOG_LEVEL | INFO | logging level (DEBUG, INFO, WARNING, ERROR) |
| HOST | 0.0.0.0 | server host |
| PORT | 8000 | server port |
| ALLOWED_ORIGINS | * | CORS allowed origins |
| SESSION_TIMEOUT | 3600 | session timeout (seconds) |
| MAX_SESSIONS | 100 | max concurrent sessions |
| MAX_ROWS | 100000 | max dataset rows |
| MAX_FILE_SIZE | 100 | max file size (MB) |

### Security Checklist

- [ ] Update `ALLOWED_ORIGINS` to specific domains
- [ ] Set `LOG_LEVEL` to `INFO` or `WARNING`
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Set strong `SESSION_TIMEOUT`
- [ ] Configure firewall rules
- [ ] Enable CORS selectively
- [ ] Use environment-specific credentials
- [ ] Monitor API usage and error rates

---

## Monitoring & Maintenance

### Health Check
```bash
curl http://your-domain.com/health
```

### View Logs
```bash
docker-compose logs --tail=100 idcfss-api
```

### Backup Sessions
Sessions are stored in-memory. For persistence, consider adding database support.

### Resource Cleanup
- Sessions expire after `SESSION_TIMEOUT` seconds
- Automatic cleanup of old sessions
- Monitor memory usage for long-running deployments

---

## Performance Optimization

1. **Use Nginx as Reverse Proxy**
   ```nginx
   location / {
       proxy_pass http://localhost:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

2. **Enable Gzip Compression**
   - Already enabled for streaming responses

3. **Use CDN for Frontend**
   - Static files (CSS, JS) can be cached

4. **Database Integration** (Future)
   - Add PostgreSQL for session persistence
   - Cache frequently used computations

---

## Troubleshooting

### Container won't start
```bash
docker-compose logs idcfss-api
docker-compose ps
```

### Out of memory errors
- Reduce `MAX_SESSIONS`
- Reduce `SESSION_TIMEOUT`
- Implement database persistence

### CORS errors
- Update `ALLOWED_ORIGINS` in .env
- Check browser console for details

### Slow performance
- Monitor CPU/memory usage
- Profile API endpoints
- Consider adding caching layer

---

## Scaling for Production

1. **Load Balancing**
   - Deploy multiple instances behind load balancer
   - Use Docker Swarm or Kubernetes

2. **Database Persistence**
   - Migrate from in-memory to PostgreSQL/MongoDB
   - Implement session persistence

3. **Caching Layer**
   - Add Redis for session caching
   - Cache profiler results

4. **Message Queue**
   - Use Celery + Redis for background tasks
   - Process large datasets asynchronously

---

## Support & Resources

- API Documentation: `http://your-domain.com/docs`
- GitHub Repository: [Link]
- Issues: [GitHub Issues]
- Email: support@idcfss.com
