const puppeteer = require('puppeteer');
const Utils = require('./Utils');

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
    'https://www.zara.com/es/es/search?searchTerm=camiseta%20blanca&section=WOMAN',
    { waitUntil: 'domcontentloaded' }
  ); 

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.product-grid-product')];

    // TODO: Get length as param
    return productList.slice(0, 2).map(product => {
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
  
  Utils.updateOutput({ zara: outputList });

  await browser.close();
})();
 