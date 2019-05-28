$$.asset.describe("Account", {
    public: {
        balance: "number",
        uname: "string",

    },
    init: function(balance, uname){
        if(!!this.uname){
            return false;
        }

        this.balance = balance;
        this.uname = uname;

        return true;
    }
});