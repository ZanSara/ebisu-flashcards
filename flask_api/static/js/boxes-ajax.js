function loadBoxes(endpoint, renderer){
    callBackend(
        endpoint=endpoint,
        method = "GET",
        body = null,
        callback = function(data) {
            // Wait for the page to be loaded
            while (document.readyState === "loading") {};
            initialBoxesRendering(data, renderer);
        }
    )
}

function createNewBox(endpoint, renderer) {
    form = document.getElementById("create-box").getElementsByTagName("form")[0];
    form = serializeForm(form);

    callBackend(
        endpoint = endpoint,
        method = "POST",
        body = form,
        callback = function(data){
            hideNewForm();
            updateBoxData(data, null, renderer);
        }
    )
}

function updateBox(boxId, endpoint, renderer) {
    form = document.getElementById(""+boxId).getElementsByTagName("form")[0];
    form = serializeForm(form)

    callBackend(
        endpoint = endpoint,
        method = "PUT",
        body = form,
        callback = function(data){
            hideForm(boxId);
            updateBoxData(data, boxId, renderer);
        }
    )
}

function deleteBox(boxId, endpoint) {
    callBackend(
        endpoint = endpoint,
        method = 'DELETE',
        body = null,
        callback = function(data){
            hideForm(boxId);
            updateBoxData(data, boxId);
        }
    )
}

