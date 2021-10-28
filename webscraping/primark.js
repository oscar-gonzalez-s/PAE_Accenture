import appConstants from "./appConstants.js";
import puppeteer from "puppeteer";
import { updateOutput } from "./Utils.js";
import csv from "csvtojson";

(async () => {
  // Set devtools to true for debugging
  const browser = await puppeteer.launch({ devtools: false });

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

  const labels = await csv().fromFile("labels.csv");

  let gen = labels[0].gender.trim();
  let pren = labels[0].prendas.trim().replace(/ +/g, "+");

  if (gen == "hombre") {
    gen = "mens";
  } else if (gen == "mujer") {
    gen = "womens";
  }

  await page.goto(
    `https://www.primark.com/search?q=${pren}%3Arelevance%3AnextToRootCategoryName%3A${gen}`,
    { waitUntil: "domcontentloaded" }
  );

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [
      ...document.querySelectorAll(".component > div > ul > li"), // product-item
    ];

    // TODO: Get length as param --> No se puede.
    return productList.slice(0, 2).map((product) => {
      const name = product
        .querySelector(".product-item__name")
        .textContent.replace(/\n/g, "")
        .trim();
      const price = product
        .querySelector(".product-item__price")
        .textContent.replace("€", "")
        .trim();
      const src = product.querySelector("a").href;
      const imageSrc = product.querySelector("img").src;

      return {
        name: name,
        price: price,
        src: src,
        imageSrc: imageSrc,
      };
    });
  });

  await updateOutput({ primark: outputList }, appConstants.retailOutput);

  await browser.close();
})();
