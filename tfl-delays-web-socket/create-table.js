// const array = Array.from(Array(300).keys())

import axios from "axios";

import { fstat, readFileSync, writeFileSync } from 'fs'

import { TableClient, AzureNamedKeyCredential, TableServiceClient } from "@azure/data-tables";

// const chunkSize = 100;
//         for (let i = 0; i < array.length; i += chunkSize) {
//             const chunk = array.slice(i, i + chunkSize);
//             console.log(chunk);
//         }

        // const rowKeyToPredictionsMap = new Map();

// const rowKey = prediction['id'].concat('_', prediction['timestamp'], '_', prediction['vehicleId']);

                // if(!rowKeyToPredictionsMap.has(rowKey)) {
                //     rowKeyToPredictionsMap.set(rowKey, []);
                // }

                // const predictionsForRowKey = rowKeyToPredictionsMap.get(rowKey);

                // rowKeyToPredictionsMap.set(rowKey, [...predictionsForRowKey, prediction]);


// const rowKeyToPredictionsMapIter = rowKeyToPredictionsMap.entries();

            // for(const [rowKey, predictions] of rowKeyToPredictionsMapIter) {
            //     if(predictions.length !== 1) {
            //         console.log(predictions.length);
            //         console.log(predictions);
            //     }
            // }

// const buffer = readFileSync('bus-lines.txt');

// const buses = buffer.toString().split(',');

// const params = {
//         app_key: "6c2701fece254c448b25dd58bc3c0a3f"
//     };

// const account = "delaycsvstorage";

// const accountKey = "prPXa/eMkACLn8RTMi9KgLQZSSVfXaQyP8bBTKZdrfIFKlSl2LmdmEXUjJDS71y7rI2aegJyq+It+AStwHg7pw==";

// const credential = new AzureNamedKeyCredential(account, accountKey);

// const tableService = new TableServiceClient(`https://${account}.table.core.windows.net`, credential);

// const tableClient = new TableClient(`https://${account}.table.core.windows.net`, "testarrivals", credential);

//         console.log('starting...')
//         const promises = [];

//         const chunkSize = 20;

//         const tableNumberToBusLinesObj = {};

//         const busLinesToTableNumber = {};

//         let tableNumber = 0;

        // for (let i = 0; i < buses.length; i += chunkSize) {
        //     const chunk = buses.slice(i, i + chunkSize);

        //     for (const busLine of chunk) {
        //         busLinesToTableNumber[busLine] = tableNumber.toString();
        //     }

        //     tableNumber++;
            // const url = "https://api.tfl.gov.uk/Line/" + chunk.join() + "/Arrivals?app_key=6c2701fece254c448b25dd58bc3c0a3f";
            // const promise = axios.get(url);
            // promises.push(promise);
        // }

        // console.log(tableNumberToBusLinesObj);

        // Promise.allSettled(promises).then((responses) => {
        //     console.log('done');
        // }).catch((err) => console.error(err));

// axios.get("https://api.tfl.gov.uk/Line/" + buffer.toString() + "/Arrivals", params).then((response) => {
//     console.log(response.data)
// }).catch((err) => console.error(err))

// setInterval(() => {

//     console.log('starting...');

//     axios.get("https://api.tfl.gov.uk/Mode/bus/arrivals", params).then((response) => {

//         const predictions = response.data;
    
//         const onlyRelevantPredictions = predictions.filter((prediction) => prediction['operationType'] !== 2 && prediction['lineName'] == '453' && prediction['direction'] == 'inbound');

//         console.log('all arrivals 453 filtered: ' + onlyRelevantPredictions.length);

//         axios.get("https://api.tfl.gov.uk/Line/453/arrivals", {app_key: "6c2701fece254c448b25dd58bc3c0a3f"}).then((response) => {
//             const onlyRelevant = response.data.filter((prediction) => prediction['operationType'] !== 2 && prediction['direction'] == 'inbound');
//             console.log('453 arrivals: ' + onlyRelevant.length);
//         });
    
