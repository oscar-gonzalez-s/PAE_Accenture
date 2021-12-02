import appConstants from './appConstants.js';
import dayjs from 'dayjs';
import isBetween from 'dayjs/plugin/isBetween.js';
import { updateMediaOutput } from './Utils.js';

/**
 * Method to enter username and password and submit log in form
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 *  */ 
export const login = async (page) => {
  console.log('Logging in...');
  await page.type('[name="username"]', appConstants.instagramAccount.username);
  await page.type('[name="password"]', appConstants.instagramAccount.password);
  await page.click('[type="submit"]'),
  await page.waitForNavigation({ waitUntil: 'networkidle0' });
  console.log(`Logged in with user ${appConstants.instagramAccount.username}`);
};

/**
 * Method to get post links from username page and get data
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 * @param {string} user Influencer username
 * @param {string} gender Influencer gender
 *  */ 
export const getUserData = async (page, user, gender) => {
  console.log(`Getting ${user} data...`);
    
  const output = [];
  const now = dayjs();
  const dateLimit = now.subtract('1', 'week');
  dayjs.extend(isBetween);
    
  await page.goto(`https://www.instagram.com/${user}/`, { waitUntil: 'networkidle2' });

  const followers = await page.evaluate(() => document.querySelectorAll('.g47SY')[1]?.title?.replace(/[,.]/g, ''));
  const postList = await page.evaluate(() => [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a')?.href));
    
  for (let post of postList) {
    const data = await getPostData(page, post, { followers, user, gender });

    if (!data) {
      console.log('   Image not found. Post is probably a video');
      continue;
    } else if (!dayjs(data.date).isBetween(dateLimit, now)) {
      break;
    }

    data.date = dayjs(data.date).format('DD/MM/YYYY');
    output.push(data);
  }

  await updateMediaOutput(output, appConstants.mediaOutput, user);
};

/**
 * Method to get post data
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 * @param {string} src Post url
 * @param {Object} additionalData Object containing followers, username and gender
 * @returns {Object | null} Post data or null if data was not found
 *  */ 
const getPostData = async (page, src, additionalData) => {

  await page.goto(src, { waitUntil: 'networkidle2' });

  const output = await page.evaluate(() => {
    const imageSrc = document.querySelector('.ltEKP .KL4Bh img')?.src;
    const likes = document.querySelector('.zV_Nj span')?.textContent?.replace(/[,.]/g, '');
    const date = document.querySelector('time')?.dateTime;

    return { likes, date, imageSrc };
  });
    
  return (output.imageSrc && output.likes) ? Object.assign(output, additionalData) : null;
};
