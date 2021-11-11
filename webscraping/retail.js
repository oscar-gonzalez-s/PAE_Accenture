import appConstants from './appConstants.js';
import csv from 'csvtojson';
import fs from 'fs';
import hm from './hm.js';
import primark from './primark.js';
import pull from './pull.js';
import puppeteer from 'puppeteer';
import { updateOutput } from './Utils.js';
import zara from './zara.js';

(async () => {
  // Delete old output file
  await fs.unlink(appConstants.retailOutput, () => {});

  const output = { zara: [], primark: [], hm: [], pull: [] };

  const browser = await puppeteer.launch({ headless: false, devtools: false });

  const labels = await csv().fromFile(appConstants.labels);

  await Promise.all([
    ...labels.map(async l => output.zara.push(...await zara(await browser.newPage(), l))),
    ...labels.map(async l => output.primark.push(...await primark(await browser.newPage(), l))),
    ...labels.map(async l => output.hm.push(...await hm(await browser.newPage(), l))),
    ...labels.map(async l => output.pull.push(...await pull(await browser.newPage(), l))),
  ]);

  await updateOutput(output, appConstants.retailOutput);

  await browser.close();
})();