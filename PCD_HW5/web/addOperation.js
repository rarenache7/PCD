function addOperation(){
	amount = document.getElementById("amountV");
    operationType = document.getElementById("operationType");
    uname =  document.getElementById("sessionId");

	var operationData = {
        uname: sessionId.value,
		amount: amount.value,
        operationType: operationType.value
	}

	const interact = pskclientRequire("interact");
    interact.enableRemoteInteractions();
    const ris = interact.createRemoteInteractionSpace('testRemote', 'http://127.0.0.1:8080', 'local/agent/expense');

    ris.startSwarm('Register1', 'addOperation', operationData).onReturn(function(response) {
        console.log(`Returning message "${response.message}"` );
        if(response.succes === true){
            var uname = response.uname;
            var q = "?user=" + uname + "&balance=" + response.balance;
            window.location.href = "account.html" + q;
		}
        else{
        	alert("Eror from server: " + response.message);
		}
    });

    ris.startSwarm("AccountManagement", "create", operationData.balance, operationData.uname)
    .onReturn(function(err, accountId){
        if(err){
            console.log(err);
        } else {
            console.log("Succes");
        }
    });
    
}