console.log('message')

console.log('加载js文件')

var video = document.getElementById("video_player");


function choose_a_video(obj) {
    console.log('click')
    console.log(obj.getAttribute('data'))
    console.log(video.videoWidth, 'innnn')
    console.log(obj.currentSrc)
    video.src = obj.currentSrc;
    video.load()
    video.play()
}


function getCurrentFrames() {

    var scale = 0.4
    var canvas = document.createElement("canvas");
    canvas.width = video.videoWidth * scale;
    canvas.height = video.videoHeight * scale;
    canvas.getContext('2d')
        .drawImage(video, 0, 0, canvas.width, canvas.height);  //可以只截取一部分图像  。。
    pictureURL = canvas.toDataURL('image/png');
    console.log(pictureURL)

    uploadPicture(pictureURL)

}

function uploadPicture(pictureURL) {

    /* 向服务器上传数据，并把返回的数据给 echart 显示  */

    echart_data = ""
    console.log(' upload ')
    $.post("http://localhost:5000/picture/",
        {
            "current_frame": pictureURL
        }
        , function (data) {
            console.log(data)
            echart_data = data
        });

    return echart_data
}

/*
事件被触发的时候启动
video.addEventListener('play', function () {

    console.log(' time update')
});
*/


function submitForm() {

    formdata = $("#site_form").serialize()
    $.post("http://localhost:5000/site/",
        formdata,
        function (data) {
            console.log(data)
        }
    )
    return false
}