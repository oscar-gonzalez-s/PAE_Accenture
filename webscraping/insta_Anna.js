const puppeteer = require('puppeteer');
const fs = require("fs");

(async () => {
    const browser = await puppeteer.launch({ devtools: true });
    const page = await browser.newPage();
    await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });


    //await page.waitForSelector('button');
    await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
    await page.screenshot({ path: './exampleInsta1.png' });
    await page.evaluate(() => {
        const buttons = [...document.querySelectorAll('button')];
        //console.log(document.querySelectorAll('button'));
        const acceptButton = buttons.find(x => x.textContent === 'Aceptar todas' || x.textContent === 'Accept All');
        if (acceptButton) {
            acceptButton.click();
        }
        setTimeout(() => { }, 4000);


    });

    await page.waitForTimeout(5000)
    await page.screenshot({ path: './exampleInsta2.png' });

    const outputList = await page.evaluate(() => {
        const productList = [...document.querySelectorAll('.v1Nh3.kIKUG._bz0w')];

        // TODO: Get length as param
        return productList.map(product => product.querySelector('a').href)
    });

    // TODO: Read existing json and change only zara value

    const out = getItemProps(page,'https://www.instagram.com/p/CUsxFYWoV4n/');


    await browser.close();

})();


const getItemProps = async (page, src) => {

    await page.goto(src, { waitUntil: 'domcontentloaded' }); 

    await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));

    const outputList = await page.evaluate(() => {
        // await page.waitForTimeout(5000)
        
        const imageSrc = document.querySelector("meta[property='og:image']").content;    
        console.log(imageSrc);
        const likes = product.querySelector('.zV_Nj span').textContent;
        console.log(likes);
        const date = product.querySelector('time').dateTime;
        console.log(date);
            
            return {
                likes: likes,
                date: date,
                imageSrc: imageSrc
            };
        
    });

    return outputList
}