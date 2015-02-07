(function(){
    $("#submit").click(function(){
        if(!isEmpty($("#search-key-word").val())
            && !isSqlInjection($("#search-key-word").val())){
            console.log("合法字符");
            $("#search-form").submit();
           
            console.log("submited")          
        }
        else{
            console.log("非法字符");
            $("#search-key-word")
                .val("")
                .attr("placeholder","您的输入含非法字符")
                .parent()
                .parent(".has-feedback")
                .addClass("has-error");
            return false;
        }
    })
})();