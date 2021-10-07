const fs = require("fs");

module.exports = { 
  updateOutput: (data) => {
    let json;
  
    try {
      json = require('./output.json');
    } catch (e) {
      json = {}
    }
    
    Object.assign(json, data)
  
    fs.writeFile('output.json', JSON.stringify(json, null, 4), 'utf8', (err) => {
      if (err) throw err;
      console.log('JSON file generated. Closing browser...');
    });
  }
};