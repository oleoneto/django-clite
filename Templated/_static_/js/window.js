/*
// window.js
// Requires spotify.js
// EKOS Visual Framework
// Developed by Leo Neto on Dec 18, 2017
// Ekletik Studios. Open-source License.
*/

$(document).ready(function() {
    window.addEventListener('offline', networkStatus);
    window.addEventListener('online', networkStatus);

    function networkStatus(e) {
        if (e.type == 'offline') {
            $("#offline-alert").removeClass("display-none");
            // $(".alert").alert();
        } else {
            // $(".alert").alert('close');
            $("#offline-alert").addClass("display-none");
        }
    }

});
