// const express = require('express');
// const app = express();
// const path = require('path');

// const hostname = '127.0.0.1';

// const port = 8080;

// app.listen(port, () => {
//     console.log("App listening");
// });

// app.use("/static", express.static("./static/"));

// app.get("/", (req, res) => {

//     const options = {
//         root: path.join(__dirname)
//     };

//     res.sendFile('index.html', options);
// });



// server.on('close', () => {
//     console.log('closing server');
//     $.connection.hub.stop(false, true);
// });

// process.on('SIGINT', () => {
//     console.log('ctrl+c pressed');
//     server.close();
// });

import axios from 'axios';

import { addPredictionsToTable } from './azure-tables-service.js';

const url = "https://api.tfl.gov.uk/Mode/bus/Arrivals";

const params = {
    app_key: "6c2701fece254c448b25dd58bc3c0a3f",
    count: -1
};

setInterval(() => {
    axios.get(url, params)
        .then(async (response) => {

        console.log('new request...');

        const predictions = response.data;

        const partitionKeyToPredictionsMap = new Map();

        predictions.forEach((prediction) => {
            const operationType = prediction['operationType'];

            if (operationType !== 2) {

                const partitionKey = prediction['lineName'];

                if (!partitionKeyToPredictionsMap.has(partitionKey)) {
                    partitionKeyToPredictionsMap.set(partitionKey, []);
                }

                const predictionsForPartitionKey = partitionKeyToPredictionsMap.get(partitionKey);

                predictionsForPartitionKey.push(prediction);
                
                }
            });

            const partitionKeyToPredictionsMapIter = partitionKeyToPredictionsMap.entries();

            // console.log(partitionKeyToPredictionsMapIter);

            for (const [partitionKey, predictions] of partitionKeyToPredictionsMapIter) {
                await addPredictionsToTable(partitionKey, predictions);
            }
            console.log('done');
        })
        .catch((err) => console.error(err));
}, 30000);