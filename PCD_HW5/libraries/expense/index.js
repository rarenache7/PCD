$$.swarms.describe("Register1", {
    register: function (user) {
        console.log("AICI");
        var file = "myJson.json"
        console.log("Register new user");
        var fs = require('fs');
        var succes = true;
        try {
            if (fs.existsSync(file)) {
                var self = this;
                console.log("file exists _________________________");
                fs.readFile(file, function read(err, rawData) {
                    if (err) {
                        console.log("Reading from file " + file + "throwing error");
                        self.return({ message: "Internal Server Error", succes: false });
                    }
                    let content = JSON.parse(rawData);
                    if (content.hasOwnProperty('users')) {
                        for (var i = 0; i < content.users.length; i++) {
                            console.log("are users");
                            if (content.users[i].uname === user.uname) {
                                console.log("Username already used");
                                succes = fale;
                                self.return({ message: "Username already used", succes: false });
                            }
                        }

                        content.users.push(user);

                        fs.writeFile(file, JSON.stringify(content), (err) => {
                            // throws an error, you could also catch it here
                            if (err) {
                                console.log("Eror on writing in file")

                                self.return({ message: "Error on register", succes: false });
                            }

                            console.log("New user registered with succes");
                            self.return({ message: "New user registered with succes", succes: true });
                        });

                    } else {
                        console.log("Property users doesn't exist");
                        this.return({ message: "Internal Server Eror", succes: false });
                    }

                    console.log(content);

                });
            } else {
                console.log("File doesn't exist");
                var fileContent = { users: [] };
                console.log(fileContent);
                var usersArray = fileContent.users;
                console.log(usersArray);
                usersArray.push(user);

                fs.writeFile(file, JSON.stringify(fileContent), (err) => {
                    // throws an error, you could also catch it here
                    if (err) {
                        consol.log("Eror on writing in file")
                        this.return({ message: "Error on register", succes: false });
                    }

                    console.log("New user registered with succes");
                    this.return({ message: "New user registered with succes", succes: true });
                });
            }
        } catch (err) {
            console.error(err)
            this.return({ message: "Internal Server Error", succes: false });
        }

    },
    login: function (user) {
        console.log("Verify if user is in database 1");
        console.log("User ..............");
        console.log(user.uname);
        console.log("email " + user.email);
        console.log(user.password);
        console.log("___________________");
        var file = "myJson.json"
        var fs = require('fs');
        var self = this;
        if (fs.existsSync(file)) {
            console.log("file exists");
            fs.readFile(file, function read(err, rawData) {
                console.log("reading files");
                if (err) {
                    console.log("Reading from file " + file + "throwing error");
                    self.return({ message: "Internal Server Error", succes: false });
                }
                let content = JSON.parse(rawData);
                if (content.hasOwnProperty('users')) {
                    console.log('Users from file: ', content.users.length)
                    for (var i = 0; i < content.users.length; i++) {
                        console.log("User " + i + " __________");
                        console.log(content.users[i].uname);
                        console.log(content.users[i].password);
                        console.log("______________________");
                        if (content.users[i].uname === user.uname && content.users[i].password === user.password) {
                            console.log("Valid user");
                            console.log(user.uname);
                            self.return({ message: "Username and password match",
                                balance: content.users[i].balance, uname: user.uname, succes: true });
                        }
                    }
                    // console.log("Invalid Username or Password");
                    // self.return({ message: "Invalid Username or Password", succes: false });
                } else {
                    console.log("Invalid Username or Password");
                    self.return({ message: "Invalid Username or Password", succes: false });
                }

            })
        } else {
            this.return({ message: "Internal Server Error", succes: false });
        }
    },

    addOperation: function (operationData) {
        var file = "myJson.json"
        var fs = require('fs');
        var self = this;
        if (fs.existsSync(file)) {
            console.log("file exists");
            fs.readFile(file, function read(err, rawData) {
                console.log("reading files");
                if (err) {
                    console.log("Reading from file " + file + "throwing error");
                    self.return({ message: "Internal Server Error", succes: false });
                }
                let content = JSON.parse(rawData);
                console.log("add " + content.users.length);

                for (var i = 0; i < content.users.length; i++) {
                    console.log("here " + operationData.uname);
                    console.log("file " + content.users[i].uname);
                    if (content.users[i].uname === operationData.uname) {
                        var newBalance = operationData.amount;
                        
                        if (operationData.operationType == "expense") {
                            console.log("true");
                            newBalance = newBalance * (-1);
                        }

                        console.log("Old Balance: " + content.users[i].balance);
                        var newBalan = parseInt(newBalance) + parseInt(content.users[i].balance);
                        content.users[i].balance = newBalan;

                        console.log("New Balance: " + content.users[i].balance);

                        fs.writeFile(file, JSON.stringify(content), (err) => {
                            // throws an error, you could also catch it here
                            if (err) {
                                console.log("Eror on writing in file")

                                self.return({ message: "Error on register", succes: false });
                            }

                            console.log("Operation added");
                            self.return({ message: "Operation added", balance:newBalan, uname: operationData.uname, succes: true });
                        });
                    } else {
                        console.log("ERROR");
                        self.return({ message: "Operation skipped", succes: false });
                    }
                }
            })
        }
    },
});
