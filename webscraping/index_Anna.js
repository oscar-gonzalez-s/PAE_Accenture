const puppeteer = require('puppeteer');
const fs = require("fs/promises");

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.zara.com/es/es/search?searchTerm=camiseta%20blanca%20mujer&section=WOMAN'); 

  await page.waitForSelector('button');

  await page.evaluate(async () => {
    const buttons = document.querySelectorAll('button');
    console.log(document.querySelectorAll('button'));
    if (buttons.length > 1) {
      buttons[1].click();
    }
  });
  
  const names = await page.evaluate(() => {  // estem en el navegador, o sigui no veuras res si fas console.log()
      return Array.from(document.querySelectorAll(".product-grid-product-info")).map(x => x.textContent)
  })

  await fs.writeFile("names.txt", names.join("\r\n"))

  // primer argument es el selector css i el segon es una funció
  const photos = await page.$$eval("img", (imgs) => {
      return imgs.map(x => x.src) 
      
  }) 

  await fs.writeFile("images.txt", photos.join("\r\n"))

  const links = await page.evaluate(() => {  
    return Array.from(document.querySelectorAll(".product-link")).map(x => x.getAttribute('href'))
  })


  await fs.writeFile("links.txt", links.join("\r\n"))


  /*for ( const photo of photos){ // se suposa que descarrega i guarda les fotos pero no em va
      const imagepage = await page.goto(photo)
      await fs.writeFile("C:\\Users\\usuario\\Documents\\GitHub\\PAE_Accenture\\webscraping\\testimages", await imagepage.buffer())  // (path --> ens quedem el nom que tenia original,)
  }*/

  await browser.close();

})();
