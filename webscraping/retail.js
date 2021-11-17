import appConstants from './appConstants.js';
import csv from 'csvtojson';
import fs from 'fs';
import hm from './hm.js';
import primark from './primark.js';
import pull from './pull.js';
import puppeteer from 'puppeteer';
import { updateOutput } from './Utils.js';
import zara from './zara.js';

const readers = { zara, primark, hm, pull };

(async () => {
  // Delete old output file
  await fs.unlink(appConstants.retailOutput, () => {});

  const output = { 
    zara: [], 
    primark: [], 
    hm: [], 
    pull: [] 
  };

  const browser = await puppeteer.launch({ headless: false, devtools: false });

  const labels = await csv().fromFile(appConstants.labels);

  // Execute all retail tasks at once
  await Promise.all(
    Object.entries(output).flatMap(([shop, results]) => 
      labels.map(async l => results.push(...await readers[shop](await browser.newPage(), l)))
    )
  );

  await updateOutput(output, appConstants.retailOutput);

  await browser.close();
})();