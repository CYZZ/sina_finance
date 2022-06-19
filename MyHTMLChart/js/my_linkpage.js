var callBackFuncs = [];
String.prototype.myFormat = function () {
    var e = arguments;
    return !!this && this.replace(/\{(\d+)\}/g, function (t, r) {
        return e[r] ? e[r] : t
    })
};
// 折线图📈
function createChart(itemId, day_data) {
    // 实例化一个chart对象
    var myChart = echarts.init(document.getElementById(itemId));
    // 2.指定配置项和数据
    /** @type EChartsOption */
    var option = {
        toolbox: {
            show: true,
            right: "5%",
            feature: {
                dataView: { show: true, readOnly: false },
                magicType: { show: true, type: ['line', 'bar'] },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            position: function (pos, params, el, elRect, size) {
                const obj = {
                    top: 10
                };
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },
            formatter: function (params) {
                var time = params[0].name
                var seriesName = params[0].seriesName
                var value = params[0].value
                return time + "<br>" + seriesName + ": " + value + "<br>" + "涨跌幅: " + ((value - day_data["prePrice"]) / day_data["prePrice"] * 100).toFixed(2) + "%"
            }
            // extraCssText: 'width: 170px'
        },
        axisPointer: {
            link: [
                {
                    xAxisIndex: 0
                }
            ],
            label: {
                backgroundColor: '#777'
            }
        },
        grid: [
            {
                // left: '8%',
                // right: '5%',
                // height: '72%'
            }
        ],
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
            }
        ],
        yAxis: [
            {
                type: 'value',
                min: day_data["min"],
                max: day_data["max"],
                axisPointer: {
                    label: {
                      formatter: function (params) {
                        // return ((params.value - base) * 100).toFixed(1) + '%';
                        var value = params.value
                        return value.toFixed(2) + " (" + ((value - day_data["prePrice"]) / day_data["prePrice"] * 100).toFixed(2) + "%)"
                      }
                    }
                  },
            }
        ],
        dataZoom: [
            {
                filterMode: 'empty',
                type: 'inside',
                xAxisIndex: 0,
                start: 0,
                end: 100,
                "filterMode": "filter"
            }
        ],
        series: []
    };

    function mySeries(name, data) {
        return {
            name: name,
            lineStyle: {
                width: 1.5
            },
            symbolSize: 3,
            showSymbol: false,
            data: data,
            type: 'line',
            markPoint: {
                data: [
                    {
                        type: 'max',
                        name: '最大值'
                    },
                    {
                        type: 'min',
                        name: '最小值'
                    }
                ]
            },
            markLine: {
                label: {
                    position: "end", // 标线的位置 start, middle end
                },
                data: [
                    {
                        label: {
                            formatter: "昨收"
                        },
                        lineStyle:{
                            color:"#5558"
                        },
                        yAxis: day_data["prePrice"]
                    },
                    // {
                    //     type:"average", // min, max, average 最小，最大，平均
                    //     label:{
                    //         formatter:"平均",
                    //         fontSize:"10"
                    //     }
                    // }
                ]
            },
            zlevel: 0, z: 0, z2: 0,
        }
    };

    // 3.指定配置项给实例对象
    // myChart.setOption(option)
    console.log("my start load init chart-------====");
    // 开始请求数据，刷新页面

    option["series"] = []
    option["xAxis"][0]["data"] = day_data["x"];
    // console.log(data)
    option["series"].push(mySeries(day_data["name"], day_data["y"]))
    myChart.setOption(option)


    window.addEventListener('resize', function () {
        myChart.resize();
    })
    return myChart
}

function reload_chart(data) {
    for (index in data["data"]) {
        chart_id = "chart-{0}".myFormat(index)
        console.log("chart_id=")
        // console.log(chart_id)
        // chart_id = "chart-1"
        obj = data["data"][index]
        myChart = createChart(chart_id, obj)
        myChart.group = 'mygroup'
    }
    // 让加入组的进行联动
    echarts.connect('mygroup')
    // createChart(data["data"][0])
}


// 立马请求数据
function fetchData() {
    // 不用缓存，直接使用最新的数据
    // $.ajaxSetup({ cache: false });
    $.ajax({
        type: "get",
        // url:"http://localhost:8989/json/test.json",
        url: "json/test.json",
        headers: {
            'cache-control': 'no-cache',
            'Pragma': 'no-cache'
        },
        contentType: 'application/json;charset=utf-8',
        async: true,
        // data:JSON.stringify(eleMarkers),
        traditional: true,
        dataType: 'json',
        timeout: 300,
        success: function (data) {
            console.log(data)
            reload_chart(data)
        }
    })
};

fetchData();

function my_reloadData() {
    fetchData();
    return "hello ,你收到数据了吗123,开始要刷新数据了";
};