function getXHR(){
    var xhr = false;
    if (window.XMLHttpRequest) {
        xhr = new XMLHttpRequest();
    } else { //code for IE6, IE5
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhr;
}

function goBack() {
    window.history.back();
}

function handleClick(self) {

    xhr = getXHR();
    if(!xhr) alert("Ajax is not supported by your browser!");

    xhr.onload = function() {
        if (xhr.status === 200){
            //reload page
	    location.reload();
        }
        else{
            alert("Error " + xhr.status);
        }
    }

    xhr.onerror = function() {
        alert("Error: No response from server.");
    }

    xhr.open('GET', "/display/?type=" + self.value);
    xhr.send(null);

}
