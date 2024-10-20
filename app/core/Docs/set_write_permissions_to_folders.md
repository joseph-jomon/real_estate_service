If you're running the application inside Docker or on a server, it's possible that the user or process running the application does not have permission to write to the specified directory. Here's how to address and handle permission issues:

### 1. **Check and Set File System Permissions (Linux-based Systems)**

In most cases, if your application is running in a container or server, the user that runs the process (e.g., `appuser` in Docker) needs to have write permissions to the directory where you're trying to save files.

To check and set file permissions, you can use the following commands:

#### **Check Permissions of the Directory**:
Run this command on the host machine or in the Docker container to check the permissions of the directory:

```bash
ls -ld /path/to/directory
```

This will display the permissions in a format like:

```bash
drwxr-xr-x  2 appuser appuser 4096 Oct 12 12:34 directory
```

Make sure that the directory is writable by the user running the application.

#### **Set Write Permissions**:

You can set write permissions for the directory using `chmod`:

```bash
chmod -R 755 /path/to/directory
```

- `755` gives read and execute permissions to everyone, but only the owner (user running the application) can write.

You can also change ownership of the directory to the user running the application with `chown`:

```bash
chown -R appuser:appuser /path/to/directory
```

Replace `appuser` with the actual user running your application.

### 2. **Docker Permissions**

If you’re using Docker, permissions can sometimes be tricky due to differences between the host and the container. Here's what you should do:

#### **Step 1: Set the Correct User in Dockerfile**:
In your Dockerfile, ensure that you're using a non-root user (which you've already done) and that this user has permissions to write to the directories you're mounting.

For example, in your Dockerfile, you've created a user `appuser`:

```dockerfile
# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create the home directory and give ownership to appuser
RUN mkdir -p /home/appuser && chown appuser:appuser /home/appuser

# Set the working directory
WORKDIR /app

# Switch to non-privileged user
USER appuser
```

#### **Step 2: Ensure the Volumes Have Correct Permissions**:
When mounting volumes in your `docker-compose.yml`, ensure that the directories are writable by `appuser`.

Here’s an example:

```yaml
volumes:
  - ./data:/app/data
```

The `./data` directory on the host machine should have appropriate permissions. You can ensure this by running the following on your host machine:

```bash
chmod -R 755 ./data
chown -R your_host_user:your_host_user ./data
```

#### **Step 3: Verify Permissions Inside the Container**:
You can check the permissions inside the running Docker container by attaching to it and checking the directories:

```bash
docker exec -it real_estate_app_debug bash
ls -ld /app/data
```

If you see permission issues, you can use `chmod` and `chown` inside the container as well.

### 3. **Run Permissions Debugging**:
You can temporarily log the user and permissions inside the application for debugging purposes. Add this to your FastAPI app (or any script):

```python
import os

# Print current user running the app
print("Current User:", os.geteuid(), os.getlogin())

# Check permissions of the target directory
directory = './data'
print(f"Directory Permissions: {os.stat(directory)}")
```

This will log the user ID and directory permissions when the app runs.

### 4. **Example of Full Setup**:

#### `Dockerfile` (Permission Setup):
```dockerfile
# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create a data directory and ensure it has the right permissions
RUN mkdir -p /app/data && chown appuser:appuser /app/data

# Switch to non-privileged user
USER appuser

# Set working directory
WORKDIR /app
```

#### `docker-compose.yml`:
```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: real_estate_app
    volumes:
      - ./data:/app/data  # Ensure this directory exists on your host and has correct permissions
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://your_db_user:your_db_password@db/your_db_name
```

### Conclusion:
- **Check directory permissions**: Ensure the directory you're trying to write to has proper write permissions.
- **Docker setup**: Make sure your Docker user (`appuser`) has permissions to write to mounted volumes.
- **Test and log permissions**: If needed, log the user and directory permissions in your application to further debug the issue.

This should help you resolve any permission issues when writing to the filesystem. Let me know if you need further assistance!