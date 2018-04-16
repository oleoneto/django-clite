//
// drag.js
// Based on W3 Schools.
// EKOS Visual Framework.
// Developed by Leo Neto on Dec 20, 2017.
// Ekletik Studios. Open-source License.

$(document).ready( function () {
   console.log("Loaded drag.js")

});


function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}