export default async function primark(page, label) {

    let gen = label.gender.trim();
    let pren = label.prendas.trim().replace(/ +/g, "+");

    if (gen == "hombre") {
        gen = "mens";
    } else if (gen == "mujer") {
        gen = "womens";
    }

    await page.goto(
        `https://www.primark.com/search?q=${pren}%3Arelevance%3AnextToRootCategoryName%3A${gen}`,
        { waitUntil: "networkidle0" }
    );

    const outputList = await page.evaluate(() => {
        const productList = [
            ...document.querySelectorAll(".component > div > ul > li"), // product-item
        ];

        return productList.slice(0, 2).map((product) => {
            const name = product
                .querySelector(".product-item__name")
                .textContent.replace(/\n/g, "")
                .trim();
            const price = product
                .querySelector(".product-item__price")
                .textContent.replace("€", "")
                .trim();
            const src = product.querySelector("a").href;
            const imageSrc = product.querySelector("img").src;

            return {
                name: name,
                price: price,
                src: src,
                imageSrc: imageSrc,
            };
        });
    });

    return outputList;
}
