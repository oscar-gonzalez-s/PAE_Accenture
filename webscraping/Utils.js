/**
 * Module to export functions that are shared across multiple scripts
 * **/

import fs from 'fs';

/**
 * Method to update retail output without modifying existing one
 * @param {Object} data Object that contains data to append
 * @param {string} path  Path to retail output file
 *  */ 
export const updateOutput = async (data, path) => {
  const json = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch(() => {return {};});
  
  Object.assign(json, data);

  await fs.promises.writeFile(path, JSON.stringify(json, null, 4), 'utf8');
  console.log('JSON file generated. Closing browser...');
};

/**
 * Method to update media output with individual user data
 * @param {Object[]} data Array containing user's posts information
 * @param {string} path Path to media output file
 * @param {string} user Influencer username to log information
 *  */ 
export const updateMediaOutput = async (data, path, user) => {
  const json = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch(() => {return { output: [] };});
  
  if (data?.length) {
    json.output.push(...data);
    await fs.promises.writeFile(path, JSON.stringify(json, null, 4), 'utf8');
    console.log(`   JSON file updated with user ${user}`);
  } else {
    console.log(`   User ${user} has no data or doesn't exist`);
  }
};

/**
 * Method to update media output when the download fails
 * @param {number} i Index of the item to be changed
 * @param {string} path Path to media output file
 *  */ 
export const updateWithNA = async (i, path) => {
  const json = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch(() => {return { output: [] };});

  json.output[i].item0 = 'N/A N/A'
  json.output[i].item1 = 'N/A N/A'

  await fs.promises.writeFile(path, JSON.stringify(json, null, 4), 'utf8');
  console.log('Image download failed. JSON file updated');
};

/**
 * Method to accept cookies consent
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 *  */ 
export const cookiesConsent = async (page) => {
  console.log('Accepting cookies consent');
  await page.evaluate(() => {
    const buttons = [...document.querySelectorAll('button')];
    const acceptButton = buttons.find(el => el.textContent === 'Aceptar todas' || el.textContent === 'Accept All');
    acceptButton?.click();
  });
  // Wait to count as clicked
  await page.waitForTimeout(1000);
};


/**
 * Method to not save login info / dismiss notifications
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 *  */ 
export const rejectConsent = async (page) => {
  await page.evaluate(() => {
    const buttons = [...document.querySelectorAll('button')];
    const acceptButton = buttons.find(el => el.textContent === 'Not now' || el.textContent === 'Ahora no');
    acceptButton?.click();
  });
  // Wait to count as clicked
  await page.waitForTimeout(1000);
};

