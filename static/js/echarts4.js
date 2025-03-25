function echarts_2() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echarts4'));

    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {type: 'shadow'},
            // formatter:'{c}' ,
        },
        grid: {
            left: '10',
            top: '30',
            right: '30',
            bottom: '10',
            containLabel: true
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
            // itemGap: 35
        },

        xAxis: [{
            type: 'category',
            name: '视频id',
            nameLocation: 'center',
            nameTextStyle: {
                color: "#fff"
            },
            boundaryGap: false,
            axisLabel: {
                rotate: 45,
                formatter: function (value) {
                    return "id " + value;
                },
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: 14,

                },
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.1)'
                }

            },

            data: ['17年3月', '17年6月', '17年9月', '17年12月', '18年3月', '18年6月', '18年9月', '18年12月', '19年3月', '19年6月', '19年9月', '19年12月']

        }, {

            axisPointer: {show: false},
            axisLine: {show: false},
            position: 'bottom',
            offset: 20,


        }],

        yAxis: [{
            type: 'value',
            name: '万',
            nameTextStyle: {
                color: "#fff"
            },
            axisTick: {show: false},
            // splitNumber: 6,
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.1)'
                }
            },
            axisLabel: {
                formatter: function (value) {
                    return value / 10000;
                },
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: 14,
                },
            },

            splitLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.1)'
                }
            }
        }],
        series: [
            {
                name: '字段1',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 5,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        color: 'rgba(228, 228, 126, 1)',
                        width: 2
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(228, 228, 126, .2)'
                        }, {
                            offset: 1,
                            color: 'rgba(228, 228, 126, 0)'
                        }], false),
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'rgba(228, 228, 126, 1)',
                        borderColor: 'rgba(228, 228, 126, .1)',
                        borderWidth: 12
                    }
                },
                data: [12.50, 14.4, 16.1, 14.9, 20.1, 17.2, 17.0, 13.42, 20.12, 18.94, 17.27, 16.10]

            }, {
                name: '字段2',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 5,
                showSymbol: false,
                lineStyle: {

                    normal: {
                        color: 'rgba(255, 128, 128, 1)',
                        width: 2
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(255, 128, 128,.2)'
                        }, {
                            offset: 1,
                            color: 'rgba(255, 128, 128, 0)'
                        }], false),
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'rgba(255, 128, 128, 1)',
                        borderColor: 'rgba(255, 128, 128, .1)',
                        borderWidth: 12
                    }
                },
                data: [-6.4, 0.1, 6.6, 11.2, 42.1, 26.0, 20.2, 18.31, 21.59, 24.42, 34.03, 32.9]
            },
            {
                name: '字段3',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 5,
                showSymbol: false,
                lineStyle: {

                    normal: {
                        color: 'rgba(255, 220, 220, 1)',
                        width: 2
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(255, 220, 220,.2)'
                        }, {
                            offset: 1,
                            color: 'rgba(255, 220, 220, 0)'
                        }], false),
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'rgba(255, 220, 220, 1)',
                        borderColor: 'rgba(255, 220, 220, .1)',
                        borderWidth: 12
                    }
                },
                data: [-6.4, 0.1, 6.6, 11.2, 42.1, 26.0, 20.2, 18.31, 21.59, 24.42, 34.03, 32.9]
            },
        ]
    };

    $.ajax({
        url: "/echarts4",
        success: function (res) {

            for (var i = 0; i < res.data.length - 1; i++) {
                option.series[i].name = res.words[i + 1];
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