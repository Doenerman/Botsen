#player.py

import os
import datetime
import time
from threading import Thread
from threading import Semaphore

from vlc import Media
from vlc import MediaPlayer

class Player:
    """The class provides basic media playback functions.
    
    The class provides functions to load local media and play it.
    """

    def __init__(self):
        """Initializes empty class variables.
        
        The class initializes the following class variables:
        vlc_player      The variable, which is used to play music via an
                        instance of a vlc.MediaPlayer. It is initialized with
                        'None'.
        wish_list       A list of file paths, that determine the files that
                        are left to play. It is initialized as an empty list.
        playing_thread  A thread that calls 'self.play()' and which is joined in
                        the destructor. It is initialized and started.
        keep_playing    A boolean that signals the method 'self.play()' and thus
                        the thread 'self.playing_thread' when to stop the
                        playback and prepare to be destructed. It is initialized
                        with 'True'.
        is_paused       The boolean signals the method 'play()' when the current
                        playback is paused and is toggled by the method
                        'self.pause()'. It is initialized with 'False'..


        Semaphores
        ----------
        change_player_list  A 'threading.Semaphore' that should be acquired and
                            released when ever 'self.wish_list' or
                            'self.wish_list'.
        """
        self.vlc_player = MediaPlayer()
        self.wish_list = list()
        self.playing_thread = Thread( target=self.play )
        self.keep_playing = True
        self.is_paused = False
        self.playing_thread.start()

        self.change_player_list = Semaphore()

    def __del__(self):
        """The destructor prepares the object to be destructed, by joining all
        threads and stopping the music.
        """
        print(f'called destructor')
        if isinstance( self.vlc_player, MediaPlayer ):
            self.vlc_player.stop()

        # stop and join the playing_thread
        self.keep_playing = False
        self.playing_thread.join()

        # delet created instance variables
        del self.vlc_player
        del self.keep_playing
        del self.is_paused
        del self.playing_thread
        del self.change_player_list




    def pause(self):
        """Pauses or resumes playing music.
        
        Calling this method toggles the 'pause' function of 'self.vlc_player' in
        case it is an instance of 'vlc.MediaPlayer'. Also the instance variable
        'self.is_paused' toggled, such that the method 'self.play()'
        recognizes that the current title is paused.
        """
        if isinstance( vlc_player, MediaPlayer ) :
            self.vlc_player.pause()
            if self.keep_playing:
                self.is_paused = False
            else:
                self.is_paused = True

    def play(self):
        """The method starts media playback and continues until
        'self.keep_playing' is set to False.

        The method starts media playback for file paths mentioned in
        'self.wish_list'. For the playback the instance variable
        'self.vlc_player', which declared as a 'MediaPlayer' in case it is of
        any other type while there is at least one element in 'self.wish_list'.
        When all elements of 'self.wish_list' are played or removed, the method
        waits until new elements are added to 'self.wish_list'.
        The method only returns if the variable 'self.keep_playing' is set to
        False.

        In order to access and edit 'self.vlc_player' the 'Semaphore'
        'self.change_player_list' is acquired and released when ever
        'self.vlc_player' or 'self.wish_list' is edited.
        """
        while self.keep_playing:
            if not self.is_paused:
                # self is expected to play until 'self.wish_list' is empty
                if len(self.wish_list) > 0:
                    # there are currently some songs to play
                    if isinstance( self.vlc_player, MediaPlayer ):
                        # the 'vls_player' is initialized with the expected type
                        if self.vlc_player.is_playing():
                            # currently playing, nothing need to happen,
                            # so it can sleep to spare some resources
                            time.sleep( 0.5 )
                        else:
                            # there is no song playing at the moment, but there are
                            # tracks in 'self.wish_list' that still needs to be
                            # played
                            
                            self.change_player_list.acquire()

                            # load the media for the next song into vlc_player
                            self.vlc_player.set_media( Media( self.wish_list[0] ) )
                            self.vlc_player.play()
                            # remove just loaded song from the wish_list
                            self.wish_list.remove( self.wish_list[0] )

                            self.change_player_list.release()

                # the length of 'self.wish_list' is not greater than 0, so there
                # is no song to play next.
                else:
                    time.sleep(0.5)
            else:
                # self is expected to pause, until the user requests to continue
                # the playback
                time.sleep(0.5)


    def skip(self):
        """The method does not finish the current track but starts playing the
        next title in 'self.wish_list'.

        In case 'self.vlc_player' is an instance of 'MediaPlayer' and
        there is at least one element in 'self.wish_list' the method
        waits to get the rights to change 'self.vlc_player' by acquiring
        'self.change_player_list'. After that, the method loads the first element
        of 'self.wish_list', loads that as new 'vlc.Media' for the
        'self.vlc_player' and starts playing the new media. After that the
        'self.change_player_list' is released.

        In order to access and edit 'self.vlc_player' the 'Semaphore'
        'self.change_player_list' is acquired and released when ever
        'self.vlc_player' or 'self.wish_list' is edited.
        """
        if isinstance( self.vlc_player, MediaPlayer ):
            if len( self.wish_list ) > 0 :
                self.change_player_list.acquire()
                
                # edit vlc_player 
                self.vlc_player.set_media( Media( self.wish_list[0] ) )
                self.vlc_player.play()
                # edit wish_list
                self.wish_list.remove( self.wish_list[0] )

                self.change_player_list.release()


    def mute(self):
        """The method toggles the mute of the audio output of the media
        player 'self.vlc_player'.

        When 'self.vlc_player' is an instance of 'MediaPlayer', the mothed
        toggles the method 'self.vlc_player.audio_toggle_mute()'.
        """
        if isinstance( self.vlc_player, MediaPlayer ):
            self.vlc_player.audio_toggle_mute()


    def queue(self,file_path):
        """The method adds the string 'file_path' to the end of the list 
        'self.wish_list' and starts playing.

        If the given parameter 'file_path' is of the type 'str' and a valid file
        path, it is appended to the list 'wish_list'.

        In order to access and edit the 'self.wish_list' the 'Semaphore'
        'self.change_player_list' is acquired and released when 'file_path' is
        added to 'self.wish_list'.

        Parameters:
        -----------
        file_path   A str of the file path towards a destination file that
                    should be played by the player instance and which is added
                    to 'self.wish_list'.
        """
        if isinstance( file_path, str ) and os.path.isfile( file_path ) :
            self.change_player_list.acquire()
            # add new media file to wish_list
            self.wish_list.append( file_path )

            self.change_player_list.release()
