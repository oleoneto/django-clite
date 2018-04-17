/*
// albums.js
// Developed by Leo Neto on Dec 18, 2017.
// Ekletik Studios. Open-source License.
*/


var allSongs = $('audio');
var songIcons = $('button > i');
var pageTitle = document.getElementsByTagName('title');
var mainTitle = pageTitle[0].textContent;
var currentSong;
var currentButton;
var currentIcon;
var currentTitle;
var songTitle;
var $songs = $(".song");

$(document).ready(function() {

    // Pauses the audio if the user switches to another tab.
    window.addEventListener('visibilitychange', function() {
        if (document.hidden){
            if (currentSong) {
                StopTracks();
                $('title')[0].textContent = "Paused: " + currentTitle;
            }
        } else {
            $('title')[0].textContent = mainTitle;
            if (currentSong) {
                ResumePlayBack(currentSong);
                UpdatePlayIcon(currentIcon);
            }
        }
    });

    // Click on the first element of the table.
    ClickTrack($songs[0]);
});


function PlayTrack(id) {
    currentSong = document.getElementById("song-" + id);
    currentButton = document.getElementById(id);
    currentIcon = currentButton.children[0];
    currentTitle = document.getElementById("title-"+id);
    currentTitle = currentTitle.textContent;
    songTitle = "Playing: " + currentTitle;

    // console.log(currentTitle);

    if (currentSong.paused === true) {
        currentSong.play();
        UpdatePlayIcon(currentIcon);
        UpdatePageTitle(songTitle);
    } else {
        currentSong.pause();
        UpdatePlayIcon(currentIcon);
    }

    StopTracks(currentSong, currentIcon, id);
}

function StopTracks(currentSong, currentIcon, id) {
    for (i = 0, len = allSongs.length; i < len; i++) {
        if (allSongs[i]) {
            if (allSongs[i] != currentSong) {
                allSongs[i].pause();
            }
            if (songIcons[i] != currentIcon){
                if (songIcons[i].className != 'fa fa-check'){
                    songIcons[i].className = 'fa fa-play';
                }
            }
        }
    }
}

function ProcessEndedTrack(el) {
    var currentButton = el.parentElement;
    var currentIcon = currentButton.children[0];
    currentIcon.className = "fa fa-check";
    currentSong = null;
    UpdatePageTitle(mainTitle);
}

function UpdatePageTitle(title) {
  pageTitle[0].textContent = title;
  // console.log(pageTitle[0].textContent);
}

function UpdatePlayIcon(playIcon) {
    if (playIcon.className == 'fa fa-play'){
        playIcon.className = 'fa fa-circle-o-notch fa-spin';
    } else if (playIcon.className == 'fa fa-circle-o-notch fa-spin'){
        playIcon.className = 'fa fa-play';
    }
}

function ResumePlayBack(currentSong) {
    currentSong.play();
    UpdatePageTitle(songTitle);
}

// ------------------------------------
// ------------------------------------
// ------------------------------------
// ------------------------------------
// ------------------------------------

function ChangeStyle(ref) {
    // Adding highlight to the track and
    // removing highlight from others.
    var $song = ref;
    $($song).addClass('song-clicked');
    $($song).siblings().removeClass('song-clicked');
}

function GetId(ref) {
    // The id of the song element...
    var id = ref.children[0].id.replace('title-', '');
    var $song_id = id; // ref.id;
    return $song_id;
}

function DisplayAlbumMetadata(ref) {

    // The title of the song that was clicked
    // The artist of the song that was clicked...
    var $song_title = ref.children[0];
    var $song_artist = ref.children[1];

    // The album of the song that was clicked...
    // Replacing the albumHeader....
    var $song_album = ref.children[2];
    $('#albumHeader').html($song_album.innerText);

    // Artwork displayed on the screen...
    var $artwork = $('#artwork');

    // The main header of the page, above the artwork
    // Replacing the header text...
    var $page = $('#artistHeader')[0];
    $page.textContent = $song_artist.innerText;

    // Replacing the artwork...
    var image = document.getElementById('image-'+ GetId(ref));
    var imageSrc = image.getAttribute("src");
    $('#artwork').attr('src', imageSrc);
}

function ClickTrack(ref) {
  // The song element that was clicked...
  var $song = ref;
  ChangeStyle(ref);
  DisplayAlbumMetadata(ref);

};//end of ClickTrack
