const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  // Set devtools to true for debugging
  const browser = await puppeteer.launch({ devtools: true });

  // Create new page
  const page = await browser.newPage();

  // await page.on("console", (msg) => console.log("PAGE LOG:", msg.text()));

  // Remove the navigation timeout
  await page.setDefaultNavigationTimeout(0);

  // Set page dimensions for better image quality
  await page.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: 1,
  });

  await page.goto(
    "https://www2.hm.com/es_es/search-results.html?q=camiseta+blanca",
    { waitUntil: "domcontentloaded" }
  );
  // per passar parametres.
  const queryString = window.location.search;

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

  // TODO: Read existing json and change only zara value
  const jsonObj = {
    hm: outputList,
  };
  fs.writeFile(
    "output.json",
    JSON.stringify(jsonObj, null, 4),
    "utf8",
    (err) => {
      if (err) throw err;
      console.log("JSON file generated. Closing browser...");
    }
  );

  await browser.close();
})();