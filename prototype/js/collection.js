//全局变量
var afx_all_result;
var afx_isbn_desc=true;
var afx_bname_desc=false;
var afx_author_desc=false;
var afx_publisher_desc=false;
var afx_price_desc=false;
var afx_totalnum_desc=false;
var afx_available_desc=false;
var afx_bookable_desc=false;
var afx_sorting_attr="isbn";//默认排序属性
var afx_attr=new Array("isbn","bname","author","publisher","price","totalnum","available","bookable");
var afx_attr_desc=new Array(afx_isbn_desc,afx_bname_desc,afx_author_desc,afx_publisher_desc,
                                afx_price_desc,afx_totalnum_desc,afx_available_desc,afx_bookable_desc);

(function(){
    afx_all_result=new Array();
    //console.log($("tbody tr").html());
    //首先提取所有信息
    $("#collection-table tbody tr").each(function(obj){
        var obj=$(this);
         
        afx_all_result.push({
            "isbn":obj.children("td:eq(0)").html(),
            "bname":obj.children("td:eq(1)").html(),
            "author":obj.children("td:eq(2)").html(),
            "publisher":obj.children("td:eq(3)").html(),
            "price":parseFloat(obj.children("td:eq(4)").html().replace("元","")),
            "totalnum":parseInt(obj.children("td:eq(5)").html()),
            "available":parseInt(obj.children("td:eq(6)").html()),
            "bookable":parseInt(obj.children("td:eq(7)").html()),
            "bookinglink":obj.children("td:eq(8)").html()
        });     
    });
    //然后绑定排序点击事件, 针对某一属性排序, 然后重新渲染html
    for(var i=0;i<afx_attr.length;++i){
        $("#collection-table thead tr th:eq("+i+") span").click(function(){
            var idx=$("#collection-table thead tr th").index($(this).parent());
            afx_attr_desc[idx]=!afx_attr_desc[idx];
            if(afx_attr_desc[idx]==true){
                order_by(afx_attr[idx],"desc");
            }else{
                order_by(afx_attr[idx],"asc");
            }
        });
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
    if(obj1[afx_sorting_attr]>obj2[afx_sorting_attr]){
        return true;
    }else{
        return false;
    }
}

//升序排列
function asc_cmp(obj1,obj2){
    if(obj1[afx_sorting_attr]<=obj2[afx_sorting_attr]){
        return true;
    }else{
        return false;
    }
}

//重新渲染tbody
function render_result(){
    var tbody=$("#collection-table tbody");
    tbody.html("");
    for(var i=0;i<afx_all_result.length;++i){
        tr=$("<tr></tr>");
        //如果在馆册数为0, 则不加class
        if(afx_all_result[i]["available"]==0){
            //pass
        }else if(afx_all_result[i]["available"]<5){
            tr.addClass("danger");
        }else if(afx_all_result[i]["available"]<10){
            tr.addClass("warning");
        }else{
            tr.addClass("info");
        }
        tr.append($("<td></td>").html(afx_all_result[i]["isbn"]))
            .append($("<td></td>").html(afx_all_result[i]["bname"]))
            .append($("<td></td>").html(afx_all_result[i]["author"]))
            .append($("<td></td>").html(afx_all_result[i]["publisher"]))
            .append($("<td></td>").html(afx_all_result[i]["price"].toFixed(afx_float_default_prec)+"元"))
            .append($("<td></td>").html(afx_all_result[i]["totalnum"]))
            .append($("<td></td>").html(afx_all_result[i]["available"]))
            .append($("<td></td>").html(afx_all_result[i]["bookable"]))
            .append($("<td></td>").html(afx_all_result[i]["bookinglink"]))
            .appendTo(tbody);
    }
}
            

