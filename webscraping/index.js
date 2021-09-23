const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.google.com/search?q=camiseta+blanca+flores&tbm=shop'); 

  await page.waitForSelector('button');

  await page.evaluate(async () => {
    const buttons = document.querySelectorAll('button');
    console.log(document.querySelectorAll('button'));
    if (buttons.length > 1) {
      buttons[1].click();
    }
  });
  
  setTimeout(async () => {
    await page.screenshot({ path: './test-images/example.png' });
  
    await browser.close();
  }, 5000);
})();
