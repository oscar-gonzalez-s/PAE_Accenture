import appConstants from "./appConstants.js";
import axios from 'axios'
import fs from 'fs';
import path from 'path'

/**
 * Method to download a single image
 * @param fileUrl 
 * @param downloadFolder 
 * @param imgName 
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
 * Download all the images of the json file
 * @param path 
 */

const downloadAll = async (path) => { 
    const dir = appConstants.downloadFolder;

    if(!fs.existsSync(dir)){
        fs.mkdirSync(dir)
    }

    var imageName = 0;
    const images = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch((e) => {throw e });
    const links = images.output.map(post => post.imageSrc);
    links.forEach(link => {
        downloadFile(link, dir, imageName); 
        imageName++;
    })

}


export default downloadAll;


