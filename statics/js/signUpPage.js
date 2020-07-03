let count = 1;


$(document).ready(
    function () {
        setInterval(function () {

            let pathPrev = 'url("../statics/img/signUp_background_pic' + count + '.jpg")';

            count += 1;

            if (count === 8){
                count = 1;
            }

            let path = 'url("../statics/img/signUp_background_pic' + count + '.jpg")';

            $('#main').animate(
                {
                "filter":"Alpha(opacity=0)","opacity":"0"
            }, 4000, function () {
                    $('#main').css({'background': path + " no-repeat center center"});
                    $('#main').animate(
                        {
                            "filter":"Alpha(opacity=100)","opacity":"1",
                            // 'background': path + " no-repeat center center"
                        }, 4000);
                });

        }, 6000)

    }
)

