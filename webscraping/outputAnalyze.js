import fs from 'fs';
import appConstants from './appConstants.js';

(async () => {
  const json = await fs.promises.readFile(appConstants.mediaOutput).then(json => JSON.parse(json)).catch(err => {
    throw new Error('media-output file not found');
  });

  const {userCount} = json.output.reduce((acc, curr, i) => {
    if (i === 1) {
      return {userCount: 1, user: curr.user}
    }  
    return acc.user !== curr.user ? {userCount: acc.userCount + 1, user: curr.user} : acc
  })

  console.log(userCount);
})()