console.log('message')

console.log('加载js文件')


var video = document.getElementById("video_player");


function choose_a_video(obj) {
    console.log('click')
    console.log(obj.getAttribute('data'))
    console.log(obj.currentSrc)
    video.src = obj.currentSrc;
    video.load()
    video.play()
}


function playVid() {
    video.play();
}

function pauseVid() {
    video.pause();
}
