//全局变量
var afx_result;
afx_ajax_loading=false;
var afx_attr=new Array("bcover","bname","author","translator",
                        "publisher","byear","pagination","price");

(function(){
    var example={"isbn":"9999999999999","bcover":"http://www.example.com/images/123456.jpg",
        "bname":"面向对象软件工程","author":"[美]佚名","translator":"张三","flag":"true",
    "publisher":"高等教育出版社","byear":"2012.9","pagination":"1024","price":"36.00",
    "totalnum":"24"}

    $("#br-input-isbn")[0].oninput=on_isbn_change;
    
    function on_isbn_change(){
        //isbn有12位的时候就ajax
        if($("#br-input-isbn").val().length==13){

            $("#feedback-isbn").attr(
                "class","glyphicon glyphicon-refresh glyphicon-refresh-animate form-control-feedback");
            
            //django需要带上csrftoken
            var csrftoken = $.cookie('csrftoken');
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
      
            isbn=$("#br-input-isbn").val();
            console.log(isbn);
            if(afx_debug==false/*&&isIsbn(isbn)*/){
                afx_ajax_loading=true;
                $.ajax({
                    url:getBaseURL()+"/RequestAjaxInsertBookInfo/",
                    data:{"isbn":isbn},
                    dataType:"json",
                    type:"POST",
                    success:function(result){
                        console.log(result);
                        afx_result=result;
                        fill_table(afx_result);
                        afx_ajax_loading=false;
                    },
                    failure: function(result){
                        alert("faild");
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
        if(obj["flag"]=="false"){
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
            if($("#br-input-"+afx_attr[i]).val()!=" "&&obj[afx_attr[i]].length!=0){
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
       
        var temp=$(this).val();
        var flag_illegal=false;
        if(isSqlInjection(temp)){
            return illegal_feedback($(this),attr,"非法输入");
        }else if(attr=="isbn"){
            if(afx_ajax_loading==true){
                return false;
            }
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
                console.log(temp);
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
    
    //submit检查
    $("#submit").parents("form").submit(function(){
        return $("#submit").click();
    });
    $("#submit").click(function(){
            return (function(){
                lst=["isbn","bcover","bname","author","publisher","byear","price","insertednum"]
                dict={
                    "isbn":"ISBN",
                    "bcover":"封面",
                    "bname":"书名",
                    "author":"作者",
                    "publisher":"出版社",
                    "byear":"出版年月",
                    "price":"价格",
                    "insertednum":"新增册数",
                }
                for(var i=0;i<lst.length;i++){
                    if($("#br-input-"+lst[i]).val()==""){
                        illegal_feedback($("#br-input-"+lst[i]),lst[i],dict[lst[i]]+"不能为空");
                        return false;
                    }
                }
                return true;
            })();
    });
    
})();
