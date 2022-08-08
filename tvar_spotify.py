import csv
import random
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

class Song:
    def __init__(self, id, name, author, priority):
        self.id = id
        self.name = name
        self.author = author
        self.priority = priority


def process_csv(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        line_count = 0
        song_list = []
        for row in csv_reader:
            song = Song(line_count, row[0], row[1], int(row[2]))
            song_list.append(song)
            line_count += 1
            # print(song.name)
        sorted_song_list = sorted(song_list, key=lambda x: x.name + x.author)
        return sorted_song_list


def prepare_priority_list(song_list):
    probability_list = []
    for song in song_list:
        for i in range(song.priority):
            probability_list.append(song)
    return probability_list


def set_song_list(song_list, song_number, new_priority):
    song_list[song_number].priority = new_priority


def refresh_file(song_list, filename):
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for song in song_list:
            writer.writerow([song.name, song.author, str(song.priority)])


def find_active_device(spotify_object):
    if len(spotify_object.devices()["devices"]) == 0:
        raise ValueError
    for device in spotify_object.devices()["devices"]:
        if device["is_active"]:
            print(device)
            return device["id"]
    return spotify_object.devices()["devices"][0]["id"]


def create_search_string(author, song_name):
    return "artist:" + author + " track:" + song_name


def find_song_result(spotify_object, song):
    song.author = song.author.replace("+", "")
    author_names = [song.author]
    if "(" in song.author:
        split = re.split('[()]', song.author)  # \(|\)
        author_names.append(split[0].strip())
        if len(split) > 1:
            author_names.append(split[1].replace("+", "").strip())
    elif " " in song.author:
        author_names.append(song.author.split(" ")[-1])
    if "," in song.author:
        authors_after_split = song.author.split(",")
        for author in authors_after_split:
            author_names.append(author)

    for author in author_names:
        search_results = spotify_object.search(create_search_string(author, song.name), type="track")["tracks"]["items"]
        if not search_results:
            search_results = \
                spotify_object.search(create_search_string(author, song.name.replace("'", "")), type="track")["tracks"][
                    "items"]
        if search_results:
            return search_results

    # Debug print: search inputs tried
    print(author_names)
    return None


def spotify_util(spotify_object, song, device):
    index = 0
    search_result = find_song_result(spotify_object, song)
    if search_result:
        uri = (search_result[index]["uri"])
        tracks = [uri]
        spotify_object.start_playback(device, None, tracks)
    else:
        raise Exception("Song not found")


def spotify_play(spotify_object, song, device):
    try:
        spotify_util(spotify_object, song, device)
    except Exception:
        return False
    return True


def spotify_pause(spotify_object, device):
    try:
        spotify_object.pause_playback(device)
    except:
        print("Cannot pause, pause manually!")


def print_info(song):
    print("Song: " + song.name)
    print("Author: " + song.author)
    print("Probability: " + str(song.priority))


def run(song_list, probability_list, filename):
    # Spotify setup
    scope = "user-read-private user-read-playback-state user-modify-playback-state"
    spotify_object = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    device = find_active_device(spotify_object)

    change = False
    print("Write E for end (anything else otherwise)")
    end = input()
    while "e" not in end and "E" not in end:
        number = random.randint(0, len(probability_list) - 1)
        song = probability_list[number]
        if spotify_play(spotify_object, song, device):
            input("Press any key to pause and show song info\n")
            print_info(song)
            spotify_pause(spotify_object, device)
        else:
            print_info(song)
            print("ERROR: Song cannot be played, play it manually!")
        print("ACTIONS: number - change probability, 0 - no change")
        while True:
            action = input()
            try:
                number = int(action)
                if number != 0:
                    set_song_list(song_list, song.id, number)
                    change = True
            except:
                print("invalid number, try again")
                continue
            break
        end = input("Write E for end, R to replay previous song (anything else otherwise)\n")
        if "R" in end or "r" in end:
            spotify_play(spotify_object, song, device)
            end = input("Write E for end, (anything else otherwise)\n")
            spotify_pause(spotify_object, device)

    if change:
        refresh_file(song_list, filename)


def main():
    """Change to your file name with songs in format: <songname>;<author>;priority
    """
    filename = "files/song_list_sample.csv"

    song_list = process_csv(filename)
    probability_list = prepare_priority_list(song_list)
    run(song_list, probability_list, filename)


load_dotenv()
main()