//         // const entityActions = onlyRelevantPredictions.map((prediction) => {
//         //     return ["create", {
//         //     partitionKey: prediction['lineName'],
//         //     rowKey: prediction['id'].concat('_', prediction['timestamp'], '_', prediction['vehicleId']),
//         //     stationName: prediction['stationName'],
//         //     timeOfPrediction: prediction['timestamp'],
//         //     expectedArrival: prediction['expectedArrival'],
//         //     timeToStation: prediction['timeToStation'],
//         //     direction: prediction['direction'],
//         //     timestamp: prediction['timestamp'],
//         //     vehicleId: prediction['vehicleId'],
//         //     naptanId: prediction['naptanId'],
//         //     destinationName: prediction['destinationName']
//         //     }]
//         // });

//         // if(entityActions.length > 100) {
//         //     //credit to https://stackoverflow.com/questions/8495687/split-array-into-chunks
//         //     const chunkSize = 100;
//         //     for (let i = 0; i < entityActions.length; i += chunkSize) {
//         //         const chunk = entityActions.slice(i, i + chunkSize);
//         //         try {
//         //             await tableClient.submitTransaction(chunk);
//         //         } catch(err) {
//         //             if(err.code == 400) {
//         //                 console.log(chunk);
//         //             }
//         //             else {
//         //                 console.error(err);
//         //             }
//         //         }
//         //     }
//         // } else{
//         //     try {
//         //         await tableClient.submitTransaction(entityActions);
//         //     } catch(err) {
//         //         if(err.code == 400) {
//         //             print(predictions);
//         //         }
//         //         else{
//         //             console.error(err);
//         //         }
//         //     }
//         // }


//         // onlyRelevantPredictions.forEach(async (prediction) => {
//         //     const entity = {
//         //         partitionKey: prediction['lineName'],
//         //     rowKey: prediction['id'].concat('_', prediction['timestamp'], '_', prediction['vehicleId']),
//         //     stationName: prediction['stationName'],
//         //     timeOfPrediction: prediction['timestamp'],
//         //     expectedArrival: prediction['expectedArrival'],
//         //     timeToStation: prediction['timeToStation'],
//         //     direction: prediction['direction'],
//         //     timestamp: prediction['timestamp'],
//         //     vehicleId: prediction['vehicleId'],
//         //     naptanId: prediction['naptanId'],
//         //     destinationName: prediction['destinationName']
//         //     }

//         //     try {
//         //         await tableClient.createEntity(entity);
//         //     } catch(err) {
//         //         console.log(entity);
//         //     }
//         // });

//         // console.log('done');

//     }).catch((err) => {
//         console.error(err);
//     })
    
// }, 30000);

// let i = 0;

// for await(const entity of tableClient.listEntities()) {
//     i++;
// }

// console.log(i);

// const content = readFileSync('predictions.txt').toString();

// const predictions = JSON.parse(content);

// const groupByPartitionKey = predictions.reduce((group, prediction) => {
//     const id = prediction['id'];

//     group[id] = group[id] ?? [];

//     group[id].push(prediction);

//     return group;
// }, {});

// const keys = Object.keys(groupByPartitionKey);

// keys.forEach((key) => {
//     if(groupByPartitionKey[key].length > 1) {
//         console.log(key);
//         console.log(groupByPartitionKey[key].length);
//     }
// });

// console.log(groupByPartitionKey[162428088]);

const data = readFileSync('bus-lines-to-table-number.txt')

const jsonData = JSON.parse(data)

console.log(jsonData['453'])

// const existingTables = Array.from(new Set(Object.values(jsonData)))

// const existingTableInts = existingTables.map((tableNumber) => parseInt(tableNumber))

// existingTableInts.sort((a, b) => a - b);

// console.log(existingTableInts);

// const azureTablesWithTop20Routes = [6,29,25,31,19,28,18,30,0,28,11,30,16,29,5,17,30,22,30];

// const azureTablesWithTop20RoutesNoDuplicates = [...new Set(azureTablesWithTop20Routes)];

// console.log(azureTablesWithTop20RoutesNoDuplicates);

// const toBeDeletedTables = existingTableInts.filter((table) => !azureTablesWithTop20RoutesNoDuplicates.includes(table));

// console.log(toBeDeletedTables);