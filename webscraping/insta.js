const puppeteer = require('puppeteer');
//const fs = require("fs/promises");

(async () => {
    const browser = await puppeteer.launch({devtools: false});
    const page = await browser.newPage();
    await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' });

    //await page.waitForSelector('button');
    //await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));

    await page.evaluate(() => {
        const buttons = [...document.querySelectorAll('button')];
        
        //console.log(document.querySelectorAll('button'));
        const acceptButton = buttons.find(x => x.textContent === 'Aceptar todas' || x.textContent === 'Accept All'  );
        if(acceptButton){
            acceptButton.click();
        }     
        
    });
    await page.screenshot({ path: './test-images/exampleInsta1.png' });

    await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });

    setTimeout(async () => {
        await page.screenshot({ path: './test-images/exampleInsta.png' });
        await browser.close();
    }, 5000);

    await browser.close();

})();
