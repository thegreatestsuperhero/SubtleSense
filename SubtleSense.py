import tkinter as tk
from tkinter import filedialog, messagebox
from time import time

def hmsms2s(t:str):
    hms = t.split(':')
    h = int(hms[0])
    m = int(hms[1])
    sm = hms[2].split(',')
    s = int(sm[0])
    ms = int(sm[1])
    return (h * 3600 + m * 60 + s + ms * 0.001)

def s2hmsms(t:float):
    h = int(t // 3600)
    m = int((t - h * 3600) // 60)
    s = int((t - h * 3600 - m * 60) // 1)
    ms = int((t - t // 1) * 1000)
    
    h = str(h).zfill(2)
    m = str(m).zfill(2)
    s = str(s).zfill(2)
    ms = str(ms).zfill(3)
    
    return f"{h}:{m}:{s},{ms}"

def timeshift(duration, shift):
    times = duration.split("-->")
    start = times[0].strip()
    end = times[1].strip()
    newstart = s2hmsms(hmsms2s(start) + shift)
    newend = s2hmsms(hmsms2s(end) + shift)
    return f"{newstart} --> {newend}"

def open_file():
    file_path = filedialog.askopenfilename(title="Open subtitle", filetypes=[("Subtitle files (.srt)", "*.srt")])
    if not file_path.lower().endswith(".srt") and len(file_path):
        messagebox.showerror("Error", "Please select a subtitle (.srt) file.")
    else:
        if len(file_path): entry_file_location.delete(0,tk.END)
        entry_file_location.insert(0, file_path)

def process_subtitle():
    file_path = entry_file_location.get()
    if not (file_path.lower().endswith(".srt") and len(file_path)):
        messagebox.showerror("Error", "Please select a subtitle (.srt) file.")
        return
    try:
        tshift = round(float(entry_timeshift.get()),3)
    except:
        messagebox.showerror("Error", "Please specify a valid time shift.")
        return
    
    try:
        with open(file_path, 'r', errors="ignore") as subfile:
            subs = subfile.read().strip()
            if subs[0:3] == "ï»¿":
                subs = subs[3:]
        
        start_time = time()

        sublines = subs.split('\n')
        lines = len(sublines)
        resub = ""
        
        i = 0
        j = 0
        while i < lines:
            if sublines[i].isnumeric():
                resub += f"{sublines[i]}\n{timeshift(sublines[i+1], tshift)}\n"
                i += 2
                j += 1
            else:
                resub += f"{sublines[i]}\n"
                i += 1
        
        resub = f"{resub.strip()}\n"

        end_time = time()
        process_time = 1000*(end_time - start_time)

        update_original = messagebox.askyesno("Success", f"{j} lines processed in {process_time:.3f} miliseconds.\nOverride original file?")

        if update_original:
            destiny = file_path
        else:
            destiny = filedialog.asksaveasfilename(title="Save subtitle as", filetypes=[("Subtitle files (.srt)", "*.srt")])
        
        if not len(destiny): return

        if not destiny.lower().endswith(".srt"):
            destiny += ".srt"
        
        with open(destiny, 'w') as newsub:
            newsub.write(resub)
        
    except Exception as e:
        messagebox.showerror("Error", "Specified file/directory not found.")

# Create the main window
root = tk.Tk()
root.title("SubtleSense - Subtitle Time Shifter")
root.resizable(False,False)

file_frame = tk.Frame(root)
file_frame.pack(side="top", fill="x", expand=True, padx=20, pady=(20,15))

file_label = tk.Frame(file_frame)
file_label.pack(side="top",fill="x", expand=True)

# Create a label and an entry for file location
label_file_location = tk.Label(file_label, text="Subtitle file location:")
label_file_location.pack(side="left", padx=20, pady=(0,5), anchor="sw")
button_browse = tk.Button(file_label, text="Browse", command=open_file)
button_browse.pack(side="right", padx=20, pady=(0,5), anchor="se")
entry_file_location = tk.Entry(file_frame, width=50)
entry_file_location.pack(side="bottom", fill="x", padx=20, pady=(5,0), anchor="s")

time_frame = tk.Frame(root)
time_frame.pack(side="top", fill="x", expand=True, padx=20, pady=(15,20))

# Create a label and an entry for time shift
label_timeshift = tk.Label(time_frame, text="Time shift (ss.mmm):")
label_timeshift.pack(side="left", padx=20, pady=(0,5), anchor="w")
entry_timeshift = tk.Entry(time_frame)
entry_timeshift.pack(side="right", fill="x", padx=20, pady=(0,5), expand=True, anchor="e")

# Create a button to process the subtitle
process_button = tk.Button(root, text="Process subtitle", command=process_subtitle)
process_button.pack(side="bottom", padx=20, pady=(0,20))

# Run the application
root.eval('tk::PlaceWindow . center')
root.mainloop()
