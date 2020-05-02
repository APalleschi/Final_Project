var i = 0;
var txt = 'Lorem ipsum dummy text blabla.';
var speed = 50;

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#restricted').addEventListener('click', password);
  // document.querySelector('#magic').addEventListener('click', e);
 
});

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("demo").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}


// password protected
  function password() {
    var testV = 1;
    var pass1 = prompt('Please Enter Your Password',' ');
    while (testV < 3) {
    if (!pass1)
    history.go(-1);
    if (pass1.toLowerCase() == "i solemnly swear that i am up to no good") {
    alert('You Got it Right!');
    // window.open('library/index.html');
    break;
    }
    testV+=1;
    var pass1 =
    prompt('Access Denied - Password Incorrect, Please Try Again.','Password');
    }
    if (pass1.toLowerCase()!="password" & testV ==3)
    history.go(-1);
    return " ";
  }
