Yes, you are correct about permissions and the need to ensure the `data` folder exists on the host. Here’s how it works:

1. **Directory Creation**:
   - Docker will automatically create the `data/images` and `data/text` directories in the container if they don’t exist there.
   - However, on the **host machine**, Docker expects the directories (`./data/images` and `./data/text`) to already be present. If they don’t exist, you should create them manually to avoid any errors when the container tries to start.

2. **Write Permissions**:
   - Ensure the host directories (`./data/images` and `./data/text`) have write permissions for the Docker process. This usually means setting appropriate permissions for the user or group running the container, typically with a command like `chmod -R 755 ./data` or using `chown` to give ownership if needed.
   - Inside the container, if the application needs to write to `/app/data/images` and `/app/data/text`, Docker should typically handle these permissions unless specific restrictions are in place. However, if you run into permission errors, you may need to add write permissions within the container setup. 

3. **Quick Setup on the Host**:
   - Run these commands to create the folders and set permissions on the host machine:
     ```bash
     mkdir -p ./data/images
     mkdir -p ./data/text
     chmod -R 755 ./data
     ```

Once these are set up, your application should be able to access and write to these folders as expected.