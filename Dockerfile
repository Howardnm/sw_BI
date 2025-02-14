# Stage 1: Base build stage
FROM python:3.8-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.8-slim

# 安装 Nginx 和 Python 依赖
RUN apt-get update && \
    apt-get install -y nginx vim && \
    rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
#RUN useradd -m -r appuser && \
#   mkdir /app && \
#   chown -R appuser /app

# 手动创建 Nginx 需要的目录并赋予权限
#RUN mkdir -p /var/lib/nginx/body && \
#    chown -R appuser:appuser /var

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY . .

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

#RUN chown -R www-data:www-data /app/app01/static/ && \
#    chmod -R 755 /app/app01/static/

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
#USER appuser

# Expose the application port
EXPOSE 8000

# Start the application using Gunicorn
# 生产环境(gunicorn支持多线程)
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "sw_BI.wsgi:application"]
# 开发环境(只支持单线程，容易崩溃)
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# 启动 Nginx 和 Django
# 启动 Nginx 并运行 Gunicorn
#CMD ["sh", "-c", "nginx & gunicorn --bind 0.0.0.0:8000 --workers 3 sw_BI.wsgi:application"]
#CMD ["nginx", "-g", "daemon off;"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "sw_BI.wsgi:application"]
# 启动 Nginx 和 Gunicorn
#CMD ["sh", "-c", "nginx -g 'daemon off;' & exec gunicorn --bind 0.0.0.0:8000 --workers 3 sw_BI.wsgi:application"]
# 启动 Nginx 和 Gunicorn
CMD ["sh", "-c", "exec nginx -g 'daemon off;' & exec gunicorn --bind 0.0.0.0:8000 --workers 3 sw_BI.wsgi:application"]