## Constants

<dl>
<dt><a href="#appConstants">appConstants</a></dt>
<dd><p>Module to export constants that are shared across multiple scripts</p>
</dd>
</dl>

## Functions

<dl>
<dt><a href="#login">login(page)</a></dt>
<dd><p>Method to enter username and password and submit log in form</p>
</dd>
<dt><a href="#getUserData">getUserData(page, user, gender)</a></dt>
<dd><p>Method to get post links from username page and get data</p>
</dd>
<dt><a href="#updateOutput">updateOutput(data, path)</a></dt>
<dd><p>Method to update retail output without modifying existing one</p>
</dd>
<dt><a href="#updateMediaOutput">updateMediaOutput(data, path, user)</a></dt>
<dd><p>Method to update media output with individual user data</p>
</dd>
<dt><a href="#cookiesConsent">cookiesConsent(page)</a></dt>
<dd><p>Method to accept cookies consent</p>
</dd>
<dt><a href="#rejectConsent">rejectConsent(page)</a></dt>
<dd><p>Method to not save login info / dismiss notifications</p>
</dd>
<dt><a href="#downloadFile">downloadFile(fileUrl, downloadFolder, imgName)</a></dt>
<dd><p>Method to download a single image</p>
</dd>
<dt><a href="#downloadAll">downloadAll(path)</a></dt>
<dd><p>Download all the images in the json file</p>
</dd>
<dt><a href="#getPostData">getPostData(page, src, additionalData)</a> ⇒ <code>Object</code> | <code>null</code></dt>
<dd><p>Method to get post data</p>
</dd>
<dt><a href="#zara">zara(page, label)</a> ⇒ <code>Object[]</code></dt>
<dd><p>Method to search a specific label in zara website</p>
</dd>
<dt><a href="#hm">hm(page, label)</a> ⇒ <code>Object[]</code></dt>
<dd><p>Method to search a specific label in hm website</p>
</dd>
<dt><a href="#pull">pull(page, label)</a> ⇒ <code>Object[]</code></dt>
<dd><p>Method to search a specific label in pull website</p>
</dd>
<dt><a href="#primark">primark(page, label)</a> ⇒ <code>Object[]</code></dt>
<dd><p>Method to search a specific label in primark website</p>
</dd>
</dl>

<a name="appConstants"></a>

## appConstants
Module to export constants that are shared across multiple scripts

**Kind**: global constant  
<a name="login"></a>

## login(page)
Method to enter username and password and submit log in form

**Kind**: global constant  

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |

<a name="getUserData"></a>

## getUserData(page, user, gender)
Method to get post links from username page and get data

**Kind**: global constant  

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |
| user | <code>string</code> | Influencer username |
| gender | <code>string</code> | Influencer gender |

<a name="updateOutput"></a>

## updateOutput(data, path)
Method to update retail output without modifying existing one

**Kind**: global constant  

| Param | Type | Description |
| --- | --- | --- |
| data | <code>Object</code> | Object that contains data to append |
| path | <code>string</code> | Path to retail output file |

<a name="updateMediaOutput"></a>

## updateMediaOutput(data, path, user)
Method to update media output with individual user data

**Kind**: global constant  

| Param | Type | Description |
| --- | --- | --- |
| data | <code>Array&lt;Object&gt;</code> | Array containing user's posts information |
| path | <code>string</code> | Path to media output file |
| user | <code>string</code> | Influencer username to log information |

<a name="cookiesConsent"></a>

## cookiesConsent(page)
Method to accept cookies consent

**Kind**: global constant  

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |

<a name="rejectConsent"></a>

## rejectConsent(page)
Method to not save login info / dismiss notifications

**Kind**: global constant  

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |

<a name="downloadFile"></a>

## downloadFile(fileUrl, downloadFolder, imgName)
Method to download a single image

**Kind**: global function  

| Param | Type | Description |
| --- | --- | --- |
| fileUrl | <code>string</code> | Url to download the image |
| downloadFolder | <code>string</code> | Folder to save the image |
| imgName | <code>string</code> | Name of the image to download |

<a name="downloadAll"></a>

## downloadAll(path)
Download all the images in the json file

**Kind**: global function  

| Param | Type | Description |
| --- | --- | --- |
| path | <code>string</code> | Path to media-output.json |

<a name="getPostData"></a>

## getPostData(page, src, additionalData) ⇒ <code>Object</code> \| <code>null</code>
Method to get post data

**Kind**: global function  
**Returns**: <code>Object</code> \| <code>null</code> - Post data or null if data was not found  

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |
| src | <code>string</code> | Post url |
| additionalData | <code>Object</code> | Object containing followers, username and gender |

<a name="zara"></a>

## zara(page, label) ⇒ <code>Object[]</code>
Method to search a specific label in zara website

**Kind**: global function  
**Returns**: <code>Object[]</code> - List of the first two products found

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |
| label | <code>string</code> | Label detected by image recognition |

<a name="hm"></a>

## hm(page, label) ⇒ <code>Object[]</code>
Method to search a specific label in hm website

**Kind**: global function  
**Returns**: <code>Object[]</code> - List of the first two products found

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |
| label | <code>string</code> | Label detected by image recognition |

<a name="pull"></a>

## pull(page, label) ⇒ <code>Object[]</code>
Method to search a specific label in pull website

**Kind**: global function  
**Returns**: <code>Object[]</code> - List of the first two products found

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |
| label | <code>string</code> | Label detected by image recognition |

<a name="primark"></a>

## primark(page, label) ⇒ <code>Object[]</code>
Method to search a specific label in primark website

**Kind**: global function  
**Returns**: <code>Object[]</code> - List of the first two products found

| Param | Type | Description |
| --- | --- | --- |
| page | <code>Puppeteer.Page</code> | Puppeteer page to evaluate |
| label | <code>string</code> | Label detected by image recognition |

