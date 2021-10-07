const puppeteer = require('puppeteer');
//const fs = require("fs/promises");

(async () => {
    const browser = await puppeteer.launch({devtools: true});
    const page = await browser.newPage();
    await page.goto('https://www.instagram.com/traffygirls/', { waitUntil: 'domcontentloaded' });

    

    //await page.waitForSelector('button');
    await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));

    await page.screenshot({ path: './exampleInsta1.png' });
    
    await page.evaluate(() => {
        const buttons = [...document.querySelectorAll('button')];
        //console.log(document.querySelectorAll('button'));
        const acceptButton = buttons.find(x => x.textContent === 'Aceptar todas' || x.textContent === 'Accept All'  );
        if (acceptButton)   {
            acceptButton.click();
        }
        setTimeout(() => {}, 4000); 
        
        
    });

    await page.waitForTimeout(5000)

    await page.screenshot({ path: './exampleInsta2.png' });

    await browser.close();

})();
