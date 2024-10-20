The sentence you're referring to is describing a simple test to check whether a web server (in this case, Google's server) is accessible over **port 80**, which is the default port used for **HTTP** (non-secure) web traffic.

### Breaking it down:
1. **Access port 80**: 
   - **Port 80** is the standard port for the **HTTP protocol** (not HTTPS, which typically uses port 443). When you visit a website using `http://`, your browser is communicating with that website's server through port 80.
   - The phrase "access port 80" means testing whether you can reach the web server through this port. This is often done using tools like `telnet`, `curl`, or `nc (netcat)` to see if the server is **listening** for connections on that specific port.

2. **www.google.com is a domain name**:
   - Yes, `www.google.com` is a domain name. Domain names are human-readable addresses that are mapped to IP addresses (the actual locations of servers) through the Domain Name System (DNS). 
   - When you access `www.google.com`, DNS translates this domain into an IP address, allowing your browser to connect to the server associated with that IP. Servers use various **ports** to listen for different types of traffic (e.g., HTTP on port 80, HTTPS on port 443, SSH on port 22).

3. **Checking if www.google.com is served from port 80**:
   - The sentence is essentially asking: **"Is there a web server (or any service) responding on port 80 at the address www.google.com?"**
   - If you can establish a connection to `www.google.com` on port 80, it means that the server at the IP address corresponding to `www.google.com` is **listening for HTTP requests** on port 80. This indicates that the web service (or some other service) on that server is **up** and reachable.

4. **The full meaning of the sentence**:
   - The test involves sending a request to port 80 of the server at `www.google.com`. If the server responds (meaning it is accepting connections on that port), then you can assume the service is running, and the command would echo (output) the message "google is up."

### Conclusion:
- The sentence describes a simple connectivity test to check if the web service on `www.google.com` is accessible over port 80 (used for HTTP traffic). 
- In practice, most websites, including Google, use **HTTPS** (which operates on port 443), but the test mentioned here focuses on the non-secure HTTP port. 
- The underlying idea is to check if any service (usually a web server) is active and reachable on a specific port of the machine (server) that hosts `www.google.com`.