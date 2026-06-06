import re

with open(r'C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Modal HTML to insert before </body>
modal_html = '''
<!-- ============ PRICING MODAL ============ -->
<div class=\"modal-overlay\" id=\"upgradeModal\">
  <div class=\"modal\">
    <button class=\"modal-close\" onclick=\"closeModal()\">\\u00d7</button>
    <div id=\"modalPricing\">
      <h3>\\u{1f680} 升级 Pro</h3>
      <p class=\"modal-subtitle\">解锁无限评分，让你的每一篇笔记都是爆款</p>
      <div class=\"plans\">
        <div class=\"plan\">
          <div class=\"plan-icon\">\\u{1f93d}</div>
          <div class=\"plan-name\">免费版</div>
          <div class=\"plan-desc\">轻度体验</div>
          <div class=\"plan-price\">\\u00a50<span>/月</span></div>
          <ul class=\"plan-features\">
            <li>每日 5 次评分</li>
            <li>3 条改写建议</li>
            <li>基础评分维度</li>
          </ul>
        </div>
        <div class=\"plan recommended\">
          <div class=\"plan-badge\">\\u{1f525} 推荐</div>
          <div class=\"plan-icon\">\\u2b50</div>
          <div class=\"plan-name\">Pro 版</div>
          <div class=\"plan-desc\">深度创作者</div>
          <div class=\"plan-price\">\\u00a59.9<span>/月</span></div>
          <ul class=\"plan-features\">
            <li>无限次评分</li>
            <li>5 条改写建议</li>
            <li>AI 智能深度分析</li>
            <li>历史记录保存</li>
          </ul>
          <a class=\"plan-btn primary\" href=\"https://afdian.com/a/yww841016\" target=\"_blank\" onclick=\"trackPay('pro')\">\\u{1f4b3} 立即订阅</a>
        </div>
        <div class=\"plan\">
          <div class=\"plan-icon\">\\u{1f680}</div>
          <div class=\"plan-name\">批量版</div>
          <div class=\"plan-desc\">MCN / 团队</div>
          <div class=\"plan-price\">\\u00a529.9<span>/月</span></div>
          <ul class=\"plan-features\">
            <li>一次生成 10 条</li>
            <li>多主题批量评分</li>
            <li>导出 Excel 报告</li>
            <li>优先客服支持</li>
          </ul>
          <a class=\"plan-btn secondary\" href=\"https://afdian.com/a/yww841016\" target=\"_blank\" onclick=\"trackPay('bulk')\">\\u{1f4b3} 立即订阅</a>
        </div>
      </div>
      <div class=\"activation-section\">
        <button class=\"toggle-link\" onclick=\"toggleCodeInput()\">\\u{1f511} 已有激活码？点此激活</button>
        <div class=\"code-input-group\" id=\"codeSection\">
          <input type=\"text\" id=\"codeInput\" placeholder=\"输入激活码\" maxlength=\"12\" autocomplete=\"off\">
          <button onclick=\"activateCode()\">激活</button>
        </div>
        <div class=\"code-msg\" id=\"codeMsg\"></div>
      </div>
      <p style=\"text-align:center;font-size:11px;color:#ccc;margin-top:12px;\">付款后前往 爱发电 私信获取激活码 \\u00b7 支持微信/支付宝</p>
    </div>
  </div>
</div>
'''

html = html.replace('</body>', modal_html + '\n</body>')

print('Modal HTML inserted OK')

with open(r'C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Step 2 done')
