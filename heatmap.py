import os
import requests
import folium
from folium.plugins import HeatMap
import tkinter as tk
from tkinter import filedialog
import threading

def main():
    UI()

def UI():
    window = tk.Tk()
    window.title("Heatmap Generator")
     
    frame_ind = tk.Frame(master=window, cursor="dot")
    frame_ind.grid(columnspan=6, row=1, sticky="n", padx=5, pady=1)

    frame_ent = tk.Frame(master=window)
    frame_ent.grid(columnspan=3, row=2, sticky='nw', padx=5, pady=1)

    frame_ent2 = tk.Frame(master=window)
    frame_ent2.grid(columnspan=3, row=3, sticky='nw', padx=5, pady=1)

    frame_btn = tk.Frame(master=window)
    frame_btn.grid(column=4,row=2,columnspan=1,sticky='nsew',padx=1, pady=1)

    # Labels within frames
    lbl_ind = tk.Label(master=frame_ind, text="Indicator", font=("Helvetica", 20))
    lbl_ind.grid(column=0, row=0, sticky='nsew')

    # Text widget within frame_ent

    tb_postal = tk.Text(master=frame_ent, width=40, height=25, font="Arial, 15")  # Adjust width and height as needed
    tb_postal.insert(tk.END, "Input your postal codes here, with each new postal code on a new line.")  # Insert  text
    tb_postal.tag_add("tag1", "1.0", "end")  # Apply the tag to the inserted text
    tb_postal.tag_config("tag1", font=("papyrus", 20, "italic"))  # Configure the tag
    tb_postal.grid(column=0, row=0, sticky='sw')  # Stick to top-left corner

    scrollbar = tk.Scrollbar(frame_ent, orient="vertical", command=tb_postal.yview) # Adds a scroll bar to the text box
    scrollbar.grid(row=0, column=1, sticky='ns')
    tb_postal.config(yscrollcommand=scrollbar.set)

    def btn1_click():
        postal_dup = tb_postal.get("1.0",'end-1c').splitlines()
        postal_set = set(postal_dup)
        tb_postal.delete("1.0",'end-1c')
        for num in postal_set:
            tb_postal.insert(tk.END,num+"\n")

    def btn2_click():
        # Initialize an empty list to store the latitude and longitude pairs
        lbl_ind.config(text="Generating Heat Map, please wait")
        lat_long_list = []
        postal_list = tb_postal.get("1.0",'end-1c').splitlines()
        for i, postal in enumerate(postal_list, start = 1):
            if postal.isnumeric():
                lbl_ind.config(text=f"Processing {i} out of {len(postal_list)} postal codes")
                url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={postal}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
                # Send a GET request to the API
                response = requests.get(url)
                # Convert the response text to a dictionary
                results_dict = response.json()
                # Check if there are any results
                if len(results_dict["results"]) > 0:
                    # Extract the latitude and longitude from the first result
                    latitude = float(results_dict["results"][0]["LATITUDE"])
                    longitude = float(results_dict["results"][0]["LONGITUDE"])
                    # Append the latitude and longitude as a tuple to the list
                    lat_long_list.append((latitude, longitude))
        map_object = folium.Map(location=[1.290270, 103.851959], zoom_start=12)
        HeatMap(lat_long_list).add_to(map_object)
        html_map = map_object.get_root().render()
        file_path = filedialog.asksaveasfilename(defaultextension=".html",filetypes=[("HTML files", "*.html")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(html_map)  # Replace html_content with your HTML content
        lbl_ind.config(text="Heat Map Generated")

    def start_thread():
        threading.Thread(target=btn2_click).start()

    btn1_dup=tk.Button(master=frame_btn,text="Remove Duplicates", font=("Helvetica", 10),bg="black",fg="white",relief="sunken",width=20,height=5,command=btn1_click).grid(column=0, row=0, sticky='nwe')
    btn2_ctr=tk.Button(master=frame_btn,text="Generate Heat Map", font=("Helvetica", 10),bg="black",fg="white",relief="sunken",width=20,height=5,command=start_thread).grid(column=0, row=1, sticky='nwe')

    window.mainloop()

if __name__ == "__main__":
    main()
