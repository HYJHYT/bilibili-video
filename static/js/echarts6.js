function echarts_6() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echarts6'));


    var option = {
        title: {
            text: '5132',
            subtext: '总体',
            x: 'center',
            y: '40%',
            textStyle: {
                color: '#fff',
                fontSize: 18,
                lineHeight: 10,
            },
            subtextStyle: {
                color: '#90979c',
                fontSize: 16,
                lineHeight: 10,

            },
        },
        tooltip: {
            trigger: 'item',
            formatter: "{b} : {c} ({d}%)"
        },

        visualMap: {
            show: false,
            min: 500,
            max: 600,
            inRange: {
                //colorLightness: [0, 1]
            }
        },
        series: [{
            name: '访问来源',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            color: ['rgb(131,249,103)', '#FBFE27', '#FE5050', '#9de562','#3F92B0'], //'#FBFE27','rgb(11,228,96)','#FE5050'
            data: [{
                "value": 1924,
                "name": "字段名称1"
            }, {
                "value": 1055,
                "name": "字段名称2"
            }, {
                "value": 1532,
                "name": "字段名称3"
            },
                {
                "value": 1532,
                "name": "字段名称4"
            }
            ].sort(function (a, b) {
                return a.value - b.value
            }),
            roseType: 'radius',

            label: {
                normal: {
                    formatter: ['{c|{c}}', '{b|{b}}'].join('\n'),
                    rich: {
                        c: {
                            color: 'rgb(241,246,104)',
                            fontSize: 16,
                            fontWeight: 'bold',
                            lineHeight: 5
                        },
                        b: {
                            color: 'rgb(98,137,169)',
                            fontSize: 14,
                            height: 44
                        },
                    },
                }
            },
            labelLine: {
                normal: {
                    lineStyle: {
                        color: 'rgb(98,137,169)',
                    },
                    smooth: 0.2,
                    length: 5,
                    length2: 8,

                }
            }
        }]
    };

    $.ajax({
        url: "/echarts6",
        success: function (res) {
            option.series[0].data = res.data;
            option.title.text = res.sum;
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    });


    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}