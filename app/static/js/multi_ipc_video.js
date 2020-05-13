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

run = false
hasGetResult = true
number = 0

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


function setCurrentFrame() {
    var scale = 1

    for (var i = 0; i < videos.length; i++) {
        video = videos[i]
        var pictureURL = getCurrentFrames(video)
        data = uploadPicture(pictureURL, i)
    }

    changeResult()
}

function setData(data) {
    i = data.id
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
    number++
    if (number == videos.length) {
        console.log(number)
        changeResult()
        chars()
        number = 0
    }

}

console.log(number)
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

function saveAsImage(id) {
    let content = myCharts[id].getDataURL({
        pixelRatio: 3,
        backgroundColor: '#fff'
        //    如果不设置背景会出现背景是黑色的现像
    });

    //dowloadPicture(content,id)

    return content
}

function dowloadPicture(content, id) {
    let aLink = document.createElement('a');
    let blob = this.base64ToBlob(content);

    let evt = document.createEvent("HTMLEvents");
    evt.initEvent("click", true, true);
    aLink.download = 'line_' + id + '.png';
    aLink.href = URL.createObjectURL(blob);
    aLink.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));

}

window.onresize = function () {
    for (var i = 0; i < doms.length; i++) {
        myCharts[i].resize()
    }
}

function rwar(i, run_text) {

    myCharts[i].setOption({
        graphic: [
            { // 删除上例中定义的 'text1' 元素。
                id: 'text1',
                $action: 'merge',
                style: {
                    fill: '#333',
                    text: run_text,
                    font: '14px Microsoft YaHei'
                }
            }
        ]
    })

}


setInterval(function () {
    console.log('定时任务')
    if (run) {
        console.log('ready to run')
        if (hasGetResult) {
            console.log('the next setCurrentframe')
            hasGetResult = false
            setCurrentFrame()
        }

    }
}, 2000);

function changeResult() {
    console.log('hasGetResult')
    hasGetResult = true
}
