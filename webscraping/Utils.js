/**
 * Module to export functions that are shared across multiple scripts
 * **/

import fs from 'fs';

export const updateOutput = async (data, path) => {
  const json = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch(() => {return {}});
  
  Object.assign(json, data)

  fs.writeFile(path, JSON.stringify(json, null, 4), 'utf8', (err) => {
    if (err) throw err;
    console.log('JSON file generated. Closing browser...');
  });
}

export const cookiesConsent = async (page) => {
  await page.evaluate(() => {
    const buttons = [...document.querySelectorAll('button')];
    const acceptButton = buttons.find(el => el.textContent === 'Aceptar todas' || el.textContent === 'Accept All');
    acceptButton?.click();
  });
  // Wait to count as clicked
  await page.waitForTimeout(1000);
}