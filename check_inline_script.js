const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('D:/Projects/market-hours-beijing-timeline/index.html','utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
if(!scripts.length) throw new Error('no inline script');
for (const [i,s] of scripts.entries()) {
  new vm.Script(s, { filename: `inline-${i}.js` });
}
if(!html.includes('统一轨道（默认同步夏令时 / 冬令时）')) throw new Error('simplified editor UI missing');
if(!html.includes('syncBothModesFromStandard')) throw new Error('sync logic missing');
console.log('syntax-ok');
