The error you're encountering indicates that your FastAPI app is trying to connect to PostgreSQL at `127.0.0.1:5432` instead of the expected service name `db` inside the Docker Compose network. This is likely because the **`DATABASE_URL`** is incorrectly set to connect to `localhost` (`127.0.0.1`) rather than using the correct Docker Compose service name (`db`).

### Core Problem:
In your **`DATABASE_URL`**, you have **`localhost`** (`127.0.0.1`), but in a Docker Compose setup, the FastAPI container cannot reach PostgreSQL using `localhost` because **each service runs in its own isolated container**. You need to use the service name `db` (as defined in your `docker-compose.yml`) for PostgreSQL to be accessible from the FastAPI container.

### Solution:

1. **Update the `DATABASE_URL`** in your `docker-compose.yml` file to use the correct host `db`, not `localhost`. Since Docker Compose provides network isolation, services refer to each other by their service names, not `localhost`.

2. **Correct `DATABASE_URL`**:
   Update your `docker-compose.yml` environment variables to point to the **`db`** service for PostgreSQL:

```yaml
services:
  web:
    environment:
      - DATABASE_URL=postgresql+asyncpg://your_db_user:your_db_password@db/your_db_name
```

Here, the hostname `db` will point to the PostgreSQL service running in your Docker Compose network.

### Example of Correct `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: ./Dockerfile
    container_name: real_estate_app_debug
    command: [ "./scripts/wait-for-it.sh", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app", "--log-level", "debug" ]
    ports:
      - "8000:8000"
      - "5678:5678" # Debugger port for IDE
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql+asyncpg://your_db_user:your_db_password@db/your_db_name
    volumes:
      - ./data/images:/app/data/images
    networks:
      - real_estate_net

  db:
    image: postgres:14
    container_name: real_estate_db_debug
    environment:
      POSTGRES_USER: your_db_user
      POSTGRES_PASSWORD: your_db_password
      POSTGRES_DB: your_db_name
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - real_estate_net

volumes:
  postgres_data:

networks:
  real_estate_net:
```

### Why This Works:
- The `db` service in Docker Compose is available under the hostname **`db`** inside the Docker Compose network. So, FastAPI will connect to `db:5432` instead of `localhost:5432`.
- **`localhost`** inside the **`web`** container only refers to the FastAPI container itself, not the PostgreSQL container. Using the service name `db` allows FastAPI to reach PostgreSQL.

### Next Steps:
1. **Update `DATABASE_URL`** as shown above.
2. **Rebuild and restart the containers**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

This should resolve the issue by ensuring that FastAPI connects to PostgreSQL using the correct service name within the Docker Compose network.

Let me know how it goes or if you have further questions!