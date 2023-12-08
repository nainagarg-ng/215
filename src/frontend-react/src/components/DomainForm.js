import React, { useState } from 'react';
import { TextField, Button, CircularProgress, Snackbar } from '@mui/material';
import DataService from '../services/DataService';

function DomainForm() {
  const [domain, setDomain] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [resultColor, setResultColor] = useState('black'); // Default color
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const checkDomain = () => {
    if (!domain){
      setResult('Please enter a domain name!');
      setResultColor('red');
      return;
    }
    setLoading(true);
    // Simulate API call

    DataService.PredictManual(domain)
    .then(function(response){
      const prediction_results = response.data;
      console.log(prediction_results);
      if (prediction_results.result === 'legit'){
        setResultColor('green');
      } else {
        setResultColor('red');
      }
      setResult(prediction_results.domain + ": " + prediction_results.result);
    })
    .catch(error => {
      console.error('Error: ', error);
      setResult('Error making prediction');
    })
    .finally(() => {
      setLoading(false);
    })
  };

  const handleDomainChange = (e) => {
    setDomain(e.target.value);
  };

  return (
    <>
      <form style={{ textAlign: 'center', margin: '20px' }}>
        <div style={{marginBottom: '10px'}}>
        <TextField label="Enter a domain name" variant="outlined" value={domain}
                   onChange={handleDomainChange} style={{ width: '100%', maxWidth: '500px' }}  />
        </div>
        <Button variant="contained" color="primary" onClick={checkDomain} disabled={loading}>
          {loading ? <CircularProgress size={24} /> : 'Check Domain'}
        </Button>
      </form>
      {result && (
        <div style={{ color: resultColor, textAlign: 'center', marginTop: '20px' }}>
          {result}
        </div>
      )}
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={() => setSnackbarOpen(false)}
                message="Domain checked!" />
    </>
  );
}

export default DomainForm;
