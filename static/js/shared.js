var _question_num = 0;

$( document ).ready(function(){
    var header = document.getElementById("header");
    header.innerHTML = "Delphi Recommendation Engine";
    
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
    if(_question_num >= 9 || yn == 0){
        $('#buttons').html(" ");
        $('#finish').html(" ");
    }

    $.ajax({
        url: 'handleQuestion',
        data: {
            'q': _question_num.toString(),
            'a': yn
        },
        dataType: 'json',
        success: function (data) {
            _question_num++;
            if(_question_num >= 10 || yn == 0){
                window.location.href = '/tbd/movie/' + data["best_movie"];
            }
            $('#question').html(questions[_question_num]);
        }
    });
};

// AJAX for posting
function submitResponse(like) {
    console.log("submitResponse is working!"); // sanity check

    $.ajax({
        url: '/tbd/handleResponse',
        data: {
            'like': like,
            'movie': movie_id
        },
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    });
};

function initQuestions() {
    for(_question_num = 0; _question_num < 10; ++_question_num){
        if(scores[_question_num] == 0){ break; }
    }
    $('#question').html(questions[_question_num]);
}

function streamingData(num) {
    var onoff = $('#Amazon').is(":checked") && num == 0;
    onoff = onoff || $('#AmazonPrime').is(":checked") && num == 1;
    onoff = onoff || $('#Netflix').is(":checked") && num == 2;
    onoff = onoff || $('#Hulu').is(":checked") && num == 3;
    onoff = onoff || $('#iTunes').is(":checked") && num == 4;
    onoff = onoff || $('#GooglePlay').is(":checked") && num == 5;
    alert(onoff);
    $.ajax({
        url: 'handleQuestion',
        data: {
            'q': num.toString(),
            'a': yn
        },
        dataType: 'json',
        success: function (data) {
            _question_num++;
            if(_question_num >= 10 || yn == 0){
                window.location.href = '/tbd/movie/' + data["best_movie"];
            }
            $('#question').html(questions[_question_num]);
        }
    });
}