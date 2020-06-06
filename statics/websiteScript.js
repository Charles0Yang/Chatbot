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
function toggleVoice() {

    voice_on = !voice_on; // Switches the state of the voice_on boolean (to true/false)
    
    // If the width of the screen is more than 775 pixels
    if ($(window).width() > 775) {

        // Turns the text to Turn Voice On or Turn Voice up
        if (document.getElementById("voiceBtn").innerHTML=="Turn Voice On") {
            document.getElementById("voiceBtn").innerHTML = "Turn Voice Off"
        } else {
            document.getElementById("voiceBtn").innerHTML = "Turn Voice On"
        }

    // If the width of the screen is less than 775 pixels
    } else {

        // Turns the text to volume up or volume down
        if (document.getElementById("voiceBtn").innerHTML=='<i class="fa fa-volume-up"></i>') {
            document.getElementById("voiceBtn").innerHTML = '<i class="fa fa-volume-off"></i>'
        } else {
            document.getElementById("voiceBtn").innerHTML = '<i class="fa fa-volume-up"></i>'
        }
    }
}


// Function to show the loading screen for a second
function theFunction() {
    myVar = setTimeout(showPage, 1000);
}


// Function to stop showing the loading screen and to show the main page
function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("myDiv").style.display = "block";
    if ($(window).width() > 775) {
        document.getElementById("voiceBtn").innerHTML = "Turn Voice On";
    }
} 


// Function to show the dropdowns of the menu bar when the button is pressed
function myFunction() {

    var x = document.getElementById("myTopnav");

    // Changes the topnav to responsive or not
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
}


// Calls the function when the user starts scrolling
window.onscroll = function() {scrollFunction()};


// Function to show the button when the user scrolls more than 20px
function scrollFunction() {

    // If the user has scrolled the distance
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {

        // If the screen width is more than 775 px
        if ($(window).width() > 775) {
            document.getElementById("myBtn").innerHTML = "Scroll to top" // Replace text to Scroll to top

        } else {
            document.getElementById("myBtn").innerHTML = "<i class='fa fa-arrow-up'></i> TOP" // Replace text to (arrow up) TOP
        }

        document.getElementById("myBtn").style.display = "block" // Show the button
    
    } else {
        document.getElementById("myBtn").style.display = "none" // Do not show the button
    }
}


// When the user clicks on the button, scroll to the top of the document
function topFunction() {

    //Scroll to top
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}