The output `drwxr-xr-x 4 root root 4096 Oct 27 16:12 ./data` indicates that the `./data` directory is currently owned by the `root` user and group, with permissions set to `755`. This means that:

- The **owner** (root) has read, write, and execute permissions.
- The **group** (also root) and **others** have only read and execute permissions, but no write permission.

Since your container runs with the non-root `appuser` (UID `10001`), it doesn’t have write access to the `./data` folder, which is likely causing the permission error.

### To Fix This

1. **Change Ownership to `appuser` UID**:
   Assign ownership of the `./data` folder to the UID `10001` (the `appuser` in your container) so it can write to the folder:
   ```bash
   sudo chown -R 10001:10001 ./data
   ```

2. **Verify Permissions After Changing Ownership**:
   After running the `chown` command, check permissions again:
   ```bash
   ls -ld ./data
   ```
   You should now see `10001 10001` as the owner and group, allowing the container's `appuser` to access and modify the `./data` directory.

This should resolve the permissions error when your application tries to create directories within `./data`.