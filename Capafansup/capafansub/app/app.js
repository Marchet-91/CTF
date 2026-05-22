const express = require('express');
const bodyParser = require('body-parser');
const vm = require('vm');
const fs = require('fs');
const path = require('path');

const app = express();

app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');

app.use(bodyParser.text());


app.get('/', (req, res) => {
    res.render('index');
});

app.get('/download', (req, res) => {
    result = {};
    // don't you dare getting any weird ideas!!
    const sandbox = {
        execSync: require('child_process').execSync,
        URL: URL,
        req: req,
        result: result
    }

    const script = new vm.Script(
        fs.readFileSync(path.join(__dirname, 'download_song.js'), 'utf8')
    );

    script.runInNewContext(sandbox);

    if(!sandbox.result.ok) {
        res.render('error', {
            error_msg: sandbox.result.error_msg
        });
    } else {
        res.render('download', {
            data: sandbox.result.data
        });
    }
});

app.listen(3000, () => {
    console.log('Running on :3000');
});