try{
    const fs = require('fs');

    fs.readFile('abuse.html', 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading file:', err);
        return;
      }
      console.log('File contents:', data);
    });
}catch(error){
    console.log(error)
}