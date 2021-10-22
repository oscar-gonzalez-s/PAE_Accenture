import appConstants from "./appConstants.js";
import { cookiesConsent } from './Utils.js';
import fs from 'fs';
import { getUserData } from './insta.js';
import puppeteer from 'puppeteer';

(async () => { 
  // Delete old output file
  await fs.unlink(appConstants.mediaOutput, () => {});

  const browser = await puppeteer.launch({ headless: false, devtools: false });
  const page = await browser.newPage();
  await page.setViewport({  width: 1920, height: 1080, deviceScaleFactor: 1 });

  // Wait until page has loaded
  await page.goto('https://www.instagram.com/accounts/login/', { waitUntil: 'networkidle0' });

  // Accept cookies consent
  await cookiesConsent(page);

  // Enter username and password
  await page.type('[name="username"]', appConstants.instagramAccount.username);
  await page.type('[name="password"]', appConstants.instagramAccount.password);

  // Submit log in credentials and wait for navigation
  await page.click('[type="submit"]'),
  await page.waitForNavigation({ waitUntil: 'networkidle0' })

  await getUserData(page, 'traffygirls', 'WOMAN');

  await browser.close();
})()