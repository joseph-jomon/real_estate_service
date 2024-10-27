If `os.makedirs(company_folder, exist_ok=True)` is causing a permission error, it likely means that the process lacks write permissions to create the directory specified by `company_folder` on the host.

Here’s how to troubleshoot and resolve it:

1. **Verify Host Directory Permissions**:
   Ensure the parent directory (`settings.DATA_OUTPUT_FOLDER`) on the host machine has the appropriate permissions. Run the following command on your host:
   ```bash
   sudo chmod -R 777 <path_to_data_output_folder>
   ```
   Replace `<path_to_data_output_folder>` with the actual path where `settings.DATA_OUTPUT_FOLDER` points. This command grants full read, write, and execute permissions, which is helpful for diagnosing permission issues.

2. **Confirm User Ownership on the Host**:
   Since the Docker container runs as the `appuser` with UID `10001`, ensure that the directory has permissions for this user:
   ```bash
   sudo chown -R 10001:10001 <path_to_data_output_folder>
   ```
   This command ensures that the container user (`appuser`) has ownership of the directory on the host.

3. **Check Docker Volumes**:
   If you’re using Docker volumes or bind mounts, permissions on the host are crucial. Make sure the folder exists on the host and has the correct permissions before starting the container, as Docker won't automatically create directories outside the container.

4. **Testing with Root User** (optional):
   You can also test by switching to the root user in your `docker-compose.yml` to see if this resolves the error:
   ```yaml
   user: root
   ```
   If it works with root, then the issue is likely permission-related for the non-root `appuser`.

5. **Check Logs for Exact Error**:
   Run `docker logs -f real_estate_app` to get more information about the permission error, which may provide additional insights into which directory specifically is causing the issue.