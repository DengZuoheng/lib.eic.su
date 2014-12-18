//全局对象
var afx_result;


(function(){
    var account="2012052207";
    var example={
        "watch_list":
            [
                {"account":"2012052207","name":"邓作恒1","lpnumber":"13726247196","spnumber":"617196","sum":"14","iswatching":"no"},
                {"account":"2012052277","name":"邓作恒2","lpnumber":"13726247196","spnumber":"617196","sum":"14","iswatching":"yes"},
                {"account":"2012052777","name":"邓作恒3","lpnumber":"13726247196","spnumber":"617196","sum":"14","iswatching":"no"}
            ]
    }
    $.ajax({
        url:URL+"/RequestAjaxAdmin",
        data:{"account":account},
        async:false,
        dataType:"json",
        type:"POST",
        success:function(result){
            afx_result=result;
            fill_table(result);
            }
        }
    });
    function fill_table(obj){
        for(var i=0;i<obj["watch_list"];++i)
        {
            item=obj["watch_list"][i];
            $("<tr></tr>")
                .append($("<td></td>").html(item["account"]))
                .append($("<td></td>").html(item["name"]))
                .append($("<td></td>").html(item["lpnumber"]))
                .append($("<td></td>").html(item["spnumber"]))
                .append($("<td></td>").html(item["sum"]))
                .append($("<td></td>").html(
                    (function(str){
                        if(str=="no"){
                            ret="否&nbsp;<span class='btn btn-warning btn-xs' id='";
                            ret+=item["account"]+"-setwatching"
                                +"''>设为值班</span>";
                            return ret;
                        }else if(str=="yes"){
                            return "是";
                        }else{
                            return "不明";
                        }
                    })(item["iswatching"])))
                .append($("<td></td>").append(
                    $("<span class='btn btn-danger btn-xs'>删除</span>")
                        .attr("id",item["account"]+"-delete")))
                .addClass("yes")
                .appendTo($("#tbody"));

            //响应设为值班按钮
            $("#"+item["account"]+"-setwatching").click(function(){
                id=$(this).attr("id").repalce("-setwatching","");
                for(var i=0;i<afx_result["watch_list"].length;++i)
                {
                    if(id==afx_result["watch_list"][i]["account"]){
                        afx_result["watch_list"][i]["iswatching"]="yes";
                    }else{
                        afx_result["watch_list"][i]["iswatching"]="no";
                    }
                }
                fill_table(afx_result);

            });
            //响应删除按钮
            $("#"+item["account"]+"-delete").click(function(){
                id=$(this).attr("id").repalce("-delete","");
                for(var i=0;i<afx_result["watch_list"].length;++i)
                {
                    if(id==afx_result["watch_list"][i]["account"]){
                        afx_result["watch_list"].splice(i,1);
                    }else{
                        afx_result["watch_list"][i]["iswatching"]="no";
                    }
                }
                fill_table(afx_result);

            });
        }
    }
})();