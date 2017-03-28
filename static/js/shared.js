$( document ).ready(function(){
    var header = document.getElementById("header");
    header.innerHTML = "Delphi Recommendation Engine";
    header.style.color = "rgb(155, 102, 102)";
    
    var answer = document.getElementById("answer");
    answer.innerHTML = "--not yet answered--";
    answer.style.color = "rgb(200, 200, 200)";
    answer.style.fontSize = "35px";
});

function clickYes() {
    var answer = document.getElementById("answer");
    answer.innerHTML = "-- answered yes --";
}

function clickNo () {
    var answer = document.getElementById("answer");
    answer.innerHTML = "-- answered no --";
}