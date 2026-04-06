const fs = require("fs");

// 读取在线列表
const online = fs.readFileSync("online_gateways.txt", "utf8")
  .split(/\r?\n/).map(s => s.trim()).filter(Boolean);

let speeds = {};
try { speeds = JSON.parse(fs.readFileSync("gateway_speeds.json", "utf8")); } catch(_) {}

online.sort((a, b) => (speeds[a] || 9999) - (speeds[b] || 9999));

if (online.length === 0) {
  console.warn("No online gateways, skipping gateways.js update.");
  process.exit(0);
}

// 写 gateways.js
const js = "const downloadGateways = [\n  " +
  online.map(u => JSON.stringify(u)).join(",\n  ") + "\n];\n";
fs.writeFileSync("gateways.js", js);
console.log(`gateways.js updated (${online.length} gateways)`);

// patch index.html
if (!fs.existsSync("index.html")) { console.log("No index.html, skip."); process.exit(0); }

let html = fs.readFileSync("index.html", "utf8");
const gwList = JSON.stringify(online, null, 2).replace(/^\[/, "[\n ").replace(/\]$/, "\n]");

// 清理历史残留的单独脚本块
html = html.replace(/<script>\s*(?:const|let|var)\s+downloadGateways\s*=\s*\[[\s\S]*?\]\s*;?\s*<\/script>\s*/g, "");

// 替换声明
const reDecl = /\b(const|let|var)\s+downloadGateways\s*=\s*\[[\s\S]*?\]\s*;?/;
if (reDecl.test(html)) {
  html = html.replace(reDecl, (_, kw) => `${kw} downloadGateways = ${gwList};`);
  fs.writeFileSync("index.html", html);
  console.log("index.html patched (declaration).");
  process.exit(0);
}

// 替换赋值
const reAssign = /\bdownloadGateways\s*=\s*\[[\s\S]*?\]\s*;?/;
if (reAssign.test(html)) {
  html = html.replace(reAssign, `downloadGateways = ${gwList};`);
  fs.writeFileSync("index.html", html);
  console.log("index.html patched (assignment).");
  process.exit(0);
}

console.error("ERROR: downloadGateways not found in index.html");
process.exit(2);
