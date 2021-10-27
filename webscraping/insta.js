import appConstants from "./appConstants.js";
import dayjs from 'dayjs';
import isBetween from 'dayjs/plugin/isBetween.js';
import { updateMediaOutput } from './Utils.js';

/**
 * Method to enter username and password and submit
 * @param page
 *  */ 
export const login = async (page) => {
  await page.type('[name="username"]', appConstants.instagramAccount.username);
  await page.type('[name="password"]', appConstants.instagramAccount.password);
  await page.click('[type="submit"]'),
  await page.waitForNavigation({ waitUntil: 'networkidle0' })
}

/**
 * Method to get post links from username page and get data
 * @param page
 * @param user
 * @param gender
 *  */ 
export const getUserData = async (page, user, gender) => {
    const output = [];

    const now = dayjs();
    const dateLimit = now.subtract("2", "week");
    dayjs.extend(isBetween);
    
    await page.goto(`https://www.instagram.com/${user}/`, { waitUntil: 'networkidle0' });

    const followers = await page.evaluate(() => document.querySelector('.g47SY')?.textContent?.replace('.', ''));
    const postList = await page.evaluate(() => [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a')?.href));
    
    for (let post of postList) {
        const data = await getPostData(page, post, { followers, user, gender });

        if (data) {
            if (dayjs(data.date).isBetween(dateLimit, now)) {
                data.date = dayjs(data.date).format('DD/MM/YYYY');
                output.push(data);
            } else {
                break;
            }
        }
    }

    await updateMediaOutput(output, appConstants.mediaOutput, user);
};

/**
 * Method to get post data
 * @param page
 * @param src
 * @param additionalData
 *  */ 
const getPostData = async (page, src, additionalData) => {

    await page.goto(src, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);

    const output = await page.evaluate(() => {
        const imageSrc = document.querySelector(".KL4Bh img")?.src;
        const likes = document.querySelector('.zV_Nj span')?.textContent?.replace(/[,.]/g, '');
        const date = document.querySelector('time')?.dateTime;

        return { likes, date, imageSrc };
    });
    
    return output.imageSrc ? Object.assign(output, additionalData) : null;
}
