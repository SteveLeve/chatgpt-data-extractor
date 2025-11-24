import subprocess
import sys
import time

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        return False

def reset_data():
    """
    Resets the data by removing the docker volume.
    """
    print("Resetting data via Docker...")
    
    # Stop containers and remove volumes
    print("Stopping containers and removing volumes...")
    if not run_command("docker compose down -v"):
        print("Failed to reset data via Docker.")
        return

    print("Data reset complete. Starting database...")
    
    # Start database
    if not run_command("docker compose up -d db"):
        print("Failed to start database.")
        return

    print("Waiting for database to be ready...")
    # Simple wait, ideally we'd check health
    time.sleep(5) 
    print("Database should be ready.")

if __name__ == "__main__":
    # Confirmation prompt
    confirm = input("This will permanently delete all data by removing Docker volumes. Are you sure? (y/N): ")
    if confirm.lower() == 'y':
        reset_data()
    else:
        print("Operation cancelled.")
