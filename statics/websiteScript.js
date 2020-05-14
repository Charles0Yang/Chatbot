function getBotResponse() {
    //Displays the user's input 
    var rawText = $("#textInput").val(); //What the user inputs
    var userHtml = '<p class="userText"><span>' + rawText + "</span></p>"; //Converts it to html
    $("#textInput").val(""); //Gets a string
    $("#chatbox").append(userHtml); //Puts the html inside the chatbox
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" }); //Makes it so that the box containing the text will increase smoothly with every input

    $.get("/get", { msg: rawText }).done(function(data) { //Goes to the /get page which will return the bot's response as a string
        raw_data = data.toString().substring(2, data.length-2);
        raw_data = raw_data.replace(/['"]+/g, '');
        var responses = raw_data.split(",");
        var sentences = responses.length;
        for (i = 0; i < sentences; i++) {
            var botHtml = '<p class="botText"><span>' + responses[i] + "</span></p>"; //Displays the response on the screen 
            $("#chatbox").append(botHtml);
            document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
        }
    });
}