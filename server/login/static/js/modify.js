(function(){
    $("#br-input-orig-pw,#br-input-new-pw,#br-input-confirm-pw").change(function(){
        temp=$(this).val();
        attr=$(this).attr("id").replace("br-input-","");
        if(temp.length<afx_min_passw_length
            ||temp.length>=afx_max_passw_length){
            return illegal_feedback($(this),attr,"密码长度不能小于6位或大于64位"); 
        }
        if(attr=='confirm-pw' && $("#br-input-new-pw").val()!=''){
            if($(this).val()!=$("#br-input-new-pw").val()){
                illegal_feedback($("#br-input-new-pw"),attr,"新密码与确认密码不一致");
                return illegal_feedback($(this),attr,"新密码与确认密码不一致");  
            }
        }
        if(attr=='new-pw' && $("#br-input-confirm-pw").val()!=''){
            console.log($("#br-input-confirm-pw").val())
            if($(this).val()!=$("#br-input-confirm-pw").val()){
                illegal_feedback($("#br-input-confirm-pw"),attr,"新密码与确认密码不一致");
                return illegal_feedback($(this),attr,"新密码与确认密码不一致");  
            }
        }
        return legal_feedback($(this),attr,"");
    });
    try{
        $("#br-input-orig-pw")[0].oninput=function(){
            if($(this).val().length>=6){
                $(this).change();
            }
        }
        $("#br-input-new-pw")[0].oninput=function(){
            if($(this).val().length>=6){
                $(this).change();
            }
        }
        $("#br-input-confirm-pw")[0].oninput=function(){
            if($(this).val().length>=$("#br-input-new-pw").val().length){
                $(this).change();
            }
        }
    }catch(e){
        console.log(e);
    }
    $("#submit").click(function(){
        if($("#br-input-orig-pw").val().length<6){
            return illegal_feedback($(this),"orig-pw","密码长度不能小于6位或大于64位"); 
        }
        if($("#br-input-new-pw").val().length<6){
            return illegal_feedback($(this),"new-pw","密码长度不能小于6位或大于64位"); 
        }
        if($("#br-input-confirm-pw").val().length<6){
            return illegal_feedback($(this),"confirm-pw","密码长度不能小于6位或大于64位"); 
        }
        orig_pw=$("#br-input-orig-pw").val();
        new_pw=$("#br-input-new-pw").val();
        confirm_pw=$("#br-input-confirm-pw").val();
        $("#br-input-orig-pw").val(md5(orig_pw));
        $("#br-input-new-pw").val(md5(new_pw));
        $("#br-input-confirm-pw").val(md5(confirm_pw));
        return true;
    });
})();