//全局变量
var afx_all_result;
var afx_time_desc=true;
var afx_pname_desc=false;
var afx_bname_desc=false;
var afx_uid_desc=false;
var afx_lpnumber_desc=false;
var afx_spnumber_desc=false;
var afx_hasreturn_desc=false;
var afx_accumulate_desc=false;
var afx_attr=new Array("time","pname","bname","uid","lpnumber","spnumber",
                        "hasreturn","accumulate");
var afx_attr_desc=new Array(afx_time_desc,afx_pname_desc,afx_bname_desc,
                        afx_uid_desc,afx_lpnumber_desc,afx_spnumber_desc,
                        afx_hasreturn_desc,afx_accumulate_desc);
var afx_attr_type = {
    "isbn":"string",
    "bname":"string",
    "author":"string",
    "publisher":"string",
    "price":"float",
    "totalnum":"int",
    "available":"int",
    "bookable":"int"
};

(function(){
    afx_all_result=new Array();
    //提取所有信息
    $("#history-table tbody tr").each(function(i){
        var obj=$(this);
        afx_all_result.push({
            "timestamp":obj.children("td:eq(0)").html(),
            "time":toTimeAbs(obj.children("td:eq(0)").html()),
            "pname":obj.children("td:eq(1)").html(),
            "bname":obj.children("td:eq(2)").html(),
            "uid":obj.children("td:eq(3)").html(),
            "lpnumber":obj.children("td:eq(4)").html(),
            "spnumber":obj.children("td:eq(5)").html(),
            "hasreturn":obj.children("td:eq(6)").children("a").html()=="归还",
            "returnlink":obj.children("td:eq(6)").html(),
            "accumulate":parseInt(obj.children("td:eq(7)").html().replace("天",""))
        });
    });
    console.log(afx_all_result);
    //然后绑定排序点击事件, 针对某一属性排序, 然后重新渲染html
    for(var i=0;i<afx_attr.length;++i){
        $("#history-table thead tr th:eq("+i+") span").click(function(){
            var idx=$("#history-table thead tr th").index($(this).parent());
            afx_attr_desc[idx]=!afx_attr_desc[idx];
            if(afx_attr_desc[idx]==true){
                $(this).removeClass("glyphicon-sort-by-attributes-alt")
                    .addClass("glyphicon-sort-by-attributes");
                order_by(afx_attr[idx],"desc");
            }else{
                $(this).removeClass("glyphicon-sort-by-attributes")
                    .addClass("glyphicon-sort-by-attributes-alt");
                order_by(afx_attr[idx],"asc");
            }
        }).css("cursor","pointer");
    }  
    
})();

//排序兼重新渲染
function order_by(str_attr,str_order){
    afx_sorting_attr=str_attr;
    if(str_order=="desc"){
        console.log("降序");
        afx_all_result.sort(desc_cmp);
        render_result();
    }else{
        console.log("升序");
        afx_all_result.sort(asc_cmp);
        render_result();
    }
}

//降序排列
function desc_cmp(obj1,obj2){
    return 0-asc_cmp(obj1,obj2);
}

//升序排列
function asc_cmp(obj1,obj2){
    if (afx_attr_type[afx_sorting_attr]=="int"){
        return parseInt(obj1[afx_sorting_attr]) - parseInt(obj2[afx_sorting_attr]);
    }else if(afx_attr_type[afx_sorting_attr]=="float"){
        return parseFloat(obj1[afx_sorting_attr]) - parseFloat(obj2[afx_sorting_attr]);
    }else{
        return obj1[afx_sorting_attr].localeCompare(obj2[afx_sorting_attr])
    }
}

//重新渲染tbody
function render_result(){
    var tbody=$("#history-table tbody");
    tbody.html("");
    for(var i=0;i<afx_all_result.length;++i){
        tr=$("<tr></tr>");
        //如果已经归还, 则什么都不做
        if(afx_all_result[i]["hasreturn"]==false){
            //pass
        }else if(afx_all_result[i]["accumulate"]>=60){
            tr.addClass("danger");
        }else if(afx_all_result[i]["accumulate"]>=30){
            tr.addClass("warning");
        }else{
            tr.addClass("info");
        }
        tr.append($("<td></td>").html(afx_all_result[i]["timestamp"]))
            .append($("<td></td>").html(afx_all_result[i]["pname"]))
            .append($("<td></td>").html(afx_all_result[i]["bname"]))
            .append($("<td></td>").html(afx_all_result[i]["uid"]))
            .append($("<td></td>").html(afx_all_result[i]["lpnumber"]))
            .append($("<td></td>").html(afx_all_result[i]["spnumber"]))
            .append($("<td></td>").html(afx_all_result[i]["returnlink"]))
            .append($("<td></td>").html(afx_all_result[i]["accumulate"]+"天"))
            .appendTo(tbody);
            
    }
}

//计算时间绝对值
//以1970年以来的毫秒数为时间绝对值
function toTimeAbs(str){
    var ret=0;
    try{
        date =new Date();
        date.setFullYear(2000+parseInt(str.substr(0,2)));
        date.setMonth(parseInt(str.substr(3,5))-1);
        date.setDate(parseInt(str.substr(6,8)));
        date.setHours(parseInt(str.substr(9,11)));
        date.setMinutes(parseInt(str.substr(12,14)));
        ret=date.getTime();
    }catch(err){
        ret=0;
    }
    return ret;
}