var fs = require('fs');
var log = {
  log_mail:function(address){
    fs.appendFile('result.log',address+"\n",function(err){
        if (!err){
          // console.log('wrote data to result.log')
        }else{
          throw err;
        }
    });
  },

  read_mails:function(){
    var data = fs.readFileSync('result.log','utf8');
    var arr = data.trim().split("\n");
    return arr;
  }
}

/*
log.log_mail('ggboy@qq.com');
log.log_mail('3213359017@qq.com');
log.log_mail('nice@qq.com');

log.read_mails();
*/
module.exports=log;
