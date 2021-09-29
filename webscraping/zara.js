const puppeteer = require('puppeteer');
const fs = require("fs");

(async () => {
  // Set devtools to true for debugging
  const browser = await puppeteer.launch({devtools: false});
  // Create new page
  const page = await browser.newPage();
  // Remove the navigation timeout
  await page.setDefaultNavigationTimeout(0);
  // Navigate to website with the search result
  // TODO: Use labels from arguments
  await page.goto(
    'https://www.zara.com/es/es/search?searchTerm=camiseta%20blanca%20mujer&section=WOMAN',
    { waitUntil: 'domcontentloaded' }
  ); 

  await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.product-grid-product')];

    return productList.map(product => {
      const title = product.querySelector('.product-grid-product-info').textContent;
      const src = product.querySelector('.product-link').href;
      const imageSrc = product.querySelector('img').src;

      return {
        title: title,
        src: src,
        imageSrc: imageSrc
      };
    })
  });

  
  // TODO: Read existing json and change only zara value
  const jsonObj = {
    zara: outputList
  }
  fs.writeFile('output.json', JSON.stringify(jsonObj, null, 4), 'utf8', (err) => {
    if (err) throw err;
    console.log('json generated. Closing browser...');
  });

  await browser.close();
})();
 