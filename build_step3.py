import re

with open(r'C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace script section
old_script_start = html.index('<script>')
old_script_end = html.index('</script>') + len('</script>')

new_js = r'''<script>
// ============ 激活码系统 ============
var VALID_CODES = [
  'XHS2024A1', 'XHS2024B2', 'XHS2024C3', 'XHS2024D4', 'XHS2024E5',
  'XHS2024F6', 'XHS2024G7', 'XHS2024H8', 'XHS2024I9', 'XHS2024J0',
  'XHSROCKET', 'XHSVIRAL1', 'XHSBOOST2', 'XHS999PRO'
];

function getProStatus() {
  try {
    var pro = JSON.parse(localStorage.getItem(\"xh_title_pro\") || \"{}\");
    if (pro.expires && new Date(pro.expires) > new Date()) return pro;
    localStorage.removeItem(\"xh_title_pro\");
    return null;
  } catch(e) { return null; }
}

function setProStatus(days) {
  days = days || 30;
  var expires = new Date();
  expires.setDate(expires.getDate() + days);
  localStorage.setItem(\"xh_title_pro\", JSON.stringify({
    expires: expires.toISOString(),
    activatedAt: new Date().toISOString(),
    plan: \"pro\"
  }));
}

function formatDate(isoStr) {
  return new Date(isoStr).toLocaleDateString(\"zh-CN\", {
    year: \"numeric\", month: \"long\", day: \"numeric\"
  });
}

// ============ 用量管理 ============
var MAX_FREE = 5;
var remaining = MAX_FREE;

function loadUsage() {
  try {
    var stored = JSON.parse(localStorage.getItem(\"xh_title_usage\") || \"{}\");
    var today = new Date().toDateString();
    if (stored.date === today) { remaining = stored.count; }
    else { remaining = MAX_FREE; saveUsage(); }
  } catch(e) { remaining = MAX_FREE; saveUsage(); }
}

function saveUsage() {
  localStorage.setItem(\"xh_title_usage\", JSON.stringify({
    date: new Date().toDateString(), count: remaining
  }));
}

// ============ UI 更新 ============
function updateUI() {
  var isPro = !!getProStatus();

  var usageText = document.getElementById(\"usageText\");
  var upgradeBtn = document.getElementById(\"upgradeBtn\");
  var remainingEl = document.getElementById(\"remaining\");

  if (isPro) {
    usageText.innerHTML = '<span style=\"color:#ffb300;font-weight:700;\">Pro 会员</span> · 无限使用';
    upgradeBtn.textContent = '⭐ Pro 已激活';
    upgradeBtn.classList.add(\"pro-active\");
  } else {
    remainingEl.textContent = Math.max(0, remaining);
    usageText.innerHTML = '\\u4eca\\u65e5\\u5269\\u4f59\\uff1a<span class=\"count\" id=\"remaining\">' + Math.max(0, remaining) + '</span> \\u6b21';
    upgradeBtn.textContent = '\\u{1f31f} \\u65e0\\u9650\\u4f7f\\u7528';
    upgradeBtn.classList.remove(\"pro-active\");
  }
  saveUsage();
}

// ============ 标题输入 ============
var titleInput = document.getElementById(\"titleInput\");
var charCount = document.getElementById(\"charCount\");

titleInput.addEventListener(\"input\", function() {
  var len = titleInput.value.length;
  charCount.textContent = len + \" / 60\";
  charCount.className = \"char-count\";
  if (len > 50) charCount.classList.add(\"warning\");
  if (len > 60) charCount.classList.add(\"over\");
});

function fillExample(text) {
  titleInput.value = text;
  titleInput.dispatchEvent(new Event(\"input\"));
}

// ============ 评分算法 ============
var DIMS = [
  { key: \"attraction\", name: \"\\u5438\\u5f15\\u529b\", icon: \"\\u{1f9f2}\" },
  { key: \"emotion\",   name: \"\\u60c5\\u7eea\\u5f20\\u529b\", icon: \"\\u{1f4a5}\" },
  { key: \"search\",    name: \"\\u641c\\u7d22\\u53cb\\u597d\", icon: \"\\u{1f50d}\" },
  { key: \"topic\",     name: \"\\u8bdd\\u9898\\u6027\", icon: \"\\u{1f525}\" },
  { key: \"concise\",   name: \"\\u7b80\\u6d01\\u5ea6\", icon: \"\\u2702\\ufe0f\" }
];

var PATTERNS = {
  number:   /(\\d+[\\u4e2a\\u79cd\\u9879\\u4ef6\\u6b3e\\u6761\\u6b65\\u62db]|[0-9]+[Kkw\\u4e07])/,
  emotion:  /(\\u8c01\\u61c2|\\u6551\\u547d|\\u7edd\\u4e86|\\u54ed\\u4e86|\\u762f\\u4e86|\\u592a|\\u771f\\u7684|\\u8d85\\u7ea7|\\u5de8|\\u7206|\\u65e0\\u654c|\\u5929\\u5450|\\u554a\\u554a|\\uff01\\uff01|\\uff01)/,
  suspense: /(\\u539f\\u6765|\\u5c45\\u7136|\\u7adf\\u7136|\\u5343\\u4e07\\u522b|\\u4e0d\\u8981\\u518d|\\u522b|\\u7ec8\\u4e8e|\\u8fd9\\u624d\\u662f|\\u624d\\u77e5\\u9053|\\u63ed\\u5f00)/,
  compare:  /(vs|\\u5bf9\\u6bd4|\\u548c|\\u8ddf|\\u6bd4|\\u78be\\u538b|\\u540a\\u6253|\\u5dee\\u522b|\\u5dee\\u8ddd)/,
  question: /[\\uff1f?]/,
  pain:     /(\\u540e\\u6094|\\u8e29\\u96f7|\\u907f\\u5751|\\u7ffb\\u8f66|\\u8e29\\u5751|\\u8840\\u6cea|\\u6559\\u8bad|\\u8bef\\u533a|\\u9677\\u9631)/,
  result:   /(\\u65b9\\u6cd5|\\u6280\\u5de7|\\u653b\\u7565|\\u6307\\u5357|\\u79d8\\u8bc0|\\u5e72\\u8d27|\\u5408\\u96c6|\\u603b\\u7ed3|\\u5206\\u4eab|\\u63a8\\u8350)/,
  hotWord:  /(202[0-9]|\\u6700\\u65b0|\\u5168\\u7f51|\\u7206\\u706b|\\u70ed\\u95e8|\\u5fc5\\u770b|\\u6536\\u85cf|\\u70b9\\u8d5e|\\u8d5e\\u7206)/
};

var EMOTION_WORDS = [\"\\u8c01\\u61c2\", \"\\u6551\\u547d\", \"\\u7edd\\u4e86\", \"\\u54ed\\u4e86\", \"\\u762f\\u4e86\", \"\\u592a\", \"\\u771f\\u7684\", \"\\u8d85\\u7ea7\", \"\\u5de8\", \"\\u7206\", \"\\u65e0\\u654c\", \"\\u5929\\u5450\", \"\\u554a\\u554a\", \"\\u54c7\\u585e\", \"OMG\", \"\\u9707\\u60ca\", \"\\u79bb\\u8c31\"];

function scoreTitle(title) {
  var scores = {};

  var attraction = 30;
  if (PATTERNS.number.test(title)) attraction += 20;
  if (PATTERNS.emotion.test(title)) attraction += 20;
  if (/[\\uff01!]$/.test(title)) attraction += 10;
  if (title.length >= 15 && title.length <= 25) attraction += 15;
  else if (title.length > 25 && title.length <= 35) attraction += 5;
  scores.attraction = Math.min(100, attraction);

  var emotion = 20;
  if (PATTERNS.emotion.test(title)) emotion += 30;
  var emotionCount = EMOTION_WORDS.filter(function(w) { return title.indexOf(w) !== -1; }).length;
  emotion += emotionCount * 15;
  if (/[\\uff01!]{2,}/.test(title)) emotion += 10;
  if (/[\\u554a\\u554a\\u5594\\u54e6]/.test(title)) emotion += 5;
  scores.emotion = Math.min(100, emotion);

  var search = 30;
  if (PATTERNS.number.test(title)) search += 10;
  if (PATTERNS.result.test(title)) search += 15;
  if (PATTERNS.hotWord.test(title)) search += 10;
  var keywords = title.match(/[^\\u7684\\u4e86\\u4e00\\u662f\\u6211\\u6709\\u548c\\u4e0d\\u7740\\u5728]/g);
  if (keywords && keywords.length >= 8) search += 15;
  if (title.length >= 10 && title.length <= 30) search += 10;
  scores.search = Math.min(100, search);

  var topic = 25;
  if (PATTERNS.compare.test(title)) topic += 20;
  if (PATTERNS.suspense.test(title)) topic += 20;
  if (PATTERNS.pain.test(title)) topic += 20;
  if (PATTERNS.question.test(title)) topic += 10;
  if (PATTERNS.hotWord.test(title)) topic += 10;
  scores.topic = Math.min(100, topic);

  var concise = 40;
  if (title.length <= 15) concise += 30;
  else if (title.length <= 20) concise += 35;
  else if (title.length <= 25) concise += 30;
  else if (title.length <= 30) concise += 15;
  else if (title.length <= 40) concise += 5;
  else concise -= 10;
  scores.concise = Math.min(100, Math.max(0, concise));

  var allScores = Object.values(scores);
  var min = Math.min.apply(null, allScores);
  var sum = 0, count = 0;
  Object.values(scores).forEach(function(s) {
    if (s !== min || allScores.indexOf(s) !== allScores.indexOf(min)) {
      sum += s; count++;
    }
  });
  if (count === 0) { sum = allScores.reduce(function(a,b){return a+b;}, 0); count = allScores.length; }
  var avg = sum / count;
  var overall = Math.round(avg * 0.6 + scores.attraction * 0.4);

  return { overall: overall, dimensions: scores };
}

// ============ AI 改写 ============
function generateRewrites(title, isPro) {
  var rewrites = [];
  var cleaned = title.replace(/[\\uff0c\\u3002\\uff01\\uff1f\\u3001\\uff1b\\uff1a\\\"\\\"\\'\\'\\uff08\\uff09\\\\(\\\\)\\[\\]\\u3010\\u3011\\s]/g, \" \");
  var words = cleaned.split(/\\s+/).filter(function(w) { return w.length >= 2; });
  var core = words.slice(0, Math.min(5, words.length)).join(\"\");

  if (!PATTERNS.number.test(title) && core.length > 2) {
    var nums = [\"3个\", \"5个\", \"6个\", \"8个\", \"10个\"];
    var num = nums[Math.floor(Math.random() * nums.length)];
    rewrites.push({
      text: num + core.slice(0, 6) + \"\\u5c0f\\u6280\\u5de7\\uff0c\\u6700\\u540e\\u4e00\\u4e2a\\u592a\\u7edd\\u4e86\\uff01\\uff01\",
      badge: \"badge-number\", badgeText: \"\\u6570\\u5b57\\u578b\",
      reason: \"\\u6570\\u5b57\\u5236\\u9020\\u5177\\u4f53\\u611f\\uff0c\\u914d\\u5408\\u60ac\\u5ff5\\u7ed3\\u5c3e\\uff0c\\u70b9\\u51fb\\u7387\\u63d0\\u5347 60%\"
    });
  } else if (core.length > 3) {
    rewrites.push({
      text: \"\\u7528\\u4e86\" + core.slice(0, 6) + \"\\u624d\\u77e5\\u9053\\uff0c\\u4ee5\\u524d\\u90fd\\u767d\\u8d39\\u4e86\\uff01\\uff01\\uff01\",
      badge: \"badge-suspense\", badgeText: \"\\u60ac\\u5ff5\\u578b\",
      reason: \"\\u5236\\u9020\\u4fe1\\u606f\\u5dee\\u5f15\\u53d1\\u597d\\u5947\\uff0c\\u4eba\\u7fa4\\u5929\\u7136\\u6015\\\"\\u9519\\u8fc7\\\"\"
    });
  }

  if (core.length > 4) {
    rewrites.push({
      text: \"\\u8c01\\u61c2\\u554a\\uff01\\uff01\\u8fd9\\u4e2a\" + core.slice(0, 4) + \"\\u771f\\u7684\\u7edd\\u4e86\\uff0c\\u540e\\u6094\\u6ca1\\u65e9\\u7528\",
      badge: \"badge-emotion\", badgeText: \"\\u60c5\\u7eea\\u578b\",
      reason: \"\\u524d\\u7f6e\\u60c5\\u7eea\\u8bcd\\u5efa\\u7acb\\u5171\\u9e23\\uff0c\\u8fde\\u7528\\u611f\\u53f9\\u53f7\\u5f3a\\u5316\\u51b2\\u51fb\\u529b\"
    });
  }

  if (core.length > 4) {
    rewrites.push({
      text: \"\\u5343\\u4e07\\u522b\\u4e71\" + core.slice(0, 4) + \"\\uff01\\uff0199%\\u7684\\u4eba\\u90fd\\u8e29\\u8fc7\\u8fd9\\u4e2a\\u5751\",
      badge: \"badge-pain\", badgeText: \"\\u75db\\u70b9\\u578b\",
      reason: \"\\u53cd\\u5e38\\u8bc6\\u5f00\\u5934 + \\u5236\\u9020\\u7126\\u8651\\u611f\\uff0c\\u9a71\\u52a8\\u7528\\u6237\\u70b9\\u5f00\\u9a8c\\u8bc1\"
    });
  }

  if (isPro && core.length > 4) {
    rewrites.push({
      text: core.slice(0, 8) + \"\\u770b\\u8fd9\\u7bc7\\u5c31\\u591f\\u4e86\\uff0c\\u5168\\u7f51\\u6700\\u5168\\u5408\\u96c6\\u{1f525}\",
      badge: \"badge-compare\", badgeText: \"\\u5408\\u96c6\\u578b\",
      reason: \"\\\"\\u770b\\u8fd9\\u7bc7\\u5c31\\u591f\\u4e86\\\"\\u5efa\\u7acb\\u6743\\u5a01\\u611f\\uff0c\\u9002\\u5408\\u5e72\\u8d27\\u7c7b\\u7b14\\u8bb0\"
    });
  }

  return rewrites;
}

// ============ 主流程 ============
function analyze() {
  var title = titleInput.value.trim();
  if (!title) {
    titleInput.focus();
    titleInput.style.borderColor = \"var(--danger)\";
    setTimeout(function() { titleInput.style.borderColor = \"var(--border)\"; }, 1500);
    return;
  }

  var isPro = !!getProStatus();

  if (!isPro && remaining <= 0) {
    showUpgrade();
    return;
  }

  if (!isPro) {
    remaining--;
    saveUsage();
    updateUI();
  }

  document.getElementById(\"loading\").classList.add(\"active\");
  document.getElementById(\"results\").classList.remove(\"active\");
  document.getElementById(\"analyzeBtn\").disabled = true;

  setTimeout(function() {
    var result = scoreTitle(title);
    var rewrites = generateRewrites(title, isPro);
    renderResults(result, rewrites);

    document.getElementById(\"loading\").classList.remove(\"active\");
    document.getElementById(\"results\").classList.add(\"active\");
    document.getElementById(\"analyzeBtn\").disabled = false;

    document.getElementById(\"results\").scrollIntoView({ behavior: \"smooth\", block: \"start\" });
  }, 800);
}

// ============ 渲染结果 ============
function renderResults(result, rewrites) {
  var gaugeFg = document.getElementById(\"gaugeFg\");
  var circumference = 376.99;
  var offset = circumference - (result.overall / 100) * circumference;

  var color;
  if (result.overall >= 85) color = \"#00c853\";
  else if (result.overall >= 70) color = \"#64dd17\";
  else if (result.overall >= 50) color = \"#ff9800\";
  else color = \"#ff2442\";

  gaugeFg.style.strokeDashoffset = offset;
  gaugeFg.style.stroke = color;

  document.getElementById(\"scoreNum\").textContent = result.overall;
  document.getElementById(\"scoreNum\").style.color = color;

  var verdict;
  if (result.overall >= 90) verdict = \"\\u{1f3c6} \\u7206\\u6b3e\\u9884\\u5b9a\\uff01\\u53d1\\u5e03\\u5c31\\u5bf9\\u4e86\";
  else if (result.overall >= 75) verdict = \"\\u{1f44d} \\u4f18\\u8d28\\u6807\\u9898\\uff0c\\u5fae\\u8c03\\u540e\\u66f4\\u70b8\";
  else if (result.overall >= 60) verdict = \"\\u{1f4dd} \\u8fd8\\u4e0d\\u9519\\uff0c\\u8fd8\\u6709\\u4f18\\u5316\\u7a7a\\u95f4\";
  else if (result.overall >= 40) verdict = \"\\u{1f527} \\u5efa\\u8bae\\u5927\\u6539\\uff0c\\u91cd\\u70b9\\u52a0\\u60c5\\u7eea\\u8bcd\";
  else verdict = \"\\u26a0\\ufe0f \\u6807\\u9898\\u592a\\u5e73\\u6de1\\uff0c\\u91cd\\u5199\\u5427\";

  document.getElementById(\"scoreVerdict\").textContent = verdict;

  var dimsEl = document.getElementById(\"dimensions\");
  dimsEl.innerHTML = DIMS.map(function(d) {
    var score = result.dimensions[d.key];
    var barColor;
    if (score >= 80) barColor = \"#00c853\";
    else if (score >= 60) barColor = \"#64dd17\";
    else if (score >= 40) barColor = \"#ff9800\";
    else barColor = \"#ff2442\";

    var tip = \"\";
    if (score < 60) {
      var tips = {
        attraction: \"\\u8bd5\\u8bd5\\u52a0\\u5165\\u6570\\u5b57\\u6216\\u60c5\\u7eea\\u8bcd\",
        emotion: \"\\u52a0\\\"\\u8c01\\u61c2\\u554a\\\"\\\"\\u7edd\\u4e86\\\"\\u7b49\\u611f\\u53f9\\u8bcd\",
        search: \"\\u52a0\\u4e0a\\u54c1\\u7c7b\\u5173\\u952e\\u8bcd\\u66f4\\u6613\\u88ab\\u641c\\u7d22\",
        topic: \"\\u7ed3\\u5408\\u70ed\\u70b9\\u8bdd\\u9898\\u6216\\u5236\\u9020\\u5bf9\\u6bd4\",
        concise: \"\\u7cbe\\u7b80\\u5230 15-25 \\u5b57\\u6548\\u679c\\u6700\\u597d\"
      };
      tip = tips[d.key] || \"\";
    }

    return \"<div class=\\\"dim-item\\\">\" +
      \"<div class=\\\"dim-icon\\\">\" + d.icon + \"</div>\" +
      \"<div class=\\\"dim-info\\\">\" +
        \"<div class=\\\"dim-name\\\">\" +
          \"<span>\" + d.name + \"</span>\" +
          \"<span style=\\\"color:\" + barColor + \";font-weight:700;\\\">\" + score + \"\\u5206</span>\" +
        \"</div>\" +
        \"<div class=\\\"dim-bar-bg\\\">\" +
          \"<div class=\\\"dim-bar-fg\\\" style=\\\"width:\" + score + \"%;background:\" + barColor + \";\\\"></div>\" +
        \"</div>\" +
        (tip ? \"<div class=\\\"dim-tip\\\">\\u{1f4a1} \" + tip + \"</div>\" : \"\") +
      \"</div>\" +
    \"</div>\";
  }).join(\"\");

  var rewritesEl = document.getElementById(\"rewrites\");
  rewritesEl.innerHTML = rewrites.map(function(r) {
    return \"<div class=\\\"rewrite-item\\\">\" +
      \"<span class=\\\"rewrite-badge \" + r.badge + \"\\\">\" + r.badgeText + \"</span>\" +
      \"<div class=\\\"rewrite-text\\\">\" + r.text + \"</div>\" +
      \"<div class=\\\"rewrite-reason\\\">\" + r.reason + \"</div>\" +
      \"<button class=\\\"copy-btn\\\" onclick=\\\"copyRewrite(this, '\" + r.text.replace(/'/g, \"\\\\'\") + \"')\\\">\\u{1f4cb} \\u590d\\u5236</button>\" +
    \"</div>\";
  }).join(\"\");
}

// ============ 复制 ============
function copyRewrite(btn, text) {
  navigator.clipboard.writeText(text).then(function() {
    btn.textContent = \"\\u2705 \\u5df2\\u590d\\u5236\";
    btn.classList.add(\"copied\");
    setTimeout(function() {
      btn.textContent = \"\\u{1f4cb} \\u590d\\u5236\";
      btn.classList.remove(\"copied\");
    }, 2000);
  });
}

// ============ 付费弹窗 ============
function showUpgrade() {
  var modal = document.getElementById(\"upgradeModal\");
  modal.classList.add(\"active\");
}

function closeModal() {
  document.getElementById(\"upgradeModal\").classList.remove(\"active\");
  document.getElementById(\"codeInput\").value = \"\";
  document.getElementById(\"codeMsg\").textContent = \"\";
  document.getElementById(\"codeMsg\").className = \"code-msg\";
  document.getElementById(\"codeSection\").classList.remove(\"active\");
}

function toggleCodeInput() {
  document.getElementById(\"codeSection\").classList.toggle(\"active\");
  document.getElementById(\"codeInput\").focus();
}

function activateCode() {
  var input = document.getElementById(\"codeInput\");
  var msg = document.getElementById(\"codeMsg\");
  var code = input.value.trim().toUpperCase();

  if (!code || code.length < 6) {
    msg.textContent = \"\\u8bf7\\u8f93\\u5165\\u6709\\u6548\\u7684\\u6fc0\\u6d3b\\u7801\";
    msg.className = \"code-msg err\";
    return;
  }

  if (VALID_CODES.indexOf(code) !== -1) {
    setProStatus(30);
    msg.textContent = \"\\u2705 \\u6fc0\\u6d3b\\u6210\\u529f\\uff01Pro \\u529f\\u80fd\\u5df2\\u89e3\\u9501\\uff0830\\u5929\\uff09\";
    msg.className = \"code-msg ok\";
    updateUI();

    // Close modal after short delay so user sees success
    setTimeout(function() {
      closeModal();
    }, 1500);
  } else {
    msg.textContent = \"\\u274c \\u6fc0\\u6d3b\\u7801\\u65e0\\u6548\\uff0c\\u8bf7\\u6838\\u5bf9\\u540e\\u91cd\\u8bd5\";
    msg.className = \"code-msg err\";
  }
}

function trackPay(plan) {
  console.log(\"Payment intent: \" + plan);
}

window.onclick = function(e) {
  if (e.target.id === \"upgradeModal\") closeModal();
};

// ============ 初始化 ============
loadUsage();
updateUI();
</script>'''

html = html[:old_script_start] + new_js + html[old_script_end:]

with open(r'C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('JS replaced OK. Size:', len(html))
