export default async function hm(page, label) {

    let gen = label.gender.trim();
    let pren = label.prendas.trim().replace(/ +/g, "+");

    if (gen == "hombre") {
        gen = "men";
    } else if (gen == "mujer") {
        gen = "ladies";
    }

    await page.goto(
        `https://www2.hm.com/es_es/search-results.html?q=${pren}&department=${gen}_all&sort=stock&image-size=small&image=stillLife&offset=0&page-size=40`,
        { waitUntil: "networkidle0" }
    );

    const outputList = await page.evaluate(() => {
        const productList = [...document.querySelectorAll(".product-item")];

        return productList.slice(0, 2).map((product) => {
            const name = product.querySelector(".link").textContent;
            const price = product
                .querySelector(".item-price")
                .textContent.replace(/\n/g, "")
                .replace("€", "")
                .trim();
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

    return outputList
}