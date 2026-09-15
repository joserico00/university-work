# Use the existing OpenVAS Docker image as a base
FROM immauss/openvas

# Update the system and install Python and pip (if needed for internal use)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Expose the port for GVM API
EXPOSE 9390

# Start OpenVAS and gvmd in foreground
CMD ["/usr/local/bin/start"]

