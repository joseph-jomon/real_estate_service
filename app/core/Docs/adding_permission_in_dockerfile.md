Yes, that's correct! These two lines should be part of your Dockerfile. They ensure that both `/home/appuser` and `/app/data` directories are created and their ownership is set to `appuser`, which is your non-root user.

Here’s how they fit into your Dockerfile:

### Updated Dockerfile Snippet:

```dockerfile
# Create a non-privileged user to run the application
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create home directory and give ownership to appuser
RUN mkdir -p /home/appuser && chown appuser:appuser /home/appuser

# Create the /app/data directory and give ownership to appuser
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Switch to non-privileged user
USER appuser

# Set working directory
WORKDIR /app
```

### What These Commands Do:

1. **Create `/home/appuser`**:
   - `mkdir -p /home/appuser`: Creates the home directory for `appuser`.
   - `chown appuser:appuser /home/appuser`: Changes ownership of this directory to `appuser`.

2. **Create `/app/data`**:
   - `mkdir -p /app/data`: Creates the `/app/data` directory if it doesn't already exist.
   - `chown -R appuser:appuser /app/data`: Recursively changes the ownership of `/app/data` and all its contents to `appuser`. The `-R` flag ensures that the ownership applies to all files and subdirectories within `/app/data`.

### Recap:
- These two lines ensure that both `/home/appuser` and `/app/data` have the correct ownership (`appuser`), allowing your application to write to the `/app/data` directory.
- After making these changes, rebuild your Docker image and restart the container.

Let me know if you need further assistance!