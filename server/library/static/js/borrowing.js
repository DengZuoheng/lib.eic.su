//全局对象
var afx_person_result;
var afx_book_result;
var afx_flag_name_filled=false;
var afx_flag_spnumber_filled=false;
var afx_flag_lpnumber_filled=false;
var afx_person_ajaxed=false;
var afx_book_ajaxed=false;
var afx_can_not_submit=false;
//TODO:允许修改学号和isbn时重新ajax

(function(){
    var person_example={"flag":"true","account":"2012052207","name":"邓作恒",
        "lpnumber":"13726247196","spnumber":"600000",
    "bookednum":9, "badcredit":"false"};
    //flag表示这个人找不找得到
    //bookednum表示这个人已经预约的书数,总数大于8就不允许了
    //badcredit表示这个人信用度已经没有了, true表示不能借书也不能预约
    
    var book_example={"flag":"true","books":
    [{"bid":"123","bname":"面向对象软件工程(上册)","binventory":"5"},
    {"bid":"234","bname":"面向对象软件工程(下册)","binventory":"6"}]};
    //flag表示有没找到, 找到和为true,没找到为false
    //bid表示书籍的序列号, 考虑isbn不能作为主键
    //bname是书名, binventory是库存量
    
    //$("#br-input-uid").change(on_account_change);
    $("#br-input-uid")[0].oninput=on_account_change;
    //$("#br-input-isbn").change(on_isbn_change);
    $("#br-input-isbn")[0].oninput=on_isbn_change;
    function on_account_change(){
        //先发生keypress事件, 然后才输入, 也就是说
        //学号输入了前9位就应该ajax请求了
        
        if($("#br-input-uid").val().length==10){

            //加载loading动画
            $("#feedback-uid").attr(
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
       
            account=$("#br-input-uid").val();
            if(afx_debug==false&&isAccount(account)){
                $.ajax({
                    url:getBaseURL()+"/RequestAjaxPerInfo/",
                    data:{"account":account},
                    async:true,
                    dataType:"json",
                    type:"POST",
                    success:function(result){
                        console.log(result);
                        afx_person_result=result;
                        fill_table(afx_person_result);
                        afx_ajaxed=true;//如果已经ajax过了就不要重复ajax了
                    }
                });
            }else if(afx_debug==true){
                afx_person_result=person_example;
                fill_table(afx_person_result);
                
            }else{
                return false;
            }
        }
    }
    
    function fill_table(obj){
        //如果已经是黑名单了, 就把所有东西红掉
        if(obj["badcredit"]=="true"){
            
            $("#feedback-uid").attr("class","glyphicon glyphicon-remove form-control-feedback");
            //禁止所有输入
            $("input,textarea,select,#submit")
                .attr("placeholder","该借书人已经多次遗失书籍或预期归还, 按照规定, 已经不能预约或借书了")
                .attr("disabled","disabled")
                .parent().addClass("has-error");
            $("#submit").addClass("btn-danger disabled");
            return false;
        }
        //如果没有找到这个人
        if(obj["flag"]=="false"){
            $("#br-input-uid,#br-input-una,#br-input-usp,#br-input-ulp")
                .attr("placeholder","数据库中没有找到缓存信息,请自行填写")
                .parent().addClass("has-warning");
            return true;
        }
        //如果找到了这个人
        //TODO: 正确反馈
        $("#feedback-uid").attr("class","glyphicon glyphicon-ok form-control-feedback");
        $("#br-input-uid").parent().addClass("has-success");
        if(afx_flag_name_filled==false){
            $("#br-input-una").val(obj["name"]);
            $("#br-input-una").parent().addClass("has-success");
            $("#br-input-una").change();
        }
        if(afx_flag_lpnumber_filled==false){
            $("#br-input-ulp").val(obj["lpnumber"]);
            $("#br-input-ulp").parent().addClass("has-success");
            $("#br-input-ulp").change();
        }
        if(afx_flag_spnumber_filled==false){
            $("#br-input-usp").val(obj["spnumber"]);
            $("#br-input-usp").parent().addClass("has-success");
            $("#br-input-usp").change();
        }
        
    }
    
    $("#br-input-una").change(function(){
        afx_flag_name_filled=true;
        $(this).parent()
            .removeClass("has-error")
            .removeClass("has-warning")
            .removeClass("has-success");
        $("#feedback-una").attr("class","glyphicon form-control-feedback");
        
        if(isSqlInjection($(this).val())){
           
            $(this).val("").attr("placeholder","姓名非法").parent().addClass("has-error");
            $("#feedback-una").addClass("glyphicon-remove");
            //禁止提交
            $("#submit").attr("disabled",true);
            return false;
        }
        if($(this).val().length==0){
           
            $(this).attr("placeholder","姓名不能为空").parent().addClass("has-warning");
            $("#feedback-una").addClass("glyphicon-warning");
            $("#submit").attr("disable",true);
            return false;
        }
        //合法
        $(this).parent().addClass("has-success");
        $("#feedback-una").addClass("glyphicon-ok");
        $("#submit").attr("disable",false);
        return true;
            
    });
    
    $("#br-input-ulp").change(function(){
        afx_flag_lpnumber_filled=true;
        $(this).parent()
            .removeClass("has-error")
            .removeClass("has-warning")
            .removeClass("has-success");
        $("#feedback-ulp").attr("class","glyphicon form-control-feedback");
        
        if(isSqlInjection($(this).val())||!isLpnumber($(this).val())){
           
            $(this).val("").attr("placeholder","长号非法").parent().addClass("has-error");
            $("#feedback-ulp").addClass("glyphicon-remove");
            //禁止提交
            $("#submit").attr("disabled",true);
            return false;
        }
        if($(this).val().length==0){
           
            $(this).attr("placeholder","长号不能为空").parent().addClass("has-warning");
            $("#feedback-ulp").addClass("glyphicon-warning");
            $("#submit").attr("disable",true);
            return false;
        }
        //合法
        $(this).parent().addClass("has-success");
        $("#feedback-ulp").addClass("glyphicon-ok");
        $("#submit").attr("disable",false);
        return true;   
    });
    
    $("#br-input-usp").change(function(){
        afx_flag_spnumber_filled=true;
        $(this).parent()
            .removeClass("has-error")
            .removeClass("has-warning")
            .removeClass("has-success");
        $("#feedback-usp").attr("class","glyphicon form-control-feedback");
        
        if(isSqlInjection($(this).val())||!isSpnumber($(this).val())){
           
            $(this).val("").attr("placeholder","短号非法").parent().addClass("has-error");
            $("#feedback-usp").addClass("glyphicon-remove");
            //禁止提交
            $("#submit").attr("disabled",true);
            return false;
        }
        if($(this).val().length!=0){
            //合法
            $(this).parent().addClass("has-success");
            $("#feedback-usp").addClass("glyphicon-ok");
        }
        $("#submit").attr("disable",false);
        return true;   
    
    });
    
    function on_isbn_change(){
        //isbn输入了前12位就应该ajax请求了
        if($("#br-input-isbn").val().length==13){
            //加载loading动画
            $("#feedback-isbn").attr("class","glyphicon glyphicon-refresh glyphicon-refresh-animate form-control-feedback");
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
            if(afx_debug==false&&isIsbn(isbn)){
                $.ajax({
                    url:getBaseURL()+"/RequestAjaxBookInfo/",
                    data:{"isbn":isbn},
                    async:true,
                    dataType:"json",
                    type:"POST",
                    success:function(result){
                        afx_book_result=result;
                        fill_book_info(afx_book_result);
                        afx_book_ajaxed=true;
                    }
                });
            }else if(afx_debug==true){
                afx_book_result=book_example;
                fill_book_info(afx_book_result);
                afx_book_ajaxed=true;
            }else{
                return false;
            }
        }
    }
    //自动填写书籍信息
    function fill_book_info(obj){
        //如果书没找到
        if(obj["flag"]=="false"){
            $("#feedback-isbn").attr("class","glyphicon glyphicon-remove form-control-feedback");
            $("#br-input-isbn")
                .attr("placeholder","ISBN不存在")
                .parent().addClass("has-error");
            $("#submit").attr("disabled",true).html("ISBN不存在");
            return false;
        }
        
        //如果找到书了
        $("#feedback-isbn").attr("class","glyphicon glyphicon-ok form-control-feedback");
        $("#br-input-isbn").parent().addClass("has-success");
        $("#br-input-bname").html("");
        for(var i=0;i<obj["books"].length;++i){
            $("<option></option>")
                .attr("value",obj["books"][i]["bid"])
                .html(obj["books"][i]["bname"])
                .appendTo($("#br-input-bname"));
        }
        $("#br-input-bname").val(obj["books"][0]["bid"]);
        fill_book_num(0,1);
        //绑定change消息
        $("#br-input-bname").change(function(){
            //取得bid
            bid=$(this).val();
            selectidx=0;
            for(var i=0;i<afx_book_result["books"].length;++i){
                if(bid==afx_book_result["books"][i]["bid"]){
                    selectidx=i;
                    break;
                }
            }
            fill_book_num(selectidx,1);
        });
        //允许提交
        if(afx_can_not_submit==false){
            $("#submit").attr("disabled",false).html("提 交");
        }
        
    }
    
    //生成可选数量
    function fill_book_num(bindex,selectedval){
        console.log(selectedval)
        $("#br-input-bnum").html("");
        var selectable_num=min(afx_book_result["books"][bindex]["binventory"], 
                afx_max_booknum-afx_person_result["bookednum"]);
        console.log(selectable_num)      
        for(var i=0;i<selectable_num; ++i){
                $("<option></option>")
                    .attr("value",i+1)
                    .html(i+1)
                    .appendTo("#br-input-bnum");
        }//for
        $("#br-input-bnum").val(min(selectedval,selectable_num));
        
        if(selectable_num<=0){
            $("#submit").attr("disabled",true).html("册数不可选").addClass("btn-danger");
            afx_can_not_submit=true;
        }
    }
    
    $("#br-input-bsubc").change(function(){
        bsubc=$(this).val();
        $(this).parent().removeClass("has-error").removeClass("has-ok");
        if(bsubc.length!=0&&isSqlInjection(bsubc)){
            $(this).parent().addClass("has-error");
            $(this).attr("placeholder","图书状态含有非法字符");
            $("#submit").attr("disabled",true);
            return false;
        }
        else if(bsubc.length!=0){
            $(this).parent().addClass("has-success");
            $("#submit").attr("disabled",false);
            return true;
        }
    });

    $("#submit").parents("form").submit(function(){
        return $("#submit").click();
    });
    $("#submit").click(function(){
        arr=['uid','una','ulp','isbn','bsubc'];
        for(var i=0;i<arr.length;i++){
            temp=$("#br-input-"+arr[i]).val();
            if(temp==''||temp==' '){
                illegal_feedback($("#br-input-"+arr[i]),arr[i],"该字段不能为空");
                return false;
            }
        }
        return true;
    });

        
})();
                
        