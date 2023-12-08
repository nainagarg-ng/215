import { BASE_API_URL } from "./Common";

const axios = require('axios');

// import axios from 'axios';

// const BASE_API_URL = 'http://localhost:9000'; // Adjust as needed

const DataService = {
    Init: function () {
        // Any application initialization logic comes here
    },
    PredictManual: async function (domain) {
        console.log(domain);
        return await axios.post(BASE_API_URL + "/predict_manual_input", { name: domain });
        //   return await axios.post(BASE_API_URL + "/predict_manual_input", { name:domain});
    },
    PredictFromFile: async function (formData) {
        return await axios.post(BASE_API_URL + "/predict_from_file", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
}


export default DataService;