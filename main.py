import os
import shutil
import psutil

def process_command(command):
    """Processes a single command and returns the output as a string."""
    parts = command.split()
    cmd = parts[0].lower() if parts else ""
    output_lines = []

    if cmd == "pwd":
        output_lines.append(os.getcwd())
    
    elif cmd == "ls":
        try:
            items = os.listdir('.')
            output_lines.extend(items)
        except Exception as e:
            output_lines.append(f"ls: an error occurred: {e}")

    elif cmd == "cd":
        try:
            if len(parts) > 1:
                directory = parts[1]
                os.chdir(directory)
                output_lines.append(f"Current directory: {os.getcwd()}")
            else:
                output_lines.append("cd: missing operand")
        except FileNotFoundError:
            output_lines.append(f"cd: no such file or directory: {parts[1]}")
        except Exception as e:
            output_lines.append(f"cd: an error occurred: {e}")

    elif cmd == "mkdir":
        try:
            if len(parts) > 1:
                dir_name = parts[1]
                os.mkdir(dir_name)
                output_lines.append(f"Directory '{dir_name}' created.")
            else:
                output_lines.append("mkdir: missing operand")
        except FileExistsError:
            output_lines.append(f"mkdir: cannot create directory '{parts[1]}': File exists")
        except Exception as e:
            output_lines.append(f"mkdir: an error occurred: {e}")

    elif cmd == "rm":
        try:
            if len(parts) > 1:
                path_to_remove = parts[1]
                if os.path.isfile(path_to_remove):
                    os.remove(path_to_remove)
                    output_lines.append(f"File '{path_to_remove}' removed.")
                elif os.path.isdir(path_to_remove):
                    shutil.rmtree(path_to_remove)
                    output_lines.append(f"Directory '{path_to_remove}' removed.")
                else:
                    output_lines.append(f"rm: cannot remove '{path_to_remove}': No such file or directory")
            else:
                output_lines.append("rm: missing operand")
        except Exception as e:
            output_lines.append(f"rm: an error occurred: {e}")
    
    elif cmd == "status":
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        output_lines.append(f"CPU Usage: {cpu_usage}%")
        output_lines.append(f"Memory Usage: {memory_info.percent}% ({memory_info.used/1024/1024:.2f} MB / {memory_info.total/1024/1024:.2f} MB)")

    elif cmd == "echo":
        try:
            # Handles 'echo "text" > filename'
            if len(parts) >= 4 and parts[-2] == '>':
                filename = parts[-1]
                # Join all parts between echo and >
                text_to_write = " ".join(parts[1:-2]).strip('"\'')
                
                with open(filename, 'w') as f:
                    f.write(text_to_write + '\n')
                output_lines.append(f"File '{filename}' created.")
            # Handles simple 'echo text'
            else:
                output_lines.append(" ".join(parts[1:]))
        except Exception as e:
            output_lines.append(f"echo: an error occurred: {e}")

    elif not cmd:
        # Don't return an error for an empty command
        pass
    
    else:
        output_lines.append(f"Command '{cmd}' not found.")

    return "\n".join(map(str, output_lines))

# This part allows you to still run main.py as a CLI if you want to test
if __name__ == "__main__":
    print("Terminal logic loaded. Run app.py to start the web server.")
    while True:
        prompt = f"py-term:{os.getcwd()} $ "
        user_input = input(prompt)
        if user_input.lower() == "exit":
            break
        result = process_command(user_input)
        if result:
            print(result)