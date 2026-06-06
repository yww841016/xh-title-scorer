import re

with open(r'C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS to insert before </style>
modal_css = '''
  /* ============ PRICING MODAL ============ */
  .modal-overlay {
    display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5); z-index: 1000;
    align-items: center; justify-content: center; padding: 20px;
  }
  .modal-overlay.active { display: flex; }

  .modal {
    background: #fff; border-radius: 20px; padding: 28px 24px 24px;
    max-width: 440px; width: 100%; max-height: 90vh; overflow-y: auto;
    position: relative; animation: slideUp 0.3s ease;
  }
  @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

  .modal-close { position: absolute; top: 12px; right: 16px; background: none; border: none; font-size: 24px; cursor: pointer; color: #999; }
  .modal-close:hover { color: #333; }
  .modal h3 { text-align: center; font-size: 20px; margin-bottom: 6px; }
  .modal-subtitle { text-align: center; font-size: 13px; color: var(--text-secondary); margin-bottom: 20px; }

  .plans { display: flex; gap: 12px; margin-bottom: 20px; }
  .plan { flex: 1; border: 2px solid var(--border); border-radius: 16px; padding: 20px 14px; text-align: center; position: relative; transition: all 0.2s; }
  .plan:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 4px 16px rgba(255,36,66,0.1); }
  .plan.recommended { border-color: var(--primary); background: var(--primary-light); }
  .plan-badge { position: absolute; top: -10px; left: 50%%; transform: translateX(-50%%); background: var(--primary); color: #fff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 10px; }
  .plan-icon { font-size: 32px; margin-bottom: 8px; }
  .plan-name { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
  .plan-desc { font-size: 12px; color: var(--text-secondary); margin-bottom: 10px; }
  .plan-price { font-size: 28px; font-weight: 800; color: var(--primary); }
  .plan-price span { font-size: 14px; font-weight: 400; color: var(--text-secondary); }
  .plan-features { list-style: none; text-align: left; font-size: 12px; color: var(--text-secondary); margin-top: 10px; }
  .plan-features li { padding: 3px 0; }
  .plan-features li::before { content: \"\\2713 \"; color: var(--success); font-weight: 700; }

  .plan-btn { display: block; width: 100%%; text-align: center; padding: 10px; border-radius: 10px; font-size: 14px; font-weight: 700; text-decoration: none; margin-top: 10px; transition: all 0.15s; }
  .plan-btn.primary { background: linear-gradient(135deg, #ff2442, #ff6b81); color: #fff; }
  .plan-btn.primary:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(255,36,66,0.3); }
  .plan-btn.secondary { background: #fff; color: var(--primary); border: 2px solid var(--primary); }
  .plan-btn.secondary:hover { background: var(--primary-light); }

  .activation-section { border-top: 1px solid var(--border); padding-top: 16px; margin-top: 4px; text-align: center; }
  .toggle-link { font-size: 13px; color: var(--primary); cursor: pointer; text-decoration: underline; background: none; border: none; }
  .code-input-group { display: none; margin-top: 12px; gap: 8px; justify-content: center; }
  .code-input-group.active { display: flex; }
  .code-input-group input { flex: 1; max-width: 220px; padding: 8px 12px; border: 2px solid var(--border); border-radius: 8px; font-size: 14px; text-align: center; letter-spacing: 2px; font-family: monospace; outline: none; }
  .code-input-group input:focus { border-color: var(--primary); }
  .code-input-group button { padding: 8px 16px; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; }
  .code-msg { font-size: 12px; margin-top: 6px; }
  .code-msg.err { color: var(--danger); }
  .code-msg.ok { color: var(--success); font-weight: 600; }

  @media (max-width: 480px) { .plans { flex-direction: column; } .modal { padding: 20px 16px 16px; } }
'''

html = html.replace('</style>', modal_css + '\n</style>')

print('CSS inserted OK')
with open(r'C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index2.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Step 1 done')
