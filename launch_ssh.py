"""
Sets up an SSH server in a Modal container.

After running this with `modal run launch_ssh.py`, connect to SSH with `ssh -p 9090 HOST:PORT`, where HOST and PORT are the values returned by the modal run command, eg:

ssh -p password root@r20.modal.host:45773

This uses simple password authentication, but you can store your own key in a modal Secret instead.
"""

import modal
import threading
import socket
import subprocess
import time

app = modal.App(
    "vscode-environment",
    image=modal.Image.from_registry(
        "nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04",
        add_python="3.11",
    )
    .apt_install("openssh-server", "wget", "git")
    .pip_install("torch", "matplotlib", "bitsandbytes", "transformers", "datasets")
    .run_commands(
        "mkdir -p /run/sshd",
        "echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config",
        "echo 'root:password' | chpasswd",
    ),
    # .add_local_dir("~/Desktop/my-pkg", "/dev/my-pkg")
)


def wait_for_port(host, port, q):
    start_time = time.monotonic()
    while True:
        try:
            with socket.create_connection(("localhost", 22), timeout=30.0):
                break
        except OSError as exc:
            time.sleep(0.01)
            if time.monotonic() - start_time >= 30.0:
                raise TimeoutError(
                    "Waited too long for port 22 to accept connections"
                ) from exc
        q.put((host, port))


@app.function(timeout=3600 * 24, gpu="A100-80GB")
def launch_ssh(q):
    with modal.forward(22, unencrypted=True) as tunnel:
        host, port = tunnel.tcp_socket
        threading.Thread(target=wait_for_port, args=(host, port, q)).start()

        subprocess.run(["/usr/sbin/sshd", "-D"])


@app.local_entrypoint()
def main():
    with modal.Queue.ephemeral() as q:
        launch_ssh.spawn(q)
        host, port = q.get()
        print(f"SSH server running at {host}:{port}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down SSH tunnel...")
