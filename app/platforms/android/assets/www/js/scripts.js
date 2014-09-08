
//PROD
var URL = "http://app.crunchyapp.com";
var API_TOKEN = "a4f9863905788d9e08db6003c1dcb91e45955beb";

var topics;


//OK
function detectBrowser() {

    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1) {
        browser_type = 'mobile';
    } else {
        browser_type = 'web';
    }
}


var app = {
    // Application Constructor
    initialize : function() {
        this.bindEvents();
        //detectBrowser();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents : function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicity call 'app.receivedEvent(...);'
    onDeviceReady : function() {
        app.receivedEvent('deviceready');
    },
    // Update DOM on a Received Event
    receivedEvent : function(id) {

    }
};



//OK
function debugMode() {

    $.ajaxSetup({
        beforeSend : function(xhr, settings) {
            xhr.setRequestHeader("Authorization", "Token " + API_TOKEN);
        }
    });

    DEBUG = true;
    $.ajax({
        url : URL + "/api/login/?twitter_account=raulgarreta",
        type : "GET",
        data : {},
        success : function(result) {

            result = eval(result)
            $('#topic-list').empty();

             for (var i in result) {
                n = result[i]
                $('#topic-list').append(n[0] + ' - ');
             }

            $.mobile.changePage('#topic-list-page');
        },
        error : function(e) {
            alert('Error: ' + e);
        }
    });

};

$( "#loginbutton" ).click(function() {
  $.ajaxSetup({
        beforeSend : function(xhr, settings) {
            xhr.setRequestHeader("Authorization", "Token " + API_TOKEN);
        }
    });

    DEBUG = true;
    $.ajax({
        url : URL + "/api/login/?twitter_account=" + $("#search1").val(),
        type : "GET",
        data : {},
        success : function(result) {

            result = eval(result)
            $('#categories').empty();

             for (var i in result) {
                n = result[i]
                $('#categories').append(
                    '<input type="checkbox" name="checkbox-v-2a" id="checkbox-v-2a" checked="checked"><label for="checkbox-v-2a">' + n[0] + '</label>');
             }

            $.mobile.changePage('#page2');
        },
        error : function(e) {
            alert('Error: ' + e);
        }
    });

});


//OK
function logout() {

    $.mobile.loading('show');
    localStorage.removeItem('api_token');
    $.mobile.changePage('index.html');
    $.mobile.loading('hide');

}



//OK
function showSummary() {


    DEBUG = true;
    $.ajax({
        url : URL + "/api/last_news_list/?twitter_account=raulgarreta",
        type : "POST",
        data : {},
        success : function(result) {

            result = eval(result)
            $('#article-list').empty();

             for (var i in result) {
                n = result[i]
                $('#article-list').append(n.title + '<br>');
             }

            $.mobile.changePage('#article-list-page');
        },
        error : function(e) {
            alert('Error: ' + e);
        }
    });

};


//OK
 $(document).on('pageshow', '#topic-list-page', function(e, data) {


     // empty list



 });



