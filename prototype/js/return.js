//return.js

(function(){
    $("#rt-input-uid").change(function(){
        uid=$(this).val();
        if(!isAccount(uid)){
            $(this)
                .val("")
                .attr("placeholder","非法输入")
                .parent().removeClass("has-success")
                .addClass("has-error");
            $("#feedback-uid")
                .attr("class","glyphicon form-control-feedback")
                .addClass("glyphicon-remove");
            $("#submit")
                .removeClass("btn-primary")
                .addClass("btn-danger")
                .attr("disabled",true);
        }else{
            $(this)
                .parent().removeClass("has-error")
                .addClass("has-success");
            $("#feedback-uid")
                .attr("class","glyphicon form-control-feedback")
                .addClass("glyphicon-ok");
            $("#submit")
                .removeClass("btn-danger")
                .addClass("btn-primary")
                .attr("disabled",false);
        }
    });
    $("#submit").click(function(){
        if($("#rt-input-uid").val().length==0)
        {
            $("rt-input-uid").change();
            return false;
        }else{
            return true;
        }
    });
})();