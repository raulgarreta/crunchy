

//PROD
var URL = "http://app.crunchyapp.com";
var API_TOKEN = "a4f9863905788d9e08db6003c1dcb91e45955beb";




// stores original size of image used by jcrop for the event thumbnail
var originalW;
var originalH;

var app = {
    // Application Constructor
    initialize : function() {
        this.bindEvents();
        detectBrowser();
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




function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function afterChildClose() {
    // After the login window is closed

    $.ajax({
        url : URL + "/api/get_api_token/",
        type : "GET",
        data : {
            token : key_token
        },
        success : function(result) {
            // store the api token in local storage
            localStorage.setItem('api_token', result.api_token);
            current_events = result.current_events;

            // setup authorization header for ajax requests to api
            $.ajaxSetup({
                beforeSend : function(xhr, settings) {
                    xhr.setRequestHeader("Authorization", "Token " + API_TOKEN);
                }
            });

            // move to event-history screen
            $.mobile.changePage("event-list.html");

        },
        error : function(e) {
            alert('Error: ' + e);
        }
    });

}

//OK
function debugMode() {

    $.ajaxSetup({
        beforeSend : function(xhr, settings) {
            xhr.setRequestHeader("Authorization", "Token " + API_TOKEN);
        }
    });

    DEBUG = true;
    $.ajax({
        url : URL + "/api/login/",
        type : "GET",
        data : {},
        success : function(result) {
            api_token = result.api_token;
            current_events = result.current_events;

            // store the api token in local storage
            //localStorage.setItem('api_token', api_token);



            $.mobile.changePage('topic-list.html');
        },
        error : function(e) {
            alert('Error: ' + e);
        }
    });


/*******************************************************************************
 * SIGN-IN
 ******************************************************************************/

//OK
$(document).on('pagebeforeshow', '#sign-in-page', function(e, data) {

    api_token = localStorage.getItem('api_token');
    if (api_token != null) {
        // setup authorization header for ajax requests to api
        $.ajaxSetup({
            beforeSend : function(xhr, settings) {
                xhr.setRequestHeader("Authorization", "Token " + api_token);
            }
        });

        // check the authentication token
        $.ajax({
            url : URL + "/api/event_history/",
            type : "GET",
            data : {},
            success : function(result) {

                $.mobile.changePage("event-list.html");

            },
            error : function(e) {
                // continue to authenticate
            }
        });

    }

});

//OK
function detectBrowser() {

    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1) {
        browser_type = 'mobile';
    } else {
        browser_type = 'web';
    }
}


//OK
function logout() {

    $.mobile.loading('show');
    localStorage.removeItem('api_token');
    $.mobile.changePage('index.html');
    $.mobile.loading('hide');

}

