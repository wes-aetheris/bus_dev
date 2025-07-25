const puppeteer = require('puppeteer');
const path = require('path');

async function htmlToPdf() {
  // Launch browser
  const browser = await puppeteer.launch({
    headless: true, // Set to false if you want to see the browser
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    // Create new page
    const page = await browser.newPage();
    
    // Set viewport for consistent rendering
    await page.setViewport({
      width: 1200,
      height: 800,
      deviceScaleFactor: 2 // Higher scale for better resolution
    });

    // Load HTML file (replace with your file path)
    const htmlPath = path.join(__dirname, 'your-file.html');
    await page.goto(`file://${htmlPath}`, {
      waitUntil: 'networkidle0' // Wait for all resources to load
    });

    // Generate PDF
    const pdf = await page.pdf({
      path: 'output.pdf',
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: {
        top: '20px',
        right: '20px',
        bottom: '20px',
        left: '20px'
      }
    });

    console.log('PDF generated successfully!');
    return pdf;

  } catch (error) {
    console.error('Error generating PDF:', error);
  } finally {
    await browser.close();
  }
}

// Run the function
htmlToPdf();