
/*
 * Spawns many new boxes at the end of the boxes list.
 * New Box button is kept at the very end.
 */
function appendBoxesInDOM(dataList, renderer){

    var template = document.getElementById("box-template");

    for (const data of dataList){
        var box = renderNewBox(data, template, renderer);
        document.getElementById("boxes-container").appendChild(box);
    }
    
    // Move the New Box button after the box
    newBox = document.getElementById("create-box");
    document.getElementById("boxes-container").appendChild(newBox);
}


/*
 * Spawns a new box at the end of the boxes list.
 * New Box button is kept at the very end.
 */
function appendBoxInDOM(data, renderer){
    appendBoxesInDOM([data], renderer);
}



/*
 * Invoked at load, renders every box using the data
 * received from the caller.
 */
function loadBoxesInDOM(boxesList, renderer) {

    // Remove loading icon if present
    document.getElementById("loading").classList.add("hidden");
    
    appendBoxesInDOM(boxesList, renderer);

    // Display the New ox button & reset its form for good measure
    newBox = document.getElementById("create-box");
    newBox.classList.remove("hidden");
    newBox.getElementsByTagName("form")[0].reset();
}


/*
 * Updates the representation of a single box,
 * either creating a box, updating an existing one, 
 * or deleting one.
 */
function updateBoxInDOM(data, boxId, renderer){
    
    if (data === ""){
        // Box was deleted
        removeBox(""+boxId);

    } else {
        if (boxId) {
            // Existing box
            box = document.getElementById(""+boxId);
            renderBox(data, box, renderer);

        } else {
            // New Box
            appendBoxInDOM(data, renderer);
        }
    }
}

/* 
 * Invoked when clicking on the EDIT button of a static box.
 * Swaps the static representation with the form representation.
 *   
 *      Requires the boxId
 */
function showFormInDOM(boxId) {

    pageModeEdit();    

    // Find selected box and the form template
    box = document.getElementById(""+boxId);  // Necessary to make boxId a string and match
    display = box.getElementsByClassName("static-info")[0];
    form = box.getElementsByTagName("form")[0];

    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    

    // Show the form of the selected box & hide the static data
    display.classList.add("hidden");
    form.classList.remove("hidden");
    box.appendChild(form);
}


/* 
 * Invoked when clicking on the CANCEL button of a box form.
 * Swaps the form representation with the static representation.
 *   
 *      Requires the boxId
 */
function hideFormInDOM(boxId) {
    pageModeRead();
}

/* 
 * Invoked when clicking on the New [Card/Deck] button.
 * Hides the button itself and adds a new div with an empty
 * form.
 */
function showNewFormInDOM() {

    pageModeEdit();

    // Find div
    box = document.getElementById('create-box');
    form = box.getElementsByTagName("form")[0];
    button = box.getElementsByTagName("button")[0];

    // Add the box class to the div
    box.classList.add("box");

    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    

    // Hide the New Box button
    button.setAttribute("disabled", "disabled");
    button.classList.add("hidden");

    // Show the form
    form.classList.remove("hidden");
}

/* 
 * Invoked when clicking on the Cancel button into a New Box form.
 * Hides the form and restores the button
 */
function hideNewFormInDOM() {

    pageModeRead();

    // Find div
    box = document.getElementById('create-box');
    form = box.getElementsByTagName("form")[0];
    button = box.getElementsByTagName("button")[0];
    
    // Remove the box class to the div
    box.classList.remove("box");
    
    // Show the New Box button
    button.removeAttribute("disabled");
    button.classList.remove("hidden");
}
