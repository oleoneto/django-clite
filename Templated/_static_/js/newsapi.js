/*
// newsapi.js
// Developed by Leo Neto on Dec 17, 2017
// Ekletik Studios. Open-source License.
*/

let timeInterval = 60 * 1000
let country = 'pt';
let apikey = 'YOUR_AKI_KEY_HERE';
let requestURL = 'https://newsapi.org/v2/top-headlines?country='+ country +'&apiKey=' + apikey;
let $news = $('#news');

$(document).ready(function () {
    NewsApi();
});


function NewsApi() {
    var random = Math.random()*4;
    random = Math.floor(random);
    var requestObject = new XMLHttpRequest();
    var index = 0;

    requestObject.open('GET', requestURL);
    requestObject.onload = function () {
        var parsedResponse = JSON.parse(requestObject.responseText);
        var articles = parsedResponse.articles;
        var length = parsedResponse.articles.length;
        var article = "";
        var count = 0;
        for (index; index < length; index++) {
            if (articles[index].urlToImage != null) {
                if (articles[index].description.length > "50") {
                    count += 1;
                    article += '<div class="col-md-4 bottom-10">';
                    article += '<div>';
                    article += '<img class="img-fluid border-radius img-news" src="' + articles[index].urlToImage + '">';
                    article += '<p><span>' + articles[index].source.id + '</span></p>';
                    article += '<a href="' + articles[index].url + '" target="_blank">';
                    article += '<h4>' + articles[index].title + '</h4>';
                    article += '</a>';
                    article += '<div class="news-content">' + articles[index].description + '</div>';
                    article += '</div>';
                    article += '</div>';
                }
                // Limits the articles to 3
                if (count==3) { index=length; }
            }
        }
        news.innerHTML = article ;
    };
    requestObject.send();
    var requestAPI = setInterval(NewsApi, timeInterval);

    // Debugging log...
    console.log("News updates from NewsApi");
}
