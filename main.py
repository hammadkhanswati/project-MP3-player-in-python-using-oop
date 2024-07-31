import customtkinter as ctk
from tkinter import filedialog, Listbox, Menu
import pygame
from PIL import Image, ImageTk
import os

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("500X500")
        self.root.resizable(False, False)  # Make the window non-resizable

        # Load the gramophone image using PIL
        self.gramophone_image = Image.open("Gramophone.png")  # Ensure you have Gramophone.png in the same directory

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Current song and song list
        self.current_song = ""
        self.song_list = []
        self.current_song_index = 0

        # Boolean to track if a song is paused
        self.paused = False

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):

        mp3_label = ctk.CTkLabel(self.root, text="MP3 Player", font=("Helvetica", 30))
        mp3_label.pack(pady=10)
        # Canvas for the gramophone image
        self.canvas = ctk.CTkCanvas(self.root, width=100, height=100, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.gramophone_photo = ImageTk.PhotoImage(self.gramophone_image)
        self.canvas.create_image(50, 50, image=self.gramophone_photo)

        # Listbox to show song list
        self.song_listbox = Listbox(self.root, bg="black", fg="white", width=60)
        self.song_listbox.pack(pady=20)
        
        # Control Frame
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(pady=20)

        # Play/Pause Button
        play_btn = ctk.CTkButton(control_frame, text="Play/Pause", command=self.play_pause, width=80, height=30)
        play_btn.grid(row=0, column=0, padx=5)

        # Next Button
        next_btn = ctk.CTkButton(control_frame, text="Next", command=self.next_song, width=80, height=30)
        next_btn.grid(row=0, column=1, padx=5)

        # Back Button
        back_btn = ctk.CTkButton(control_frame, text="Back", command=self.previous_song, width=80, height=30)
        back_btn.grid(row=0, column=2, padx=5)

        # Volume Slider
        volume = ctk.CTkLabel(self.root, text="Volume", font=("Helvetica", 16))
        volume.pack(pady=10)

        self.volume_slider = ctk.CTkSlider(self.root, from_=0, to=1, orientation="horizontal", command=self.set_volume)
        self.volume_slider.pack(pady=10)
        self.volume_slider.set(0.5)
        
        # QUIT BUTTON
        quit_btn = ctk.CTkButton(control_frame, text="Quit", command=self.root.quit, width=80, height=30)
        quit_btn.grid(row=0, column=3, padx=5)

        # Menu for loading songs
        menu = Menu(self.root)
        self.root.config(menu=menu)
        add_song_menu = Menu(menu)
        menu.add_cascade(label="Add Songs", menu=add_song_menu)
        add_song_menu.add_command(label="Add One Song To Playlist", command=self.add_song)
        add_song_menu.add_command(label="Add Many Songs To Playlist", command=self.add_many_songs)

    def add_song(self):
        song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
        if song:
            self.song_listbox.insert(ctk.END, song)
            self.song_list.append(song)

    def add_many_songs(self):
        songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose Songs", filetypes=(("mp3 Files", "*.mp3"),))
        for song in songs:
            if song:
                self.song_listbox.insert(ctk.END, song)
                self.song_list.append(song)

    def play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.paused = True
            else:
                try:
                    self.current_song = self.song_list[self.song_listbox.curselection()[0]]
                    pygame.mixer.music.load(self.current_song)
                    pygame.mixer.music.play(loops=0)
                    self.paused = False
                except:
                    pass

    def next_song(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        self.current_song = self.song_list[self.current_song_index]
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play(loops=0)

    def previous_song(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
        self.current_song = self.song_list[self.current_song_index]
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play(loops=0)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = MP3Player(root)
    root.mainloop()