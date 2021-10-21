
import fs from 'fs';
import path from 'path'
import axios from 'axios'

const dir = '../instaImages';
const pathJson = './media-output.json';

if(!fs.existsSync(dir)){
  fs.mkdirSync(dir)
}

// fileUrl: the absolute url of the image to be downloaded

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

const downloadAll = async (path) => { // Download all the images of the json file
  var imageName = 0;
  const images = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch((e) => {throw e });
  const links = images.output.map(post => post.imageSrc);
  links.forEach(link => {
    downloadFile(link, dir, imageName); 
    imageName++;
  })

}


downloadAll(pathJson);


