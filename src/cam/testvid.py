import tkinter as tk
from PIL import Image, ImageTk
import cv2
import requests
import numpy as np

# Flask video stream URL
VIDEO_URL = "http://127.0.0.1:5000/video_feed"  # Change to Raspberry Pi IP if needed

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flask Video Stream in Tkinter")

        # Create a Label to display the video
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Start updating frames
        self.update_frame()

    def update_frame(self):
        """Fetch a frame from the Flask video stream and update Tkinter Label"""
        try:
            response = requests.get(VIDEO_URL, stream=True)
            bytes_data = b""
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b"\xff\xd8")  # JPEG start
                b = bytes_data.find(b"\xff\xd9")  # JPEG end
                if a != -1 and b != -1:
                    jpg = bytes_data[a : b + 2]
                    bytes_data = bytes_data[b + 2 :]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # Convert to RGB and update Tkinter
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=img)

                    self.video_label.imgtk = imgtk
                    self.video_label.config(image=imgtk)

        except Exception as e:
            print("Error fetching video frame:", e)

        # Call update_frame again after 10ms
        self.root.after(10, self.update_frame)

# Run the Tkinter app
root = tk.Tk()
app = VideoApp(root)
root.mainloop()
