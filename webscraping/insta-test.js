import { cookiesConsent } from './Utils.js';
import dayjs from 'dayjs';
import puppeteer from 'puppeteer';

(async () => {
    const now = dayjs();
    const dateLimit = now.subtract("2", "week");

    const browser = await puppeteer.launch({ devtools: true });
    const page = await browser.newPage();
    await page.setViewport({  width: 1920, height: 1080, deviceScaleFactor: 1 });
    await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
    
    // TODO: Get user from external source
    await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Accept cookies consent
    await cookiesConsent(page);

    // TODO: Get followers count and pass it to getItemProps
    const postList = await page.evaluate(() => 
        [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a').href)
    );

    // TODO: Make it a loop using productList
    const output = await getItemProps(page,'https://www.instagram.com/p/CUsxFYWoV4n/');
    console.log(output);

    await browser.close();
})();


const getItemProps = async (page, src) => {

    await page.goto(src, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000)

    const outputList = await page.evaluate(() => {
        const imageSrc = document.querySelector("meta[property='og:image']").content;
        const likes = document.querySelector('.zV_Nj span').textContent;
        const date = document.querySelector('time').dateTime;
            
            return {
                //followers: followers,
                likes: likes,
                date: date,
                imageSrc: imageSrc
            };
    });

    return outputList
}