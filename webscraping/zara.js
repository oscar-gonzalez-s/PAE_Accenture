/**
 * Method to search a specific label in Zara website
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 * @param {string} label Label detected by image recognition
 * @returns {Object[]} List of the first two products found
 */
export default async function zara(page, label) {

  let gender = label.gender;
  let items = label.item.trim().replace(/_+/g, ' ').replace(/ +/g, '%20');

  await page.goto(
    `https://www.zara.com/es/es/search?searchTerm=${items}&section=${gender}`,
    { waitUntil: 'networkidle2' }
  );

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.product-grid-product')];

    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector('.product-grid-product-info__name').textContent;
      const price = product.querySelector('.product-grid-product-info__price').textContent.replace('EUR', '').trim();
      const src = product.querySelector('.product-link').href;
      const imageSrc = product.querySelector('img').src;

      return { name, price, src, imageSrc };
    });
  });

  return outputList.map(item => Object.assign(item, { gender: label.gender }));
}
