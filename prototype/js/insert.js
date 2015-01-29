//全局变量
var afx_result;
var afx_flag_bcover_filled=false;
var afx_flag_bname_filled=false;
var afx_flag_author_filled=false;
var afx_flag_translator_filled=false;
var afx_flag_publisher_filled=false;
var afx_flag_byear_filled=false;
var afx_flag_pagination_filled=false;
var afx_flag_price_filled=false;
var afx_flag_dict={"bcover":afx_flag_bcover_filled,"bname":afx_flag_bcover_filled,
                    "author":afx_flag_author_filled,"translator":afx_flag_translator_filled,
                    "publisher":afx_flag_publisher_filled,"byear":afx_flag_byear_filled,
                    "pagination":afx_flag_pagination_filled,"price":afx_flag_price_filled};
var afx_attr=new Array("bcover","bname","author","translator",
                        "publisher","byear","pagination","price");

(function(){
    var example={"isbn":"9999999999999","bcover":"http://www.example.com/images/123456.jpg",
        "bname":"面向对象软件工程","author":"[美]佚名","translator":"张三","flag":"true",
    "publisher":"高等教育出版社","byear":"2012.9","pagination":"1024","price":"36.00",
    "totalnum":"24"}
    $("#br-input-isbn").keypress(on_isbn_change);
    
    function on_isbn_change(){
        //isbn有12位的时候就ajax
        if($("#br-input-isbn").val().length==12){
            console.log("G");
            $("#feedback-isbn").attr(
                "class","glyphicon glyphicon-refresh glyphicon-refresh-animate form-control-feedback");
            isbn=$("#br-input-isbn").val();
            if(afx_debug==false&&isIsbn(isbn)){
                $.ajax({
                    url:URL+"/RequestAjaxInsertBookInfo/",
                    data:{"isbn":isbn},
                    async:true,
                    dataType:"json",
                    type:"POST",
                    success:function(result){
                        afx_result=result;
                        fill_table(afx_result);
                    }
                });
            }else if(afx_debug==true){
                afx_result=example;
                fill_table(afx_result);
            }else{
                return false;
            }
        }
    }
    //自动填写书籍信息
    function fill_table(obj){
        $("#feedback-isbn").attr("class","glyphicon form-control-feedback");
        
        //如果书没找到
        if(obj["falg"]=="false"){
            $("#feedback-isbn").addClass("glyphicon-warning");
            $("#br-input-isbn")
                .attr("placeholder","ISBN找不到, 注意是否正确")
                .parent().addClass("has-warning");
            $("#br-input-totalnum-static").html("0");
            return false;
        }
        
        //如果找到书了
        $("#feedback-isbn").addClass("glyphicon-ok");
        $("#br-input-isbn").parent().addClass("has-success");
        for(var i=0;i<afx_attr.length;++i){
            if(afx_flag_dict[afx_attr[i]]==false&&obj[afx_attr[i]].length!=0){
                console.log(obj[afx_attr[i]]);
                $("#br-input-"+afx_attr[i]).val(obj[afx_attr[i]]).change();
            }
        }
        $("#br-input-totalnum-static").html(obj["totalnum"]);   
    }
    //各种change事件响应
    $("#br-input-isbn,#br-input-bcover,#br-input-bname,#br-input-author,\
      #br-input-translator,#br-input-publisher,#br-input-byear,\
      #br-input-pagination,#br-input-price,#br-input-insertednum").change(function(){
        
        attr=$(this).attr("id").replace("br-input-","");
        afx_flag_dict[attr]=true;
       
        var temp=$(this).val();
        var flag_illegal=false;
        if(isSqlInjection(temp)){
            return illegal_feedback($(this),attr,"非法输入");
        }else if(attr=="isbn"){
            if(!isIsbn(temp)){
                return illegal_feedback($(this),attr,"ISBN非法");
            }else{
                return legal_feedback($(this),attr,"");
            }
        }else if(attr=="bcover"){
            if(!isURI(temp)){
                return illegal_feedback($(this),attr,"封面路径非法");
            }else if(temp.length!=0){
                return legal_feedback($(this),attr,"");
            }
        }else if(attr=="byear"){
            if(!isYearMonth(temp)){
                return illegal_feedback($(this),attr,"年月格式非法");
            }else if(temp.length!=0){
                return legal_feedback($(this),attr,"");
            }
        }else if(attr=="pagination"||attr=="insertednum"){
            if(!isIntBetween(temp,-9999,9999)){
                return illegal_feedback($(this),attr,"非法数字");
            }else if(temp.length!=0){
                return legal_feedback($(this),attr,"");
            }
        }else if(attr=="price"){
            if(!isFloatBetween(temp,0,9999.99)){
                return illegal_feedback($(this),attr,"价格非法");
            }else if(temp.length!=0){
                return legal_feedback($(this),attr,"");
            }
        }else{
            return legal_feedback($(this),attr,"");
        }
    });
    //非法反馈
    function illegal_feedback(obj,attr,placeholder){
        
        $("#feedback-"+attr).attr("class","glyphicon glyphicon-remove form-control-feedback");
        obj.val("").parent().removeClass("has-success").addClass("has-error"); 
        obj.attr("placeholder",placeholder);
        $("#submit").removeClass("btn-primary").addClass("btn-danger").attr("disabled",true);
        return false;
    }
    //合法反馈
    function legal_feedback(obj,attr,placeholder){
        console.log(attr+"合法");
        $("#feedback-"+attr).attr("class","glyphicon glyphicon-ok form-control-feedback");
        obj.parent().removeClass("has-error").addClass("has-success");
        $("#submit").removeClass("btn-danger").addClass("btn-primary").attr("disabled",false);
        return true;
    }
    
})();
