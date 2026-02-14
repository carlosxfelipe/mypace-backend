# generate_secret_key.py
"""
Script para gerar uma nova SECRET_KEY para projetos Django.
Uso: python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    print(get_random_secret_key())
