The logs you're seeing indicate that the server is killing its workers due to running out of memory, signaled by the `SIGKILL` (signal 9) messages. This means the batch processing you're running is likely consuming too much memory, causing the operating system to terminate the worker processes.

Here’s how to address this **Out of Memory (OOM)** issue professionally:

### 1. **Reduce Batch Size**
The most direct approach is to reduce the size of the batches you're processing. Since you're encoding images into base64, this could be memory-intensive, especially with large image datasets. Start by reducing the `BATCH_SIZE` in your code further, perhaps down to something like 10 or 20.

In your `batch_processing.py`:

```python
BATCH_SIZE = 20  # Reduce the batch size to limit memory usage
```

### 2. **Process in Streams or Use Generators**
Instead of loading all the data into memory at once, use Python generators or streams to process the data one-by-one or in small chunks. For instance, you can read the CSV file in smaller chunks rather than loading the entire file into memory. Here’s how you can adjust the processing:

```python
def stream_csv_batches(csv_path, batch_size):
    df_iter = pd.read_csv(csv_path, chunksize=batch_size)
    for batch_df in df_iter:
        yield batch_df.to_dict(orient='records')

async def process_text_data_in_batches():
    # Stream the CSV in chunks
    dataset_path = os.path.join(settings.DATA_OUTPUT_PATH, "filtered_final_dataset.csv")
    for text_batch in stream_csv_batches(dataset_path, BATCH_SIZE):
        task_id = await send_text_batch(text_batch)
        print(f"Text batch sent with task ID: {task_id}")

async def process_image_data_in_batches():
    dataset_path = os.path.join(settings.DATA_OUTPUT_PATH, "filtered_final_dataset.csv")
    for image_batch in stream_csv_batches(dataset_path, BATCH_SIZE):
        task_id = await send_image_batch(image_batch)
        print(f"Image batch sent with task ID: {task_id}")
```

### 3. **Increase Memory Limits for Docker (If Applicable)**
If you are running the server in Docker, the container might have a memory limit that causes it to be killed when it reaches the threshold. You can increase the memory allocated to the container in your `docker-compose.yml`:

```yaml
services:
  web:
    build:
      context: .
      dockerfile: ./Dockerfile
    container_name: real_estate_app_debug
    ports:
      - "8000:8000"
    mem_limit: "1g"  # Increase the memory limit to 1GB (adjust as needed)
    environment:
      - DATABASE_URL=postgresql://user:password@db/your_db
```

### 4. **Use Swap Space (Last Resort)**
If you're running on a system without much RAM, you can add swap space, which is disk space used as memory. This will slow down the processing but prevent the system from running out of memory. Adding swap space is system-specific, but here’s how you would add swap space on a Linux machine:

```bash
# Create a swap file (2GB in this example)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make the swap permanent (optional)
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 5. **Optimize Memory Usage**
Make sure you are not keeping unnecessary data in memory. For example, ensure that batches are cleared after processing:

```python
image_batches = []
# After processing, clear the batch to free memory
task_id = await send_image_batch(image_batches)
image_batches.clear()  # Clear the batch to release memory
```

### 6. **Offload Heavy Tasks to a Celery Worker**
If you can, offload the batch processing to an asynchronous task queue system like Celery, which allows you to process batches in the background, freeing up the main server to handle incoming requests without crashing.

### 7. **Monitor Memory Usage**
Set up monitoring (e.g., Prometheus, Grafana) or use simple tools like `top`, `htop`, or Docker's built-in stats (`docker stats`) to observe memory consumption during the batch processing and adjust accordingly.

By implementing these steps, you should be able to avoid memory overflows and handle the batches more efficiently.