FROM mcr.microsoft.com/devcontainers/python:3-trixie

# System deps for pygame + noVNC stack
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    supervisor xvfb x11vnc fluxbox websockify novnc \
    libasound2 libsndfile1 \
    libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pygame

# Supervisor config
RUN mkdir -p /etc/supervisor/conf.d
COPY novnc.conf /etc/supervisor/conf.d/novnc.conf

# Make supervisord the container command (so it starts even without postStart)
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
