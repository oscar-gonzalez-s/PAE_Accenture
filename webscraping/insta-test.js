const puppeteer = require('puppeteer');
const fs = require("fs");
const dayjs = require('dayjs');

(async () => {
    try {
        const now = dayjs();
        const dateLimit = now.subtract("2", "week");

        const browser = await puppeteer.launch({ devtools: true });
        const page = await browser.newPage();
        await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
        
        // TODO: get user to navigate form external source
        await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(2000);

        // Accept cookies consent
        await page.evaluate(() => {
            const buttons = [...document.querySelectorAll('button')];
            const acceptButton = buttons.find(el => el.textContent === 'Aceptar todas' || el.textContent === 'Accept All');
            if (acceptButton) {
                acceptButton.click();
            }
        });

        // TODO: Get follower count and pass it to getItemProps
        const postList = await page.evaluate(() => 
            [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')].map(post => post.querySelector('a').href)
        );

        // TODO: Make it a loop using productList
        const output = await getItemProps(page,'https://www.instagram.com/p/CUsxFYWoV4n/');
        console.log(output);

        await browser.close();

    } catch (e) { throw e }
})();


const getItemProps = async (page, src) => {

    await page.goto(src, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5000)

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