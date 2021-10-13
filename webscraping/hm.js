import appConstants from "./appConstants.js";
import puppeteer from 'puppeteer';
import { updateOutput } from "./Utils.js";

(async () => {
  // Devtools set to true is required
  const browser = await puppeteer.launch({ devtools: true });

  // Create new page
  const page = await browser.newPage();

  // await page.on("console", (msg) => console.log("PAGE LOG:", msg.text()));

  // Remove the navigation timeout
  await page.setDefaultNavigationTimeout(0);

  // Set page dimensions for better image quality
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  await page.goto(
    "https://www2.hm.com/es_es/search-results.html?q=camiseta+blanca",
    { waitUntil: "domcontentloaded" }
  );

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll(".product-item")];

    // TODO: Get length as param
    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector(".link").textContent;
      const price = product.querySelector(".item-price").textContent;
      const src = product.querySelector(".item-link").href;
      const imageSrc = product.querySelector("img").src;

      return {
        name: name,
        price: price,
        src: src,
        imageSrc: imageSrc,
      };
    });
  });

  await updateOutput({ hm: outputList }, appConstants.retailOutput);
  
  await browser.close();
})();
