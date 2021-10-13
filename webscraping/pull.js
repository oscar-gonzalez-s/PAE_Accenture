import appConstants from "./appConstants.js";
import puppeteer from 'puppeteer';
import { updateOutput } from "./Utils.js";

(async () => {
  // Devtools set to true is required
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
    'https://www.pullandbear.com/es/mujer-n6417?q=Camiseta+blanca&filter=hierarchical_category%3A%22mujer%22',
    { waitUntil: 'domcontentloaded' }
  ); 

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.ebx-grid-item')];
    // TODO: Get length as param
    return productList.slice(0, 2).map(product => {
      const name = product.querySelector('.ebx-result__title').textContent;
      const price = product.querySelector('.ebx-result-price__value').textContent;
      const src = product.querySelector('.ebx-result-link').href;
      const imageSrc = product.querySelector('img').src;
       
      return {
        name: name,
        price: price,
        src: src,
        imageSrc: imageSrc
      };
    })
  });
  
  await updateOutput({ pull: outputList }, appConstants.retailOutput);

  await browser.close();
})();
 