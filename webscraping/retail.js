import appConstants from "./appConstants.js";
import csv from "csvtojson";
import fs from 'fs';
import hm from "./hm.js";
import primark from "./primark.js";
import pull from "./pull.js";
import puppeteer from 'puppeteer';
import { updateOutput } from './Utils.js';
import zara from "./zara.js";

(async () => {
  // Delete old output file
  await fs.unlink(appConstants.retailOutput, () => {});

  const output = {
    zara: [],
    primark: [],
    hm: [],
    pull: []
  }

  // Init browser
  const browser = await puppeteer.launch({ headless: false, devtools: false });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  const labels = await csv().fromFile(appConstants.labels);
  
  for (let label of labels) {
    const zaraOutput = await zara(page, label);
    output.zara.push(...zaraOutput);

    const primarkOutput = await primark(page, label);
    output.primark.push(...primarkOutput);

    const hmOutput = await hm(page, label);
    output.hm.push(...hmOutput);

    const pullOutput = await pull(page, label);
    output.pull.push(...pullOutput);
  }

  // TODO: include gender
  await updateOutput(output, appConstants.retailOutput);

  await browser.close();
})();