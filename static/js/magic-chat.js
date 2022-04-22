function openForm() {
    document.getElementById("myForm").style.display = "inline-block";
  }
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }


// toggles Chat Icon on and off
function chatIconOff(){
  var icon = document.getElementById("chat_ui");
    icon.style.display = "none";
}

function chatIconOn(){
  var icon = document.getElementById("chat_ui");
    icon.style.display = "inline-block";
}
