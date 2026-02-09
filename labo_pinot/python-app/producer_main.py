import os
import sys
import subprocess

MODE = os.getenv("PRODUCER_TYPE", "random")

if MODE == "api":
    print("🚀 Iniciando Producer API")
    subprocess.run([
        "uvicorn",
        "producer_api:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

elif MODE == "random":
    print("🎲 Iniciando Producer Random")
    subprocess.run([
        "python",
        "producer_example.py"
    ])

else:
    print(f"❌ Modo desconocido: {MODE}")
    sys.exit(1)
