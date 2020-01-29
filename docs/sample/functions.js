
function sendValue (url) {
            jQuery.get( url )
}

function sendData () {

    var urlbase = 'http://localhost:8000'
    var params = '?cookie=' + document.getElementById('data').value;
    var url = urlbase + params
    sendValue (url)
}

function setCookie () {

    document.cookie = "username=sample;";
    document.write (document.cookie);
    document.setElementById('data').value = "something";

}