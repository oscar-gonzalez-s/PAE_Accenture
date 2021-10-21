import appConstants from "./appConstants.js";
import puppeteer from "puppeteer";
import { updateOutput } from "./Utils.js";
import csv from "csvtojson";

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

  const labels = await csv().fromFile("labels.csv");

  let gen = labels[0].gender.trim();
  let pren = labels[0].prendas.trim().replace(/ +/g, "+");

  if (gen == "hombre") {
    gen = "men";
  } else if (gen == "mujer") {
    gen = "ladies";
  }

  await page.goto(
    `https://www2.hm.com/es_es/search-results.html?q=${pren}&department=${gen}_all&sort=stock&image-size=small&image=stillLife&offset=0&page-size=40`,
    { waitUntil: "domcontentloaded" }
  );

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll(".product-item")];

    // TODO: Get length as param
    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector(".link").textContent;
      const price = product
        .querySelector(".item-price")
        .textContent.replace(/\n/g, "")
        .replace("€", "")
        .trim();
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
