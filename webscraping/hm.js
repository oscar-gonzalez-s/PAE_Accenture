/**
 * Method to search a specific label in HM website
 * @param {Puppeteer.Page} page Puppeteer page to evaluate
 * @param {string} label Label detected by image recognition
 * @returns {Object[]} List of the first two products found
 */
export default async function hm(page, label) {

  let gender = label.gender === 'MAN' ? 'men' : 'ladies';
  let items = label.item.trim().replace(/ +/g, '+');

  await page.goto(
    `https://www2.hm.com/es_es/search-results.html?q=${items}&department=${gender}_all&sort=stock&image-size=small&image=stillLife&offset=0&page-size=40`,
    { waitUntil: 'networkidle2' }
  );

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll('.product-item')];

    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector('.link').textContent;
      const price = product.querySelector('.item-price').textContent.replace(/\n/g, '').replace('€', '').trim();
      const src = product.querySelector('.item-link').href;
      const imageSrc = product.querySelector('img').src;

      return { name, price, src, imageSrc };
    });
  });

  return outputList.map(item => Object.assign(item, { gender: label.gender }));
}