import spotipy

from spotipy.oauth2 import SpotifyOAuth


class SpotifyManager:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id="05edf4051ff448dbba535b2e24e3afbf",
                client_secret="ad9a3f6a59464012ade2e2c376c508ea",
                redirect_uri="http://127.0.0.1:8888/callback",
                scope="""
                user-read-playback-state
                user-modify-playback-state
                user-read-currently-playing
                playlist-read-private
                user-library-read
                user-read-playback-position
                user-read-recently-played
                user-read-private
                """
            )
        )

    def get_current_playback(self):
        return self.sp.current_playback()

    def get_queue(self):
        return self.sp.queue()

    def get_playlists(self):
        return self.sp.current_user_playlists()

    def next_song(self):
        self.sp.next_track()

    def previous_song(self):
        self.sp.previous_track()

    def pause(self):
        self.sp.pause_playback()

    def play(self):
        self.sp.start_playback()