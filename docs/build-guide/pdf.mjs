// Needs: npm i playwright. Run from this folder: node pdf.mjs
import {chromium} from 'playwright';
const b=await chromium.launch({});
const p=await b.newPage(); await p.goto('file://'+process.cwd()+'/guide.html'); await p.waitForTimeout(500);
await p.pdf({path:'../module-build-guide.pdf',format:'A4',printBackground:true,displayHeaderFooter:true,
 headerTemplate:'<div></div>',
 footerTemplate:'<div style="font-family:DejaVu Sans,sans-serif;font-size:7.5pt;color:#64748b;width:100%;padding:0 17mm;display:flex;justify-content:space-between"><span>ESPHome Capacitive Rain Sensor · Module Build Guide</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
 margin:{top:'18mm',bottom:'20mm',left:'17mm',right:'17mm'}});
await b.close();
