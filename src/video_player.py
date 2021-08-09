"""A video player class."""
from .video_playlist import Playlist
from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_playing_video = []
        self.current_playing_video_obj = []
        self.current_video_status = 0  # Playing or Stopped
        self.current_video_pause_status = 0  # Paused or not paused
        self.play_lists = {}
        self.flagged_videos = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:", end='\n\t')
        video_Objects = self._video_library.get_all_videos()
        all_videos_sorted = []
        for obj in video_Objects:
            if obj.video_id in self.flagged_videos.keys():
                all_videos_sorted.append(obj.title + ' (' + obj.video_id + ') ' + str(list(obj.tags)).replace('\'', '').replace(',', '')+" - FLAGGED (reason: "+self.flagged_videos[obj.video_id]+")")
            else:
                all_videos_sorted.append(obj.title + ' (' + obj.video_id + ') ' + str(list(obj.tags)).replace('\'', '').replace(',', ''))
        all_videos_sorted.sort()
        print(*all_videos_sorted, sep='\n\t')


    def play_video(self, video_id):
        if video_id in self.flagged_videos.keys():
            print("Cannot play video: Video is currently flagged (reason:",self.flagged_videos[video_id]+")")
        elif self._video_library.get_video(video_id) is None:
            print('Cannot play video: Video does not exist')
        elif self.current_video_status == 0:
            video = self._video_library.get_video(video_id).title
            print('Playing video:', video)
            self.current_playing_video = [video]
            self.current_video_status = 1
            self.current_video_pause_status = 0
            self.current_playing_video_obj = [self._video_library.get_video(video_id)]
        else:
            video = self._video_library.get_video(video_id).title
            self.stop_video()
            print('Playing video:', video)
            self.current_playing_video = [video]
            self.current_video_status = 1
            self.current_video_pause_status = 0
            self.current_playing_video_obj = [self._video_library.get_video(video_id)]

        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

    def stop_video(self):
        """Stops the current video."""
        if self.current_playing_video and self.current_video_status == 1:
            print('Stopping video:', self.current_playing_video[0])
            self.current_video_status = 0
            self.current_video_pause_status = 0
        else:
            print('Cannot stop video: No video is currently playing')


    def play_random_video(self):
        """Plays a random video from the video library."""
        video_list = self._video_library.get_all_videos()
        flagged_video = True
        if len(video_list) == len(self.flagged_videos):
            print("No videos available")
        else:
            while flagged_video:
                random_video_index = random.randint(0, len(video_list) - 1)
                if video_list[random_video_index].video_id in self.flagged_videos.keys():
                    continue
                else:
                    self.play_video(video_list[random_video_index].video_id)
                    flagged_video = False

    def pause_video(self):
        """Pauses the current video."""
        if self.current_video_pause_status == 0 and self.current_video_status == 1:
            self.current_video_pause_status = 1
            print('Pausing video:', self.current_playing_video[0])
        elif self.current_video_status == 0:
            print('Cannot pause video: No video is currently playing')
        elif self.current_video_pause_status == 1 and self.current_video_status == 1:
            print('Video already paused:', self.current_playing_video[0])

    def continue_video(self):
        """Resumes playing the current video."""
        if self.current_video_pause_status == 0 and self.current_video_status == 1:
            print('Cannot continue video: Video is not paused')
        elif self.current_video_pause_status == 1 and self.current_video_status ==1:
            print("Continuing video:",self.current_playing_video[0])
            self.current_video_pause_status = 0
        else:
            print('Cannot continue video: No video is currently playing')


    def show_playing(self):
        """Displays video currently playing."""
        if self.current_video_pause_status == 0 and self.current_video_status == 1:
            print('Currently playing:',self.current_playing_video_obj[0].title + ' (' + self.current_playing_video_obj[0].video_id + ') ' + str(list(self.current_playing_video_obj[0].tags)).replace('\'', '').replace(',', ''))
        elif self.current_video_pause_status == 1 and self.current_video_status == 1:
            print('Currently playing:',
                  self.current_playing_video_obj[0].title + ' (' + self.current_playing_video_obj[0].video_id + ') ' + str(list(self.current_playing_video_obj[0].tags)).replace('\'', '').replace(',', ''),'- PAUSED')
        else:
            print('No video is currently playing')

    def check_playlist(self,playlist_name):
        playlist_name = playlist_name.lower().replace(' ','_')
        keys = list(self.play_lists.keys())
        if playlist_name in keys:
            return True
        else:
            return False





    def create_playlist(self, playlist_name):
        playlist_name_stored = playlist_name.lower().replace(' ','_')
        if self.check_playlist(playlist_name) == True:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.play_lists[playlist_name_stored] = Playlist(playlist_name,[])
            print("Successfully created new playlist:",playlist_name)

        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

    def add_to_playlist(self, playlist_name, video_id):
        if video_id in self.flagged_videos.keys():
            print("Cannot add video to my_playlist: Video is currently flagged (reason:",self.flagged_videos[video_id]+")")
        elif self.check_playlist(playlist_name) == True and self._video_library.get_video(video_id) is not None:
            playlist_name_stored = playlist_name.lower().replace(' ', '_')
            previous_videos_obj = self.play_lists[playlist_name_stored]
            list_of_previous_videos = previous_videos_obj.playlist_items
            if video_id in list_of_previous_videos:
                print("Cannot add video to",playlist_name+': Video already added')
            else:
                previous_stored_videos = self.play_lists[playlist_name_stored]
                previous_stored_videos = previous_stored_videos.playlist_items
                previous_stored_videos.append(video_id)
                all_videos_obj = Playlist(playlist_name,previous_stored_videos)
                self.play_lists[playlist_name_stored] = all_videos_obj
                print('Added video to',playlist_name+':',self._video_library.get_video(video_id).title)
        elif not self.check_playlist(playlist_name):
            print("Cannot add video to",playlist_name+': Playlist does not exist')
        else:
            print("Cannot add video to", playlist_name + ': Video does not exist')

        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """


    def show_all_playlists(self):
        """Display all playlists."""
        sorted_video_list = []
        if self.play_lists == {}:
            print("No playlists exist yet")
        else:
            playlist_videos_obj = self.play_lists.values()
            for obj in playlist_videos_obj:
                sorted_video_list.append(obj.playlist_name)
                sorted_video_list.sort()
            print("Showing all playlists:", *sorted_video_list,sep='\n\t')

    def show_playlist(self, playlist_name):
        playlist_name_stored = playlist_name.lower().replace(' ', '_')
        if playlist_name_stored in self.play_lists.keys():
            playlist_obj = self.play_lists[playlist_name_stored]
            if not playlist_obj.playlist_items:
                print('Showing playlist:',playlist_name,end='\n\t')
                print("No videos here yet")
            else:
                print('Showing playlist:', playlist_name)
                for video_id in playlist_obj.playlist_items:
                    obj = self._video_library.get_video(video_id)
                    if video_id in self.flagged_videos.keys():
                        print('\t'+obj.title + ' (' + obj.video_id + ') ' + str(list(obj.tags)).replace('\'', '').replace(',', ''),"- FLAGGED (reason:",self.flagged_videos[video_id]+")")
                    else:
                        print('\t'+obj.title + ' (' + obj.video_id + ') ' + str(list(obj.tags)).replace('\'', '').replace(',', ''))
        else:
            print("Cannot show playlist",playlist_name+': Playlist does not exist')

        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

    def remove_from_playlist(self, playlist_name, video_id):
        playlist_name_stored = playlist_name.lower().replace(' ', '_')
        if self.check_playlist(playlist_name_stored):
            playlist_items_obj = self.play_lists[playlist_name_stored]
            if video_id in playlist_items_obj.playlist_items:
                new_playlist_items = playlist_items_obj.playlist_items
                new_playlist_items.remove(video_id)
                self.play_lists[playlist_name_stored] = Playlist(playlist_name,new_playlist_items)
                print("Removed video from",playlist_name+':',self._video_library.get_video(video_id).title)
            elif self._video_library.get_video(video_id) == None:
                print("Cannot remove video from",playlist_name+': Video does not exist')
            else:
                print("Cannot remove video from",playlist_name+': Video is not in playlist')
        else:
            print("Cannot remove video from",playlist_name+': Playlist does not exist')


        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

    def clear_playlist(self, playlist_name):
        playlist_name_stored = playlist_name.lower().replace(' ', '_')
        if self.check_playlist(playlist_name_stored):
            self.play_lists[playlist_name_stored] = Playlist(playlist_name,[])
            print("Successfully removed all videos from",playlist_name)
        else:
            print("Cannot clear playlist",playlist_name+': Playlist does not exist')
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

    def delete_playlist(self, playlist_name):
        playlist_name_stored = playlist_name.lower().replace(' ', '_')
        if self.check_playlist(playlist_name_stored):
            self.play_lists.pop(playlist_name_stored)
            print("Deleted playlist:",playlist_name)
        else:
            print("Cannot delete playlist",playlist_name+': Playlist does not exist')
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

    def search_videos(self, search_term):
        related_video_titles = []
        related_video_ids = []
        lower_case_search_term = search_term.lower()
        all_video_objs = self._video_library.get_all_videos()
        for vid_object in all_video_objs:
            if vid_object.title.lower().count(lower_case_search_term) > 0 and vid_object.video_id not in self.flagged_videos.keys():
                related_video_titles.append(vid_object.title.lower())
                related_video_ids.append(vid_object.video_id)
        if len(related_video_titles)>0:
            print("Here are the results for",search_term+':')
            related_video_ids.sort()
            for index in range(len(related_video_titles)):
                obj = self._video_library.get_video(related_video_ids[index])
                print('\t'+str(index+1)+')',obj.title + ' (' + obj.video_id + ') ' + str(list(obj.tags)).replace('\'', '').replace(',', ''))
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_answer = input()
            if user_answer.isnumeric():
                if int(user_answer) <= len(related_video_titles):
                    self.play_video(related_video_ids[int(user_answer)-1])
        else:
            print("No search results for",search_term)



        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

    def search_videos_tag(self, video_tag):
        related_video_ids = []
        lower_case_video_tag = video_tag.lower()
        all_video_objs = self._video_library.get_all_videos()
        for vid_object in all_video_objs:
            video_tags = str(vid_object.tags)
            if video_tags.lower().count(lower_case_video_tag) > 0 and vid_object.video_id not in self.flagged_videos.keys():
                related_video_ids.append(vid_object.video_id)
        if len(related_video_ids) > 0:
            print("Here are the results for",video_tag+':')
            related_video_ids.sort()
            for index in range(len(related_video_ids)):
                obj = self._video_library.get_video(related_video_ids[index])
                print('\t'+str(index+1)+')',obj.title + ' (' + obj.video_id + ') ' + str(list(obj.tags)).replace('\'', '').replace(',', ''))
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_answer = input()
            if user_answer.isnumeric():
                if int(user_answer) <= len(related_video_ids):
                    self.play_video(related_video_ids[int(user_answer) - 1])
        else:
            print("No search results for", video_tag)
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

    def flag_video(self, video_id, flag_reason="Not supplied"):
        if self._video_library.get_video(video_id) is None:
            print("Cannot flag video: Video does not exist")
        elif video_id in self.flagged_videos.keys():
            print("Cannot flag video: Video is already flagged")
        elif self._video_library.get_video(video_id).title in self.current_playing_video:
            self.stop_video()
            print("Successfully flagged video:",self._video_library.get_video(video_id).title,"(reason:",flag_reason+")")
            self.flagged_videos[video_id] = flag_reason
        else:
            print("Successfully flagged video:", self._video_library.get_video(video_id).title, "(reason:",flag_reason + ")")
            self.flagged_videos[video_id] = flag_reason






        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

    def allow_video(self, video_id):
        if self._video_library.get_video(video_id) is None:
            print("Cannot remove flag from video: Video does not exist")
        elif video_id not in self.flagged_videos.keys():
            print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Successfully removed flag from video:",self._video_library.get_video(video_id).title)
            self.flagged_videos.pop(video_id)

        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
