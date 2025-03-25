$(window).load(function () {
    $(".loading").fadeOut()
});

/****/
$(document).ready(function () {
    var whei = $(window).width();
    $("html").css({fontSize: whei / 20});
    $(window).resize(function () {
        var whei = $(window).width();
        $("html").css({fontSize: whei / 20})
    });
});

$(function () {
    echarts_1();
    echarts_2();
    echarts_3();
    echarts_4();
    echarts_5();
    echarts_6();
    table();
});

//给表格传值
function table() {
    var table = $("#tabledata");
    $.ajax({
        url: "/table",
        success: function (res) {
            var data = res.data;
            var str = "";//把数据组装起来
           var header= "<tr><th>"+res.words[0]+"</th><th>"+res.words[1]+"</th><th>"+res.words[2]
            +"</th><th>"+res.words[3]+"</th></tr>";

           str += header;
            for (var i = 0; i < data.length; i++) {
                   str += "<tr><th>"+data[i][0]+"</th><th>"+data[i][1]+"</th><th>"+data[i][2]
            +"</th><th>"+data[i][3]+"</th></tr>";
               }

                table.html(str)
            }


    });

}


		
		
		


		



















