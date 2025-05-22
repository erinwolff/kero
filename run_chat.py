import subprocess
import time
import os


def is_ollama_running():
    try:
        subprocess.check_output(["lsof", "-i", ":11434"])
        return True
    except subprocess.CalledProcessError:
        return False


def start_ollama():
    print("🔄 Starting Ollama server...")
    return subprocess.Popen(["ollama", "serve"])


def start_chainlit():
    print("🚀 Launching Chainlit app...")

    project_dir = os.path.abspath(os.path.dirname(__file__))
    venv_python = os.path.join(project_dir, "venv/bin/python")
    main_script = os.path.join(project_dir, "main.py")

    # Ensure we run the command from inside the correct folder
    os.chdir(project_dir)

    try:
        subprocess.run([venv_python, "-m", "chainlit", "run", main_script])
    except KeyboardInterrupt:
        print("🛑 Chainlit stopped by user.")


def kill_process(proc, name):
    if proc and proc.poll() is None:
        print(f"🛑 Stopping {name}...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    ollama_proc = None

    try:
        if not is_ollama_running():
            ollama_proc = start_ollama()
            time.sleep(2)  # Give it time to bind the port

        start_chainlit()

    finally:
        kill_process(ollama_proc, "Ollama")
