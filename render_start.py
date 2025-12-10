import os
import subprocess
import sys

port = os.environ.get("PORT", "8000")

# Inicia o servidor WSGI com Gunicorn
cmd = [
    "uv",
    "run",
    "gunicorn",
    "config.wsgi:application",
    "--bind",
    f"0.0.0.0:{port}",
]

r = subprocess.run(cmd)
if r.returncode != 0:
    sys.exit(r.returncode)
