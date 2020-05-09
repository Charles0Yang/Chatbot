function getBotResponse() {
    //Displays the user's input 
    var rawText = $("#textInput").val();
    var userHtml = '<p class="userText"><span>' + rawText + "</span></p>"; 
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" }); //Makes it so that the box containing the text will increase smoothly with every input

    $.get("/get", { msg: rawText }).done(function(data) { //Goes to the /get page which will return the bot's response as a string
        var botHtml = '<p class="botText"><span>' + data + "</span></p>"; //Displays the response on the screen 
        $("#chatbox").append(botHtml);
        document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
    });
}