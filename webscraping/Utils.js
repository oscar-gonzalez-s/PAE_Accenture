/**
 * Module to export functions that are shared across multiple scripts
 * **/

import fs from 'fs';

/**
 * Method to update retail output without modifying existing
 * @param data
 * @param path
 *  */ 
export const updateOutput = async (data, path) => {
    const json = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch(() => {return {}});
  
    Object.assign(json, data)

    fs.writeFile(path, JSON.stringify(json, null, 4), 'utf8', (err) => {
        if (err) throw err;
        console.log('JSON file generated. Closing browser...');
    });
}

/**
 * Method to update media output with individual user data
 * @param data
 * @param path
 * @param user
 *  */ 
export const updateMediaOutput = async (data, path, user) => {
    const json = await fs.promises.readFile(path).then(json => JSON.parse(json)).catch(() => {return { output: [] }});
  
    if (data?.length) {
        json.output.push(...data);

        fs.writeFile(path, JSON.stringify(json, null, 4), 'utf8', (err) => {
            if (err) throw err;
            console.log(`JSON file updated with user ${user}`);
        });
    } else {
        console.log(`User ${user} has no data or doesn't exist`);
    }
}

/**
 * Method to update accept cookies consent
 * @param page
 *  */ 
export const cookiesConsent = async (page) => {
    console.log('Accepting cookies consent...');
    await page.evaluate(() => {
        const buttons = [...document.querySelectorAll('button')];
        const acceptButton = buttons.find(el => el.textContent === 'Aceptar todas' || el.textContent === 'Accept All');
        acceptButton?.click();
    });
    // Wait to count as clicked
    await page.waitForTimeout(1000);
}


/**
 * Method to not save login info / dismiss notifications
 * @param page
 *  */ 
export const rejectConsent = async (page) => {
    await page.evaluate(() => {
        const buttons = [...document.querySelectorAll('button')];
        const acceptButton = buttons.find(el => el.textContent === 'Not now' || el.textContent === 'Ahora no');
        acceptButton?.click();
    });
    // Wait to count as clicked
    await page.waitForTimeout(1000);
}

