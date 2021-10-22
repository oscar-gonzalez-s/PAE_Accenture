import appConstants from "./appConstants.js";
import dayjs from 'dayjs';
import isBetween from 'dayjs/plugin/isBetween.js';
import { updateMediaOutput } from './Utils.js';

export const getUserData = async (page, user, gender) => {
    const output = [];

    const now = dayjs();
    const dateLimit = now.subtract("2", "week");
    dayjs.extend(isBetween);
    
    await page.goto(`https://www.instagram.com/${user}/`, { waitUntil: 'networkidle0' });

    const followers = await page.evaluate(() => document.querySelector('.g47SY')?.textContent?.replace('.', ''));
    const postList = await page.evaluate(() => [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a')?.href));
    
    for(let i = 0; i < postList?.length; i++) {
        const data = await getPostData(page, postList[i], { followers, user, gender });
        if (dayjs(data?.date).isBetween(dateLimit, now)) {
            data.date = dayjs(data.date).format('DD/MM/YYYY');
            output.push(data);
        } else {
            break;
        }
    }

    await updateMediaOutput(output, appConstants.mediaOutput, user);
};


const getPostData = async (page, src, additionalData) => {

    await page.goto(src, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);

    const output = await page.evaluate(() => {
        const imageSrc = document.querySelector(".KL4Bh img")?.src;
        const likes = document.querySelector('.zV_Nj span')?.textContent?.replace(/[,.]/g, '');
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
