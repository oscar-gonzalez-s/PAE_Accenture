const puppeteer = require('puppeteer');
const fs = require("fs");

(async () => {
  // Set devtools to true for debugging
  const browser = await puppeteer.launch({devtools: false});

  // Create new page
  const page = await browser.newPage();

  // Remove the navigation timeout
  await page.setDefaultNavigationTimeout(0);

  // Set page dimensions for better image quality
  await page.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: 1,
  });

  // Uncomment to view page logs
  // await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
  
  // Navigate to website with the search result
  // TODO: Use labels from arguments
  await page.goto(
    'https://www.zara.com/es/es/search?searchTerm=camiseta%20blanca%20mujer&section=WOMAN',
    { waitUntil: 'domcontentloaded' }
  ); 

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.product-grid-product')];

    return productList.map(product => {
      const name = product.querySelector('.product-grid-product-info__name').textContent;
      const price = product.querySelector('.product-grid-product-info__price').textContent;
      const src = product.querySelector('.product-link').href;
      const imageSrc = product.querySelector('img').src;

      return {
        name: name,
        price: price,
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
    console.log('JSON file generated. Closing browser...');
  });

  await browser.close();
})();
 