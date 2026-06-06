import re, json, html, os

# Read the HTML file
with open(r"C:\Users\yww66\Desktop\xiaohongshu-title-scorer\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Check if payment features exist
has_upgrade = "upgradeModal" in content
has_afdian = "爱发电" in content
has_activate = "activateCode" in content

print(f"upgradeModal: {has_upgrade}")
print(f"爱发电: {has_afdian}")  
print(f"activateCode: {has_activate}")
print(f"File size: {len(content)} bytes")

# Check if this is the new version with full payment modal
if "升级 Pro 会员" in content or "升级 Pro" in content:
    print("This IS the new version with full payment modal")
elif "验证阶段" in content:
    print("This is the OLD version with alert popup")
else:
    print("Unknown version")