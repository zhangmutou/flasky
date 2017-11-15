$(function () {
    $.getJSON($SCRIPT_ROOT + '/mointor/all', {
    },
        function(data) {
            console.log(data.series);
            $('#container').highcharts({
                chart: {
                    type: 'line'
                },
                title: {
                    text: '服务器监控'
                },
                subtitle: {
                    text: ''
                },
                xAxis: {
                    categories: data.x_categories
                },
                yAxis: {
                    title: {
                        text: '百分比（%）'
                    }
                },
                plotOptions: {
                    line: {
                        dataLabels: {
                            enabled: true          // 开启数据标签
                        },
                        enableMouseTracking: true // 关闭鼠标跟踪，对应的提示框、点击事件会失效
                    }
                },
                series: data.series
            });
        }
    );
});