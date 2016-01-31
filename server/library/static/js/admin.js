//全局对象
var afx_result;


(function(){

    var example={
        "watch_list":
            [
                {"account":"0000000000","name":"干事姓名","lpnumber":"13700000000",
                "spnumber":"600000","watchsum":"14","iswatching":"no","type":"new"},    
            ]
    }
    if(afx_debug==true){
        afx_result=example;
        fill_table(afx_result);
    }else{

        //django需要带上csrftoken

        var csrftoken = $.cookie('csrftoken');
        console.log(csrftoken)
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

        $.ajax({
            url:getBaseURL()+"/RequestAjaxAdmin/",
            async:true,
            dataType:"json",
            type:"POST",
            success:function(result){
                afx_result=result;
                fill_table(afx_result);
                }
            }
        );
    }
    function fill_table(obj){
        $("#tbody").html("");
        console.log(obj);
        for(var i=0;i<obj["watch_list"].length;++i)
        {
            var item=obj["watch_list"][i];
            var adding_htm;
            var adding_class;
            if(item["type"]=="delete"){
                continue;
            }
            //是否当前值班会导致表格内容不同, 这里准备好
            if(item["iswatching"]=="yes"){
                adding_htm="是&nbsp;<span class='btn btn-default btn-xs' id='";
                adding_htm+=item["account"]+"-cancelwatching"
                                +"''>撤销值班</span>";
                adding_class="warning";
            }else if(item["iswatching"]=="no"){
                adding_htm="否&nbsp;<span class='btn btn-warning btn-xs' id='";
                adding_htm+=item["account"]+"-setwatching"
                                +"''>设为值班</span>";
                adding_class="info";
            }else {
                adding_htm="不明";
                adding_class="danger";
            }
            //填充表格
            $("<tr></tr>")
                .append($("<td></td>").html(item["account"]))
                .append($("<td></td>").html(item["name"]))
                .append($("<td></td>").html(item["lpnumber"]))
                .append($("<td></td>").html(item["spnumber"]))
                .append($("<td></td>").html(item["watchsum"]))
                .append($("<td></td>").html(adding_htm))
                .append($("<td></td>").append(
                    $("<span class='btn btn-danger btn-xs' title='删除是不可逆的'>删除</span>")
                        .attr("id",item["account"]+"-delete")))
                .addClass(adding_class)
                .appendTo($("#tbody"));
                

            //响应设为值班按钮
            $("#"+item["account"]+"-setwatching").click(function(){
                id=$(this).attr("id").replace("-setwatching","");
                console.log(id);
                for(var i=0;i<afx_result["watch_list"].length;++i)
                {
                    /*
                    if(id==afx_result["watch_list"][i]["account"]){
                        afx_result["watch_list"][i]["iswatching"]="yes";
                    }else{
                        afx_result["watch_list"][i]["iswatching"]="no";
                    }
                    */
                    if(id==afx_result["watch_list"][i]["account"]){
                        afx_result["watch_list"][i]["iswatching"]="yes";
                    }
                }
                
                fill_table(afx_result);

            });
            //响应取消值班按钮
            $("#"+item["account"]+"-cancelwatching").click(function(){
                id=$(this).attr("id").replace("-cancelwatching","");
                console.log(id);
                for(var i=0;i<afx_result["watch_list"].length;++i)
                {
                    /*
                    if(id==afx_result["watch_list"][i]["account"]){
                        afx_result["watch_list"][i]["iswatching"]="yes";
                    }else{
                        afx_result["watch_list"][i]["iswatching"]="no";
                    }
                    */
                    if(id==afx_result["watch_list"][i]["account"]){
                        afx_result["watch_list"][i]["iswatching"]="no";
                    }
                }
                
                fill_table(afx_result);
            })
            //响应删除按钮
            $("#"+item["account"]+"-delete").click(function(){
                id=$(this).attr("id").replace("-delete","");
                for(var i=0;i<afx_result["watch_list"].length;++i)
                {
                    if(id==afx_result["watch_list"][i]["account"]){
                        console.log("ideq");
                        console.log(afx_result["watch_list"][i]);
                        if(afx_result["watch_list"][i]["type"]=="normal"){
                            console.log("noreq");
                            afx_result["watch_list"][i]["type"]="delete";
                        }else if(afx_result["watch_list"][i]["type"]=="new"){
                            console.log("neweq");
                            afx_result["watch_list"].splice(i,1);
                        }
                        
                    }
                }
                fill_table(afx_result);

            });
        }
        $("<tr>\
                <td>\
                    <input id='adding_account' type='text' class='form-control' placeholder='新值班干事学号' />\
                </td>\
                <td>\
                    <input id='adding_name' type='text' class='form-control' placeholder='新值班干事姓名' />\
                </td>\
                <td>\
                    <input id='adding_lpnumber' type='text' class='form-control' placeholder='新值班干事长号' />\
                </td>\
                <td>\
                    <input id='adding_spnumber' type='text' class='form-control' placeholder='新值班干事短号' />\
                </td>\
                <td> - </td>\
                <td> - </td>\
                <td><span class='btn btn-success btn-xs' id='adding_push'>添加</span></td>\
            </tr>\
        ").appendTo($("#tbody"));
        //响应添加按钮
        $("#adding_push").click(function(){
            var adding_account=$("#adding_account").val();
            var adding_name=$("#adding_name").val();
            var adding_lpnumber=$("#adding_lpnumber").val();
            var adding_spnumber=$("#adding_spnumber").val();
            var adding_sum=0;
            var adding_iswatching="no";
            //检查输入是否合法
            var flag_has_error=false;
            $(".has-feedback").css("padding-right","0");
            //检查学号
            if(isEmpty(adding_account)||isSqlInjection(adding_account) 
                ||!isAccount(adding_account)) {
                    
                $("#adding_account")
                .attr("placeholder","学号不合法")
                .parent().addClass("has-error");
                flag_has_error=true;
            }
            //检查姓名
            if(isEmpty(adding_name)||isSqlInjection(adding_account) ){
                $("#adding_name")
                .attr("placeholder","姓名不合法")
                .parent().addClass("has-error");
                flag_has_error=true;
            }
            //检查长号短号不能同时为空
            if(isEmpty(adding_lpnumber)&&isEmpty(adding_spnumber)){
                $("#adding_lpnumber, #adding_spnumber")
                .attr("placeholder","长短号不能同时为空")
                .parent().addClass("has-error");
                flag_has_error=true;
            }
            //检查长号是否合法
            if(isSqlInjection(adding_lpnumber)&&isLpnumber(adding_lpnumber)){
                $("#adding_lpnumber")
                .attr("placeholder","长号不合法")
                .parent().addClass("has-error");
                flag_has_error=true;
            }
            //检查短号是否合法
            if(isSqlInjection(adding_spnumber)&&isSpnumber(adding_spnumber)){
                $("#adding_spnumber")
                .attr("placeholder","短号不合法")
                .parent().addClass("has-error");
                flag_has_error=true;
            }
            //没问题就添加到列表中
            //注意此时数据并没有提交到服务器
            if(flag_has_error==false){
                afx_result.watch_list.push({
                    "account":adding_account,
                    "name":adding_name,
                    "lpnumber":adding_lpnumber,
                    "spnumber":adding_spnumber,
                    "watchsum":adding_sum,
                    "iswatching":adding_iswatching,
                    "type":"new",
                });
                fill_table(afx_result);
                return true;
            }
            
            return false;
        });
       
    }  
    //响应提交
    $("#submit").click(function(){
        if(has_no_watching()==true){
            alert_danger("不能没有值班干事")
            return false;
        }
            
        try{
            if(afx_debug==true)
            {
                throw "debug";
            }
            //django需要带上csrftoken

            var csrftoken = $.cookie('csrftoken');
            console.log(csrftoken)
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
            $.ajax({
                url:getBaseURL()+"/PushAjaxAdmin/",
                data:{'data':JSON.stringify(afx_result),},
                async:true,
                dataType:"json",
                type:"POST",
                success:function(result){
                    if(result['flag_succeed']=='true'){
                        succeed_str="提交成功!  "
                        try{
                            if (typeof(result['warning']) == "undefined"){
                                throw "undefined warning";
                            }
                            succeed_str+='<strong>'+result['warning'];
                            succeed_str+="&nbsp;单击&nbsp;"
                                +'<a href="/account/logout" class="btn btn-success btn-xs">退出</a>'
                                +'&nbsp;完成操作';
                           
                        }catch(e){}
                        alert_success(succeed_str);
                        for(var i=0;i<afx_result['watch_list'].length;i++){
                            var item=afx_result['watch_list'][i];
                            if(item['type']=="delete"){
                                afx_result["watch_list"].splice(i,1);
                            }else{
                                item['type']="normal";
                            }
                            
                        }
                    }else{
                        error_str="提交失败, 请重试或联系管理员";
                        try{
                            error_str+=result['error'];
                        }catch(e){}
                        
                        alert_danger(error_str);
                    }
                }
            });
        }catch(e){
            console.log(e);
            alert("提交失败, 请重试或联系管理员");
        }
    });
    //检查是不是没有值班干事, 没有值班干事返回真
    function has_no_watching(){
        flag=0;
        for(var i=0;i<afx_result['watch_list'].length;i++){
            if(afx_result['watch_list'][i]['iswatching']=="yes"&&
                afx_result['watch_list'][i]['type']!='delete'){
                flag++;
            }
        }
        if(flag>=1){
            return false;
        }else{
            return true;
        }
    }
    function alert_success(str){
        now=new Date();
        str=now.toString()+": "+str;
        $("#submit").parent().after(
            $("<div class='container'></div>").append(           
                $("<div class='alert alert-success' role='alert'></div>").html(str)
            )
            
        );
    }  

    function alert_danger(str){
        now=new Date();
        str=now.toString()+": "+str;
        $("#submit").parent().after(
            $("<div class='container'></div>").append(
                $("<div class='alert alert-danger' role='alert'></div>").html(str)
            )
        );
    }   
})();