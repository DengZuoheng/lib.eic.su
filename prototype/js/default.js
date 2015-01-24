//全局变量
var afx_debug=true;//设定JS是否处于debug状态

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
        var pattern = /\d{10}/; 
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
        var pattern = /\d{11}/; 
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
        var pattern = /\d{6}/; 
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

//检查是否debug状态
function isDebug(){
    return true;
}
