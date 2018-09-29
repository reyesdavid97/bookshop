

var creditcardNumberElementId = "creditcard-number";
var creditcardIconsElementId = "icons";
var creditcardNumberElement = document.getElementById(creditcardNumberElementId);
var creditcardIconsElement = document.getElementById(creditcardIconsElementId);

// to insert the credit cards icons after the input element
creditcardNumberElement.parentNode.insertBefore(creditcardIconsElement,creditcardNumberElement.nextSibling);



// pattern to match
var visaPattern = /^4[0-9]{12}(?:[0-9]{3})?$/;
var mastercardPattern = /^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$/;
var aexpressPattern = /^3[47][0-9]{13}$/;
var discoverPattern = /^6(?:011|5[0-9]{2})[0-9]{12}$/;

// no magic strings/numbers
var baseDir = "/static/img/";
var visa = 'visa';
var mastercard = 'mastercard';
var discover = 'discover';
var aexpress = 'aexpress';
var greyedPrefix = '_g';
var extension = '.png';
var elementIndex = 0;
var patternIndex = 1;

//
var creditcardIcons = {
    visa        : [document.getElementById(visa),       visaPattern],
    mastercard  : [document.getElementById(mastercard), mastercardPattern],
    discover    : [document.getElementById(discover),   discoverPattern],
    aexpress    : [document.getElementById(aexpress),   aexpressPattern]
}

document.getElementById(creditcardNumberElementId).onchange = function(){
    this.value = this.value.trim();
    handleInput(this.value);
}

document.getElementById(creditcardNumberElementId).onkeypress = function(){
    this.value = this.value.trim();
    handleInput(this.value);
}

document.getElementById(creditcardNumberElementId).onkeyup = function(){
    this.value = this.value.trim();
    handleInput(this.value);
}

document.getElementById(creditcardNumberElementId).onpaste = function(){
    this.value = this.value.trim();
    handleInput(this.value);
}

function handleInput(text){
    console.log("here");
    for (var key in creditcardIcons){
        var pattern = creditcardIcons[key][patternIndex];
        var element = creditcardIcons[key][elementIndex];
        if (pattern.test(text)) activateIcon(element)
        else inactivateIcon(element);
    }
}

function activateIcon(element){
    setIcon(element,true);
}

function inactivateIcon(element){
    setIcon(element,false);
}

function setIcon(element,set){
    var id = element.id;
    var filename = baseDir + id + ( set ? extension : greyedPrefix + extension );
    element.src = filename;

}

// check for a number loaded with the form
handleInput(creditcardNumberElement.value);

    
