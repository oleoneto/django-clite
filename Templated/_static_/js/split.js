//
// split.js
// Based on a project by Traversy Media.
// EKOS Visual Framework.
// Developed by Leo Neto on Dec 20, 2017.
// Ekletik Studios. Open-source License.


$(document).ready(function () {
    var wrapper = $('#wrapper');
    var topLayer = $('#wrapper .top');
    var handle = $('.handle');
    var skew = 0;
    var delta = 0;
    if(wrapper.hasClass('skewed')){
        skew = 1000;
    }
    wrapper.on('mousemove', function(e) {
        delta = (e.clientX - window.innerWidth/2) * 0.5;
        handle.css("left", e.clientX+delta+'px');
        topLayer.css("width", e.clientX+skew+delta+'px');
    });
});