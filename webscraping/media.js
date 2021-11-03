import { getUserData, login } from './insta.js';

import appConstants from "./appConstants.js";
import { cookiesConsent, rejectConsent } from './Utils.js';
import csv from "csvtojson";
import downloadAll from './imageDownload.js'
import fs from 'fs';
import puppeteer from 'puppeteer';

(async () => { 
  // Delete old output file
  await fs.unlink(appConstants.mediaOutput, () => {});
  // Delete old image folder
  await fs.rmdir(appConstants.downloadFolder, { recursive: true }, () => {});

  // Init browser
  const browser = await puppeteer.launch({ headless: false, devtools: false });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  // Wait until page has loaded
  await page.goto('https://www.instagram.com/accounts/login/', { waitUntil: 'networkidle0' });

  // Accept cookies consent
  await cookiesConsent(page);


  // Log in
  await login(page);

  //Don't save logIn
  //await rejectConsent(page);

  //Turn off notifications
  //await rejectConsent(page);

  const users = await csv().fromFile(appConstants.influencers);

  for (let user of users) {
    await getUserData(page, user.username, user.gender);
  }

  await browser.close();

  await downloadAll(appConstants.mediaOutput);
})()