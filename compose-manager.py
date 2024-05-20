from flask import Flask, request, jsonify
import docker
import threading
import time
import os

app = Flask(__name__)
client = docker.from_env()

# Dictionary to store the last restart time for each container
last_restart_time = {}

# Function to restart container asynchronously
def restart_container_async(container_name):
    try:
        container = client.containers.get(container_name)
        container.restart()
    except Exception as e:
        print(f"Error restarting container {container_name}: {e}")

@app.route('/restart/<container_id>', methods=['GET', 'POST'])
def restart_container(container_id):
    container_name = f"comfyui-dockers-comfy-{container_id}-1"
    token = request.args.get('token')
    
    # Path to the password file
    password_file_path = f'comfy-{container_id}/ComfyUI/login/PASSWORD'
    
    # Check if the password file exists
    if os.path.exists(password_file_path):
        # Read the token from the password file
        with open(password_file_path, 'r') as file:
            correct_token = file.readline().strip()
        
        # Compare the provided token with the correct token
        if token != 'heartai': # TODO: it's temporary, need to figure out a way to check permission, maybe using Session logged_in?
            if token != correct_token:
                return jsonify({"error": "Invalid token"}), 403
    
    current_time = time.time()
    
    # Check if the container has been restarted recently
    if container_name in last_restart_time:
        elapsed_time = current_time - last_restart_time[container_name]
        if elapsed_time < 10:
            return jsonify({"error": f"Please wait {10 - int(elapsed_time)} seconds before restarting again"}), 429
    
    try:
        # Start a new thread to restart the container asynchronously
        threading.Thread(target=restart_container_async, args=(container_name,)).start()
        # Update the last restart time
        last_restart_time[container_name] = current_time
        return jsonify({"message": f"Restarting container {container_name}"}), 200
    except docker.errors.NotFound:
        return jsonify({"error": "Container not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
