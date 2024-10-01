import os
import time
import pygame
import tkinter as tk
from tkinter import ttk, filedialog, Listbox, END, messagebox
from PIL import Image, ImageTk

# Initialize pygame mixer
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Music Player")
        self.root.geometry("600x500")
        self.is_dark_mode = True

        # Playlist listbox (music list)
        self.playlist = []
        self.current_song_index = -1
        self.is_paused = False

        # Volume control
        self.volume = 1.0

        # Dark/Light mode colors
        self.dark_bg = "#1f1f1f"
        self.light_bg = "#f0f0f0"
        self.dark_fg = "#ffffff"
        self.light_fg = "#000000"

        # Icons (minimalist white icons)
        self.icons = {
            "play": ImageTk.PhotoImage(Image.open("icons/play_white.png").resize((30, 30))),
            "pause": ImageTk.PhotoImage(Image.open("icons/pause_white.png").resize((30, 30))),
            "stop": ImageTk.PhotoImage(Image.open("icons/stop_white.png").resize((30, 30))),
            "next": ImageTk.PhotoImage(Image.open("icons/next_white.png").resize((30, 30))),
            "prev": ImageTk.PhotoImage(Image.open("icons/prev_white.png").resize((30, 30))),
            "add": ImageTk.PhotoImage(Image.open("icons/add_white.png").resize((30, 30))),
            "remove": ImageTk.PhotoImage(Image.open("icons/remove_white.png").resize((30, 30))),
            "volume_up": ImageTk.PhotoImage(Image.open("icons/volume_white.png").resize((30, 30))),
            "dark_mode": ImageTk.PhotoImage(Image.open("icons/dark_mode.png").resize((30, 30))),
            "light_mode": ImageTk.PhotoImage(Image.open("icons/light_mode.png").resize((30, 30))),
        }

        # Create the playlist box with styles
        self.playlist_box = Listbox(
            self.root, selectmode=tk.SINGLE, bg=self.dark_bg, fg=self.dark_fg, font=("Arial", 12),
            width=60, height=10, highlightthickness=0, selectbackground="#0000FF"
        )
        self.playlist_box.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # Button style
        button_style = {
            "bd": 0,
            "highlightthickness": 0
        }

        # Add buttons with icons and styles
        self.add_button = tk.Button(self.root, image=self.icons["add"], command=self.add_song, **button_style)
        self.add_button.grid(row=1, column=0, padx=10, pady=10)

        self.remove_button = tk.Button(self.root, image=self.icons["remove"], command=self.remove_song, **button_style)
        self.remove_button.grid(row=1, column=1, padx=10, pady=10)

        # Play/Pause button (combined)
        self.play_pause_button = tk.Button(self.root, image=self.icons["play"], command=self.play_pause_music, **button_style)
        self.play_pause_button.grid(row=2, column=2, padx=10, pady=10)

        # Stop button
        self.stop_button = tk.Button(self.root, image=self.icons["stop"], command=self.stop_music, **button_style)
        self.stop_button.grid(row=2, column=3, padx=10, pady=10)

        # Next/Prev button (combined)
        self.next_prev_button = tk.Button(self.root, image=self.icons["next"], command=self.next_prev_song, **button_style)
        self.next_prev_button.grid(row=2, column=1, padx=10, pady=10)

        # Dark/Light Mode Button
        self.mode_button = tk.Button(self.root, image=self.icons["light_mode"], command=self.toggle_mode, **button_style)
        self.mode_button.grid(row=2, column=4, padx=10, pady=10)

        # Volume Control Slider
        self.volume_slider = ttk.Scale(
            self.root, from_=0, to=1, orient=tk.HORIZONTAL, length=300,
            command=self.set_volume, style="TScale"
        )
        self.volume_slider.set(1.0)  # Default volume (100%)
        self.volume_slider.grid(row=3, column=0, columnspan=4, pady=10, padx=10)

        # Volume label
        self.volume_label = tk.Label(self.root, text="Volume", bg=self.dark_bg, fg=self.dark_fg, font=("Arial", 12))
        self.volume_label.grid(row=3, column=0, padx=10, sticky=tk.W)

        # Progress bar (elapsed time)
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=300)
        self.progress_bar.grid(row=4, column=0, columnspan=4, pady=10, padx=10)

        # Styling the slider and progress bar
        self.style = ttk.Style(self.root)
        self.style.configure("TScale", background=self.dark_bg, troughcolor="#333333", sliderlength=20, sliderthickness=15)
        self.update_mode()

    # Add song to playlist
    def add_song(self):
        song_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if song_path:
            song_name = os.path.basename(song_path)
            self.playlist.append(song_path)
            self.playlist_box.insert(END, song_name)

    # Remove song from playlist
    def remove_song(self):
        try:
            selected_song_index = self.playlist_box.curselection()[0]
            self.playlist_box.delete(selected_song_index)
            del self.playlist[selected_song_index]
        except IndexError:
            messagebox.showerror("Error", "No song selected")

    # Play/Pause button functionality
    def play_pause_music(self):
        if len(self.playlist) > 0:
            if pygame.mixer.music.get_busy() and not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_pause_button.config(image=self.icons["play"])
            else:
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                else:
                    selected_song_index = self.playlist_box.curselection()[0]
                    pygame.mixer.music.load(self.playlist[selected_song_index])
                    pygame.mixer.music.play()
                self.play_pause_button.config(image=self.icons["pause"])
                self.update_progress_bar()

    # Stop button functionality
    def stop_music(self):
        pygame.mixer.music.stop()
        self.play_pause_button.config(image=self.icons["play"])

    # Next/Prev button functionality
    def next_prev_song(self):
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play()
        elif self.current_song_index > 0:
            self.current_song_index -= 1
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play()
        self.update_progress_bar()

    # Set volume
    def set_volume(self, volume_level):
        self.volume = float(volume_level)
        pygame.mixer.music.set_volume(self.volume)

    # Progress bar update
    def update_progress_bar(self):
        if pygame.mixer.music.get_busy():
            song_length = pygame.mixer.Sound(self.playlist[self.current_song_index]).get_length()
            for i in range(int(song_length)):
                time.sleep(1)
                self.progress_bar['value'] = (i / song_length) * 100
                self.root.update()

    # Dark/Light mode toggle
    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_mode()

    def update_mode(self):
        if self.is_dark_mode:
            self.root.config(bg=self.dark_bg)
            self.playlist_box.config(bg=self.dark_bg, fg=self.dark_fg)
            self.volume_label.config(bg=self.dark_bg, fg=self.dark_fg)
            self.mode_button.config(image=self.icons["light_mode"])
        else:
            self.root.config(bg=self.light_bg)
            self.playlist_box.config(bg=self.light_bg, fg=self.light_fg)
            self.volume_label.config(bg=self.light_bg, fg=self.light_fg)
            self.mode_button.config(image=self.icons["dark_mode"])

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
