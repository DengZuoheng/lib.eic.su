(function(){
//设置data-upload-url
    $("#input-file-redo")
        .attr("data-upload-url",getBaseURL()+"/backups/PushAjaxRedoFile")
        .fileinput({
            'showUpload':true,
            'showPreview':false,
            //'allowedFileExtensions':['json'],
            'browseClass':'btn btn-warning',
            'browseLabel':'选择文件用以<strong>&nbsp;增量还原&nbsp;</strong>',
            'uploadLabel':'上传',
            'removeLabel':'移除',
            'cancelLabel':'取消',
            'ajaxSettings':{headers: {'X-CSRFToken':$.cookie('csrftoken')}},
        
        })
        .on('filebatchuploadsuccess',function(event,data,previewId,index){
            response = data.response;
            console.log(response)
            var str;
            
            if(response['flag']=='true'){
                //success
                str = success_alert_str(
                        response['filename'],
                        '已经添加到数据库中!');
                append_restore_record(response['restore_record']);
                
            }else{
                str = failed_alert_str(
                        response['filename'],
                        response['exception'],
                        '还原失败');
            }
            $("form:last").after($("<div></div>").html(str));
        });
    
    function success_alert_str(filename,extra_str){
        now = new Date();
        str= "<div class='lead'></div>"+
                "<div class='alert alert-success' role='alert'>"+
                    "<p>"+
                        "<span class='glyphicon glyphicon-ok' aria-hidden='true'>&nbsp;</span>"+
                        now.toString()+" - "+
                        "&nbsp;您上传的文件<strong>"+
                            filename+
                        "</strong>&nbsp;"+extra_str+
                    "</p>"+
                "</div>";
        return str;
    }

    function failed_alert_str(filename,exception,extra_str){
        now = new Date();
        str = "<div class='lead'></div>"+
                "<div class='alert alert-danger' role='alert'>"+
                    "<p>"+
                        "<span class='glyphicon glyphicon-remove' aria-hidden='true'>&nbsp;</span>"+
                        now.toString()+" - "+
                        "&nbsp;"+extra_str+ "- <strong>"+
                            filename+" - "+exception+
                        "</strong>&nbsp;"+
                    "</p>"+
                "</div>";
        return str;
    }

    function append_restore_record(record){
        if($("#norestoreflag").length>0){
            $("#restore-table tbody").html("");
        }
        $("<tr></tr>").append($("<td></td>").html(record['rtime']))
            .append($("<td></td>").html(record['version']))
            .append($("<td></td>").html(record['operator']))
            .append($("<td></td>").html(record['rtype']))
            .appendTo($("#restore-table tbody"));
    }

    $("#input-file-overide")
        .attr("data-upload-url",getBaseURL()+"/backups/PushAjaxOverideFile")
        .fileinput({
            'showUpload':true,
            'showPreview':false,
            'allowedFileExtensions':['json'],
            'browseClass':'btn btn-danger',
            'browseLabel':'&emsp;&emsp;选择文件用以<strong>&nbsp;覆盖&nbsp;</strong>',
            'uploadLabel':'上传',
            'removeLabel':'移除',
            'cancelLabel':'取消',
            'ajaxSettings':{headers: {'X-CSRFToken':$.cookie('csrftoken')}},
        })
        .on('filebatchuploadsuccess',function(event,data,previewId,index){
            response = data.response;
            console.log(response)
            var str;
            
            if(response['flag']=='true'){
                //success
                str = success_alert_str(
                        response['filename'],
                        '已经覆盖当前数据库!');
                append_restore_record(response['restore_record']);
                
            }else{
                str = failed_alert_str(
                        response['filename'],
                        response['exception'],
                        '覆盖失败');
            }
            $("form:last").after($("<div></div>").html(str));
        });
    if($("#nobackupflag").length==0){
        $("td a").each(function(){
            $(this).click(function(){
                pattern = /.*(\d+)$/;
                try{
                    id=pattern.exec($(this).attr('href'))[1];
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
                    if($(this).hasClass('overide')){
                        $.ajax({
                            url:getBaseURL()+"/backups/PushAjaxOverideID",
                            data:{'id':id},
                            async:true,
                            dataType:"json",
                            type:"POST",
                            success:function(result){
                                var str;
                                if(result['flag']=='true'){
                                    str = success_alert_str(
                                        result['filename'],
                                        '已经覆盖当前数据库!');
                                    append_restore_record(result['restore_record']);
                                }else{
                                    str = failed_alert_str(
                                            result['filename'],
                                            result['exception'],
                                            '覆盖失败');
                                }
                                $("form:last").after($("<div></div>").html(str));
                            }
                        });
                    }else if($(this).hasClass('redo')){
                        $.ajax({
                            url:getBaseURL()+"/backups/PushAjaxRedoID",
                            data:{'id':id},
                            async:true,
                            dataType:"json",
                            type:"POST",
                            success:function(result){
                               var str;
            
                                if(result['flag']=='true'){
                                    //success
                                    str = success_alert_str(
                                            result['filename'],
                                            '已经添加到数据库中!');
                                    append_restore_record(result['restore_record']);
                                    
                                }else{
                                    str = failed_alert_str(
                                            result['filename'],
                                            result['exception'],
                                            '还原失败');
                                }
                                $("form:last").after($("<div></div>").html(str));    
                            }
                        });
                    }
                    
                }catch(e){
                    //pass
                }
                
                return false;
            });
        });
    }

})();