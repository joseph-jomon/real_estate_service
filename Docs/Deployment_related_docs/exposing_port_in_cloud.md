You're correct in thinking that your FastAPI service is currently running on port 8000, while most web traffic to a server (like your DigitalOcean droplet) expects to connect via port 80 by default.

To access your FastAPI service using `http://domainname` (which would attempt to connect via port 80), you have a couple of simple options without adding a reverse proxy like Traefik:

### Option 1: Map Docker Port 8000 to Port 80
In your `docker-compose.yml` file, you can modify the port mapping for your FastAPI service to bind port 80 on the host machine (the droplet) to port 8000 inside the container. This way, incoming traffic to `http://domainname` (which defaults to port 80) will be forwarded to your FastAPI service running on port 8000.

Modify the `ports` section for your `fastapi_service_batch_processing` to:

```yaml
  fastapi_service_batch_processing:
    build:
      context: .  # Set the build context to the parent directory
      dockerfile: fastapi_service/Dockerfile  # Specify the Dockerfile location
    volumes:
      - ./myapp:/myapp  # Mount the myapp directory to /myapp in the container
    ports:
      - "80:8000"  # Map port 80 on the host to port 8000 in the container
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1  # Ensure Python output is flushed and displayed in real-time
      - WORKERS=4  # Number of Gunicorn workers
    command: ["gunicorn", "myapp.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

With this change, traffic sent to `http://domainname` will be forwarded to your FastAPI app on port 8000 within the container, making it accessible without needing to specify port 8000 in the URL.

### Option 2: Change Gunicorn Binding to Port 80
Alternatively, you could change the Gunicorn binding directly to port 80. However, this may require running your container as root, which is generally not recommended for security reasons. Stick to the first option for simplicity and security.

### Option 3: Use `iptables` to Forward Traffic
If you don't want to modify the Docker Compose file, you could also use `iptables` on the host to forward traffic from port 80 to port 8000. This would involve running the following command on the host machine (your droplet):

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
```

This approach doesn't require any changes to your `docker-compose.yml` but would require root access on the droplet and isn't as portable as modifying the Compose file.

### Conclusion:
The simplest and most efficient approach would be **Option 1**—modifying the port mapping in your `docker-compose.yml` file to map port 80 on the host to port 8000 in the container. This way, you won't need any additional software or services.