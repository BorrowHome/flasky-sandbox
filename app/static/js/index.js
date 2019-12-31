console.log('message')

console.log('加载js文件')

var video = document.getElementById("video_player");


function choose_a_video(obj) {
    console.log('click')
    console.log(obj.getAttribute('data'))
    console.log(video.videoWidth, 'innnn')
    console.log(video.videoHeight, 'innnn')

    console.log(obj.currentSrc)
    video.src = obj.currentSrc;

    video.load()
    // video.play()
    // 默认不让他播放
}

function setBackground(pictureURL) {
    $.ajax({
        url: "http://localhost:5000/background/",//请求路径
        data: {back_frame: pictureURL},
        type: "POST",//GET,
        async: false,
        success: function (resp) {
            //处理 resp.responseText;
            console.log(resp)
            console.log("设置背景")
            alert("设置背景成功")
        },
        error: function (a, b, c) {
            //a,b,c三个参数,具体请参考JQuery API
        }
    })
}


function getCurrentFrames(scale) {

    var canvas = document.createElement("canvas");
    console.log(scale)
    canvas.width = video.videoWidth * scale;
    console.log(video.videoWidth)
    canvas.height = video.videoHeight * scale;
    canvas.getContext('2d')
        .drawImage(video, 0, 0, canvas.width, canvas.height);  //可以只截取一部分图像  。。
    pictureURL = canvas.toDataURL('image/png');
    console.log(pictureURL)

    return pictureURL
}

function uploadPicture(pictureURL) {


    echart_data = ""
    console.log(' upload ')
    $.ajax({
        url: "http://localhost:5000/picture/",//请求路径
        data: {current_frame: pictureURL},
        type: "POST",//GET,
        async: false,
        //dataType: "JSON",//需要返回JSON对象(如果Ajax返回的是手动拼接的JSON字符串,需要Key,Value都有引号)
        success: function (resp) {
            //处理 resp.responseText;
            console.log(resp)
            echart_data = resp
        },
        error: function (a, b, c) {
            //a,b,c三个参数,具体请参考JQuery API
        }
    })

    return echart_data
}

function submitForm() {

    formdata = $("#site_form").serialize()
    $.post("http://localhost:5000/site/",
        formdata,
        function (data) {
            console.log(data)
        }
    )
}

function setBackgroundByFrame() {
    var scale = 0.3
    var pictureURL = getCurrentFrames(scale)
    setBackground(pictureURL)
}


