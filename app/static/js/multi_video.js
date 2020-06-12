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

var data =
    [
        {
            'list_x': [100, 200, 300, 400, 500, 600, 700],
            'list_y': [1, 2, 3, 4, 5, 6, 7],
            'id': 0
        },
        {
            'list_x': [100, 200, 300, 400, 500, 600, 700],
            'list_y': [1, 2, 3, 4, 5, 6, 7],
            'id': 1
        }
    ]


for (var e = 0; e < doms.length; e++) {
    myCharts[e] = echarts.init(doms[e])

    console.log("hell", e)
}

for (var i = 0; i < myCharts.length; i++) {
    myCharts[i].on('click', chartClick);

}

run = false
hasGetResult = true
number = 0


var app = {};
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

function chartClick(params) {
    older_data1 = x;
    // older_data2=params[0].value;
    older_data2 = y;
    id = this.getDom().getAttribute('data')
    console.log(id)
    document.getElementById("ds").innerHTML = "当前位置 (" + older_data1 + "," + older_data2 + ")" + "  id=" + id;
    document.getElementById('ds').setAttribute('index', id)
    // document.getElementById("new_data_x").value=older_data1;
    document.getElementById("new_data_x").innerHTML = older_data1;
    document.getElementById("new_data_y").value = older_data2;

}


function setCurrentFrame() {
    var scale = 1
    this.run = true
    for (var i = 0; i < videos.length; i++) {
        video = videos[i]
        var pictureURL = getCurrentFrames(video)
        data = uploadPicture(pictureURL, i)
    }

}

function setData(data) {
    i = data.id
    if (this.run != true) {
        return
    } else {
        this.data[i] = data
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

        video = this.videos[i]
        var pictureURL = getCurrentFrames(video)
        return uploadPicture(pictureURL, i)
    }

}

function change_data(idx) {
    data_x = parseInt(document.getElementById("new_data_x").innerHTML);
    data_y = parseInt(document.getElementById("new_data_y").value);

    document.getElementById("newer_data").innerHTML = "修改后的数据(" + data_x + "," + data_y + ")";
    changeEchartData(data_x, data_y, idx)

    console.log(data[idx])
    for (var i = 0; i < data[idx].list_x.length; i++) {
        if (data_x == data[idx].list_x[i]) {
            data[idx].list_y[i] = data_y;
            break;
        }
    }

    myCharts[idx].setOption({
        series: [{
            data: data[idx].list_y
        }]
    });

    myCharts[idx].setOption({
        xAxis: {
            data: data[idx].list_x
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
    if (run) {
        console.log('ready to run')
        if (hasGetResult) {
            hasGetResult = false
        }

    }
}, 5000);


