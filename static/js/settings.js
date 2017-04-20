$( document ).ready(function(){
    var movie = document.getElementById("movieList");
    $.ajax({
        url: 'handleMovie',
        data: {
            'q': _question_num.toString(),
            'a': yn,
            'finish': false
        },
        dataType: 'json',
        success: function (data) {
            _question_num++;
            if(_question_num >= 10){
                window.location.href = '/tbd/movie/' + data["best_movie"];
            }
            $('#question').html(questions[_question_num]);
        }
    });
});