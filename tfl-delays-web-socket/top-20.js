import axios from 'axios';

import { addPredictionsToTable } from './azure-tables-service.js';

const busLines = ["208", "N199", "89", "N89", "5", "N15", "468", "N68", "11", "N11", "3", "N3", "427", "207", "N207", "44", "N44", "65", "N65"];

const url = "https://api.tfl.gov.uk/Line/" + busLines.join() + "/Arrivals?app_key=6c2701fece254c448b25dd58bc3c0a3f&operationType=1";

setInterval(() => {
    
    console.log('new request');

    axios.get(url).then(async (response) => {
        const predictions = response.data;

        const groupByPartitionKey = predictions.reduce((group, prediction) => {
            const lineName = prediction['lineName'];

            group[lineName] = group[lineName] ?? [];

            group[lineName].push(prediction);

            return group;
        }, {});

    const partitionKeys = Object.keys(groupByPartitionKey);

    for (const partitionKey of partitionKeys) {
        if (groupByPartitionKey[partitionKey].length !== 0) {
            await addPredictionsToTable(partitionKey, groupByPartitionKey[partitionKey]);
        }
    }

    console.log('done');

    }).catch((error) => console.error(error));

}, 30000);