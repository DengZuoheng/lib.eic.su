//全局对象
var afx_result;
var afx_flag_name_filled=false;
var afx_flag_spnumber_filled=false;
var afx_flag_lpnumber_filled=false;

//TODO:允许修改学号时重新ajax

(function(){
    var example={"flag":"true","account":"2012052207","name":"邓作恒",
        "lpnumber":"13726247196","spnumber":"600000",
    "bookednum":9, "badcredit":"false"};
    //bookednum表示这个人已经预约的书数,总数大于8就不允许了
    //badcredit表示这个人信用度已经没有了, true表示不能借书也不能预约
    try{
        $("#br-input-uid")[0].oninput=on_account_change;
    }catch(e){
        $("#br-input-uid").change(on_account_change);
    }    

    function on_account_change()
    {

        //先发生input事件, 然后才输入, 也就是说

        if($("#br-input-uid").val().length==10){
            
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
                        afx_result=result;
                        fill_table(afx_result);
                        afx_ajaxed=true;//如果已经ajax过了就不要重复ajax了

                    }
                });
            }else{
                afx_result=example;
                fill_table(afx_result);
                afx_ajaxed=true;
            }
        }
    }
    
    function fill_table(obj){
        $("#feedback-uid").attr("class","glyphicon form-control-feedback");
        console.log(obj);
        //如果没有找到这个人
        if(obj["flag"]=="false"){
            $("#br-input-uid,#br-input-una,#br-input-usp,#br-input-ulp,#br-input-bnum")
                .attr("placeholder","数据库中没有找到缓存信息,请自行填写")
                .parent()
                .removeClass('has-error has-success')
                .addClass("has-warning");
            $("#feedback-uid,#feedback-una,#feedback-ulp,#feedback-usp")
                .attr("class","glyphicon form-control-feedback glyphicon-exclamation-sign");
            $("#submit").removeClass("btn-danger disabled");
            return false;
        }

        //如果已经是黑名单了, 就把所有东西红掉
        if(obj["badcredit"]=="true"){
            $("#br-input-uid,#br-input-una,#br-input-usp,#br-input-ulp,#br-input-bnum")
                .addClass("disabled")
                .attr("placeholder","您已经多次遗失书籍或预期归还, 按照规定, 您已经不能预约或借书了")
                .parent()
                .removeClass('has-warning has-success')
                .addClass("has-error");
            $("#feedback-uid,#feedback-una,#feedback-usp,#feedback-ulp")
                .attr("class","glyphicon form-control-feedback glyphicon-remove");
            $("#submit").addClass("btn-danger disabled") ;
            return false;
        }
        
        //如果找到了这个人,而且不是黑名单
        $("#feedback-uid").addClass("glyphicon-ok");
        $("#br-input-uid").parent().removeClass("has-warning has-error").addClass("has-success");
        console.log($("#br-input-una").val());
        if($("#br-input-una").val()!=" "){

            $("#br-input-una").val(obj["name"]).change();
        }
        if($("#br-input-ulp").val()!=" "){
            $("#br-input-ulp").val(obj["lpnumber"]).change();
        }
        if($("#br-input-usp").val()!=" "){
            $("#br-input-usp").val(obj["spnumber"]).change();
        }
        //限制借书和预约数量
        book_bookable=$("#br-input-bnum option:last").html();
        $("#br-input-bnum").html("");
       
        console.log(book_bookable);
        user_bookable=afx_max_booknum - afx_result["bookednum"];
        fin_bookable=min(book_bookable,user_bookable);
        for(var i=0;i<fin_bookable;++i){
            $("<option></option>")
                .attr("value",i+1).html(i+1)
                .appendTo($("#br-input-bnum"));
        }
        $("#br-input-bnum").val(1);
        return true;
        
    }
    
    $("#br-input-una").change(function(){
        var temp=$(this).val();
        if(isSqlInjection(temp)){
            return illegal_feedback($(this),"una","非法输入");
        }else{
            return legal_feedback($(this),"una","");
        }

    });
    $("#br-input-ulp").change(function(){
        var temp=$(this).val();
        if(isSqlInjection(temp)||!isLpnumber(temp)){
            return illegal_feedback($(this),"ulp","非法输入");
        }else{
            return legal_feedback($(this),"ulp","");
        }
    });
    $("#br-input-usp").change(function(){
        var temp=$(this).val();
        if(!temp){return true;}
        if(isSqlInjection(temp)||!isSpnumber(temp)){
            return illegal_feedback($(this),"usp","非法输入");
        }else{
            return legal_feedback($(this),"usp","");
        }
    });
    $("#submit").parents("form").submit(function(){
        return $("#submit").click();
    })
    $("#submit").click(function(){
        var uid=$("#br-input-uid").val();
        var una=$("#br-input-una").val();
        var usp=$("#br-input-usp").val();
        var ulp=$("#br-input-ulp").val();
        if(isSqlInjection(uid)||!isAccount(uid)){
            $("#br-input-uid")
                .attr("placeholder","学号不合法").val("")
                .parent().addClass("has-error");
            return false;
        }
        if(isSqlInjection(una)||una.length==0){
            $("#br-input-una")
                .attr("placeholder","姓名不合法").val("")
                .parent().addClass("has-error");
            return false;
        }
        if(isSqlInjection(usp)){
            $("#br-input-usp")
                .attr("placeholder","短号不合法").val("")
                .parent().addClass("has-error");
            return false;
        }
        if(isSqlInjection(ulp)||!isLpnumber(ulp)){
            $("#br-input-ulp")
                .attr("placeholder","长号不合法").val("")
                .parent().addClass("has-error");
            return false;
        }

        return true;
    });
                  
})();