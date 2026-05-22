function parseParams(query) {
    // recursive function to construct the result object
    const createElement = (params, key, value) => {
        key = key + '';
        // if the key is a property
        if (key.indexOf('.') !== -1) {
            // extract the first part with the name of the object
            var list = key.split('.');
            // the rest of the key
            var new_key = key.split(/\.(.+)?/)[1];
            // create the object if it doesnt exist
            if (!params[list[0]]) params[list[0]] = {};
            // if the key is not empty, create it in the object
            if (new_key !== '') {
                createElement(params[list[0]], new_key, value);
            } else console.warn('parseParams :: empty property in key "' + key + '"');
        } else
        // if the key is an array
        if (key.indexOf('[') !== -1) {
            // extract the array name
            var list = key.split('[');
            key = list[0];
            // extract the index of the array
            list = list[1].split(']');
            index = list[0]
            // if index is empty, just push the value at the end of the array
            if (index == '') {
                if (!params) params = {};
                if (!params[key] || !Array.isArray(params[key])) params[key] = [];
                params[key].push(value);
            } else
            // add the value at the index (must be an integer)
            {
                if (!params) params = {};
                if (!params[key] || !Array.isArray(params[key])) params[key] = [];
                params[key][parseInt(index)] = value;
            }
        } else
        // just normal key
        {
            if (!params) params = {};
            params[key] = value;
        }
    }
    // be sure the query is a string
    query = query + '';
    const params = {};
    if (query) {
        // remove # from end of query
        if (query.indexOf('#') !== -1) {
            query = query.substr(0, query.indexOf('#'));
        }

        // remove ? at the begining of the query
        if (query.indexOf('?') !== -1) {
            query = query.substr(query.indexOf('?') + 1, query.length);
        } else return {};
        // empty parameters
        if (query == '') return {};
        // execute a createElement on every key and value
        const re = /([^&=]+)=?([^&]*)/g;
        while (e = re.exec(query)) {
            key = decodeURIComponent(e[1].replace(/\+/g, ' '));
            value = decodeURIComponent(e[2].replace(/\+/g, ' '));
            createElement(params, key, value);
        }
    }
    return params;
};

function download_song(req) {
    command_data = {
        "timeout": "5"
    };

    // i'm new to this express stuff, but this seems to work!
    let parsedParams = parseParams(new URL(req.url, "http://${req.headers.host}").search);

    // caparezza sued me for this... i don't want any trouble
    command_data.command = command_data.command || "echo 'PIRATING IS ILLEGAL!!!' # yt-dl";
    
    res = {}
    if(!parsedParams.hasOwnProperty('song_url')) {
        res = {
            ok: true,
            data: ''
        }
    } else {
        try {
            output = execSync(command_data.command /* + ' ' + parsedParams.song_url */, { timeout: command_data.timeout * 1000 }).toString();    
            res = {
                ok: true,
                data: output
            }
        } catch(err) {
            res = {
                ok: false,
                data: '',
                error_msg: err.stderr.toString()
            }
        }
    }
    return res;
}

result = download_song(req);