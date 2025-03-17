const TurndownService = require('turndown');
const turndownPluginGfm = require('joplin-turndown-plugin-gfm');

// 初始化 Turndown.js
const turndownService = new TurndownService();

// 启用 GFM 插件（支持表格）
turndownService.use(turndownPluginGfm.gfm);

// 读取 HTML 输入并转换
function convertHTMLtoMarkdown(html) {
    return turndownService.turndown(html);
}

// 从标准输入读取数据
let data = '';
process.stdin.on('data', chunk => {
    data += chunk;
});

process.stdin.on('end', () => {
    try {
        const input = JSON.parse(data);
        console.log(convertHTMLtoMarkdown(input.html));
    } catch (e) {
        console.error('Error parsing input:', e);
        process.exit(1);
    }
});
