var videos = document.getElementsByClassName("video_player")

var video_run = document.getElementById("multi-video-run")
var video_stop = document.getElementById("multi-video-stop")
var set_background = document.getElementById("site-change-set-background")
var set_currentframe = document.getElementById("site-change-set-currentframe")
var save_image = document.getElementById("save_image")

var chart = document.getElementById("chart")

var site_left_top = document.getElementById("site_left_top")
var site_left_bottom = document.getElementById("site_left_bottom")
var site_right_top = document.getElementById("site_right_top")
var site_right_bottom = document.getElementById("site_right_bottom")

var doms = document.getElementsByClassName("echart-back");
var myCharts = []
for (var e = 0; e < doms.length; e++) {
    myCharts[e] = echarts.init(doms[e])
    console.log("hell", e)
}

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
            return params.name + "," + params.value;
        },
        axisPointer: {
            animation: false
        }
    },
    xAxis: {
        type: 'category',
        data: [100, 200, 300, 400, 500, 600, 700]
    },

    yAxis: {
        min: 0,
        max: 7,
        type: 'value',
        smooth: true
    },
    title: {
        text: '沙子面积',
        left: 'center'
    },
    toolbox: {
        feature: {
            saveAsImage: {
                pixelRatio: 3,
                title: 'save',
                offsetX: -1,
                iconStyle: {
                    borderType: 'solid',
                    borderWidth: 2,
                }
            }
        }
    },
    series:
        [{
            data: [1, 2, 2.4, 3.6, 5, 6, 7],
            type: 'line',
            smooth: true
        }],
    grid: {
        left: '2%',
        right: '2%',
        bottom: '3%',
        containLabel: true
    },
    graphic: [
        {
            type: 'group',
            left: '5%',
            top: '5%',
            children: [
                {
                    type: 'rect',
                    z: 100,
                    left: 'center',
                    top: 'middle',
                    shape: {
                        width: 190,
                        height: 90
                    },
                    style: {
                        fill: '#fff',
                        stroke: '#555',
                        lineWidth: 2,
                        shadowBlur: 8,
                        shadowOffsetX: 3,
                        shadowOffsetY: 3,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                },
                {
                    id: 'text1',
                    type: 'text',
                    z: 100,
                    left: 'center',
                    top: 'middle',
                    style: {
                        fill: '#333',
                        text: [
                            "area:0",
                            "volume:0",
                            "scale:0"
                        ].join('\n'),
                        font: '14px Microsoft YaHei'
                    }
                }
            ]
        }

    ]

}
;
myCharts[0].on('click', function (params) {
    older_data1 = x;
    // older_data2=params[0].value;
    older_data2 = y;
    document.getElementById("ds").innerHTML = "当前位置 (" + older_data1 + "," + older_data2 + ")";
    // document.getElementById("new_data_x").value=older_data1;
    document.getElementById("new_data_x").innerHTML = older_data1;
    document.getElementById("new_data_y").value = older_data2;
});

setInterval(function () {
    console.log("intervel")
}, 2000);
;

function setCurrentFrame() {
    var scale = 1

    for (var i = 0; i < videos.length; i++) {

        video = videos[i]
        var pictureURL = getCurrentFrames(scale, video)

        data = uploadPicture(pictureURL, i)
        myCharts[i].setOption({
            series: [{
                data: data.list_y,
                type: 'line',
                smooth: true
            }]
        });
        myCharts[i].setOption({
            xAxis: {
                data: data.list_x
            },
            yAxis: {
                min: 0,
                max: data.max,
                type: 'value'
            },
        })
        ;


    }


}


function change_data() {
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

    myCharts[0].setOption({
        series: [{
            data: data['list_y']
        }]
    });

    myCharts[0].setOption({
        xAxis: {
            data: data['list_x']
        }
    })

    alert("处理成功")


}

if (option && typeof option === "object") {
    for (var i = 0; i < doms.length; i++) {
        myCharts[i].setOption(option, true);

    }
}

function base64ToBlob(code) {
    let parts = code.split(';base64,');
    let contentType = parts[0].split(':')[1];
    let raw = window.atob(parts[1]);
    let rawLength = raw.length;

    let uInt8Array = new Uint8Array(rawLength);

    for (let i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }
    return new Blob([uInt8Array], {type: contentType});
}

function saveAsImage() {
    let content = myCharts[0].getDataURL({
        pixelRatio: 3,
        backgroundColor: '#fff'
        //    如果不设置背景会出现背景是黑色的现像
    });

    let aLink = document.createElement('a');
    let blob = this.base64ToBlob(content);

    let evt = document.createEvent("HTMLEvents");
    evt.initEvent("click", true, true);
    aLink.download = "line.png";
    aLink.href = URL.createObjectURL(blob);
    aLink.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
    return content
}


window.onresize = function () {
    for (var i = 0; i < doms.length; i++) {
        myCharts[i].resize()
    }
}
