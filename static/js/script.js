const chatBox=document.getElementById("chat-box");
const userInput=document.getElementById("user-input");
const sendBtn=document.getElementById("send-btn");

async function sendMessage(){
    const message=userInput.value.trim();
    if (message==="") return;
    //Display user message
    const userMsg=document.createElement("div");
    userMsg.className="user-message";
    userMsg.textContent=message;
    chatBox.appendChild(userMsg);
    userInput.value="";

    chatBox.scrollTop=chatBox.scrollHeight;

    //send to flask backend
    const response=await fetch("http://127.0.0.1:5000/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message}),
    });

    const data=await response.json();
    const botMsg=document.createElement("div");
    botMsg.className="bot-message";
    botMsg.textContent=data.reply;
    chatBox.appendChild(botMsg);

    chatBox.scrollTop=chatBox.scrollHeight;
}

sendBtn.addEventListener("click",sendMessage);
userInput.addEventListener("keypress",(e)=>{
    if (e.key==="Enter") sendMessage();
});
   