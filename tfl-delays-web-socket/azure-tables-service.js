import { TableServiceClient, TableClient, AzureNamedKeyCredential } from "@azure/data-tables";

// const account = "delaycsvstorage";

// const accountKey = "prPXa/eMkACLn8RTMi9KgLQZSSVfXaQyP8bBTKZdrfIFKlSl2LmdmEXUjJDS71y7rI2aegJyq+It+AStwHg7pw==";

// const credential = new AzureNamedKeyCredential(account, accountKey);

// const tableServiceClient = new TableServiceClient(
//   `https://${account}.table.core.windows.net`,
//   credential,
// );

const devAccount = "devstoreaccount1";

const devAccountKey = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==";

const devCredential = new AzureNamedKeyCredential(devAccount, devAccountKey);

const tableServiceClientDev = new TableServiceClient(
    "http://127.0.0.1:10002/devstoreaccount1", devCredential, {allowInsecureConnection: true}
);

const createTableJustInCase = async (tableName) => {
    await tableServiceClientDev.createTable(tableName, {
        onResponse: (response) => {
            if(response.status !== 201 && response.status !== 409) {
                throw response;
            }
        }
    });
};

let devTableClient;

const addPredictionsToTable = async (tableName, partitionKey, predictions) => {

    const entityActions = predictions.map((prediction) => {
        return ["create", {
        partitionKey: partitionKey,
        rowKey: prediction['timestamp'].concat('_', prediction['naptanId']),
        id: prediction['id'],
        stationName: prediction['stationName'],
        estimatedArrival: prediction['expectedArrival'],
        timeToStation: prediction['timeToStation'],
        }]
    });


    // const tableClient = new TableClient(`https://${account}.table.core.windows.net`, tableName, credential);

    if(devTableClient === undefined || devTableClient.tableName !== tableName) {
        devTableClient = new TableClient("http://127.0.0.1:10002/devstoreaccount1", tableName, devCredential, {allowInsecureConnection: true});
    }

    try {
        await devTableClient.submitTransaction(entityActions);
    } catch(err) {
        if(err.statusCode !== 409) {
            console.error(err);
        }
    }
} ;

export { addPredictionsToTable, createTableJustInCase };