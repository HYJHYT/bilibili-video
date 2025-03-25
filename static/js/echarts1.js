function echarts_4() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echarts1'));
    var myColor = ['#eb2100', '#eb3600', '#d0570e', '#d0a00e', '#34da62', '#00e9db', '#00c0e9', '#0096f3'];
    var option = {

        grid: {
            left: '2%',
            top: '1%',
            right: '5%',
            bottom: '0%',
            containLabel: true
        },
         tooltip: {
            trigger: 'item',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        xAxis: [{
            show: false,
        }],
        yAxis: [{
            axisTick: 'none',
            axisLine: 'none',
            offset: '7',
            axisLabel: {
                textStyle: {
                    color: 'rgba(255,255,255,.6)',
                    fontSize: '14',
                }
            },
            data: []

        }, {
            axisTick: 'none',
            axisLine: 'none',
            axisLabel: {
                textStyle: {
                    color: 'rgba(255,255,255,.6)',
                    fontSize: '14',
                }
            },
            data: [],

        }, {
            name: '单位：件',
            nameGap: '50',
            nameTextStyle: {
                color: 'rgba(255,255,255,.6)',
                fontSize: '16',
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(0,0,0,0)'
                }
            },
            data: [],
        }],
        series: [{
            name: '币占比',
            type: 'bar',
            yAxisIndex: 0,
            data: [],
            label: {
                normal: {
                    show: true,
                    position: 'right',
                    formatter: function (param) {
                        return param.value + '%';
                    },
                    textStyle: {
                        color: 'rgba(255,255,255,.8)',
                        fontSize: '12',
                    }
                }
            },
            barWidth: 15,
            itemStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [{
                        offset: 0,
                        color: '#03c893'
                    },
                        {
                            offset: 1,
                            color: '#0091ff'
                        }
                    ]),
                    barBorderRadius: 15,
                }
            },
            z: 2
        }, {
            name: '占比',
            type: 'bar',
            yAxisIndex: 1,
            barGap: '-100%',
            data: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
            barWidth: 15,
            itemStyle: {
                normal: {
                    color: 'rgba(0,0,0,.2)',
                    barBorderRadius: 15,
                }
            },
            z: 1
        }]
    };

    $.ajax({
        url: "/echarts1",
        success: function (res) {
            option.yAxis[0].data = res.data1;
            option.yAxis[1].data = res.data2;
            option.series[0].data = res.data3;
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    });

    window.addEventListener("resize", function () {
        myChart.resize();
    });
}