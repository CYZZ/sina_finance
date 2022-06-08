var callBackFuncs = [];
String.prototype.myFormat = function () {
    var e = arguments;
    return !!this && this.replace(/\{(\d+)\}/g, function (t, r) {
        return e[r] ? e[r] : t
    })
};
// 折线图📈
(function () {
    // 实例化一个chart对象
    var myChart = echarts.init(document.querySelector('.row-header .chart'));
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
            // textStyle: {
            //     color: '#fff'
            // },
            position: function (pos, params, el, elRect, size) {
                const obj = {
                    top: 10
                };
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },
            // extraCssText: 'width: 170px'
        },
        axisPointer: {
            link: [
                {
                    xAxisIndex: [0, 1]
                }
            ],
            label: {
                backgroundColor: '#777'
            }
        },
        grid: [
            {
                left: '5%',
                right: '5%',
                height: '50%'
            },
            {
                left: '5%',
                right: '5%',
                top: '68%',
                height: '16%'
            }
        ],
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
            },
            {
                type: 'category',
                boundaryGap: false,
                gridIndex: 1,
                show: false
            },
        ],
        yAxis: [
            {
                type: 'value'
            },
            {
                type: 'value',
                gridIndex: 1,
                splitNumber: 3,
            },
        ],
        dataZoom: [
            {
                filterMode: 'empty',
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 0,
                end: 100,
                "filterMode": "filter"
            },
            {
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                top: '85%',
                start: 0,
                end: 100,
                height:20
            }
        ],
        series: [],
        visualMap: [
            {
                // 不显示图例
                show: false,
                seriesIndex: 3,
                dimension: 1,
                pieces: [
                    { gte: 3, lte: 30, color: 'red' },
                ],
                outOfRange: {
                    color: '#ee6666'
                }
            },
            {
                show: false,
                seriesIndex: 4,
                dimension: 1,
                pieces: [
                    { gte: 3, lte: 30, color: 'red' },
                ],
                outOfRange: {
                    color: '#73c0de'
                }
            },
        ]
    };

    function mySeries(name, data) {
        return {
            name: name,
            lineStyle: {
                width: 1.5
            },
            // 绘制渐变色
            // label:{show:true},
            // areaStyle: {
            //     color: new echarts.graphic.LinearGradient(
            //         0, 0, 0, 1,
            //         [
            //             {
            //                 offset: 0,
            //                 color: 'rgba(1,132,213,0.4'
            //             },
            //             {
            //                 offset: 0.8,
            //                 color: 'rgba(1,132,213,0.1'
            //             }
            //         ],
            //         false
            //     )
            // },
            // symbol: 'circle',
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
            zlevel: 0, z: 0, z2: 0,
            
        }
    };

    function sumRateSeries(name, data) {
        return {
            name: name,
            lineStyle: {
                width: 1
            },
            label: { show: true },
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            data: data,
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            zlevel: 1, z: 1, z2: 1,
            markArea:{
                // silent:true,
                data: [
                    [{
                        name: '黄区',
                        yAxis: 3,
                        itemStyle: {
                            color: '#eeff6688',
                        }
                    },
                    {
                        yAxis: 30
                    }]
                ]
            }
        }
    };

    // 3.指定配置项给实例对象
    // myChart.setOption(option)
    console.log("my start load init chart-------====");
    // 开始请求数据，刷新页面

    var callBack = function (data) {
        option["series"] = []
        option["xAxis"][0]["data"] = data["x"];
        console.log(data)
        yKeyValue = data["y"]
        for (var key in yKeyValue) {
            option["series"].push(mySeries(key, yKeyValue[key]))
            console.log(key)
        }
        // 绘制回撤区域
        areaData = []
        retraceMent = data["retracement"]
        for (index in retraceMent["begin_date"]) {
            var xName = -(retraceMent["retracement"][index] * 100).toFixed(1);
            var abc = "ceshi {0} {1}".myFormat("test", 123);
            console.log(abc)
            areaData.push(
                [{
                    "name": '{0}%'.myFormat(xName),
                    "xAxis": retraceMent["begin_date"][index],
                    "yAxis": retraceMent["end_number"][index]
                },
                {
                    "xAxis": retraceMent["end_date"][index],
                    "yAxis": retraceMent["begin_number"][index]
                }]
            )
        }

        option["series"][0]["markArea"] = {
            "silent": true,
            "label": {
                "show": true,
                "position": "top",
                "color": "black",
                "margin": 8
            },
            "data": areaData,
            "itemStyle": {
                "color": "rgba(20, 255, 20, 0.2)"
            }
        };

        // 绘制底部的折线图
        option["xAxis"][1]["data"] = data["x"]
        sum_rate = data["sum_rate"]
        option["series"].push(sumRateSeries("hushen_sum_rate", sum_rate[0]))
        option["series"].push(sumRateSeries("chuangye_sum_rate", sum_rate[1]))
        myChart.setOption(option)
    };
    // 存储到数组中在需要的时候调用刷新数据
    callBackFuncs.push(callBack)

    window.addEventListener('resize', function () {
        myChart.resize();
    })
})();

