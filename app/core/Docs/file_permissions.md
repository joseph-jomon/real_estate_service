The error `[Errno 13] Permission denied: './data'` indicates that the user or process running your code does not have sufficient permissions to create or write to the `./data` directory.

### Solution: Fix the Permission Issue

Since this error is happening with the `./data` directory, the permissions for this folder must be adjusted. Here’s how you can resolve the issue:

### Step 1: Check Directory Permissions
Run this command on the **host machine** to check the current permissions of the `./data` directory (if it exists):

```bash
ls -ld ./data
```

This will display something like:

```bash
drwxr-xr-x  2 your_host_user your_host_user 4096 Oct 12 12:34 data
```

Make sure the user running the application (in Docker or on the host) has **write** access to this directory.

### Step 2: Change Directory Permissions
To fix the permissions and allow your process (or Docker container) to write to the directory, run the following command:

```bash
sudo chmod -R 755 ./data
```

- **755** allows the owner to read, write, and execute. Others can read and execute, but not write.

Alternatively, if you are running in a Docker container or in a multi-user environment, you may need to **change the ownership** of the directory to match the user running your code:

```bash
sudo chown -R your_host_user:your_host_user ./data
```

Replace `your_host_user` with the user running the process or Docker container.

### Step 3: Ensure Correct Docker Setup (if using Docker)
If you're running the application inside a Docker container and mounting the `./data` directory, make sure the `appuser` inside Docker has the correct permissions to access and write to this directory.

- Check if the `appuser` has ownership or proper permissions inside the container:

```bash
docker exec -it <container_name> bash
ls -ld /app/data
```

If needed, inside the container, you can set the permissions:

```bash
chmod -R 755 /app/data
```

### Step 4: Create Directory if It Doesn’t Exist
Make sure the `data` directory exists before trying to write to it:

```python
if not os.path.exists('./data'):
    os.makedirs('./data', exist_ok=True)
```

This will create the directory if it doesn't exist and ensure it has the right permissions.

### Recap:

1. **Check permissions** of the `./data` directory on the host machine.
2. **Set the correct permissions** using `chmod` or change the ownership with `chown`.
3. If using **Docker**, ensure the user inside the container has write permissions to the mounted `data` directory.
4. Use `os.makedirs()` to create the directory if it doesn’t exist.

After following these steps, the permission issue should be resolved, and your app should be able to write to `./data/text/final_dataset.csv`.