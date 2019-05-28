function register(){
	uname = document.getElementById("uname");
	email = document.getElementById("email");
	password = document.getElementById("password");
	balance = document.getElementById("initBalance");


	var registerData = {
		uname: uname.value,
		email: email.value,
		password: password.value,
		balance: balance.value
	}
	
	const interact = pskclientRequire("interact");
    interact.enableRemoteInteractions();
    const ris = interact.createRemoteInteractionSpace('testRemote', 'http://127.0.0.1:8080', 'local/agent/expense');

    ris.startSwarm('Register1', 'register', registerData).onReturn(function(response) {
        console.log(`Returning message "${response.message}"` );
        if(response.succes === true) {
			window.location.href = "index.html";
		}
        else{
        	alert("Eror from server: "+ response.message);
			fname:
				uname.value = "";
				email.value = "";
				password.value = "";
		}
    });
}