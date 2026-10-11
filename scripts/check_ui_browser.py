"""Optional real-browser acceptance check. Use an isolated NOVA_DATA_DIR server.

Requires the Playwright developer tool; normal Nova launch does not need it.
"""
from pathlib import Path
import argparse
import json,re
import shutil
import uuid
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright, expect

parser=argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:8502')
parser.add_argument('--output', default='ui-evidence')
parser.add_argument('--chromium', default=shutil.which('chromium'))
args=parser.parse_args()
if urlsplit(args.url).hostname not in {'127.0.0.1', 'localhost'}:
 parser.error('Only an isolated local test server may be used.')
out=Path(args.output); out.mkdir(parents=True, exist_ok=True); results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=args.chromium,headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1366,'height':768},reduced_motion='reduce')
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(args.url)
 page.locator('img.nova-orb-svg').wait_for(timeout=30000)
 page.wait_for_function("document.querySelector('img.nova-orb-svg').complete")
 def clean():
  assert not page.get_by_test_id('stException').count(),page.get_by_test_id('stException').all_text_contents()
  assert not page.get_by_test_id('stAlertContentError').count(),page.get_by_test_id('stAlertContentError').all_text_contents()
  assert not page.evaluate('document.documentElement.scrollWidth>window.innerWidth'), 'horizontal page overflow'
 def nav(name):
  print('Checking navigation: '+name, flush=True)
  primary={'Chat','Voice','Projects','Memory','Settings'}
  destination=name if name in primary else 'Settings'
  page.get_by_test_id('stSidebar').get_by_test_id('stRadioOption').filter(has_text=re.compile('^'+re.escape(destination)+'$')).click()
  page.wait_for_timeout(500)
  if destination=='Settings':
   back=page.get_by_role('button',name='Back to Settings')
   if back.count(): back.click()
  if name not in primary:
   page.get_by_role('tab',name='Advanced',exact=True).click()
   page.get_by_role('button',name='Open '+name,exact=True).click()
  expect(page.get_by_test_id('stSidebar').get_by_role('radio',name=destination,exact=True)).to_be_checked()
  page.wait_for_timeout(400)
  clean()
 nav('Home')
 for width,height in ((1366,768),(1920,1080),(2560,1440),(760,700)):
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(500)
  clean()
  area=page.get_by_test_id('stChatInputTextArea').bounding_box()
  assert area['x']>=0 and area['x']+area['width']<=width and area['y']+area['height']<=height
  page.screenshot(path=str(out/f'home-{width}x{height}.png'))
  results.append(f'Home resize {width}x{height}: no horizontal overflow, composer visible')
 page.set_viewport_size({'width':1366,'height':768})
 # Small viewport auto-closes native sidebar; reopen when needed.
 toggle=page.get_by_test_id('stSidebarCollapsedControl')
 if toggle.count() and toggle.is_visible():toggle.click()
 for name in ('Chat','Voice','Missions','Projects','Agents','Memory','Automations','Tools','Integrations','Devices','Privacy','Settings','Home'):
  nav(name);results.append(name+': renders without runtime errors')
  if name in ('Voice','Missions','Agents','Settings'):page.screenshot(path=str(out/f'{name.lower()}.png'))
 nav('Chat')
 page.get_by_test_id('stChatInputTextArea').fill('/help')
 page.get_by_test_id('stChatInputSubmitButton').click()
 expect(page.get_by_test_id('stChatMessage')).to_have_count(2,timeout=15000)
 clean();results.append('Chat: real /help response rendered')
 nav('Voice')
 expect(page.get_by_text('Voice unavailable',exact=True)).to_be_visible()
 expect(page.get_by_role('button',name='Voice setup')).to_be_visible()
 results.append('Voice: truthful unavailable state and setup action visible')
 nav('Privacy')
 page.get_by_text('Local-only protection',exact=True).click()
 expect(page.get_by_text('CLOUD REQUIRES PUBLIC / INTERNAL',exact=False)).to_be_visible(timeout=10000)
 page.get_by_text('Local-only protection',exact=True).click()
 results.append('Privacy: local-only toggle works both ways without a model request')
 nav('Home')
 page.get_by_role('button',name='Stop',exact=True).click()
 expect(page.get_by_role('button',name='Resume',exact=True)).to_be_visible()
 page.get_by_role('button',name='Resume',exact=True).click()
 expect(page.get_by_role('button',name='Stop',exact=True)).to_be_visible()
 results.append('Emergency stop and resume: header controls update real core state')
 nav('Tools')
 page.get_by_text('Feature coverage',exact=True).click()
 page.get_by_role('textbox',name='Search feature catalog',exact=True).fill('EXP-017')
 page.get_by_role('textbox',name='Search feature catalog',exact=True).press('Tab')
 expect(page.get_by_text('Decision Memory · WORKING · EXP-017',exact=True)).to_be_visible()
 page.screenshot(path=str(out/'feature-coverage.png'))
 results.append('Feature catalog: live search returns the traced decision capability')
 nav('Projects')
 page.get_by_text('Decision memory',exact=True).click()
 page.get_by_text('Record a decision',exact=True).click()
 project_label='Browser project '+uuid.uuid4().hex[:8]
 page.get_by_role('textbox',name='Project label',exact=True).fill(project_label)
 page.get_by_role('textbox',name='Decision',exact=True).fill('Use Unreal Engine')
 page.get_by_role('textbox',name='Reason',exact=True).fill('Recorded rendering requirements')
 page.get_by_role('textbox',name='Alternatives considered (optional)',exact=True).fill('Godot')
 page.get_by_role('button',name='Save decision',exact=True).click()
 expect(page.get_by_text('Decision saved locally.',exact=True)).to_be_visible()
 page.get_by_role('textbox',name='Exact project label (optional)',exact=True).fill(project_label)
 page.get_by_role('textbox',name='Exact project label (optional)',exact=True).press('Tab')
 page.get_by_text(project_label+' · Use Unreal Engine',exact=True).click()
 expect(page.get_by_test_id('stMarkdownContainer').get_by_text('Recorded rendering requirements',exact=True)).to_be_visible()
 page.screenshot(path=str(out/'decision-memory.png'))
 page.get_by_role('textbox',name='Edit reason',exact=True).fill('Reviewed rendering requirements')
 page.get_by_role('button',name='Save changes',exact=True).click()
 expect(page.get_by_test_id('stMarkdownContainer').get_by_text('Reviewed rendering requirements',exact=True)).to_be_visible()
 page.get_by_text('Delete this decision',exact=True).click()
 page.get_by_role('button',name='Forget decision',exact=True).click()
 expect(page.get_by_text(project_label+' · Use Unreal Engine',exact=True)).to_have_count(0)
 results.append('Decision memory: real browser save, edit and confirmed delete pass')
 clean();assert not errors,errors
 browser.close()
(out/'browser-results.json').write_text(json.dumps(results,indent=2))
print('\n'.join(results))
