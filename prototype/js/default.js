//检查SQL注入特征, 含有SQL住区这返回真
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

//检查是否debug状态
function isDebug(){
    return true;
}
