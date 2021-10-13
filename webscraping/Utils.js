/**
 * Module to export functions that are shared across multiple scripts
 * **/
module.exports = { 
  updateOutput: (data, path) => {
    const fs = require("fs");
    let json;
  
    try {
      json = require(path);
    } catch (e) {
      json = {}
    }
    
    Object.assign(json, data)
  
    fs.writeFile(path, JSON.stringify(json, null, 4), 'utf8', (err) => {
      if (err) throw err;
      console.log('JSON file generated. Closing browser...');
    });
  }
};