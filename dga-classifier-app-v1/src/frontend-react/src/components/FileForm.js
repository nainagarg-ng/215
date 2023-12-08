import React, { useState } from 'react';
import Button from '@mui/material/Button';
import { Typography } from '@mui/material';
import FormControl from '@mui/material/FormControl';
import Input from '@mui/material/Input';
import { Alert } from '@mui/material';
import DataService from '../services/DataService';

function FileForm() {
  const [fileUploaded, setFileUploaded] = useState(false); // State to track if file is uploaded
  const [globalPredictionResults, setGlobalPredictionResults] = useState(null);
  const [uploadError, setUploadError] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.name.endsWith('.txt')) {
        setFileUploaded(true); // Set filedUploaded to true when a file is selected
        uploadFile(file);
        setUploadError(''); // Clear any previous errors
      } else {
        setFileUploaded(false);
        setUploadError('Please upload a file in .txt format.'); // Set the error message
        event.target.value = ''; // Reset the file input
      }
    }
  };

  const uploadFile = (file) => {
    const formData = new FormData();
    formData.append("file", file);
    DataService.PredictFromFile(formData)
      .then(function (response) {
        setGlobalPredictionResults(response.data);
        console.log(response.data);
        alert("File uploaded"); // Pop up window to show that file is uploaded
      }).catch(function (error) {
        console.error('Error uploading file: ', error);
        setUploadError('Error uploading file.'); // Set the error message for upload failure
        setFileUploaded(false); // Reset fileUploaded on error
      });
  };

  const outputResult = () => {
    if (!fileUploaded) {
      alert("Please upload a file");
      return;
    }

    const textToWrite = JSON.stringify(globalPredictionResults, null, 2);
    const textBlob = new Blob([textToWrite], { type: 'text/plain' });
    const downloadUrl = window.URL.createObjectURL(textBlob);

    // Create a temporary link to trigger the download
    const tempLink = document.createElement('a');
    tempLink.href = downloadUrl;
    tempLink.download = "prediction_results.txt";
    document.body.appendChild(tempLink); // Required for Firefox
    tempLink.click();
    document.body.removeChild(tempLink); // Clean up
  };

  return (
    <form style={{ textAlign: 'center', margin: '20px' }}>
      <Typography variant="body1" style={{ margin: '20px 0' }}>
        Or upload a text file for bulk check:
      </Typography>
      <FormControl variant="outlined" style={{ marginRight: '10px' }}>
        <Input type="file" id="file-upload" accept=".txt" aria-label="Upload file" style={{ display: 'none' }} onChange={handleFileChange} />
        <Button variant="contained" color="primary" component="label" htmlFor="file-upload">
          Upload a file
        </Button>
      </FormControl>
      <Button variant="contained" color="primary" onClick={outputResult} style={{ marginLeft: '10px' }}>
        Download Results
      </Button>
      {uploadError && (
        <Alert severity="error" style={{ marginTop: '20px' }}>{uploadError}</Alert>
      )}
    </form>
  );
}

export default FileForm;
