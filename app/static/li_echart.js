var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
option = null;
option = {
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },

    yAxis: {
        type: 'value'
    },
    series: [{
        data: [1, 2, 3, 4, 5, 6, 7],
        type: 'line',
        smooth: true
    }]
};

setInterval(function () {

    if (video.paused == false) {
        console.log(
            "播放数据  嘻嘻"
        )

        /*        var data = getCurrentFrames()

                myChart.setOption({
                    series: [{
                        data: data['list_y']
                    }]
                });
                myChart.setOption({
                    xAxis: {
                        data: data['list_x']
                    }
                })*/
    }


}, 2000);
;

function setCurrentFrame() {

    console.log(
        "播放数据  嘻嘻"
    )

    var pictureURL = getCurrentFrames()
    var data = uploadPicture(pictureURL)

    for (i = 0; i < data["list_y"].length; i++) {

        data["list_y"][i] = 244 - data["list_y"][i]
    }

    myChart.setOption({
        series: [{
            data: data['list_y']
        }]
    });
    myChart.setOption({
        xAxis: {
            data: data['list_x']
        }
    })

    alert("处理成功")

}

if (option && typeof option === "object") {
    myChart.setOption(option, true);
}
