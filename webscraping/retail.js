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

  // Init browser
  const browser = await puppeteer.launch({ headless: false, devtools: false });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  const labels = await csv().fromFile(appConstants.labels);

  for (let label of labels) { output.zara.push(...await zara(page, label)); }
  for (let label of labels) { output.primark.push(...await primark(page, label)); }
  for (let label of labels) { output.hm.push(...await hm(page, label)); }
  for (let label of labels) { output.pull.push(...await pull(page, label)); }

  await updateOutput(output, appConstants.retailOutput);

  await browser.close();
})();