function echarts_1() {
    var myChart = echarts.init(document.getElementById('echarts3'));

    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {type: 'shadow'},
        }, "grid": {
            "top": "18%",
            "right": "30",
            "bottom": "20",
            "left": "30",
        },
        legend: {
            data: [],
            right: 'center', width: '100%',
            textStyle: {
                color: "#fff"
            },
            itemWidth: 12,
            itemHeight: 10,
        },


        "xAxis": [
            {
                "type": "category",
                name: '视频id',
                nameTextStyle: {
                    color: "#fff"
                },
                nameLocation: 'center',
                data: ['2016', '2017', '2018', '2019'],
                axisLine: {lineStyle: {color: "rgba(255,255,255,.1)"}},
                axisLabel: {
                    textStyle: {color: "rgba(255,255,255,.7)", fontSize: '14',},
                    formatter: function (value) {
                        return "id " + value;
                    },
                },

            },
        ],
        "yAxis": [
            {
                "type": "value",
                "name": "万",
                nameTextStyle: {
                    color: "#fff"
                },
                position: 'left',
                axisTick: {show: true},
                splitLine: {
                    show: false,

                },
                "axisLabel": {
                    "show": true,
                    formatter: function (value) {
                        return value / 10000;
                    },
                    fontSize: 12,
                    color: "rgba(255,255,255,.6)"

                },
            },
            {
                "type": "value",
                "name": "万",
                nameTextStyle: {
                    color: "#fff"
                },
                "show": true,
                "axisLabel": {
                    "show": true,
                    fontSize: 12,
                    formatter: function (value) {
                        return value / 10000;
                    },
                    color: "rgba(255,255,255,.6)"
                },
                axisTick: {show: false},
                axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//右线色
                splitLine: {show: true, lineStyle: {color: 'rgba(255,255,255,.1)'}},//x轴线
            },

        ],
        "series": [

            {
                "name": "",
                "type": "bar",
                "data": [36.6, 38.80, 40.84, 41.60],
                "barWidth": "15%",
                "itemStyle": {
                    "normal": {
                        barBorderRadius: 15,
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#8bd46e'
                        }, {
                            offset: 1,
                            color: '#09bcb7'
                        }]),
                    }
                },
                "barGap": "0.2"
            },
            {
                "name": "",
                "type": "bar",
                "data": [14.8, 14.1, 15, 16.30],
                "barWidth": "15%",
                "itemStyle": {
                    "normal": {
                        barBorderRadius: 15,
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#248ff7'
                        }, {
                            offset: 1,
                            color: '#6851f1'
                        }]),
                    }
                },
                "barGap": "0.2"
            },
            {
                "name": "",
                "type": "bar",
                "data": [9.2, 9.1, 9.85, 8.9],
                "barWidth": "15%",
                "itemStyle": {
                    "normal": {
                        barBorderRadius: 15,
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#fccb05'
                        }, {
                            offset: 1,
                            color: '#f5804d'
                        }]),
                    }
                },
                "barGap": "0.2"
            },
            {
                "name": "",
                "type": "line",
                smooth: true,
                "yAxisIndex": 1,
                "data": [0, 6.01, 5.26, 1.48],
                lineStyle: {
                    normal: {
                        width: 2
                    },
                },
                "itemStyle": {
                    "normal": {
                        "color": "#86d370",

                    }
                },

            }
            ,
            {
                "name": "",
                "type": "line",
                "yAxisIndex": 1,

                "data": [0, -4.73, 6.38, 8.67],
                lineStyle: {
                    normal: {
                        width: 2
                    },
                },
                "itemStyle": {
                    "normal": {
                        "color": "#3496f8",

                    }
                },
                "smooth": true
            },
            {
                "name": "",
                "type": "line",
                "yAxisIndex": 1,

                "data": [0, -1.09, 8.24, -9.64],
                lineStyle: {
                    normal: {
                        width: 2
                    },
                },
                "itemStyle": {
                    "normal": {
                        "color": "#fbc30d",

                    }
                },
                "smooth": true
            }
        ]
    };

    $.ajax({
        url: "/echarts3",
        success: function (res) {

            for (var i = 0; i < res.data.length - 1; i++) {
                option.series[i].name = res.words[i];
                option.series[i].data = res.data[i + 1]
            }
            option.legend.data = res.words;
            option.xAxis[0].data = res.data[0];
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    });

    window.addEventListener("resize", function () {
        myChart.resize();
    });


}