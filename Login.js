let username=document.getElementById('usrn');
let password=document.getElementById('pswd');

function Check(){
  console.log(username.value);
  console.log(password.value);
  if(username.value == "test" && password.value == "admin"){
    alert("Success");
    
  }
  else{
    username.value="";
    password.value="";
    alert("Wrong Username or Password");
  }
}

