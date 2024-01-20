import docker

client = docker.from_env()

# Stop and remove the existing container with the same name
existing_container_name = 'ollama'
try:
    existing_container = client.containers.get(existing_container_name)
    existing_container.stop()
    existing_container.remove()
    print(f"Stopped and removed existing container: {existing_container_name}")
except docker.errors.NotFound:
    print(f"No existing container found with the name: {existing_container_name}")

# Start the new container
new_container = client.containers.run(
    "ollama/ollama",
    detach=True,
    volumes={'ollama': {'bind': '/root/.ollama', 'mode': 'rw'}},
    ports={'11434': '11434'},
    name='ollama'
)

# Print the container ID
print(f"Container ID: {new_container.id}")

# List containers (optional)
print(client.containers.list())

# Get user input for the prompt
user_prompt = input("Enter your prompt: ")

# Run model using exec_run
command = f'ollama run llama2 "{user_prompt}"'
exec_result = new_container.exec_run(command, tty=True)

# Wait for the command to complete
exit_code = exec_result.exit_code
print(f"Command exit code: {exit_code}")

# Print the output after the command completes
exec_result_output = exec_result.output.decode('utf-8')
print(f"Command output: {exec_result_output}")

# List containers again (optional)
print(client.containers.list())
