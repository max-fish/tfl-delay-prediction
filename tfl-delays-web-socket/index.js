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

import { removeOutdatedPredictions, generateTableName } from './pre-processing.js';

import { hasTableNameInCache, addTableNameToCache } from './table-name-cache.js';

import { addPredictionsToTable, createTableJustInCase } from './azure-tables-service.js';

const url = "https://api.tfl.gov.uk/Mode/bus/Arrivals";

const params = {
    app_key: "6c2701fece254c448b25dd58bc3c0a3f"
};
    setInterval(() => {
    console.log('starting new request...');
    axios.get(url, params)
        .then(async (response) => {
            const onlyNewPredictions = removeOutdatedPredictions(response.data);

            const tableNameToPredictionsMap = new Map();

            onlyNewPredictions.forEach((prediction) => {
                const tableName = generateTableName(prediction);

                if(!tableNameToPredictionsMap.has(tableName)) {
                    tableNameToPredictionsMap.set(tableName, new Map());
                }
                
                const busIdToPrecictionsMap = tableNameToPredictionsMap.get(tableName);

                const busId = prediction['vehicleId'];

                if(!busIdToPrecictionsMap.has(busId)) {
                    busIdToPrecictionsMap.set(busId, []);
                }

                const predictionsForBusId = busIdToPrecictionsMap.get(busId);

                busIdToPrecictionsMap.set(busId, [...predictionsForBusId, prediction]);
            });

            const tableNameToPredictionsMapIter = tableNameToPredictionsMap.entries();

            // console.log(tableNameToPredictionsMapIter);

            for(const [tableName, busToPrecictionsMap] of tableNameToPredictionsMapIter) {
                if(!hasTableNameInCache(tableName)){
                    try {
                        await createTableJustInCase(tableName);
                    } catch(err) {
                        console.error(err);
                        continue;
                    }
                }

                const busToPrecictionsMapIter = busToPrecictionsMap.entries();

                for(const [busId, predictions] of busToPrecictionsMapIter) {
                    await addPredictionsToTable(tableName, busId, predictions);
                }

                addTableNameToCache(tableName);
            }

            console.log('done');
        })
        .catch(err => console.error(err));
    }, 30000);