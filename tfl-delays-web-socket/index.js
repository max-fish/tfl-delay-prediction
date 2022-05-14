const express = require('express');
const app = express();
const path = require('path');

const hostname = '127.0.0.1';

const port = 8080;

app.listen(port, () => {
    console.log("App listening");
});

app.use("/static", express.static("./static/"));

app.get("/", (req, res) => {

    const options = {
        root: path.join(__dirname)
    };

    res.sendFile('index.html', options);
});

// server.on('close', () => {
//     console.log('closing server');
//     $.connection.hub.stop(false, true);
// });

// process.on('SIGINT', () => {
//     console.log('ctrl+c pressed');
//     server.close();
// });