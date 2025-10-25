// index.js
    const express = require('express');
    const path = require('path'); // The 'path' module helps build paths to files.
    const app = express();
    const port = 3000;

    // Tell Express to serve the static files from the 'public' directory
    app.use(express.static(path.join(__dirname, 'templates')));

    app.listen(port, () => {
        console.log(`Server is running at http://localhost:${port}`);
    });