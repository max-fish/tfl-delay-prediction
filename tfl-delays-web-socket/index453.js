import axios from 'axios';

import { addPredictionsToTable } from './azure-tables-service-453.js';

const url = "https://api.tfl.gov.uk/Mode/bus/Arrivals";

const params = {
    app_key: "6c2701fece254c448b25dd58bc3c0a3f"
};

    axios.get(url, params)
        .then(async (response) => {

        console.log('new request...');

        const startTime = Date.now();

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

            for (const [partitionKey, predictions] of partitionKeyToPredictionsMapIter) {
                await addPredictionsToTable(partitionKey, predictions);
            }

            const endTime = Date.now();

            console.log(`${endTime - startTime} ms`);

            console.log('done');
        })
        .catch((err) => console.error(err));