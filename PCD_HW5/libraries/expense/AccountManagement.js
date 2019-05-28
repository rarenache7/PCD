if(typeof $$ !== "undefined" && typeof $$.blockchain === "undefined"){
    const pskDB = require("pskdb");
    const pds = pskDB.startDB("../expenses");
}

$$.transaction.describe("AccountManagement", {
    create: function(balance, uname){
        let transaction = $$.blockchain.beginTransaction({});
        let account = transaction.lookup('global.Account', uname);

        account.init(balance, uname);

        try{
            transaction.add(account);
            $$.blockchain.commit(transaction);
        }catch(err){
            this.return("Account creating failed!");
            return;
        }
        console.log("Added to blockchain --------------------");
        this.return(null, uname);
    }
});