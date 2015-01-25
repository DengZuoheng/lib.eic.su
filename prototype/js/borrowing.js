//全局对象
var afx_person_result;
var afx_book_result;
var afx_flag_name_filled=false;
var afx_flag_spnumber_filled=false;
var afx_flag_lpnumber_filled=false;
var afx_person_ajaxed=false;
var afx_book_ajaxed=false;
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
    $("#br-input-uid").keypress(on_account_change);
    //$("#br-input-isbn").change(on_isbn_change);
    $("#br-input-isbn").keypress(on_isbn_change);
    function on_account_change(){
        //先发生keypress事件, 然后才输入, 也就是说
        //学号输入了前9位就应该ajax请求了
        
        if($("#br-input-uid").val().length==9){
            console.log("F");
            //加载loading动画
            $("#br-input-uid")
                .parent().append(
                    $("<span></span>").attr({
                        "class":"glyphicon glyphicon-refresh glyphicon-refresh-animate form-control-feedback",
                        "id":"feedback-uid"})
                    );
                        
            account=$("#br-input-uid").val();
            if(afx_debug==false&&isAccount(account)){
                $.ajax({
                    url:URL+"/RequestAjaxPerInfo/",
                    data:{"account":account},
                    async:true,
                    dataType:"json",
                    type:"POST",
                    success:function(result){
                        afx_person_result=result;
                        fill_table(afx_person_result);
                        afx_ajaxed=true;//如果已经ajax过了就不要重复ajax了
                    }
                });
            }else{
                afx_person_result=person_example;
                fill_table(afx_person_result);
                
            }
        }
    }
    
    function fill_table(obj){
        //如果已经是黑名单了, 就把所有东西红掉
        if(obj["badcredit"]=="true"){
            console.log(9);
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
        if(afx_flag_name_filled==false){
            $("#br-input-una").val(obj["name"]);
        }
        if(afx_flag_lpnumber_filled==false){
            $("#br-input-ulp").val(obj["lpnumber"]);
        }
        if(afx_flag_spnumber_filled==false){
            $("#br-input-usp").val(obj["spnumber"]);
        }
        
    }
    
    $("#br-input-una").change(function(){afx_flag_name_filled=true;});
    $("#br-input-ulp").change(function(){afx_flag_lpnumber_filled=true;});
    $("#br-input-usp").change(function(){afx_flag_spnumber_filled=true;});
    
    function on_isbn_change(){
        //isbn输入了前12位就应该ajax请求了
        if($("#br-input-isbn").val().length==12){
            isbn=$("#br-input-isbn").val();
            if(afx_debug==false&&afx_ajaxed==false&&isIsbn(isbn)){
                $.ajax({
                    url:URL+"RequestAjaxBookInfo/",
                    data:{"isbn":account},
                    async:true,
                    dataType:"json",
                    type:"POST",
                    success:function(result){
                        afx_book_result=result;
                        fill_book_info(afx_book_result);
                        afx_book_ajaxed=true;
                    }
                });
            }else{
                afx_book_result=book_example;
                fill_book_info(afx_book_result);
                afx_book_ajaxed=true;
            }
        }
    }
    //自动填写书籍信息
    function fill_book_info(obj){
        //如果书没找到
        if(obj["flag"]=="false"){
            $("#br-input-isbn")
                .attr("placeholder","ISBN不存在")
                .parent().addClass("has-error");
            $("#submit").attr("disabled",true).html("ISBN不存在");
            return false;
        }
        
        //如果找到书了
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
        $("#submit").attr("disabled",false).html("提交");
    }
    
    //生成可选数量
    function fill_book_num(bindex,selectedval){
        $("#br-input-bnum").html("");
        for(var i=0;
            i<min(afx_book_result["books"][bindex]["binventory"], 
            afx_max_booknum-afx_person_result["bookednum"]);
            ++i){
                $("<option></option>")
                    .attr("value",i+1)
                    .html(i+1)
                    .appendTo("#br-input-bnum");
        }//for
        $("#br-input-bnum").val(max(selectedval,min(afx_book_result["books"][bindex]["binventory"], 
            afx_max_booknum-afx_person_result["bookednum"])));
    }
        
})();
                
        