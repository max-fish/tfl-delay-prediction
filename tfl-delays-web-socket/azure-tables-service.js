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

const tableClient = new TableClient(`https://${account}.table.core.windows.net`, "arrivals3", credential);

// const devTableClient = new TableClient("http://127.0.0.1:10002/devstoreaccount1", "arrivals", devCredential, {allowInsecureConnection: true});

const addPredictionsToTable = async (partitionKey, predictions) => {

    const entityActions = predictions.map((prediction) => {
        return ["create", {
        partitionKey: partitionKey,
        rowKey: prediction['id'].concat('_', prediction['timestamp']),
        stationName: prediction['stationName'],
        timeOfPrediction: prediction['timestamp'],
        expectedArrival: prediction['expectedArrival'],
        timeToStation: prediction['timeToStation'],
        direction: prediction['direction'],
        timestamp: prediction['timestamp'],
        vehicleId: prediction['vehicleId'],
        naptanId: prediction['naptanId']
        }]
    });
    try {
        await tableClient.submitTransaction(entityActions);
    } catch(err) {
        if(err.statusCode !== 409) {
            console.error(err);
        }
    }
};

export { addPredictionsToTable };