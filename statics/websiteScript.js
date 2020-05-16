function getBotResponse() {
    //Displays the user's input 
    var rawText = $("#textInput").val(); //What the user inputs
    var userHtml = '<p class="userText"><span> ' + rawText + "</span></p>"; //Converts it to html
    $("#textInput").val(""); //Gets a string
    $("#chatbox").append(userHtml); //Puts the html inside the chatbox
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" }); //Makes it so that the box containing the text will increase smoothly with every input

    $.get("/get", { msg: rawText }).done(function(data) { //Goes to the /get page which will return the bot's response as a string
        raw_data = data.toString().substring(2, data.length-2);
        var min_string_length = 70 //The minimum strength length after which the response should have a "long" in the tag
        if (raw_data.length > min_string_length){ //Checks if the response is long enough to display in multiple lines
            raw_data = raw_data.replace(/['"]+/g, ''); //Removes all the " and ' which separate each sentence so they don't appear in the response
            var responses = raw_data.split(","); //Splits the response based on the commas which represent new lines
        }
        else{ //If the length of the response is not that long, there is no need to remove commas or apostrophes
            var responses = []
            responses.push(raw_data) //Add the message to the responses array so that it can be accessed in the response
        }
        var sentences = responses.length; //Gets the number of sentences that should be displayed
        for (i = 0; i < sentences; i++) { //For each sentence a new HTML line needs to be generated
            var botHtml = '<p class="botText" ><span>' + responses[i] + "</span></p>"; //Displays the response on the screen 
            $("#chatbox").append(botHtml); //Adds the html to the appropriate identifier
            document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
        }
    });
}

