/**
 * Created by Chunyuan on 16-5-11.
 */
$(function(){

    $( "#query_input" ).autocomplete({
        width: 260,
        minLength: 0,
        selectFirst: false,
        source: function(request, response){
            // request对象只有一个term属性，对应用户输入的文本
            // response是一个函数，在你自行处理并获取数据后，将JSON数据交给该函数处理，以便于autocomplete根据数据显示列表
            $.ajax( {
                url: "/suggest",
                data : { "term" :request.term },
                dataType: 'json',
                success: function(dataObj){
                  //  $.cookie("suggest" , $.toJSON(dataObj));
                    response(dataObj); //将数据交给autocomplete去展示
                }
            } );
	    },
        focus: function() {
          // 防止在获得焦点时插入值
          return false;
        },
        select: function( event, ui ) {
            console.log(ui.item.value.split("--")[0]);
            $("#query_input").val(ui.item.value.split("--")[0]);
            $('#form_sub').click();
            event.preventDefault();  //阻止默认浏览器动作(W3C)
            event.stopPropagation();
        }
    }).focus(function() {
        $(this).autocomplete("search");
        return false;
    }).blur(function() {
    });

});






