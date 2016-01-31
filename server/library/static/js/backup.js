//全局对象
var afx_result;
(function(){
    var example={
        "flag":"true",
        "version":"lib.eic.su.backups.2012.5.22.12.34.56.json",
        "url":"http://libeicsu-backups.stor.sinaapp.com/lib.eic.su.backups.2012.5.22.12.34.56.json",
        "gtime":"2012/05/22 12:34",
        "operator":"Administrator",
        "delete_url":"/delete/1"
    };
    $("#new-backup").click(function(){
        if(afx_debug==true){
            afx_result=example;
            append_result(afx_result);
        }else{
            var csrftoken = $.cookie('csrftoken');
            function csrfSafeMethod(method){
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings){
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });   
            $.ajax({
                url:getBaseURL()+"/backups/RequestAjaxBackup",
                async:true,
                dataType:"json",
                type:"POST",
                success:function(result){
                    console.log(result);
                    afx_result=result;
                    append_result(afx_result);
                }
            });
        }
    });
    
    function append_result(obj)
    {
        if(obj["flag"]=="false"){
            alert_danger(obj);
            return false;
        }
        
        alert_success(obj);

        function get_download_str(str){
            ret = '<a href="'
                + str
                +'" class="btn btn-default btn-xs" download>'
                +'<span class="glyphicon glyphicon-download-alt"></span>'
                +'&nbsp;下 载</a>';
            return ret;

        }
        function get_delete_str(str){
            ret = '<a href="'
                + str
                +'" class="btn btn-danger btn-xs">'
                +'<span class="glyphicon glyphicon-trash"></span>'
                +'&nbsp;删 除</a>';
            return ret;
        }
    }
    function alert_danger(obj){
        now=new Date();
        str = now.toString()+" - 创建失败: "+obj['error']+"!";
        $("#new-backup").parent().after(
            $("<div class='container'></div>").append(
                $("<div class='alert alert-danger' role='alert'></div>").html(str)
            )
        );
    }
    function alert_success(obj){
        now=new Date();
        str = now.toString()+" - 创建成功! 请稍后再刷新查看, 备份操作将在24小时内自动完成";
        $("#new-backup").parent().after(
            $("<div class='container'></div>").append(
                $("<div class='alert alert-success' role='alert'></div>").html(str)
            )
        );
    }
})();