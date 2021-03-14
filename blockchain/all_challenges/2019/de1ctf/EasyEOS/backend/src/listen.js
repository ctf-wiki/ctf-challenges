function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

var target_account = 'de1ctf111eos';

var fs = require('fs');
var sendmail = require("./sendmail.js");
var log = require('./log.js');

require("dotenv").config();
const { Api, JsonRpc, RpcError} = require('eosjs');
const { JsSignatureProvider } = require('eosjs/dist/eosjs-jssig');
const fetch = require('node-fetch');
const { TextEncoder, TextDecoder } = require('util');
const privateKey = process.env.PRIVATE_KEY;
const rpc = new JsonRpc(process.env.EOS_HTTP_ENDPOINT, { fetch });
const signatureProvider = new JsSignatureProvider([privateKey]);
const api = new Api({ rpc, signatureProvider, textDecoder: new TextDecoder(), textEncoder: new TextEncoder() });

emails = new Array();
if(fs.existsSync('result.log')){
  emails = log.read_mails();
}

(async ()=>{
  while(true){
    ret = await rpc.get_table_rows({
      json: true, // Get the response as json
      code: target_account, // Contract that we target
      scope: target_account, // Account that owns the data
      table: 'mails', // Table name
      limit: 10, // maximum number of rows that we want to get
    });

    for(i=0; i < ret.rows.length; ++i){
      data = ret.rows[i];

      if(emails.indexOf(data.address) == -1 ){
        emails.push(data.address);
        log.log_mail(data.address);
        sendmail(data.address);
        console.log(data)
      }
    }
    await sleep(5000);
  }

})().catch(error => console.log(error.message));




