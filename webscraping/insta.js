import { cookiesConsent, updateMediaOutput } from './Utils.js';

import appConstants from "./appConstants.js";
import dayjs from 'dayjs';
import isBetween from 'dayjs/plugin/isBetween.js';

const instagram = async (page, user, gender) => {
    const output = [];

    const now = dayjs();
    const dateLimit = now.subtract("2", "week");
    dayjs.extend(isBetween);

    // await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
    
    await page.goto(`https://www.instagram.com/${user}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Accept cookies consent
    await cookiesConsent(page);

    const followers = await page.evaluate(() => 
        document.querySelector('.g47SY')?.textContent?.replace('.', '')
    );
    const postList = await page.evaluate(() => 
        [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a')?.href)
    );

    console.log(postList.length);
    
    for(let i = 0; i < postList?.length; i++) {
        const data = await getItemProps(page, postList[i], { followers, user, gender });
        if (dayjs(data?.date).isBetween(dateLimit, now)) {
            data.date = dayjs(data.date).format('DD/MM/YYYY');
            output.push(data);
        } else {
            break;
        }
    }

    await updateMediaOutput(output, appConstants.mediaOutput, user);
};


const getItemProps = async (page, src, additionalData) => {

    console.log(src);
    await page.goto(src, { waitUntil: 'domcontentloaded' });
    //await page.waitForTimeout(2000);
    const location = await page.url();
    console.log(location);

    const output = await page.evaluate(() => {
        const imageSrc = document.querySelector("meta[property='og:image']")?.content;
        const likes = document.querySelector('.zV_Nj span')?.textContent?.replace('.', '');
        const date = document.querySelector('time')?.dateTime;
            
            return {
                likes: likes,
                date: date,
                imageSrc: imageSrc
                //comments: comments,
            };
    });
    
    return Object.assign(output, additionalData);
}

export default instagram;
