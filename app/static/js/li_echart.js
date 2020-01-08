var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
var data = {};
option = null;
option = {
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            params = params[0];
            y = params.value;
            x = params.name;
            // console.log("写一点"+params.data+params.value+params.name)
            // return params.data+params.value;
            return params.name + "," + params.value;
        },
        axisPointer: {
            animation: false
        }
    },
    xAxis: {
        type: 'category',
        // type:'time',
        // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        data: [100, 200, 300, 400, 500, 600, 700]
    },

    yAxis: {
        min: 0,
        max: 80,
        type: 'value'
    },
    series: [{
        data: [1, 2, 3, 4, 5, 6, 7],
        type: 'line',
        smooth: true
    }],

};
myChart.on('click', function (params) {
    older_data1 = x;
    // older_data2=params[0].value;
    older_data2 = y;
    document.getElementById("ds").innerHTML = "当前位置 (" + older_data1 + "," + older_data2 + ")";
    // document.getElementById("new_data_x").value=older_data1;
    document.getElementById("new_data_x").innerHTML = older_data1;
    document.getElementById("new_data_y").value = older_data2;
});
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

    //html我们可以通过属性得到他们的当前位置。
    // video.currentTime = 1577
    console.log(video.currentTime)


}, 2000);
;

function setCurrentFrame() {

    console.log(
        "播放数据  嘻嘻"
    )
    var scale = 1
    var pictureURL = getCurrentFrames(scale)
    data = uploadPicture(pictureURL)
    for (i = 0; i < data["list_y"].length; i++) {

        data["list_y"][i] = data["max"] - data["list_y"][i]
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
    ;

    alert("处理成功")

}


function change_data() {
    alert('修改数据');

    console.log(
        "播放数据  嘻嘻"
    )

    data_x = parseInt(document.getElementById("new_data_x").innerHTML);
    data_y = parseInt(document.getElementById("new_data_y").value);
    document.getElementById("newer_data").innerHTML = "修改后的数据(" + data_x + "," + data_y + ")";
    $.ajax({
        url: "http://localhost:5000/change_datas/",//请求路径
        data: {current_frame: JSON.stringify([data_x, data_y])},
        type: "POST",//GET,
        async: false,
        traditional: true,
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

    for (var i = 0; i < data["list_x"].length; i++) {
        if (data_x == data["list_x"][i]) {
            data["list_y"][i] = data_y;
            break;
        }
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

