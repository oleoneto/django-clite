/*
// spotify.js
// EKOS Visual Framework.
// EKOS is based on Bootstrap 4 and jQuery.
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



$(document).ready(function() {
    console.log("Loaded spotify.js");

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
