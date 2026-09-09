// Record footage from the live three.js stage (or the flat visualizer) with headless Chrome.
// usage: node tools/record-stage.mjs <out.webm> <url> <seconds> <width> <height> [setupJS] [actionsJSON]
//   setupJS     runs in the page after load, before recording starts
//   actionsJSON [[tSeconds, js], ...] — js evaluated in the page at t seconds into the recording
//   In js, `key(k)` dispatches a keydown to the page (and into the visualizer iframe on the stage page).
import puppeteer from "/Users/britonbaker/.npm/_npx/7d92d9a2d2ccc630/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js";

const [out, url, secs = "8", w = "1080", h = "1920", setup = "", actionsJSON = "[]"] = process.argv.slice(2);
const actions = JSON.parse(actionsJSON);
const browser = await puppeteer.launch({
  headless: true,
  args: ["--use-gl=angle", "--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist", "--autoplay-policy=no-user-gesture-required", `--window-size=${w},${h}`],
  defaultViewport: { width: +w, height: +h, deviceScaleFactor: 1 },
});
const page = await browser.newPage();
page.on("pageerror", e => console.error("pageerror", e.message));
await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });
await new Promise(r => setTimeout(r, 9000));                 // models, fonts, iframe visualizer
await page.evaluate(() => {
  window.key = k => {
    const ev = new KeyboardEvent("keydown", { key: k });
    window.dispatchEvent(ev);
    const mon = document.getElementById("mon");            // stage page: the stage forwards keys itself
    if (!mon) { /* flat page: window handler already got it */ }
  };
});
if (setup) await page.evaluate(setup);
await new Promise(r => setTimeout(r, 1500));
const t0 = Date.now();
const rec = await page.screencast({ path: out, fps: 30 });
for (const [t, js] of actions.sort((a, b) => a[0] - b[0])) {
  const wait = t0 + t * 1000 - Date.now();
  if (wait > 0) await new Promise(r => setTimeout(r, wait));
  await page.evaluate(js);
}
const remain = t0 + +secs * 1000 - Date.now();
if (remain > 0) await new Promise(r => setTimeout(r, remain));
await rec.stop();
await browser.close();
console.log("recorded", out);
