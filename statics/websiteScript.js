// Javascript file

// At the start there is no voice
var voice_on = false;

// Function to get the chatbot response
function getBotResponse() {

    // Displays the user's input 
    var rawText = $("#textInput").val(); // What the user inputs
    var userHtml = '<p class="userText"><span> ' + rawText + "</span></p>"; // Converts it to html
    $("#textInput").val(""); // Gets a string
    $("#chatbox").append(userHtml); // Puts the html inside the chatbox
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" }); // Makes it so that the box containing the text will increase smoothly with every input

    $.get("/get", { msg: rawText }).done(function(data) { // Goes to the /get page which will return the bot's response as a string
        
        raw_data = data.toString().substring(2, data.length-2); // The chatbot response
        var min_string_length = 100 // The minimum strength length after which the response should have a "long" in the tag
        
        // Checks if the response is long enough to display in multiple lines
        if (raw_data.length > min_string_length){
            raw_data = raw_data.replace(/['"]+/g, ''); // Removes all the " and ' which separate each sentence so they don't appear in the response
            var responses = raw_data.split(","); // Splits the response based on the commas which represent new lines
        }

        // If the length of the response is not that long, there is no need to remove commas or apostrophes
        else{
            var responses = []
            responses.push(raw_data) // Add the message to the responses array so that it can be accessed in the response
        }

        // Gets the number of sentences that should be displayed
        var sentences = responses.length;

        // For each sentence a new HTML line needs to be generated
        for (i = 0; i < sentences; i++) { 

            var botHtml = '<p class="botText" ><span>' + responses[i] + "</span></p>"; // Displays the response on the screen 
            $("#chatbox").append(botHtml); // Adds the html to the appropriate identifier
            document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" }); // Makes it so that the box containing the text will increase smoothly with every output from the chatbot
            
            // Checks if the user has toggled on voice
            if (voice_on == true){ 
                
                // If voice has been turned on read out the message as audio output
                textToSpeech(responses[i]);
            }
        }

    });

}


// Function that reads the text
function textToSpeech(msg) {

    // Get all voices that browser offers
	var available_voices = window.speechSynthesis.getVoices();

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

    // If an english voice isn't availabe, use any available voice
    if(english_voice === '') {
        english_voice = available_voices[0];
    }    

    var message = new SpeechSynthesisUtterance(msg); // Creates a new object
    message.pitch = 1.5 // Assigns pitch to message
    message.rate = 1; // Assigns rate of speed of message
    window.speechSynthesis.speak(message); // Outputs the message in audio format
}


// Function to toggle the voice on
function toggleVoiceOn() {

    voice_on = !voice_on; // Switches the state of the voice_on boolean (to true)
    
    // Sets the voice off button as displayed and the other button as hidden
    document.getElementById("voiceBtn").style.display = "none" 
    document.getElementById("voice2Btn").style.display = "block"
}

// Function to toggle the voice off
function toggleVoiceOff() {

    voice_on = !voice_on; // Switches the state of the voice_on boolean (to false) 

    // Sets the voice on button as displayed and the other button as hidden
    document.getElementById("voiceBtn").style.display = "block"
    document.getElementById("voice2Btn").style.display = "none"
}