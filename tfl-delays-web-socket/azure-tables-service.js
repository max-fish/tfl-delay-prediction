import { TableClient, AzureNamedKeyCredential } from "@azure/data-tables";

const account = "delaycsvstorage";

const accountKey = "prPXa/eMkACLn8RTMi9KgLQZSSVfXaQyP8bBTKZdrfIFKlSl2LmdmEXUjJDS71y7rI2aegJyq+It+AStwHg7pw==";

const credential = new AzureNamedKeyCredential(account, accountKey);

// const devAccount = "devstoreaccount1";

// const devAccountKey = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==";

// const devCredential = new AzureNamedKeyCredential(devAccount, devAccountKey);

// const tableServiceClientDev = new TableServiceClient(
//     "http://127.0.0.1:10002/devstoreaccount1", devCredential, {allowInsecureConnection: true}
// );


// const devTableClient = new TableClient("http://127.0.0.1:10002/devstoreaccount1", "arrivals", devCredential, {allowInsecureConnection: true});

let chunkCounter = 0;

const addPredictionsToTable = async (partitionKey, predictions) => {

const tableClient = new TableClient(`https://${account}.table.core.windows.net`, `arrivals`, credential);

    const rowKeys = [];

    const entityActions = [];

    for (const prediction of predictions) {

        const rowKey = prediction['id'].concat('_', prediction['timestamp'], '_', prediction['vehicleId'], '_', prediction['direction']);

        if(!rowKeys.includes(rowKey)) {

            entityActions.push(["upsert", {
                partitionKey: partitionKey,
                rowKey: rowKey,
                stationName: prediction['stationName'],
                timeOfPrediction: prediction['timestamp'],
                expectedArrival: prediction['expectedArrival'],
                timeToStation: prediction['timeToStation'],
                direction: prediction['direction'],
                timestamp: prediction['timestamp'],
                vehicleId: prediction['vehicleId'],
                naptanId: prediction['naptanId'],
                destinationName: prediction['destinationName']

                }]);

            rowKeys.push(rowKey);
        }
    }
    
        if(entityActions.length > 100) {
            //credit to https://stackoverflow.com/questions/8495687/split-array-into-chunks
            const chunkSize = 100;
            for (let i = 0; i < entityActions.length; i += chunkSize) {
                const chunk = entityActions.slice(i, i + chunkSize);
                try {
                    await tableClient.submitTransaction(chunk);

                } catch(err) {
                    console.log(err);
                }
            }

        } else{
            try {
                await tableClient.submitTransaction(entityActions);

            } catch(err) {
                console.log(err);
            }
        }
    }

const addSinglePrediction = async (prediction) =>  {
    const newEntity = {
        partitionKey: prediction['lineName'],
        rowKey: prediction['id'].concat('_', prediction['timestamp'], '_', prediction['vehicleId'], '_', prediction['direction']),
        stationName: prediction['stationName'],
        timeOfPrediction: prediction['timestamp'],
        expectedArrival: prediction['expectedArrival'],
        timeToStation: prediction['timeToStation'],
        direction: prediction['direction'],
        timestamp: prediction['timestamp'],
        vehicleId: prediction['vehicleId'],
        naptanId: prediction['naptanId'],
        destinationName: prediction['destinationName']
        };

    await tableClient.createEntity(newEntity);
}

export { addPredictionsToTable, addSinglePrediction };