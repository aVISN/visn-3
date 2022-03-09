function openForm() {
    document.getElementById("myForm").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }

function chatToggle(){
  alert("why");
  var icon = document.getElementById("chat_ui");
  if(icon.style.display === "none"){
      icon.style.display = "inline-block";
  }
  else{
      icon.style.display = "none";
  }
}