// 绘制多个bar并排📊
(function () {
    var myChart = echarts.init(document.getElementById("year_rate"))
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
        title: {
            text: '年收益',
            subtext: 'Fake Data'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow',
                shadowStyle: {
                    color: '#0221'
                }
            }
        },
        legend: {
            itemHeight: 10,
            itemWidth: 15,
            itemGap:15,
            textStyle: {
                fontSize: 10,
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                // prettier-ignore
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0],
                start: 20,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0],
                type: 'slider',
                top: '88%',
                start: 20,
                end: 100,
                height:10
            }
        ],
        series: []
    };

    function myYearBar(name, data) {
        return {
            name: name,
            type: 'bar',
            data: data,
            label: {
                "show": true,
                "position": "top",
                "margin": 8,
                "formatter": "{c}%",
                color:'auto'
            },
        }
    }

    var callBack = function (data) {
        // should reset
        option["series"] = []
        year_rate = data["year_rate"]
        option["xAxis"][0]["data"] = year_rate["x"]
        console.log(year_rate)
        for (var key in year_rate["values"]) {
            option["series"].push(myYearBar(key, year_rate["values"][key]))
        }
        myChart.setOption(option)
    }
    // 存储到数组中在需要的时候调用刷新数据
    callBackFuncs.push(callBack)

    // myChart.setOption(option)
    window.addEventListener('resize', function () {
        myChart.resize();
    })
})();

// 绘制收益贡献率📊
(function () {
    var myChart = echarts.init(document.getElementById("revenu_contribution"))
    var option = {
        title: {
            text: '收益贡献率'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            show:false,
            itemHeight: 10,
            itemWidth: 15,
            textStyle: {
                fontSize: 10,
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',

                "axisLabel": {
                    "show": true,
                    "position": "top",
                    "rotate": 30,
                    "margin": 8
                },
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                "type": "bar",
                "name": "收益贡献率",
                "data": [],
                "showBackground": false,
                "barWidth": "50%",
                itemStyle: {
                    // 普通状态的颜色
                    normal: {
                        color: function (params) {
                            var colorList = ["#5470c6","#91cc75","#fac858","#ee6666","#73c0de","#3ba272","#fc8452","#9a60b4","#ea7ccc"];
                            return colorList[params.dataIndex];
                        }
                    },
                    // 鼠标悬停的时候设置的颜色
                    emphasis:{
                        shadowBlur:10,
                        shadowOffsetX:0,
                        shadowColor:'rgba(0,0,0,0.5'
                    }
                },
                "label": {
                    "show": true,
                    "position": "top",
                    "margin": 8,
                    color:'auto'
                },
            }
        ]
    };

    var callBack = function (data) {
        year_rate = data["revenue_contribution"]
        option["xAxis"][0]["data"] = []
        option["series"][0]["data"] = []
        for (var key in year_rate) {
            option["xAxis"][0]["data"].push(key)
            option["series"][0]["data"].push((year_rate[key] - 1).toFixed(2))
        }
        myChart.setOption(option)
    }
    // 存储到数组中在需要的时候调用刷新数据
    callBackFuncs.push(callBack)

    // myChart.setOption(option)
    window.addEventListener('resize', function () {
        myChart.resize();
    })
})();

// 绘制交易频次饼图
(function () {
    var myChart = echarts.init(document.getElementById("trading_count"))
    option = {
        title: {
            text: '交易频次',
            left: 'center'
        },
        tooltip: {
            show:false,
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
            itemHeight: 10,
            itemWidth: 10,
            icon:'circle',
            textStyle: {
                fontSize: 10,
            },
            orient: 'vertical',
            left: 'right'
        },
        series: [
            {
                name: '交易频次',
                type: 'pie',
                radius: ['40%', '70%'],
                // center: ["35%", "50%"],
                avoidLabelOverlap: false,
                data: [],
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '100%',
                        fontWeight: 'bold',
                        formatter: "{b} \n 次数:{c}\n ({d}%)",
                    },
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    var callBack = function (data) {
        option["series"][0]["data"] = []
        trading_count = data["trading_count"]
        for (var key in trading_count) {
            option["series"][0]["data"].push({ name: key, value: trading_count[key] })
        }
        myChart.setOption(option)
    }
    // 存储到数组中在需要的时候调用刷新数据
    callBackFuncs.push(callBack)

    // myChart.setOption(option)
    window.addEventListener('resize', function () {
        myChart.resize();
    })
})();

// 立马请求数据
function fetchData() {
    // 不用缓存，直接使用最新的数据
    // $.ajaxSetup({ cache: false });
    $.ajax({
        type: "get",
        // url:"http://localhost:8989/json/test.json",
        url: "json/test_mytest.json",
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
            console.log(callBackFuncs.length)
            for (var index in callBackFuncs) {
                console.log(callBackFuncs[index])
                callBackFuncs[index](data)
            }
        }
    })
};
fetchData();

function completeAndReturnName() {
    fetchData();
    return "hello ,你收到数据了吗123";
};