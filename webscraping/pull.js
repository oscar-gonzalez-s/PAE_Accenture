/**
 * Method to search a specific label in pull&bear website
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 * @param {string} label Label detected by image recognition
 * @returns {Object[]} List of the first two products found
 */
export default async function pull(page, label) {

  let gender = label.gender === 'MAN' ? 'hombre' : 'mujer';
  let items = label.item.trim().replace(/ +/g, '+');

  await page.goto(
    `https://www.pullandbear.com/es/mujer-n6417?q=${items}&filter=hierarchical_category%3A%22${gender}%22`,
    { waitUntil: 'networkidle2' }
  );

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.ebx-result')];

    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector('.ebx-result__title').textContent;
      const price = product.querySelector('.ebx-result-price__value').textContent.replace('€', '').trim();
      const src = product.querySelector('.ebx-result-link').href;
      const imageSrc = product.querySelector('img').src;

      return { name, price, src, imageSrc };
    });
  });

  return outputList.map(item => Object.assign(item, { gender: label.gender }));
}
