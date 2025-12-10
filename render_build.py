import subprocess
import sys


def run(cmd):
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(r.returncode)


# Instala dependências do projeto
run(["uv", "sync"])

# Realiza as migrações do banco de dados
run(["uv", "run", "python", "manage.py", "migrate"])

# Coleta arquivos estáticos
run(["uv", "run", "python", "manage.py", "collectstatic", "--noinput"])
