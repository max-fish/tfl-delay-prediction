import axios from 'axios';

import { addPredictionsToTable } from './azure-tables-service.js';

import { readFileSync } from 'fs'

const buffer = readFileSync('bus-lines.txt');

const busLinesToTableNumberJson = JSON.parse(readFileSync('bus-lines-to-table-number.txt').toString());

const buses = buffer.toString().split(',');

setInterval(() => {

    console.log('new request...');
    
    const tflPromises = [];
    
    const azurePromises = [];
    
    const chunkSize = 20;
    
    for (let i = 0; i < buses.length; i += chunkSize) {
        const chunk = buses.slice(i, i + chunkSize);
        const url = "https://api.tfl.gov.uk/Line/" + chunk.join() + "/Arrivals?app_key=6c2701fece254c448b25dd58bc3c0a3f&operationType=1"
        const tflPromise = axios.get(url);
        tflPromises.push(tflPromise);
    }
    
    Promise.allSettled(tflPromises).then(async (responses) => {
    
        const onlyFulfilledResponses = responses.filter((response) => response.status === "fulfilled");
    
        for (const response of onlyFulfilledResponses) {
            const predictions = response.value.data;
    
            // console.log(predictions.length);
    
            const groupByPartitionKey = predictions.reduce((group, prediction) => {
                const lineName = prediction['lineName'];
    
                group[lineName] = group[lineName] ?? [];
    
                group[lineName].push(prediction);
    
                return group;
            }, {});
    
            const partitionKeys = Object.keys(groupByPartitionKey);
    
            for (const partitionKey of partitionKeys) {
                if (groupByPartitionKey[partitionKey].length !== 0) {
                    azurePromises.push(addPredictionsToTable(partitionKey, groupByPartitionKey[partitionKey], busLinesToTableNumberJson[partitionKey]));
                }
            }
        }
    
        await Promise.allSettled(azurePromises);
    
        console.log('done');
    
    }).catch((err) => console.error(err));
    
}, 30000);
    


        // predictions.forEach((prediction) => {
        //     const operationType = prediction['operationType'];

        //     if (operationType !== 2) {

        //         const partitionKey = prediction['lineName'];

        //         if (!partitionKeyToPredictionsMap.has(partitionKey)) {
        //             partitionKeyToPredictionsMap.set(partitionKey, []);
        //         }

        //         const predictionsForPartitionKey = partitionKeyToPredictionsMap.get(partitionKey);

        //         predictionsForPartitionKey.push(prediction);
                
        //         }
        //     });

        //     const partitionKeyToPredictionsMapIter = partitionKeyToPredictionsMap.entries();

        //     // console.log(partitionKeyToPredictionsMapIter);

        //     for (const [partitionKey, predictions] of partitionKeyToPredictionsMapIter) {
        //         await addPredictionsToTable(partitionKey, predictions);
        //     }
            