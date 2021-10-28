export default async function zara(page, label) {

  let gen = label.gender.trim();
  let pren = label.prendas.trim().replace(/ +/g, "%20");

  if (gen == "hombre") {
    gen = "MAN";
  } else if (gen == "mujer") {
    gen = "WOMAN";
  }

  await page.goto(
    `https://www.zara.com/es/es/search?searchTerm=${pren}&section=${gen}`,
    { waitUntil: "networkidle0" }
  );

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll(".product-grid-product")];

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

  return outputList
}
