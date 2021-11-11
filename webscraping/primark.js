export default async function primark(page, label) {

  let gen = label.gender.trim() === 'hombre' ? 'mens' : 'womens';
  let pren = label.prendas.trim().replace(/ +/g, '+');
    
  await page.goto(
    `https://www.primark.com/search?q=${pren}%3Arelevance%3AnextToRootCategoryName%3A${gen}`,
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

  return Object.assign(outputList, { gender: label.gender });
}
