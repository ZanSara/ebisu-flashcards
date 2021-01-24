/* 
 * Retrieve cookie by name.
 * Returns null if not found.
 */
function getCookie(cookieName) {
    var name = cookieName + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieEntries = decodedCookie.split(';');

    for(var i = 0; i <cookieEntries.length; i++) {
        var cookieEntry = cookieEntries[i];
        while (cookieEntry.charAt(0) == ' ') {
            cookieEntry = cookieEntry.substring(1);
        }
        if (cookieEntry.indexOf(name) == 0) {
            return cookieEntry.substring(name.length, cookieEntry.length);
        }
    }
    return null;
}


/*
 * Given a Form element, returns its JSON representation.
 * Checkboxes are always all present, with a true/false value.
 */
function serializeForm(form){

    // Create the form data object to be passed to JSON
    formData = new FormData(form);
    formJSON = {}
    formData.forEach(function(value, key){
        formJSON[key] = value;
    });
    // Render the checkbox as true/false values
    for (const checkbox of form.querySelectorAll('input[type=checkbox')) {
        formJSON[checkbox.name] = checkbox.checked;
    }
    return JSON.stringify(formJSON);
}


/*
 * Perform fetch call to the backend, 
 * authenticating with the various cookies.
 */
function callBackend(endpoint, method, body, callback, errorCallback = reportError, params, prefix=""){

    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch(prefix+endpoint, 
        {   
            method: method,
            headers:  new Headers({
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'X-CSRF-TOKEN': csrf_token,
            }),
            body: body,
            credentials: 'include'
    })
    .then(res => {
        if (!res.ok) {
            console.log(res);
            return Promise.reject(res);
        }
        return res;
    })
    .then(res => {
        console.log(res);
        return res.json();
    })
    .then(data => callback(data, params))
    .catch(errorCallback);  /* TODO: HANDLE BETTER */
}


/* TODO: HANDLE BETTER */
function reportError(error) {
    console.log(error);
    alert("An error occured.");
}
