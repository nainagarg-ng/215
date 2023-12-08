// API URL
axios.defaults.baseURL = 'http://localhost:9000/';

var resultElement = document.getElementById('input_result');
var input_file = document.getElementById("file-upload");
var resultElement2 = document.getElementById('file_result');
var globalPredictionResults = null;  // Global variable to store the prediction results

document.getElementById('domainForm').addEventListener('submit', function(event) {
    event.preventDefault();
    checkDomain();
});

function check_domain(){
    // Read the entered domain
    var domain = document.getElementById('domainInput').value;
    resultElement.style.display = 'block';
    resultElement.innerHTML = "";
    console.log(domain);

    if(domain === ''){
        resultElement.innerHTML = "Please enter a domain name!";
    } else {

    // Post the domain name to the /predict_manual_input API
    axios.post("/predict_manual_input", { name:domain})
    .then(function (response){
        var prediction_results = response.data;
        console.log(prediction_results);

        // Display the results
        // Check if the result is 'legit' and update the style
            if(prediction_results['result'] === 'legit'){
            resultElement.style.color = 'green'; // Set text color to green
        } else {
            // Optionally handle other cases (e.g., 'not legit')
            resultElement.style.color = 'red'; // For example, set text color to red
        }
        resultElement.innerHTML = prediction_results['domain'] + ": " + prediction_results['result'];
    });
}
}

function file_upload() {
    // Clear
    resultElement2.style.display = 'block';
    resultElement2.innerHTML = "";
    input_file.click();
}

// Attach an onchange event
input_file.onchange = input_file_onchange;

function input_file_onchange(){
    // Read the uploaded file
    var file_to_upload = input_file.files[0];
    resultElement2.innerHTML = "";

    // Post the file to the /predict_from_file API
    var formData = new FormData();
    formData.append("file", file_to_upload);
    axios.post('/predict_from_file', formData,{
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(function (response){
        globalPredictionResults = response.data;  // Store the results in the global variable
        console.log(globalPredictionResults);
    });
}

function outputResult(){
    if (!globalPredictionResults) {
        alert("No results to download");
        return;
    }

    // Convert the results object to a string (you might need to adjust this based on your actual results format)
    var textToWrite = JSON.stringify(globalPredictionResults, null, 2);

    // Create a blob from the text
    var textBlob = new Blob([textToWrite], {type: 'text/plain'});

    // Create a link element to download the blob
    var downloadLink = document.createElement("a");
    downloadLink.download = "prediction_results.txt";
    downloadLink.innerHTML = "Download File";
    if (window.webkitURL != null) {
        // Chrome allows the link to be clicked without actually adding it to the DOM
        downloadLink.href = window.webkitURL.createObjectURL(textBlob);
    }    else {
        // Firefox requires the link to be added to the DOM before it can be clicked
        downloadLink.href = window.URL.createObjectURL(textBlob);
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }

    // Simulate a click on the link to trigger the download
    downloadLink.click();
}

function destroyClickedElement(event) {
    // Remove the link from the DOM
    document.body.removeChild(event.target);
}

