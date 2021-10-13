const puppeteer = require("puppeteer");
const Utils = require("./Utils");
const appConstants = require("./appConstants");
const csv = require("csvtojson");

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

  if (labels[0].gender == "hombre") {
    labels[0].gender = "MAN";
  }
  if (labels[0].gender == "mujer") {
    labels[0].gender = "WOMAN";
  }

  console.log(labels[0].gender);

  https: await page.goto(
    `https://www.zara.com/es/es/search?searchTerm=${labels[0].prendas
      .split(" ")
      .join("%20")}&section=${labels[0].gender}`,
    { waitUntil: "domcontentloaded" }
  );

/*   await page.goto(
    'https://www.zara.com/es/es/search?searchTerm=camiseta%20blanca&section=WOMAN',
    { waitUntil: 'domcontentloaded' }
  ); */

  await page.waitForTimeout(2000);

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll(".product-grid-product")];

    // TODO: Get length as param
    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector(
        ".product-grid-product-info__name"
      ).textContent;
      const price = product.querySelector(
        ".product-grid-product-info__price"
      ).textContent;
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

  Utils.updateOutput({ zara: outputList }, appConstants.retailOutput);

  await browser.close();
})();
