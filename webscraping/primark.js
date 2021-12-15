/**
 * Method to search a specific label in Primark website
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 * @param {string} label Label detected by image recognition
 * @returns {Object[]} List of the first two products found
 */
export default async function primark(page, label) {

  let gender = label.gender === 'MAN' ? 'hombre' : 'mujer';
  let items = label.item.trim().replace(/_+/g, ' ').replace(/ +/g, '+');
    
  await page.goto(
    `https://www.primark.com/es/search?text=${items}+${gender}`,
    { waitUntil: 'networkidle2'}
  );

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.product-listing__list > li')];

    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector('.product-item__name').textContent.replace(/\n/g, '').trim();
      const price = product.querySelector('.product-item__price').textContent.replace('€', '').trim();
      const src = product.querySelector('a').href;
      const imageSrc = product.querySelector('img').src;

      return { name, price, src, imageSrc };
    });
  });

  return outputList.map(item => Object.assign(item, { gender: label.gender }));
}
