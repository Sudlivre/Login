// 使用时需要在项目目录安装puppeteer
// node i puppeteer
// node dingtalk.js
var puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const iphone = devices['iPhone 6'];
const conf = {
    headless: false,
    defaultViewport: {
        width: 1300,
        height: 900
    },
    slowMo: 30
};
puppeteer.launch(conf).then(async browser => {
    var page = await browser.newPage();
    await page.emulate(iphone);
    await page.goto('https://www.dingtalk.com/oasite/register_h5_new.htm');
    //关键点1
    await page.evaluate(async () => {
        Object.defineProperty(navigator, 'webdriver', {get: () => false})
    });
    // 错误输入，触发验证码
    await page.type('#mobileReal', '18181762479');
    await page.click('#dingapp > div > div > div > div > div._38BOT4Nk > a');
    await page.type('#mobileReal', '');
    await page.keyboard.press('Backspace');
    await page.click('._2q5FIy80');
    // 等待滑块出现
    var slide_btn = await page.waitForSelector('#nc_1_n1t', {timeout: 30000});
    // 计算滑块距离
    const rect = await page.evaluate((slide_btn) => {
        const {top, left, bottom, right} = slide_btn.getBoundingClientRect();
        return {top, left, bottom, right}
    }, slide_btn);
    console.log(rect);
    rect.left = rect.left + 10;
    rect.top = rect.top + 10;
    const mouse = page.mouse;
    await mouse.move(rect.left, rect.top);
    // 关键点2
    await page.touchscreen.tap(rect.left, rect.top); // h5需要手动分发事件 模拟app的事件分发机制。
    await mouse.down();
    var start_time = new Date().getTime();
    await mouse.move(rect.left + 800, rect.top, {steps: 25});
    await page.touchscreen.tap(rect.left + 800, rect.top,);
    console.log(new Date().getTime() - start_time);
    await mouse.up();
    console.log(await page.evaluate('navigator.webdriver'));
    console.log('end')
    // await page.close()

});