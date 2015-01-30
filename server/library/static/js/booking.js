//全局对象
var afx_result;
var afx_flag_name_filled=false;
var afx_flag_spnumber_filled=false;
var afx_flag_lpnumber_filled=false;
var afx_ajaxed=false;
//TODO:允许修改学号时重新ajax

(function(){
    var example={"flag":"true","account":"2012052207","name":"邓作恒",
        "lpnumber":"13726247196","spnumber":"600000",
    "bookednum":9, "badcredit":"false"};
    //bookednum表示这个人已经预约的书数,总数大于8就不允许了
    //badcredit表示这个人信用度已经没有了, true表示不能借书也不能预约
    $("#br-input-uid").change(on_account_change);
    $("#br-input-uid").keypress(on_account_change);
    function on_account_change()
    {
        //先发生keypress事件, 然后才输入, 也就是说
        //学号输入了前9位就应该ajax请求了
        if($("#br-input-uid").val().length==9){
            account=$("#br-input-uid").val();
            if(afx_debug==false&&afx_ajaxed==false&&isAccount(account)){
                $.ajax({
                    url:URL+"/RequestAjaxPerInfo",
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
        //如果已经是黑名单了, 就把所有东西红掉
        if(obj["badcredit"]=="true"){
            $("#br-input-uid,#br-input-una,#br-input-usp,#br-input-ulp,#br-input-br-bnum")
                .addClass("disabled")
                .attr("placeholder","您已经多次遗失书籍或预期归还, 按照规定, 您已经不能预约或借书了")
                .parent().addClass("has-error");
            $("#submit").addClass("btn-danger disabled");
            return false;
        }
        //如果没有找到这个人
        if(obj["flag"]=="false"){
            $("#br-input-uid,#br-input-una,#br-input-usp,#br-input-ulp")
                .attr("placeholder","数据库中没有找到缓存信息,请自行填写")
                .parent().addClass("has-warning");
            return false;
        }
        //如果找到了这个人
        if(afx_flag_name_filled==false){
            $("#br-input-una").val(obj["name"]);
        }
        if(afx_flag_lpnumber_filled==false){
            $("#br-input-ulp").val(obj["lpnumber"]);
        }
        if(afx_flag_spnumber_filled==false){
            $("#br-input-usp").val(obj["spnumber"]);
        }
        //限制借书和预约数量
        $("#br-input-bnum").html("");
        for(var i=0;i<afx_max_booknum - afx_result["booknum"];++i){
            $("<option></option>")
                .attr("value",i+1).html(i+1)
                .appendTo($("#br-input-bnum"));
        }
        $("#br-input-bnum").val(1);
        return true;
        
    }
    
    $("#br-input-una").change(function(){afx_flag_name_filled=true;});
    $("#br-input-ulp").change(function(){afx_flag_lpnumber_filled=true;});
    $("#br-input-usp").change(function(){afx_flag_spnumber_filled=true;});
    
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