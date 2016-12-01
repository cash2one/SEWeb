/**
 * Created by Chunyuan on 16-5-11.
 */
$(function(){

    $( "#query_input" ).autocomplete({
        width: 260,
        selectFirst: false,
        source: function(request, response){
            // request对象只有一个term属性，对应用户输入的文本
            // response是一个函数，在你自行处理并获取数据后，将JSON数据交给该函数处理，以便于autocomplete根据数据显示列表
            $.ajax( {
                url: "/suggest",
                data : { "term" :request.term },
                dataType: 'json',
                success: function(dataObj){
                    $.cookie("suggest" , $.toJSON(dataObj));
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
    });

   
});




function clickType(obj){
  /*   var id = $(obj).attr("id");
     if(id == "6"){
        qita_click($('#current_search_cache').val(),1);
     }else if(id == "2"){
         $(obj).css("color","#000000")
         page_click($('#current_search_cache').val(),1);
     }*/

 }

function page_click(search,pn) {
    var query_input = document.getElementById("query_input").value;
    var url_type = document.getElementById("url_type").value;
    url = '/'+url_type+'?url_type='+url_type
    url = url + '&q=' + query_input
            + "&"+search+'=true'
            + "&pn=" + pn;
    window.location.href = url;
    console.log(url);
};

    function clickPrePage(){
        var pn = $('#current_page_cache').val();
        var pnInt = parseInt(pn);
        if(pnInt == 1){return;}
        pnInt = pnInt-1;
        page_click($('#current_search_cache').val(),pnInt)
    }

    function clickNextPage(){
        var pn = $('#current_page_cache').val();
        var pnInt = parseInt(pn);
        if(pnInt == 10){return;}
        pnInt = pnInt+1;
        page_click($('#current_search_cache').val(),pnInt)
    }

function qita_click(search,pn) {
    var query_input = document.getElementById("query_input").value;
    url = '/queryQita?' + 'q=' + query_input
            + "&"+search+'=true'
            + "&pn=" + pn;
    window.location.href = url;
};