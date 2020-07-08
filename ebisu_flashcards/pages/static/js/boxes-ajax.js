function callLoadBoxes(endpoint, renderer){
    callBackend(
        endpoint=endpoint,
        method = "GET",
        body = null,
        callback = function(data) {
            // Wait for the page to be loaded
            while (document.readyState === "loading") {};
            loadBoxesInDOM(data, renderer);
        }
    )
}

function callCreateNewBox(endpoint, renderer) {
    form = document.getElementById("create-box").getElementsByTagName("form")[0];
    form = serializeForm(form);

    callBackend(
        endpoint = endpoint,
        method = "POST",
        body = form,
        callback = function(data){
            hideNewFormInDOM();
            updateBoxInDOM(data, null, renderer);
        }
    )
}

function callUpdateBox(boxId, endpoint, renderer) {
    form = document.getElementById(""+boxId).getElementsByTagName("form")[0];
    form = serializeForm(form)

    callBackend(
        endpoint = endpoint,
        method = "PUT",
        body = form,
        callback = function(data){
            hideFormInDOM(boxId);
            updateBoxInDOM(data, boxId, renderer);
        }
    )
}

function callDeleteBox(boxId, endpoint) {
    callBackend(
        endpoint = endpoint,
        method = 'DELETE',
        body = null,
        callback = function(data){
            //hideFormInDOM(boxId);
            updateBoxInDOM(data, boxId);
        }
    )
}

