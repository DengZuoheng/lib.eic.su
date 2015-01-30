//全局变量
var afx_debug=true;//设定JS是否处于debug状态
var afx_max_booknum=12;//最大借书和预约数量
var afx_float_default_prec=2;//默认浮点数精度

//检查SQL注入特征, 含有SQL语句这返回真
function isSqlInjection(str){
    try{
        re=/select|update|delete|truncate|join|union|exec|insert|drop|count|’|"|;|>|<|%/i;
        if(re.test(str.toLowerCase())){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return true;
    }
    
}

//检查字符串是否为空, 空则返回真
function isEmpty(str){
    try{
        return str.length==0;
    }catch(e){
        console.log(e);
        return true;
    }
    
}

//检查是否合法学号, 合法返回真
function isAccount(str){
    try{
        var pattern = /^\d{10}$/; 
        if(pattern.test(str)){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return false;
    }
}

//检查是否合法长号, 合法返回真
function isLpnumber(str){
    try{
        var pattern = /^\d{11}$/; 
        if(pattern.test(str)){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return false;
    }
}

//检查是否合法短号, 合法返回真
function isSpnumber(str){
    try{
        var pattern = /^\d{6}$/; 
        if(pattern.test(str)){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return false;
    }
}

//检查是否合法isbn, 合法返回真
function isIsbn(str){
    try{
        var pattern13=/^\d{13}$/;
        var pattern9=/^\d{9}$/;
        if(pattern13.test(str)||pattern9.test(str)){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return false;
    }
}

//检查是否debug状态
function isDebug(){
    return true;
}

function min(i1,i2){
    if(i1<=i2){return i1;}
    else{return i2;}
}

function max(i1,i2){
    if(i1<=i2){return i2;}
    else{return i1;}
}

//检查是不是一定范围内的整数
function isIntBetween(str,min,max){
    try{
        pattern=/^[0-9]{0,99}$/;
        if(!pattern.test(str)){
            return false;
        }
        var ret=parseInt(str);
        if(ret>=min&&ret<max){
            return true;
        }
        return false;
    }catch(err){
        console.log(err);
        return false;
    }
}

//检查是不是一定范围内的浮点数
function isFloatBetween(str,min,max){
    try{
        pattern=/^[0-9\.]{0,9}$/;
        if(!pattern.test(str)){
            return false;
        }
        var ret=parseFloat(str);
        if(ret>=min&&ret<max){
            return true;
        }
        return false;
    }catch(err){
        console.log(err);
        return false;
    }
}

//检查是不是URI
function isURI(str){
    try{
        pattern=/^http:\/\/[A-Za-z0-9\.-]{3,}\.[A-Za-z]{3}/;
        if(pattern.test(str)){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return false;
    }
}

//检查年月
function isYearMonth(str){
    try{
        pattern=/^(\d{4}\.\d{1})|(\d{4}\.\d{2})$/;
        if(pattern.test(str)){
            return true;
        }else{
            return false;
        }
    }catch(e){
        console.log(e);
        return false;
    }
}