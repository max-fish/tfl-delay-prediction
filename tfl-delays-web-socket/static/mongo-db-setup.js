const MongoClient = require("mongodb").MongoClient;

const uri = "mongodb+srv://gmnapster:M@ximfishman123@cluster0.ibipj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";

const client = new MongoClient(uri);

let database;

client.connect().then(() => {
    client.db("arrivalsDB");
}).catch((err) => {
    console.error(err);
    process.abort();
});

const insertArrivals = async function(collection, arrivalsList) {
    const arrivalsCollection = database.collection(collection);

    const result = await arrivalsCollection.insertMany(arrivalsList);

    console.log(`${result.insertedCount} documents were inserted.`);
}

const closeDatabaseConnection = async function() {
    await client.close();
}

exports.insertArrivals = insertArrivals;

exports.closeDatabaseConnection = closeDatabaseConnection;