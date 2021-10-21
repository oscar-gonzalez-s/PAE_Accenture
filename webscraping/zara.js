import appConstants from "./appConstants.js";
import csv from "csvtojson";
import puppeteer from "puppeteer";
import { updateOutput } from "./Utils.js";

//export const zaras = async () =>

(async () => {
  // Set devtools to true for debugging

  const browser = await puppeteer.launch({ devtools: false });

  // Create new page
  const page = await browser.newPage();

  // Remove the navigation timeout
  await page.setDefaultNavigationTimeout(0);

  // Set page dimensions for better image quality
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  // Uncomment to view page logs
  // await page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));

  // Navigate to website with the search result

  const labels = await csv().fromFile("labels.csv");

  let gen = labels[0].gender.trim();
  let pren = labels[0].prendas.trim().replace(/ +/g, "%20");

  if (gen == "hombre") {
    gen = "MAN";
  } else if (gen == "mujer") {
    gen = "WOMAN";
  }
  //console.log(pren);

  await page.goto(
    `https://www.zara.com/es/es/search?searchTerm=${pren}&section=${gen}`,
    { waitUntil: "domcontentloaded" }
  );

  await page.waitForTimeout(2000); // TODO :passa algo molt raro de que quan tornes a executar no les pilla.

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll(".product-grid-product")];

    // TODO: Get length as param

    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector(
        ".product-grid-product-info__name"
      ).textContent;
      const price = product
        .querySelector(".product-grid-product-info__price")
        .textContent.replace("EUR", "")
        .trim();
      const src = product.querySelector(".product-link").href;
      const imageSrc = product.querySelector("img").src;

      return {
        name: name,
        price: price,
        src: src,
        imageSrc: imageSrc,
      };
    });
  });

  await updateOutput({ zara: outputList }, appConstants.retailOutput);

  await browser.close();
})();
