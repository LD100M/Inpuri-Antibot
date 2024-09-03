const puppeteer = require('puppeteer');

const main = async () => {
	// Launch a new browser
	const browser = await puppeteer.launch({ headless: false });

	// Create a new page
	const page = await browser.newPage();

	// Navigate to the desired URL
	await page.goto('http://127.0.0.1:3000/site/login.html', {
		waitUntil: 'load',
	});

	// Take a screenshot (optional)
	await page.screenshot({ path: 'screenshot.png' });

	// Wait for 3000 milliseconds
	await new Promise((resolve) => setTimeout(resolve, 50000000));

	// Close the browser
	await browser.close();
};

(async () => {
	while (true) {
		await main();
	}
})();
