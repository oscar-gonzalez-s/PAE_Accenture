import appConstants from './appConstants.js';
import axios from 'axios';
import fs from 'fs';
import path from 'path';

/**
 * Method to download a single image
 * @param {string} fileUrl Url to download the image
 * @param {string} downloadFolder Folder to save the image
 * @param {string} imgName Name of the image to download
 */
const downloadFile = async (fileUrl, downloadFolder, imgName) => { // Download a single image
  // Set the file name
  const fileName = String(imgName)+'.jpg';

  // The path of the downloaded file on our machine
  const localFilePath = path.resolve(downloadFolder, fileName);

  //download the image
  try {
    const response = await axios({
      method: 'GET',
      url: fileUrl,
      responseType: 'stream',
    });

    response.data.pipe(fs.createWriteStream(localFilePath));
  
  } catch (err) {
    throw new Error(err);
  }
}; 

/**
 * Download all the images in the json file
 * @param {string} path Path to media-output.json
 */
const downloadAll = async (path) => { 
  const dir = appConstants.downloadFolder;

  if(!fs.existsSync(dir)){
    fs.mkdirSync(dir);
  }

  var imageName = 0;
  const images = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch((e) => {throw e; });
  const links = images.output.map(post => post.imageSrc);
  links.forEach(link => {
    downloadFile(link, dir, imageName); 
    imageName++;
  });

};


export default downloadAll;


