function echarts_5() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echarts5'));

    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {type: 'shadow'},
        }, "grid": {
            "top": "20%",
            "right": "10%",
            "bottom": "20",
            "left": "10%",
        },
        legend: {
            data: ['字段1', '字段2'],
            right: 'center',
            top: 0,
            textStyle: {
                color: "#fff"
            },
            itemWidth: 12,
            itemHeight: 10,
        },
        "xAxis": [
            {
                "type": "category",

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
                splitLine: {show: false},
                axisTick: {show: false},
                "axisLabel": {
                    "show": true,
                    formatter: function (value) {
                        return value / 10000;
                    },
                    color: "rgba(255,255,255,.6)"

                },
                axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//左线色

            },
            {
                "type": "value",
                "name": "万",
                nameTextStyle: {
                    color: "#fff"
                },
                "show": true,
                axisTick: {show: false},
                "axisLabel": {
                    "show": true,
                    formatter: function (value) {
                        return value / 10000;
                    },
                    color: "rgba(255,255,255,.6)"
                },
                axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//右线色
                splitLine: {show: true, lineStyle: {color: 'rgba(255,255,255,.1)'}},//x轴线
            },
        ],
        "series": [
            {
                "name": "字段1",
                "type": "bar",
                "data": [
                    18453.35, 20572.22, 24274.22, 30500.00
                ],
                "barWidth": "20%",

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
                "barGap": "0"
            },
            {
                "name": "字段2",
                "type": "line",
                "yAxisIndex": 1,

                "data": [0, 11.48, 18.00, 25.65],
                lineStyle: {
                    normal: {
                        width: 2
                    },
                },
                "itemStyle": {
                    "normal": {
                        "color": "#ff3300",

                    }
                },
                "smooth": true
            }
        ]
    };

    $.ajax({
        url: "/echarts5",
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