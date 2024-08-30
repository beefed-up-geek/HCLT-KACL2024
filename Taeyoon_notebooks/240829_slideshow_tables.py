import os
import time
import psutil
import subprocess

# visualized가 있는 디렉터리 이름
html_directory = r'C:\Users\tenny\Desktop\visualized'

# Get a list of all HTML files in the directory
html_files = [f for f in os.listdir(html_directory) if f.endswith('.html')]

# Get screen dimensions
screen_width = 1920  # Replace with your screen width
screen_height = 1080  # Replace with your screen height

# Calculate 80% of the screen size
width_80 = int(screen_width * 0.8)
height_80 = int(screen_height * 0.8)

# Open each HTML file, wait for user input, and then close the browser
for html_file in html_files:
    file_path = os.path.join(html_directory, html_file)
    
    # Open the HTML file in Edge with 80% size
    subprocess.Popen([
        'start', 'msedge', 
        f'file:///{file_path}', 
        f'--window-size={width_80},{height_80}'
    ], shell=True)
    
    # Wait for the user to press Enter or Spacebar
    input("Press Enter or Spacebar to continue to the next file...")
    
    # Find and close the specific Edge process that was started
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == 'msedge':
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                proc.kill()

print("Completed opening and closing all HTML files.")
