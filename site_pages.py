"""Generate crawlable articles and policies from the site's real configuration."""
from pathlib import Path
from html import escape, unescape
import json
import re
from urllib.parse import urlparse
from guide_content import EXTRA_GUIDES, SUPPLEMENTS

BASE = Path(__file__).parent
ROOT = BASE / 'dist'
CONFIG = json.loads((BASE / 'site-config.json').read_text())
ORIGIN = CONFIG['origin'].rstrip('/')
if urlparse(ORIGIN).scheme != 'https' or not urlparse(ORIGIN).netloc:
    raise ValueError('A real HTTPS public origin is required')
UPDATED = CONFIG['updated']
EMAIL = CONFIG.get('contactEmail')
if EMAIL and not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+', EMAIL):
    raise ValueError('Invalid contact email')
CORRECTIONS = CONFIG['correctionsUrl']
ADSENSE_ACCOUNT = CONFIG.get('adsenseAccount')
if ADSENSE_ACCOUNT and not re.fullmatch(r'ca-pub-\d{16}', ADSENSE_ACCOUNT):
    raise ValueError('Invalid AdSense account identifier')
ADSENSE_META = f'<meta name="google-adsense-account" content="{ADSENSE_ACCOUNT}">' if ADSENSE_ACCOUNT else ''
GOOGLE_SITE_VERIFICATION = CONFIG.get('googleSiteVerification')
if GOOGLE_SITE_VERIFICATION and not re.fullmatch(r'[A-Za-z0-9_-]{1,256}', GOOGLE_SITE_VERIFICATION):
    raise ValueError('Invalid Google site verification token')
SEARCH_CONSOLE_META = f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">' if GOOGLE_SITE_VERIFICATION else ''
FAVICON_LINKS = '<link rel="icon" href="/favicon.ico?v=3" sizes="16x16 32x32 48x48"><link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png?v=3"><link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png?v=3"><link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png?v=3"><meta name="theme-color" content="#b63b27">'
HEADER = '''<a class="skip-link" href="#main-content">Skip to content</a><header class="header"><a class="brand" href="/" aria-label="MenuNori home"><span class="brandmark">메</span>Menu<span>Nori</span></a><nav aria-label="Main navigation"><a href="/">Practice</a><a href="/guides/">Travel guides</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav></header>'''
FOOTER = '''<footer><a class="brand" href="/">Menu<span>Nori</span></a><p>Free ordering practice for travelers to Korea.</p><div><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/editorial/">Content policy</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div><small>© 2026 MenuNori · By Jeremy (제레미) · Fictional menus, real practice.</small></footer>'''
CONTACT = (f'<p>Email Jeremy: <a href="mailto:{escape(EMAIL, quote=True)}">{escape(EMAIL)}</a>.</p>' if EMAIL else '') + f'<p>Report a site problem or suggest a correction through <a href="{escape(CORRECTIONS, quote=True)}" target="_blank" rel="noopener">MenuNori’s public GitHub issue tracker</a>. A GitHub account is needed to submit an issue. Reports are public; do not include private information.</p>'

def plain(text):
    return unescape(re.sub('<[^>]+>', ' ', text))

