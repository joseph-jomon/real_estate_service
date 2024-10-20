Apologies for the confusion! Let me clarify:

You **do not** need to change the port in the `--listen` argument inside the Docker Compose `command`. The `--listen` argument refers to the **internal port** that the container listens on, and it should remain as `5678` inside the container. 

Here’s what you should do:

1. **Docker Compose (`docker-compose-debug.yml`) - `ports` section**:
   - Change the **left side** (the host-side port) to `5679`:
     ```yaml
     ports:
       - "8000:8000"
       - "5679:5678"  # Expose 5679 on host and map to 5678 in the container
     ```

2. **Docker Compose (`docker-compose-debug.yml`) - `command`**:
   - **Do not change** the internal port in the command. Keep it as `5678`:
     ```yaml
     command: ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", ...]
     ```
   - The container will still listen on port `5678`, but the host will map it to `5679`.

3. **`launch.json`**:
   - Change the `port` from `5678` to `5679` to match the new host port:
     ```json
     "port": 5679  // Host port you want to attach the debugger to
     ```

### Summary:
- **Host-side** port should be `5679` in `ports` (`5679:5678`).
- Keep the **container-side** `--listen` argument as `5678`.
- Update **`launch.json`** to use `5679` for the debugger.

This will properly expose the internal container port `5678` as `5679` on your host system and resolve the port conflict.