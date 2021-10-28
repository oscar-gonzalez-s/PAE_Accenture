export default async function pull(page, label) {

  let gen = label.gender.trim();
  let pren = label.prendas.trim().replace(/ +/g, "+");

  await page.goto(
    `https://www.pullandbear.com/es/mujer-n6417?q=${pren}&filter=hierarchical_category%3A%22${gen}%22`,
    { waitUntil: "networkidle0" }
  );

  const outputList = await page.evaluate(() => {
    const productList = [...document.querySelectorAll(".ebx-result")];

    return productList.slice(0, 2).map((product) => {
      const name = product.querySelector(".ebx-result__title").textContent;
      const price = product
        .querySelector(".ebx-result-price__value")
        .textContent.replace("€", "")
        .trim();
      const src = product.querySelector(".ebx-result-link").href;
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
