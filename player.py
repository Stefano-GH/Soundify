##############################
# IMPORT LIBRARIES
##############################
import os
from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
from tkinter import ttk


##############################
# FUNCTION DEFINITION
##############################
def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Stefano/musica/classica/", title='Choose a song', filetypes=(("mp3 files", "*.mp3"), ))
    song = song.replace("C:/Stefano/musica/classica/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="C:/Stefano/musica/classica/", title='Choose a song', filetypes=(("mp3 files", "*.mp3"), ))
    for song in songs:
        song = song.replace("C:/Stefano/musica/classica/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)

def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Stefano/musica/classica/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    play_time()
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)

def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')

def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.pause()
        paused = False
    else:
        pygame.mixer.music.unpause()
        paused = True

def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song = f'C:/Stefano/musica/classica/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one)

def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'C:/Stefano/musica/classica/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one)

def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_song():
    song_box.delete(0, END)
    pygame.mixer.music.stop()

def play_time():
    current_time = pygame.mixer.music.get_pos() // 1000
    slider_label.config(text=f'Slider: {int(my_slider.get())} and Song position {int(current_time)}')
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    current_song = song_box.curselection()
    song = song_box.get(current_song)
    song = f'C:/Stefano/musica/classica/{song}.mp3'
    # Load song with mutagen
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    # Convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(my_slider.get()) == int(song_length):
        my_slider.config(to=slider_position, value=int(my_slider.get()))
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time elapsed: {converted_current_time}  of  {converted_song_length}  ')
        
        # Move the slider along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000, play_time)


def slider(e):
    slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Stefano/musica/classica/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(my_slider.get()))


##############################
# MAIN BODY
##############################
root = Tk()
root.geometry('600x600')
root.title('Music Player')
#root.iconphoto(False, PhotoImage(file='universe.png'))

# Initialize pygame mixer
pygame.mixer.init()

# Create a playlist box
song_box = Listbox(root, bg='black', fg='green', width=60, selectbackground='gray', selectforeground='black')
song_box.pack(pady=20)

#Create frame
control_frame = Frame(root)
control_frame.pack()

paused = False

# Create player control button
back_button = Button(control_frame, text='<<', command=previous_song)
forward_button = Button(control_frame, text='>>', command=next_song)
play_button = Button(control_frame, text='Play', command=play)
pausa_button = Button(control_frame, text='Pause', command=lambda: pause(paused))
stop_button = Button(control_frame, text='Stop', command=stop)
back_button.grid(row=0, column=0)
forward_button.grid(row=0, column=1)
play_button.grid(row=0, column=2)
pausa_button.grid(row=0, column=3)
stop_button.grid(row=0, column=4)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add song', menu=add_song_menu)
add_song_menu.add_command(label='Add one song to playlist', command=add_song)
add_song_menu.add_command(label='Add many songs to playlist', command=add_many_songs)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Remove songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Delete a song from playlist', command=delete_song)
remove_song_menu.add_command(label='Delete all song from playlist', command=delete_all_song)

# Create a status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fil=X, side=BOTTOM, ipady=2)

my_slider = ttk.Scale(root, from_=0, to=100, length=360, command=slider)
my_slider.pack(pady=20)

slider_label = Label(root, text='0')
slider_label.pack(pady=10)

root.mainloop()