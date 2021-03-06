var _question_num = 0;

$( document ).ready(function(){
    var header = document.getElementById("header");
    header.innerHTML = "Delphi Recommendation Engine";
    
    var answer = document.getElementById("answer");
    answer.innerHTML = "--not yet answered--";
    answer.style.color = "rgb(200, 200, 200)";
    answer.style.fontSize = "35px";
});

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
    var list = window.location.href.split("/");
    var movie_id = list[list.length - 2];

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
    $.ajax({
        url: '/tbd/handleStreamingServices',
        data: {
            'service': num.toString(),
            'toggle': onoff
        },
        dataType: 'json',
        success: function (data) {
            console.log("Success!");
        }
    });
}

function addToFav(add, id) {
    var movie_id = "1";
    if (add == 1){
        var list = window.location.href.split("/");
        if(list[list.length - 1] == ""){
            movie_id = list[list.length - 2];
        }else{
            movie_id = list[list.length - 1];
        }
    }else{
        movie_id = id;
    }
    $.ajax({
        url: '/tbd/added',
        data: {
            'movie_id': movie_id,
            'add': add
        },
        dataType: 'json',
        success: function (data) {
            console.log("Success!");
        }
    });
}