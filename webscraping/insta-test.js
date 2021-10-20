import { cookiesConsent } from './Utils.js';
import puppeteer from 'puppeteer';

(async () => {
    const browser = await puppeteer.launch({ devtools: true });
    const page = await browser.newPage();
    await page.setViewport({  width: 1920, height: 1080, deviceScaleFactor: 1 });
    await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
    
    await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Accept cookies consent
    await cookiesConsent(page);

    const postList = await page.evaluate(() => 
        [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')]
    );

    //await postList[0].hover();
    await page.hover('.v1Nh3.kIKUG._bz0w > img');
    await page.screenshot({ path: 'hover.png' })

    await browser.close();
})();