def make_page(path, title, description, body, *, guide=False, kind='article'):
    canon = ORIGIN + '/' + path.strip('/') + '/'
    data = {'@context': 'https://schema.org', '@type': 'Article' if guide else 'WebPage',
            'headline': title, 'description': description, 'inLanguage': 'en', 'url': canon}
    if guide:
        data.update({'author': {'@type': 'Person', 'name': 'Jeremy', 'url': ORIGIN+'/about/'},
                     'publisher': {'@type': 'Organization', 'name': 'MenuNori', 'url': ORIGIN},
                     'datePublished': '2026-10-02', 'dateModified': UPDATED,
                     'mainEntityOfPage': canon})
    crumbs = [('MenuNori', ORIGIN+'/')]
    if guide:
        crumbs.append(('Travel guides', ORIGIN+'/guides/'))
    crumbs.append((title, canon))
    breadcrumbs = {'@context':'https://schema.org','@type':'BreadcrumbList', 'itemListElement':[
        {'@type':'ListItem','position':i+1,'name':name,'item':url} for i,(name,url) in enumerate(crumbs)]}
    trail = '<a href="/">MenuNori</a> / ' + ('<a href="/guides/">Travel guides</a> / ' if guide else '') + f'<span aria-current="page">{escape(title)}</span>'
    toc = ''
    introduction = ''
    if guide:
        # Put the direct answer before navigation, in the same HTML crawlers read.
        lead = re.search(r'<p class="lead">.*?</p>', body, flags=re.S)
        if lead:
            introduction = lead[0]
            body = body[:lead.start()] + body[lead.end():]
        headings = []
        def add_id(match):
            heading_id = f'section-{len(headings)+1}'
            headings.append((heading_id, plain(match[1]).strip()))
            return f'<h2 id="{heading_id}">{match[1]}</h2>'
        body = re.sub(r'<h2>(.*?)</h2>', add_id, body, flags=re.S)
        toc = '<nav class="article-toc" aria-label="In this guide"><strong>In this guide</strong><ol>' + ''.join(f'<li><a href="#{hid}">{escape(label)}</a></li>' for hid,label in headings) + '</ol></nav>'
        words = len(plain(introduction + body).split())
        metadata = f'<p class="updated">By <a href="/about/">Jeremy (제레미)</a> · <time datetime="{UPDATED}">October 2, 2026</time> · {max(1, round(words/200))} min read</p>'
    else:
        metadata = ''
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · MenuNori</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{canon}"><meta property="og:type" content="{'article' if guide else 'website'}"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canon}"><meta property="og:site_name" content="MenuNori">{FAVICON_LINKS}<link rel="stylesheet" href="/assets/style.css"><script type="application/ld+json">{json.dumps(data,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(breadcrumbs,ensure_ascii=False)}</script></head><body>{HEADER}<main id="main-content"><article class="{kind}"><div class="breadcrumbs">{trail}</div><p class="eyebrow">KOREAN RESTAURANT FIELD NOTES</p><h1>{escape(title)}</h1>{metadata}{introduction}{toc}{body}</article></main>{FOOTER}</body></html>'''
    destination = ROOT / path
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'index.html').write_text(doc)

def build_pages(original_guides):
    guides = [(slug,title,desc,body+SUPPLEMENTS.get(slug,'')) for slug,title,desc,body in original_guides] + EXTRA_GUIDES
    missions = {'korean-kiosk':2, 'dine-in-takeaway':1, 'read-korean-menu':3, 'spice-and-extras':2, 'check-your-order':4, 'quantity-and-prices':3, 'restaurant-ordering-phrases':1}
    for slug,title,desc,body in guides:
        # Tables use real header groups and explicit column semantics.
        body = re.sub(r'<table><tr>(.*?)</tr>', r'<table><thead><tr>\1</tr></thead><tbody>', body, flags=re.S)
        body = re.sub(r'<table>(?!<thead>)(.*?)</table>',r'<table>\1</table>',body,flags=re.S)
        body = body.replace('<th>', '<th scope="col">')
        body = re.sub(r'(<tbody>(?:(?!</tbody>).)*?)</table>',r'\1</tbody></table>',body,flags=re.S)
        body = re.sub(r'(<table>.*?</table>)', r'<div class="table-scroll" role="region" aria-label="Menu reference table" tabindex="0">\1</div>', body, flags=re.S)
        related = ''.join(f'<li><a href="/guides/{s}/">{tt}</a></li>' for s,tt,_,_ in guides if s!=slug)
        note = '<p class="article-context">Original learning examples from MenuNori’s fictional shop. Restaurant screens, recipes and prices vary. <a href="/editorial/">How we make these guides</a>.</p>'
        make_page('guides/'+slug,title,desc,note+body+f'<a class="primary practice-link" href="/?mission={missions[slug]}">Try this in the practice shop</a><aside class="related-guides"><h2>Keep learning</h2><ul>{related}</ul></aside>',guide=True)

    cards=''.join(f'<a href="/guides/{s}/"><span>0{i+1} / FIELD GUIDE</span><h2>{escape(tt)}</h2><p>{escape(d)}</p></a>' for i,(s,tt,d,b) in enumerate(guides))
    make_page('guides','How to Order Food in Korea: A Traveler’s Guide','Learn how to order food in Korea with English guides to restaurant kiosks, Korean menus, takeaway, spice levels, prices and simple ordering phrases.',f'''<p class="lead">Ordering food in Korea without speaking Korean? Start with a few menu names and the choices that change your order. These English guides explain restaurant kiosk buttons, takeaway, portions and short phrases through worked examples.</p><div class="reading-route"><h2>How to order food in Korea, step by step</h2><ol><li>Choose <a href="/guides/dine-in-takeaway/">dine-in or takeaway: 매장 vs 포장</a>.</li><li><a href="/guides/read-korean-menu/">Read the Korean menu</a> and match the complete dish name.</li><li>Set the <a href="/guides/quantity-and-prices/">quantity and check the price in won</a>.</li><li>Read <a href="/guides/spice-and-extras/">spice levels and extra options</a> before adding the dish.</li><li><a href="/guides/check-your-order/">Check your basket before paying</a>.</li></ol><p>At a screen, follow the <a href="/guides/korean-kiosk/">Korean restaurant kiosk guide</a>; at a counter, try these <a href="/guides/restaurant-ordering-phrases/">Korean restaurant ordering phrases</a>. The sequence can differ at each restaurant. If a label is unclear, use translation or ask staff for help.</p><p>Read a guide, then rehearse in our fictional shop. The game stops before any real payment.</p></div><img class="food-photo" src="/assets/bunsik-warm.jpg" alt="Illustrative gimbap, rice cakes, noodles, fish cake soup and dumplings from the fictional MenuNori shop" width="1200" height="800"><p class="photo-caption">AI-created illustration of our practice menu; not a real restaurant photograph.</p><div class="guide-cards">{cards}</div><a class="primary practice-link" href="/">Open the practice menu</a>''',kind='guide-index')

    make_page('about','About MenuNori & Jeremy','Meet the operator and understand what MenuNori’s Korean restaurant practice can teach.',f'''<p class="lead">MenuNori is an independent project by Jeremy (제레미), made for English-speaking travelers who want to feel less lost when looking at a Korean restaurant menu.</p><h2>A small problem worth practicing</h2><p>You may know what you want to eat and still hesitate at the screen: which button means takeaway, whether cheese is included, or how many portions are in your basket. MenuNori focuses on those decisions. A translation app remains useful at the actual restaurant; this site gives you a place to rehearse before you go.</p><h2>Two ways to use the site</h2><p>The <a href="/">practice shop</a> has six dishes and five short missions. Choose the order type, quantities and options, then check a simulated receipt. The <a href="/guides/">travel guides</a> explain the same decisions with Korean labels, worked examples and short phrases. All guides can be read without JavaScript or an account.</p><h2>What is invented, and what is real?</h2><p>The restaurant, its prices, recipe descriptions and ordering screen are fictional. The food artwork was generated with AI for this project; it is not a photograph of an actual business. Korean dish names and ordering words are learning examples. The site does not list real restaurants, process payments or send orders to a shop.</p><h2>Who writes the content?</h2><p>Jeremy operates and publishes MenuNori. AI assists with drafting and artwork. The menu, missions and explanations are fixed published content, rather than live AI conversations. We do not claim a language-teaching qualification, a restaurant affiliation or completed independent native-speaker review.</p><p>Our <a href="/editorial/">content policy</a> explains how fictional examples, external references and corrections are handled. Please report unclear translations or errors so they can be checked.</p><h2>How the project is funded</h2><p>MenuNori is currently free and self-funded. There are no advertising or analytics scripts in this version. Advertising may support the explanatory guides later; that will be disclosed before ads run. We do not sell restaurant bookings or accept real payments.</p><h2>Contact the operator</h2>{CONTACT}<p><a href="/contact/">Contact and correction details</a></p>''')

    make_page('contact','Contact & corrections','Contact Jeremy about MenuNori or report a translation, menu example or site problem.',f'''<p class="lead">MenuNori is operated by Jeremy (제레미). Questions about the project, unclear wording and reports of site problems are welcome.</p><h2>Get in touch</h2>{CONTACT}<h2>Help us check a correction</h2><p>Include the page URL, the Korean word or English explanation you are asking about, and what seems wrong. For a game issue, include the mission number and your menu choices. A screenshot of the practice screen can help; remove any personal information first.</p><h2>What we can help with</h2><p>We can review MenuNori content and software issues. We cannot change a real restaurant order, give an allergy guarantee, arrange a refund or provide restaurant customer support. Contact the actual restaurant for those questions.</p><h2>Privacy when you contact us</h2><p>Messages may include your name, reply address and the details you choose to provide. Those details are used to respond and investigate the report. Public issue reports remain visible through GitHub. Read the <a href="/privacy/">privacy notice</a> before sharing information.</p>''')

    make_page('editorial','How our guides are made','MenuNori’s approach to original content, sources, fictional examples, AI assistance and corrections.',f'''<p class="updated">Published October 2, 2026 · Operator: Jeremy (제레미)</p><p class="lead">Our guides explain a specific decision at a Korean restaurant. We aim to show what to read, why it matters and how to check your choice.</p><h2>Original examples, a clearly fictional shop</h2><p>MenuNori’s walkthroughs, practice slips and missions are written around its own fixed menu. We do not copy restaurant menus, photographs or logos. Prices, recipe configurations and the shop’s ordering flow are invented, and are labelled as examples rather than current restaurant information.</p><h2>References and their limits</h2><p>We link to the Korea Tourism Organization for general dining and food context. These references support the topic they describe; they do not verify MenuNori’s prices, every Korean phrase or our game. We paraphrase briefly rather than reproduce source articles.</p><ul><li><a href="https://english.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=903&amp;vcontsId=229195" target="_blank" rel="noopener">VISITKOREA: About Korean Food</a> — background on restaurant service and ordering.</li><li><a href="https://english.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=205&amp;vcontsId=140730" target="_blank" rel="noopener">VISITKOREA: Bunsik & Street Food</a> — background on the food category used in our fictional shop.</li></ul><h2>AI assistance and language review</h2><p>AI assists with initial drafts and illustrative food artwork. Content is saved as fixed pages and examples; this site does not generate personalized travel or language advice at runtime. Independent native-speaker review is not yet completed, and no completed professional review is implied. We do not score pronunciation or promise that a particular restaurant uses these exact labels.</p><h2>Changes and correction reports</h2><p>Guide dates identify the published version. When content changes materially, the date and relevant explanation are updated. Typographical fixes do not create a claim of a new independent review. Reports are checked against the page and practice behavior before a correction is published.</p><p><a href="/contact/">Send a correction or report a problem</a>. Include the exact wording and page so we can check the intended meaning.</p><h2>Advertising is separate from instruction</h2><p>No ads run in this version. If advertising is added, it will be clearly identified and kept away from order controls and simulated checkout. Paid promotion will be disclosed. Advertising will not change the game’s scoring or turn clicking an ad into part of a mission.</p>''')

    make_page('privacy','Privacy & your practice data','Learn what MenuNori stores locally, what Vercel and font requests process, and how to clear your progress.',f'''<p class="updated">Effective October 2, 2026 · Operator: Jeremy (제레미)</p><p class="lead">MenuNori does not require an account or collect real orders, card details, voice recordings or location permissions.</p><h2>Practice progress in your browser</h2><p>The game uses localStorage under <code>menunori-completed</code> for the completed mission numbers. It stays in your browser profile until cleared. The basket is held in page memory and is discarded when the page reloads. MenuNori does not send your basket or mission results to its own database. Other people using the same browser profile may see the saved progress.</p><h2>Clear your saved progress</h2><p><button class="secondary" id="clear-data">Clear MenuNori practice data</button></p><p id="clear-status" role="status" aria-live="polite">This clears only MenuNori’s practice progress and any old MenuNori language preference in this browser. You can also use your browser’s site-data settings.</p><script>document.getElementById('clear-data').onclick=()=>{{try{{localStorage.removeItem('menunori-language');localStorage.removeItem('menunori-completed');document.getElementById('clear-status').textContent='Your MenuNori practice progress has been cleared.'}}catch{{document.getElementById('clear-status').textContent='Browser storage is unavailable. Use your browser settings to clear site data.'}}}};</script><h2>Hosting and technical requests</h2><p>The public site is hosted by Vercel. Delivering a page involves technical data such as an IP address, requested URL, browser information and request time. Vercel may process and retain service and security logs under its own practices; MenuNori does not promise that infrastructure logs are absent. See <a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener">Vercel’s privacy policy</a>.</p><p>The stylesheet requests fonts from Google Fonts. Your browser contacts Google’s font service and may transmit technical request information, including an IP address. See <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google’s privacy policy</a>. MenuNori does not use these requests to build a personal profile.</p><h2>Messages and public correction reports</h2><p>If you contact the operator, the information you provide is used to reply and investigate the question. Do not send passwords, payment details, identity documents or medical records. GitHub issues are public and are subject to <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub’s privacy practices</a>. We do not operate a hidden contact form or collect form data on this site.</p><h2>Advertising and cookies</h2><p>This version loads no Google AdSense ads and no analytics scripts. MenuNori does not set advertising cookies. Its practice localStorage is separate from advertising tracking.</p><p>If ads are introduced, this notice will be revised before activation to identify the actual providers and choices. Google and other advertising partners may then use cookies, web beacons, IP addresses or other identifiers to serve and measure advertising. Learn <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from partner sites</a>. Where required, a suitable consent mechanism will be configured before advertising runs; none is represented as active today.</p><h2>Your choices and contact</h2><p>You can clear local progress, block browser storage, or stop using the site. Guides remain readable without saving progress. External links have their own privacy practices. For a question about this notice or information you sent to the operator, use our <a href="/contact/">contact page</a>.</p>{CONTACT}''')

    make_page('terms','Terms of use','Conditions for using MenuNori’s fictional Korean restaurant practice and original guides.','''<p class="updated">Effective October 2, 2026 · Operator: Jeremy (제레미)</p><p class="lead">MenuNori is a free educational simulation. Adding food to a basket or confirming an order creates no real order and no payment obligation.</p><h2>The practice menu</h2><p>The shop, prices, recipes and order configurations are invented. Food pictures are AI-created illustrations. Real restaurants may use different labels, ingredients, portion sizes, charges and service arrangements. Check the current restaurant menu and final total when ordering real food.</p><h2>Limits of the guidance</h2><p>Use the examples to learn ordering decisions, alongside translation tools and staff assistance when needed. The site does not provide professional language instruction, ingredient verification, allergy guarantees or real restaurant booking services. Independent native-speaker review is not claimed.</p><h2>Original content and outside sources</h2><p>The interface, explanations and practice examples are MenuNori project content. References belong to their publishers. You may link to guides and use the exercises for personal learning. Do not represent copied content or the fictional shop as your own real restaurant. For other reuse requests, <a href="/contact/">contact the operator</a>.</p><h2>Browser data and availability</h2><p>Practice progress is local to the browser. It can be cleared or lost, and is not an account-based record. See our <a href="/privacy/">privacy notice</a>. We may change or correct the content and interface, and do not promise uninterrupted access.</p><h2>Corrections and questions</h2><p>Jeremy (제레미) operates MenuNori. Use the <a href="/contact/">contact and corrections page</a> for a question about these terms, content reuse or a site problem. Our <a href="/editorial/">content policy</a> explains how published examples and changes are handled.</p>''')

    (ROOT/'404.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found · MenuNori</title>{FAVICON_LINKS}<link rel="stylesheet" href="/assets/style.css"></head><body>{HEADER}<main id="main-content"><article class="article"><h1>This page isn’t on the menu.</h1><p>The link may have changed. Return to the practice shop or <a href="/guides/">browse the travel guides</a>.</p><a class="primary practice-link" href="/">Back to the menu</a></article></main>{FOOTER}</body></html>''')
    routes = ['/','/guides/','/about/','/contact/','/editorial/','/privacy/','/terms/'] + ['/guides/'+s+'/' for s,_,_,_ in guides]
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{p}</loc><lastmod>{UPDATED}</lastmod></url>' for p in routes)+'</urlset>')
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
    index=ROOT/'index.html'
    home=index.read_text()
    home=re.sub(r'<link rel="canonical" href="[^"]+">',f'<link rel="canonical" href="{ORIGIN}/">',home)
    home=re.sub(r'<meta property="og:url" content="[^"]+">',f'<meta property="og:url" content="{ORIGIN}/">',home)
    def home_schema(match):
        data=json.loads(match[1])
        if data.get('@type')=='WebSite':
            data['url']=ORIGIN+'/'
            data['publisher']['url']=ORIGIN+'/about/'
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
    home=re.sub(r'<script type="application/ld\+json">(.*?)</script>',home_schema,home,flags=re.S)
    home=home.replace('read all five travel guides','read our travel guides')
    home=re.sub(r'<footer>.*?</footer>',FOOTER,home,flags=re.S)
    if 'Skip to content' not in home:
        home=home.replace('<body>','<body><a class="skip-link" href="#main-content">Skip to content</a>')
    home=home.replace('<main>','<main id="main-content">')
    if 'href="/contact/"' not in home.split('</header>')[0]:
        home=home.replace('</nav></header>','<a href="/contact/">Contact</a></nav></header>',1)
    if 'id="home-learning"' not in home:
        learning='''<section class="home-learning" id="home-learning" aria-labelledby="learning-title"><div><p class="eyebrow">WHAT YOU’RE PRACTICING</p><h2 id="learning-title">Five orders. Five useful habits.</h2><p>Start with the first mission or choose a situation you want to rehearse. Your receipt is the place to check your work.</p></div><ol><li><strong>Takeaway:</strong> one gimbap and one dumpling portion. Notice <span lang="ko">포장</span> before confirming.</li><li><strong>Mild + cheese:</strong> open the options on tteokbokki. Read the difference between an extra and a separate dish.</li><li><strong>For two:</strong> two noodle portions and one dumpling portion. Check the quantities and the ₩12,000 ceiling.</li><li><strong>Fix the basket:</strong> remove the wrong item. Adding the correct food does not remove a mistake.</li><li><strong>On your own:</strong> choose two non-spicy dishes without extras and finish under ₩9,000.</li></ol><p class="learning-link"><a href="/guides/quantity-and-prices/">Read portions and prices</a><a href="/guides/restaurant-ordering-phrases/">Try a short ordering phrase</a></p></section><section class="home-faq" aria-labelledby="faq-title"><h2 id="faq-title">Before you practice</h2><details><summary>Will this place a real order?</summary><p>No. The menu and restaurant are fictional, and the confirmation makes no payment. No card details are requested.</p></details><details><summary>Do I need to know Korean first?</summary><p>No. Instructions are in English, with Korean where you would see it on a menu. Use the guides to learn a few useful words as you go.</p></details><details><summary>Can I use these prices and recipes on my trip?</summary><p>Use the current restaurant menu for actual prices and ingredients. Our examples teach a decision process, and mild does not mean spice-free or allergen-free.</p></details><details><summary>What if I make a mistake?</summary><p>Review the feedback and keep editing your order. You can retry any mission. Only completed mission numbers are saved in this browser; <a href="/privacy/">clear them here</a>.</p></details></section>'''
        home=home.replace('</main>',learning+'</main>',1)
    home=re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>','',home)
    home=re.sub(r'<meta name="theme-color"[^>]*>','',home)
    home=re.sub(r'<meta name="google-adsense-account"[^>]*>','',home)
    home=re.sub(r'<meta name="google-site-verification"[^>]*>','',home)
    home=home.replace('</head>',FAVICON_LINKS+ADSENSE_META+SEARCH_CONSOLE_META+'</head>',1)
    index.write_text(home)
    # Apply the same icon set to every generated route, including the error page.
    for path in ROOT.rglob('*.html'):
        if path==index:
            continue
        doc=path.read_text()
        doc=re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>','',doc)
        doc=re.sub(r'<meta name="theme-color"[^>]*>','',doc)
        doc=re.sub(r'<meta name="google-adsense-account"[^>]*>','',doc)
        doc=re.sub(r'<meta name="google-site-verification"[^>]*>','',doc)
        path.write_text(doc.replace('</head>',FAVICON_LINKS+ADSENSE_META+SEARCH_CONSOLE_META+'</head>',1))
    print(f'Generated {len(guides)} guides and {len(routes)} public routes for {ORIGIN}')
