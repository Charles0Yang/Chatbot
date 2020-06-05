var voice_on = false;

function getBotResponse() {
    // Displays the user's input 
    var rawText = $("#textInput").val(); // What the user inputs
    var userHtml = '<p class="userText"><span> ' + rawText + "</span></p>"; // Converts it to html
    $("#textInput").val(""); // Gets a string
    $("#chatbox").append(userHtml); // Puts the html inside the chatbox
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" }); // Makes it so that the box containing the text will increase smoothly with every input

    $.get("/get", { msg: rawText }).done(function(data) { // Goes to the /get page which will return the bot's response as a string
        raw_data = data.toString().substring(2, data.length-2);
        var min_string_length = 100// The minimum strength length after which the response should have a "long" in the tag
        if (raw_data.length > min_string_length){ // Checks if the response is long enough to display in multiple lines
            raw_data = raw_data.replace(/['"]+/g, ''); // Removes all the " and ' which separate each sentence so they don't appear in the response
            var responses = raw_data.split(","); // Splits the response based on the commas which represent new lines
        }
        else{ // If the length of the response is not that long, there is no need to remove commas or apostrophes
            var responses = []
            responses.push(raw_data) // Add the message to the responses array so that it can be accessed in the response
        }
        var sentences = responses.length; // Gets the number of sentences that should be displayed
        for (i = 0; i < sentences; i++) { // For each sentence a new HTML line needs to be generated
            var botHtml = '<p class="botText" ><span>' + responses[i] + "</span></p>"; // Displays the response on the screen 
            $("#chatbox").append(botHtml); // Adds the html to the appropriate identifier
            document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
            if (voice_on == true){ // Checks if the user has toggled on voice 
                textToSpeech(responses[i]); // If voice has been turned on read out the message as audio output
            }
        }
    });
}

function textToSpeech(msg) {
<<<<<<< HEAD
    //Get all voices that browser offers
    var available_voices = window.speechSynthesis.getVoices();
=======
    // Get all voices that browser offers
	var available_voices = window.speechSynthesis.getVoices();
>>>>>>> f09d0eb0d0c2e090a19ced055e77661b0ffa8576

	// This will hold an english voice
    var english_voice = '';
    
    // Find voice by language locale "en-UK"
	// If not then select the first voice
	for(var i=0; i<available_voices.length; i++) {
		if(available_voices[i].lang === 'en-UK') {
			english_voice = available_voices[i];
			break;
		}
    }
    if(english_voice === '') { // If an english voice isn't availabe, use any available voice
        english_voice = available_voices[0];
<<<<<<< HEAD
    }    
    var message = new SpeechSynthesisUtterance(msg); //Creates a new object
    message.pitch = 1.5 //Assigns pitch to message
    message.rate = 1; //Assigns rate of speed of message
    window.speechSynthesis.speak(message); //Outputs the message in audio format
=======
}    
    var message = new SpeechSynthesisUtterance(msg); // Creates a new object
    message.pitch = 1.5 // Assigns pitch to message
    message.rate = 1; // Assigns rate of speed of message
    window.speechSynthesis.speak(message); // Outputs the message in audio format
>>>>>>> f09d0eb0d0c2e090a19ced055e77661b0ffa8576
}

function toggleVoiceOn() {
    voice_on = !voice_on; // Switches the state of the voice_on boolean
    // Sets the voice on button as displayed and the other button as hidden
    document.getElementById("voiceBtn").style.display = "none" 
    document.getElementById("voice2Btn").style.display = "block"
}

function toggleVoiceOff() {
    voice_on = !voice_on; 
    document.getElementById("voiceBtn").style.display = "block"
    document.getElementById("voice2Btn").style.display = "none"
}