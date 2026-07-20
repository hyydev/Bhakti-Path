# ─────────────────────────────────────────
# STAGE 1: Builder
# ─────────────────────────────────────────
# Kyun 2 stages?
# Builder mein: gcc, build tools install karte hain
# (packages compile karne ke liye zaroori)
# Production image mein: sirf runtime chahiye
# Result: Production image bahut chhoti hoti hai
# Builder: ~800MB → Production: ~200MB
FROM python:3.12-slim AS builder

# WORKDIR = working directory set karo container mein
# Aage ke saare commands yahan se chalenge
WORKDIR /app

# System dependencies install karo
# gcc: C compiler (kuch Python packages compile karte hain)
# libpq-dev: PostgreSQL client library (psycopg2 ke liye)
# --no-install-recommends: unnecessary packages mat lo
# rm -rf /var/lib/apt/lists/*: apt cache clean karo (image size kam)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt PEHLE copy karo
# Kyun? Layer caching!
# requirements.txt change nahi hua → pip install cache se
# Code change kiya → sirf code layer rebuild, pip nahi
COPY requirements.txt .

# pip install
# --no-cache-dir: pip ka cache mat rakho (image size kam)
# --upgrade pip: latest pip use karo
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────
# STAGE 2: Production
# ─────────────────────────────────────────
FROM python:3.12-slim AS production

WORKDIR /app

# Sirf runtime dependency chahiye
# gcc nahi chahiye production mein (compile ho chuka)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Builder stage se installed packages copy karo
# Yahi magic hai multi-stage build ka
# Build tools nahi aaye, sirf installed packages aaye
COPY --from=builder /usr/local/lib/python3.12/site-packages \
                    /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Project files copy karo
COPY . .

# Zarori directories banao
# logs: error logging ke liye
# media: user uploaded files ke liye
# staticfiles: collectstatic ke liye
RUN mkdir -p logs media staticfiles

# Non-root user banao — SECURITY
# Root user se app run karna dangerous hai
# Agar container compromise ho → limited damage
RUN groupadd --system django \
    && useradd --system --gid django django

# Files ka ownership django user ko do
RUN chown -R django:django /app

# Ab django user se kaam karo
USER django

# Port expose karo
# Yeh sirf documentation hai — actually port open karta hai docker-compose
EXPOSE 8000

# Entrypoint script copy karo
COPY --chown=django:django docker-entrypoint.sh /app/
# Executable banao
RUN chmod +x /app/docker-entrypoint.sh

CMD ["/app/docker-entrypoint.sh"]