To check the permissions of a folder, you can use the following command on your host machine:

```bash
ls -ld <path_to_folder>
```

Replace `<path_to_folder>` with the path to the folder you want to check, such as `./data` or any subdirectories like `./data/text`. This command will display the permissions, owner, and group for the specified directory.

### Example

If your folder is `./data`, run:

```bash
ls -ld ./data
```

The output will look something like this:

```plaintext
drwxr-xr-x 2 youruser yourgroup 4096 Oct 26 12:00 ./data
```

### Understanding the Output
- **First Part (e.g., `drwxr-xr-x`)**: This represents the permissions.
  - `d` indicates a directory.
  - `rwx` after `d` represents read, write, and execute permissions for the owner.
  - The next `r-x` is for the group.
  - The final `r-x` is for others.
  
- **Owner and Group** (e.g., `youruser yourgroup`): This shows the user and group that own the folder. Ensure it aligns with the `appuser` UID in your container (`10001`).

Let me know the results of this command, and I can guide you further based on the current permissions.