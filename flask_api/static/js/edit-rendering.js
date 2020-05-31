/* 
 * Given a card data and a box,
 * returns a box with the updated data rendered in.
 */
function updateBox(data, card){
    
    // Render proper data in the template
    card.id = data._id.$oid;
    card.getElementsByClassName("question")[0].innerHTML = data.question;
    card.getElementsByClassName("question-form")[0].value = data.question;
    card.getElementsByClassName("answer")[0].innerHTML = data.answer;
    card.getElementsByClassName("answer-form")[0].value = data.answer;

    // Append extra fields in form
    extraFields = card.getElementsByClassName("extra-fields")[0];
    extraFields.innerHTML = data.extra_fields;

    // Render the extra field values
    for (const input of extraFields.querySelectorAll("input[type=checkbox]")){
        input.checked = data[input.name];
    }

    // Render card id into the HREFs
    for (const element of card.getElementsByTagName('a')) {
        const oldUrl = element.getAttribute("href");
        if (oldUrl) {
            element.setAttribute("href", oldUrl.replace("_card_id_", data._id.$oid ));
        }
    }
    for (const element of card.getElementsByTagName('button')) {
        const oldValue = element.getAttribute("onclick");
        if (oldValue) {
            element.setAttribute("onclick", oldValue.replace("_card_id_", data._id.$oid ));
        }
    }
    // Return rendered card
    return card;
}



/* 
 * Given a card data and the template, 
 * returns a new box with the new data rendered in.
 */
function createBox(data, template){

    // Clone template & remove the hiding class
    var card = template.cloneNode(true);
    card.classList.remove("hidden");
    
    updateBox(data, card);

    // Return rendered copy
    return card;
}



/* 
 * Given a card id, removes its box.
 * Fails if box does not exits.
 */
function deleteBox(card_id){
    document.getElementById(card_id).remove();
}



/* 
 * Puts the page into Read Mode 
 * (no visible forms)
 */
function pageModeRead(){

    // Enable all buttons for the cards
    for (const card of document.getElementsByClassName('card')){
        for (const element of card.getElementsByTagName('button')) {
            element.removeAttribute("disabled");
        }
        for (const element of card.getElementsByTagName('a')) {
            element.removeAttribute("disabled");
        }    
    }
    // Enable New card button
    newcardDiv = document.getElementById('create-card');
    newcardDiv.classList.remove("hidden");
    newcardDiv.getElementsByTagName("button")[0].removeAttribute("disabled");   

    // Hide all forms 
    forms = document.getElementsByTagName('form');
    for (const form of forms){
        form.classList.add("hidden");
    }
    
    // Display all static-info
    displays = card.getElementsByClassName("static-info");
    for (const display of displays){
        display.classList.remove("hidden");
    }    
    
    // Reset the Newcard form & hide all extra fields
    form = document.getElementById('create-card').getElementsByTagName("form")[0];
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
    
    // Disable all buttons for the cards
    for (const card of document.getElementsByClassName('card')){
        for (const element of card.getElementsByTagName('button')) {
            element.setAttribute("disabled", "disabled");
        }
        for (const element of card.getElementsByTagName('a')) {
            element.setAttribute("disabled", "disabled");
        }    
    }
    // Disable New card button
    newcardButton = document.getElementById('create-card').getElementsByTagName("button")[0];
    newcardButton.setAttribute("disabled", "disabled");
}
