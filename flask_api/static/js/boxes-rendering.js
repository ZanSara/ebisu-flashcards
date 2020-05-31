/* 
 * Given a box data and a box,
 * returns a box with the updated data rendered in.
 */
function renderBox(data, box, renderCallback){
    
    // Render proper data in the template
    box.id = data._id.$oid;

    renderCallback(data, box);

    // Append extra fields in form
    extraFields = box.getElementsByClassName("extra-fields")[0];
    extraFields.innerHTML = data.extra_fields;

    // Render the extra field values
    for (const input of extraFields.querySelectorAll("input[type=checkbox]")){
        input.checked = data[input.name];
    }

    // Render box id into the HREFs
    for (const element of box.getElementsByTagName('a')) {
        const oldUrl = element.getAttribute("href");
        if (oldUrl) {
            element.setAttribute("href", oldUrl.replace("_box_id_", data._id.$oid ));
        }
    }
    for (const element of box.getElementsByTagName('button')) {
        const oldValue = element.getAttribute("onclick");
        if (oldValue) {
            element.setAttribute("onclick", oldValue.replace("_box_id_", data._id.$oid ));
        }
    }
    // Return rendered box
    return box;
}



/* 
 * Given a box data and the template, 
 * returns a new box with the new data rendered in.
 */
function createBox(data, template, renderer){

    // Clone template & remove the hiding class
    var box = template.cloneNode(true);
    box.classList.remove("hidden");
    
    renderBox(data, box, renderer);

    // Return rendered copy
    return box;
}



/* 
 * Given a box id, removes its box.
 * Fails if box does not exits.
 */
function removeBox(box_id){
    document.getElementById(box_id).remove();
    pageModeRead();
}



/* 
 * Puts the page into Read Mode 
 * (no visible forms)
 */
function pageModeRead(){

    // Enable all buttons for the boxs
    for (const box of document.getElementsByClassName('box')){
        for (const element of box.getElementsByTagName('button')) {
            element.removeAttribute("disabled");
        }
        for (const element of box.getElementsByTagName('a')) {
            element.removeAttribute("disabled");
        }    
    }
    // Enable New box button
    newboxDiv = document.getElementById('create-box');
    newboxDiv.classList.remove("hidden");
    newboxDiv.getElementsByTagName("button")[0].removeAttribute("disabled");   

    // Hide all forms 
    forms = document.getElementsByTagName('form');
    for (const form of forms){
        form.classList.add("hidden");
    }
    
    // Display all static-info
    displays = document.getElementsByClassName("static-info");
    for (const display of displays){
        display.classList.remove("hidden");
    }    
    
    // Reset the Newbox form & hide all extra fields
    form = document.getElementById('create-box').getElementsByTagName("form")[0];
    form.reset();
    for (const fields of form.getElementsByClassName("extra-fields")){
        fields.classList.add("hidden");
    }
}



/* 
 * Puts the page into Edit Mode 
 * (everything disabled, caller should re-enable its components) 
 */
function pageModeEdit(){
    
    // Disable all buttons for the boxs
    for (const box of document.getElementsByClassName('box')){
        for (const element of box.getElementsByTagName('button')) {
            element.setAttribute("disabled", "disabled");
        }
        for (const element of box.getElementsByTagName('a')) {
            element.setAttribute("disabled", "disabled");
        }    
    }
    // Disable New box button
    newboxButton = document.getElementById('create-box').getElementsByTagName("button")[0];
    newboxButton.setAttribute("disabled", "disabled");
}
