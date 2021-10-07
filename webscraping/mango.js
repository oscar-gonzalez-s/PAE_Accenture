const puppeteer = require('puppeteer');
const fs = require("fs");

(async () => {
  // Set devtools to true for debugging
  const browser = await puppeteer.launch({devtools: true});

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
    'https://shop.mango.com/es/search?kw=camiseta%20blanca&brand=she&origin=caja-busqueda',
    { waitUntil: 'domcontentloaded' }
  ); 

  await page.waitForTimeout(10000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.page > div > ul > li')];

    // TODO: Get length as param
    return productList.slice(0, 2).map(product => {
      const name = product.querySelector('.product-name').textContent;
      const price = product.querySelector('.price-sale').textContent;
      const src = product.querySelector('._6vE5I').href;
      const imageSrc = product.querySelector('.product-image').src;

      return {
        name: name,
        price: price,
        src: src,
        imageSrc: imageSrc
      };
    })
  });
  
  // TODO: Read existing json and change only mango value
  const jsonObj = {
    mango: outputList
  }
  fs.writeFile('output.json', JSON.stringify(jsonObj, null, 4), 'utf8', (err) => {
    if (err) throw err;
    console.log('JSON file generated. Closing browser...');
  });

  await browser.close();
})();
 