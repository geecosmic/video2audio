import tkinter as tk
from tkinter import filedialog, messagebox
from customtkinter import *
from moviepy.editor import VideoFileClip
from tkinter.ttk import Progressbar
import threading

class VideoToAudioConverter(CTk):
    def __init__(self):
        super().__init__()
        self.title("Video to Audio Converter")
        self.geometry("400x400")
        self.resizable(False, False)
        # self.attributes("-fullscreen", False)
        
        self.file_path = None
        
        self.top_frame = CTkFrame(self, fg_color="#221c16", border_color="red", border_width=5)
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        label = CTkLabel(self.top_frame, text="Select a video file to convert to audio:")
        label.place(relx=0.26,rely=0.1)
        
        self.file_label = CTkLabel(self.top_frame, text="", wraplength=300)
        self.file_label.place(relx=0.3,rely=0.4)
        
        btn_browse = CTkButton(self.top_frame, text="Browse", command=self.browse_file)
        btn_browse.place(relx=0.33,rely=0.36)
        
        btn_convert = CTkButton(self.top_frame, text="Convert", command=self.start_conversion)
        btn_convert.place(relx=0.33,rely=0.86)
        
        self.progress = Progressbar(self.top_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.place(relx=0.182,rely=0.6)
        
    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        self.file_label.configure(text=self.file_path)
    
    def start_conversion(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a video file first!")
            return
        self.progress["value"] = 0
        conversion_thread = threading.Thread(target=self.convert_video_to_audio)
        conversion_thread.start()
    
    def convert_video_to_audio(self):
        try:
            video = VideoFileClip(self.file_path)
            audio = video.audio
            audio_file_path = self.file_path.replace('.mp4', '.mp3')  # Replace with .mp3 or desired audio format
            
            # Get video duration to calculate progress
            duration = video.duration
            
            # Function to update progress
            def update_progress(current_time):
                progress_value = (current_time / duration) * 100
                self.progress["value"] = progress_value
                self.update_idletasks()
            
            # Save audio file
            audio.write_audiofile(audio_file_path)
            
            # Simulate progress bar update
            for current_time in range(int(duration)):
                self.after(10, update_progress, current_time)
                
            video.close()
            self.after(0, lambda: messagebox.showinfo("Success", "Conversion completed successfully!"))
            self.after(0, lambda: self.progress.set(0))  # Reset progress bar
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            self.after(0, lambda: self.progress.set(0))  # Reset progress bar in case of error

if __name__ == "__main__":
    app = VideoToAudioConverter()
    app.mainloop()
