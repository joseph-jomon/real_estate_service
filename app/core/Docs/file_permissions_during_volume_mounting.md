No, you **don’t need** to manually adjust the permissions on the local host if you’ve correctly set the permissions inside the **Dockerfile**. Here's why:

When you run your application in Docker, the **container** operates in an isolated environment. The permissions you set in the Dockerfile are applied within the container, and they don’t affect the permissions on your host machine.

However, there are a few situations where you might need to ensure correct permissions on the local host:

### 1. **If You’re Mounting a Volume from the Local Host**
   - If you're **mounting** a directory from your host machine into the container (e.g., mounting `./data` from the local host to `/app/data` inside the container), the container uses the permissions from the **local host**.
   - In this case, if the local directory (`./data`) doesn’t have the correct permissions, you’ll face issues inside the container as well.

   Example:
   ```yaml
   volumes:
     - ./data:/app/data
   ```

   **If this is the case, you do need to adjust the permissions on the local directory**. For instance, you can run:

   ```bash
   chmod -R 755 ./data
   ```

   This ensures that the `./data` directory on your local machine is writable by Docker when it's mounted into the container.

### 2. **No Volume Mounting (All Inside the Container)**
   - If you **don’t mount** any local directories (i.e., no `volumes:` directive in `docker-compose.yml`), the changes in your Dockerfile ensure that the permissions inside the container are set correctly. In this case, no changes on the local host are necessary because the filesystem inside the container is isolated.

### Summary:

- **If you’re mounting a directory from the local host to the container** (with Docker volumes), you’ll need to ensure that the local host directory has the proper write permissions. Otherwise, the container may inherit the local host's restrictive permissions.
- **If you’re not mounting a directory from the local host** and everything is inside the container, you don’t need to make any changes to the local host.

Let me know if you're using volume mounts and I can help adjust the permissions accordingly!