$(document).ready(function() {
    firstBotMessage();
});


function replaceEnter(str)
{
    if (str == undefined || str == null) return "";

    str = str.replace(/\r\n/ig, '<br>');
    str = str.replace(/\\n/ig, '<br>');
    str = str.replace(/\n/ig, '<br>');
    return str
}



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var xhr;

function sendAsk() {
    ctext = document.getElementById("chattext").value;
    if(ctext == "") {
        document.getElementById("chattext").focus();
        return false;
    }

    addtext = "<div class='chatMe'> <span>" + ctext + "</span></div>";
    document.getElementById("chatbox").innerHTML += addtext;

    var strurl = "chat?chatinput=" + ctext;

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var data = xhr.responseText;

            var obj = JSON.parse(data);

            if(obj.flag == "0"){
                ans = replaceEnter(obj.chatanswer)
                bottext = "<div class='chatBot'><span>" + ans + "</span></div>";
                document.getElementById("chatbox").innerHTML += bottext;

                var objDiv = document.getElementById("chatbox");
                objDiv.scrollTop = objDiv.scrollHeight;

                document.getElementById("chattext").value = "";
                document.getElementById("chattext").focus();
            }
        }
    };

    xhr.open("GET", strurl);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(null);

}