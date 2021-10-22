// TODO: Borrar json antes de empezar
// TODO: Genero de la cuenta
// TODO: Controlar si existen los users
import instagram from './insta.js';
import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({ headless: false, devtools: false });
  const page = await browser.newPage();
  await page.setViewport({  width: 1920, height: 1080, deviceScaleFactor: 1 });

  await instagram(page, 'traffygirls', 'WOMAN');
  // await instagram(page, 'annapenello', 'WOMAN');

  await browser.close();
})()