import appConstants from './appConstants.js';
import csv from 'csvtojson';
import fs from 'fs';

export default async function outputAnalyze() {
  const json = await fs.promises.readFile(appConstants.mediaOutput).then(json => JSON.parse(json)).catch(() => {
    throw new Error('Error: media-output file not found');
  });

  const {userCount} = json.output.reduce((acc, curr, i) => {
    if (i === 1) {
      return {userCount: 1, user: curr.user};
    }  
    return acc.user !== curr.user ? {userCount: acc.userCount + 1, user: curr.user} : acc;
  });

  const users = await csv().fromFile(appConstants.influencers);

  console.log(`${json.output.length} images retrieved from ${userCount}/${users.length} users`);
}