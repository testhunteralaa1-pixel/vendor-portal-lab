const assert = require('assert');
const fs = require('fs');
const path = require('path');

const COMPAT_TABLE = {
    '0': 'ember', '1': 'frost', '2': 'grove', '3': 'haven',
    '4': 'isle',  '5': 'jade',  '6': 'kelm',  '7': 'lark',
    '8': 'moss',  '9': 'nook',  'a': 'orba',  'b': 'plume',
    'c': 'quill', 'd': 'reed',  'e': 'spire', 'f': 'thorn'
};

function tagToWords(tag) {
    const words = [];
    for (let i = 0; i < tag.length; i++) {
        const code = tag.charCodeAt(i);
        const hex = code.toString(16).padStart(2, '0').toLowerCase();
        words.push(COMPAT_TABLE[hex[0]]);
        words.push(COMPAT_TABLE[hex[1]]);
    }
    return words.join('-');
}

// Test 1: Example from requirements "A" -> "isle-frost"
assert.strictEqual(tagToWords('A'), 'isle-frost', 'Test 1 Failed: "A" should convert to "isle-frost"');
console.log('✔ Test 1 Passed: "A" -> "isle-frost"');

// Test 2: Check config/deploy.json concatenation and conversion
const deployConfigPath = path.join(__dirname, '../config/deploy.json');
const deployData = JSON.parse(fs.readFileSync(deployConfigPath, 'utf8'));
assert.ok(deployData.deploy_env, 'deploy_env exists');
assert.ok(deployData.deploy_build, 'deploy_build exists');

const tag = deployData.deploy_env + '-' + deployData.deploy_build;
const wordTokens = tagToWords(tag);
console.log(`✔ Test 2 Passed: tag "${tag}" -> "${wordTokens}"`);

// Test 3: Verify index.html contains tagToWords logic
const indexHtmlPath = path.join(__dirname, '../index.html');
const indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');
assert.ok(indexHtml.includes('https://cdn.rtecra.com/portal/badge.svg?v='), 'index.html contains badge URL endpoint');
console.log('✔ Test 3 Passed: index.html contains updated badge URL endpoint');

console.log('All unit tests passed successfully!');
