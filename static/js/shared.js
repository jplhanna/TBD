var _question_num = 0;

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

// AJAX for posting
function submit(yn) {
    console.log("yes is working!") // sanity check
    if(_question_num >= 9){
        $('#buttons').html(" ");
    }

    $.ajax({
        url: 'handleQuestion',
        data: {
            'q': _question_num.toString(),
            'a': yn,
            'finish': false
        },
        dataType: 'json',
        success: function (data) {
            _question_num++;
            if(_question_num >= 10){
                alert(data['best_movie']);
            }
            $('#question').html(questions[_question_num]);
        }
    });
};

function initQuestions() {
    for(_question_num = 0; _question_num < 10; ++_question_num){
        if(scores[_question_num] == 0){ break; }
    }
    $('#question').html(questions[_question_num]);
    alert("HEY");
}