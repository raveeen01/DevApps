import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import folium
import os

def get_ip_info():
    try:
        # Fetch IP information from ipinfo.io
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        
        # Extract relevant information
        ip_address = data.get('ip', 'N/A')
        location = data.get('loc', 'N/A').split(',')
        isp = data.get('org', 'N/A')
        country_code = data.get('country', 'N/A')

        return ip_address, location, isp, country_code
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP info: {e}")
        return None, None, None, None

def create_map(location):
    # Create a Folium map centered at the location
    lat, lon = float(location[0]), float(location[1])
    map_obj = folium.Map(location=[lat, lon], zoom_start=12)

    # Add a marker for the location
    folium.Marker([lat, lon], popup='Your Location').add_to(map_obj)

    # Save the map to an HTML file
    map_file = "map.html"
    map_obj.save(map_file)
    
    return map_file

def on_button_click():
    ip_address, location, isp, country_code = get_ip_info()
    if ip_address:
        messagebox.showinfo("IP Information", 
            f"Public IPv4 Address: {ip_address}\n"
            f"Location: {location}\n"
            f"ISP: {isp}\n"
            f"Country Code: {country_code}")

        # Create and open the map
        map_file = create_map(location)
        os.startfile(map_file)  # This will open the HTML file in your default browser
    else:
        messagebox.showerror("Error", "Failed to retrieve IP information.")

# Create the main application window
root = tk.Tk()
root.title("IP Address Finder")

# Create a button to fetch the IP address and display information
fetch_button = tk.Button(root, text="Get IP Information", command=on_button_click)
fetch_button.pack(pady=20)

# Run the application
root.mainloop()