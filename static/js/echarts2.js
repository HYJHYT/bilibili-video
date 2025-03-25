function echarts_3() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echarts2'));

    var option = {

        tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: ['粉丝数'],
            right: 'center',
            top: 0,
            textStyle: {
                color: "#fff"
            },
            itemWidth: 12,
            itemHeight: 10,
            // itemGap: 35
        },
        grid: {
            left: '0',
            right: '20',
            bottom: '0',
            top: '5%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['字段1', '字段2', '字段3', '字段3', '字段4', '字段5', '字段6', '字段7', '字段8', '字段9'],
            axisLabel: {
                rotate: 45,
                formatter: function (value) {
                    return value.split("").join("");
                },
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: 10,
                }
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,0.3)'
                }
            },
        },
        yAxis: {
            type: 'value',
            splitNumber: 4,
            axisTick: {show: false},
            splitLine: {
                show: true,
                lineStyle: {
                    color: 'rgba(255,255,255,0.1)'
                }
            },
            axisLabel: {
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: 14,
                }
            },
            axisLine: {show: false},
        },

        series: [{
            name: '关注数',
            type: 'bar',
            stack: 'a',
            barWidth: 20,
            barGap: 10,
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
            data: []
        }
        ]
    };

    $.ajax({
        url: "/echarts2",
        success: function (res) {
            option.xAxis.data = res.data1;
            option.series[0].data = res.data2;
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    });

    window.addEventListener("resize", function () {
        myChart.resize();
    });
}