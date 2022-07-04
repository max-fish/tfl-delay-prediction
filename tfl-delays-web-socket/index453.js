import axios from 'axios';

import { addPredictionsToTable } from './azure-tables-service-453.js';

const url = "https://api.tfl.gov.uk/Line/1,100,101,102,103,104,105,106,107,108,109,11,110,111,112,113,114,115,116,453/Arrivals";

const params = {
    app_key: "6c2701fece254c448b25dd58bc3c0a3f"
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

                const partitionKey = prediction['vehicleId'];

                if (!partitionKeyToPredictionsMap.has(partitionKey)) {
                    partitionKeyToPredictionsMap.set(partitionKey, []);
                }

                const predictionsForPartitionKey = partitionKeyToPredictionsMap.get(partitionKey);

                predictionsForPartitionKey.push(prediction);
                
                }
            });

            const partitionKeyToPredictionsMapIter = partitionKeyToPredictionsMap.entries();

            for (const [partitionKey, predictions] of partitionKeyToPredictionsMapIter) {
                await addPredictionsToTable(partitionKey, predictions);
            }
            console.log('done');
        })
        .catch((err) => console.error(err));
}, 30000);