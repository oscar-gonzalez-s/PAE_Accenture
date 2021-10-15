import { cookiesConsent, updateOutput } from './Utils.js';

import appConstants from "./appConstants.js";
import dayjs from 'dayjs';
import isBetween from 'dayjs/plugin/isBetween.js';
import puppeteer from 'puppeteer';

(async () => {
    const output = [];

    const now = dayjs();
    const dateLimit = now.subtract("2", "week");
    dayjs.extend(isBetween);

    const browser = await puppeteer.launch({ devtools: true });
    const page = await browser.newPage();
    await page.setViewport({  width: 1920, height: 1080, deviceScaleFactor: 1 });
    // await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
    
    // TODO: Get user from external source
    await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Accept cookies consent
    await cookiesConsent(page);

    // TODO: Get followers count and pass it to getItemProps
    const followers = await page.evaluate(() => 
        document.querySelector('.g47SY')?.textContent
    );
    const postList = await page.evaluate(() => 
        [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a')?.href)
    );
    
    // TODO: Format follower and like numbers (remove dot)
    for(let i = 0; i < postList?.length; i++) {
        const data = await getItemProps(page, postList[i], followers);
        if (dayjs(data?.date).isBetween(dateLimit, now)) {
            data.date = dayjs(data.date).format('DD/MM/YYYY');
            output.push(data);
        } else {
            break;
        }
    }

    // TODO: Handle WOMAN or MAN tags
    await updateOutput(output, appConstants.mediaOutput);

    await browser.close();
})();


const getItemProps = async (page, src, followers) => {

    await page.goto(src, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);

    const output = await page.evaluate(() => {
        const imageSrc = document.querySelector("meta[property='og:image']")?.content;
        const likes = document.querySelector('.zV_Nj span')?.textContent;
        const date = document.querySelector('time')?.dateTime;
            
            return {
                //comments: comments,
                likes: likes,
                date: date,
                imageSrc: imageSrc
            };
    });
    
    return Object.assign(output, { followers: followers });
}