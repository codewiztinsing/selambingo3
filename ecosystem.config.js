module.exports = {
    apps: [{
      name: "django-bot",
      script: "gunicorn",
      args: "--workers 3 --timeout 120 --bind 0.0.0.0:8000 botbackend.wsgi:application",
      interpreter: "none", // Required for non-Node.js apps
      autorestart: true,
      watch: false, // Disable watch unless needed
      max_memory_restart: "1G", // Restart if memory exceeds 1GB
      env: {
        DJANGO_SETTINGS_MODULE: "botbackend.settings",
        PYTHONUNBUFFERED: "1", // Disable stdout buffering
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: "logs/error.log",
      out_file: "logs/output.log",
    }]
  };