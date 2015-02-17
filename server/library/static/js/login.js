(function(){
    $("#fake-captcha").attr("src",$("#hidden-form img.captcha").attr("src"));
    $("#br-input-uid").val($("#hidden-form #id_account").val())
    //$("#br-input-pw").val($("#hidden-form #id_password").val())
    //看不清,换一张
    $("#fake-refresh,#fake-captcha").click(function(){
        //TODO:wp8 ie这里有bug
        $form = $("#hidden-form");
        var url = getBaseURL() + "/captcha/refresh/";
        $.getJSON(url, {}, function(json) {
            console.log(json);
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
            $("#fake-captcha").attr("src",$("#hidden-form img.captcha").attr("src"));
        });

        return false;
    });
    try{
        hidden_error=$(".errorlist li").html()
        console.log(hidden_error)
        if(hidden_error.length>=0){
            if("Invalid CAPTCHA"==hidden_error){
                hidden_error="验证码错误";
            }
            $("#br-input-uid").parent().parent().before(
                $("<div class='form-group has-feedback'>"
                        +"<label class='text-danger col-sm-2 control-label'>* 异常</label>"
                        +"<div class='col-sm-10 form-control-static' role='alert'>"
                            +"<strong class='text-danger'>"+hidden_error+"</strong>"
                        +"</div>"
                    +"</div>"
                )
            );
        }
    }catch(e){
        //pass
    }
    $("#br-input-uid").change(function(){
        temp=$(this).val();
        if(temp.length==4 && temp=='root'){
            return legal_feedback($(this),"uid","");
        }else if(temp.length>=10){
            if($(this).val()=='root'||isAccount($(this).val())){
                return legal_feedback($(this),"uid","");
            }else{
                return illegal_feedback($(this),"uid","非法输入");
            }
        }
        
    });
    $("#br-input-pw").change(function(){
        if(!isSqlInjection($(this).val())){
            return legal_feedback($(this),"pw","");
        }else{
            return illegal_feedback($(this),"pw","非法输入");
        }
    });
    $("#br-input-capt").change(function(){
        if($(this).val().length>4||$(this).val()==''){
            return illegal_feedback($(this),"capt","非法输入");
        }else if($(this).val().length=4){
            return legal_feedback($(this),"capt","");
        }
    });
    try{
        $("#br-input-pw")[0].oninput=function(){
            $(this).change();
        }
        $("#br-input-uid")[0].oninput=function(){
            $(this).change();
        }
        $("#br-input-capt")[0].oninput=function(){
            //$("#id_captcha_1").val($("#br-input-capt").val());
            $(this).change();
        }
    }catch(e){
        console.log(e);
    }
    $("#submit").parents("form").submit(function(){
        return $("#submit").click();
    });
    
    $("#submit").click(function(){
        $("#br-input-pw,#br-input-uid,#br-input-capt").change();
        if($("#br-input-pw").val()==' '||$("#br-input-pw").val()==''){
            illegal_feedback($("#br-input-pw"),"pw","密码不能为空");
            return false;

        }
        if($("#br-input-uid").val()==' '||$("#br-input-uid").val()==''){
            illegal_feedback($("#br-input-uid"),"uid","账号不能为空");
            return false;
        }
        if($("#br-input-capt").val()==' '||$("#br-input-capt").val()==''){
            illegal_feedback($("#br-input-capt"),"capt","验证码不能为空");
            return false;
        }
        $("#id_account").val($("#br-input-uid").val());
        $("#id_password").val(md5($("#br-input-pw").val()));
        //$("#id_password").val($("#br-input-pw").val());
        $("#id_captcha_1").val($("#br-input-capt").val());
        $("#hidden-form").submit();
        return false;

    });
    
})();