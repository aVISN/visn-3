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

// function toggleChat(className){
//   var chatBox = document.getElementById('chat-box');
//   var chatName = document.getElementById('chat-namebar');
  
//   if(className = 'chat-box')
//   {
//     chatBox.classList.toggle('chat-hide');
//     document.getElementById('chat-box').style.display = "none";

//   }
//   else
//   {
//     chatBox.classList.toggle('chat-hide');
//     chatName.classList.toggle('chat-hide');
//   }
  
// }

