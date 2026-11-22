"""Rebuild the GitHub Pages site from the repository root with python3 -B _source/build.py. Browser assets live in site-assets/."""
from hashlib import sha256
from html import escape
from urllib.parse import urlencode
from pathlib import Path
import json

from page_content import ALL_FAQS, CITIES, HOME_FAQS, SERVICES, YARD_CARE

OUT = Path(__file__).resolve().parents[1]
DOMAIN = "https://lostlegendsrecovery.com"
NAME = "Lost Legends Metal Detection & Recovery"
PHONE = "(402) 309-6379"
PHONE_E164 = "+14023096379"
TEL = "tel:" + PHONE_E164
SMS = "sms:" + PHONE_E164
TEXT_CHECKLIST = "For the fastest reply, text the item, an address or GPS pin, and a photo of the search area."
EMAIL = "LostLegendsRecovery@gmail.com"
PROFILE = "https://theringfinders.com/Alex.Kaffenberger/"
JOURNAL = "https://theringfinders.com/blog/Alex.Kaffenberger/"
FORM = "https://formspree.io/f/xvzbrqkw"
CARTIER_SOCIAL = "https://static.theringfinders.com/wp-content/uploads/2026/04/20260414_cd65d_09cd6-e1776140644279.jpeg"
HOME_SOCIAL = DOMAIN + "/site-assets/alex-field-social.jpg"
KEYS_SOCIAL = "https://static.theringfinders.com/wp-content/uploads/2026/04/20260411_78817_0490c-scaled.jpeg"


def icon(name):
    return f'<svg class="icon" aria-hidden="true" focusable="false"><use href="/site-assets/icons.svg#{name}"></use></svg>'


def brand():
    return '''<a class="brand" href="/" aria-label="Lost Legends home">
      <img src="/site-assets/lost-legends-seal.webp" width="53" height="53" alt="">
      <span class="brand-type"><strong>Lost Legends</strong><small>Metal Detection &amp; Recovery</small></span>
    </a>'''


NAV = [("services", "Services"), ("recoveries", "Recoveries"), ("area", "Service area"), ("/about/", "About Alex")]


def navigation(home):
    prefix = "" if home else "/"
    links = "".join(
        f'<a href="{anchor if anchor.startswith("/") else prefix + "#" + anchor}">{label}</a>'
        for anchor, label in NAV
    )
    return f'''<header class="site-header" id="top">
      <div class="wrap header-inner">
        {brand()}
        <nav class="desktop-nav" aria-label="Main navigation">{links}</nav>
        <div class="header-actions">
          <a class="header-phone header-sms" href="{SMS}" aria-describedby="sms-help" title="{TEXT_CHECKLIST}">{icon("chat")}<span>Text Alex</span></a>
          <details class="mobile-menu"><summary aria-label="Site navigation">{icon("menu")}{icon("close")}</summary>
            <nav aria-label="Mobile navigation">{links}<a class="menu-request" href="{prefix}#request">Request a search</a></nav>
          </details>
        </div>
      </div>
    </header>'''


def footer(home):
    prefix = "" if home else "/"
    return f'''<footer class="site-footer"><div class="wrap footer-inner">
      {brand()}<nav aria-label="Footer navigation"><a href="/faq/">FAQ</a><a href="{prefix}#request">Contact</a><a href="{PROFILE}">The Ring Finders</a></nav>
      <small>© 2026 Lost Legends</small>
    </div></footer>'''


def label(text):
    return f'<p class="section-label">{text}</p>'


def asset_url(name):
    version = sha256((OUT / "site-assets" / name).read_bytes()).hexdigest()[:10]
    return f"/site-assets/{name}?v={version}"


def price_label(service):
    if "rate" in service:
        return f"${service['rate']} per {service['unit']}"
    return service["price"]


def service_offer(service):
    url = f"{DOMAIN}/{service['slug']}/"
    offer = {
        "@type": "Offer", "@id": url + "#offer", "url": url,
        "name": f"{service['name']} ({price_label(service)})",
        "description": service["summary"],
        "itemOffered": {
            "@type": "Service", "@id": url + "#service",
            "name": service["name"], "url": url,
            "provider": {"@id": DOMAIN + "/#business"},
        },
    }
    if "rate" in service:
        offer["priceSpecification"] = {
            "@type": "UnitPriceSpecification", "price": service["rate"],
            "priceCurrency": "USD", "unitText": service["unit"],
        }
    return offer


def shell(title, desc, body, path="/", og_image=HOME_SOCIAL, faqs=(), article=False, index=True, service=None):
    canonical = DOMAIN + path
    title = escape(title, quote=True)
    desc = escape(desc, quote=True)
    structured = {
        "@type": "LocalBusiness", "@id": DOMAIN + "/#business", "name": NAME, "url": DOMAIN + "/",
        "description": "Lost ring and jewelry recovery, existing property marker locating, and junk metal cleanup. Based in Plattsmouth and serving the Omaha metro, southeast Nebraska, and southwest Iowa. Farther travel is by arrangement.",
        "telephone": PHONE_E164, "email": EMAIL, "image": HOME_SOCIAL, "logo": DOMAIN + "/site-assets/lost-legends-seal.webp",
        "address": {
            "@type": "PostalAddress", "addressLocality": "Plattsmouth", "addressRegion": "NE",
            "postalCode": "68048", "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "name": "Plattsmouth, Nebraska", "latitude": 41.0117, "longitude": -95.8828},
        "areaServed": [
            {"@type": "Place", "name": "Omaha metro"},
            {"@type": "City", "name": "Plattsmouth, Nebraska"},
            {"@type": "City", "name": "Omaha, Nebraska"},
            {"@type": "City", "name": "Bellevue, Nebraska"},
            {"@type": "City", "name": "Papillion, Nebraska"},
            {"@type": "City", "name": "Gretna, Nebraska"},
            {"@type": "City", "name": "Council Bluffs, Iowa"},
            {"@type": "AdministrativeArea", "name": "Cass County, Nebraska"},
            {"@type": "City", "name": "Nebraska City, Nebraska"},
        ],
        "priceRange": "$",
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "telephone": PHONE_E164},
        "hasOfferCatalog": {"@id": DOMAIN + "/#service-catalog"},
        "founder": {"@type": "Person", "name": "Alex Kaffenberger"}, "sameAs": [PROFILE],
    }
    if path == "/":
        structured["hasOfferCatalog"].update({
            "@type": "OfferCatalog", "name": "Metal Detection & Recovery Services",
            "itemListElement": [service_offer(item) for item in SERVICES],
        })
    graph = [structured]
    if faqs:
        graph.append({"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in faqs
        ]})
    if service:
        graph.append({"@type": "Service", "@id": canonical + "#service", "name": service["name"], "url": canonical,
                      "description": service["summary"], "provider": {"@id": structured["@id"]},
                      "areaServed": structured["areaServed"], "offers": service_offer(service)})
    robots = "index,follow" if index else "noindex,follow"
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="{robots}">
<meta name="author" content="{escape(NAME)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#f9f6ed"><meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:site_name" content="{escape(NAME)}"><meta property="og:locale" content="en_US"><meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/site-assets/favicon.png" type="image/png">
<link rel="preload" href="/site-assets/fonts/dm-serif-text.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset_url('styles.css')}"><script defer src="{asset_url('site.js')}"></script>
<script type="application/ld+json">{schema}</script>
</head><body><a class="skip" href="#main">Skip to content</a>{navigation(path == "/")}
<main id="main">{body}</main>{footer(path == "/")}</body></html>
'''


stories = [
    {"slug": "cartier-ring-roadside", "category": "Jewelry recovery", "icon": "ring", "place": "Omaha–Council Bluffs area",
     "title": "A Cartier ring on the roadside", "photo": "cartier-in-hand", "alt": "The three interlocking gold bands of the recovered Cartier ring in Alex’s hand.",
     "teaser": "She lost it helping a stranded driver in a snowstorm. On my third trip back, I found it an inch under the grass.",
     "when": "April 13, 2026", "iso": "2026-04-13", "social": CARTIER_SOCIAL, "source": JOURNAL+"2026/04/18k-cartier-trinity-ring-recovered-roadside-miracle-council-bluffs-ia/",
     "intro": "An EMS worker called after losing the 18k Cartier Trinity ring she’d worn for more than a decade.",
     "body": ["She’d stopped to help a stranded driver during a snowstorm. When she shook the snow from her hands, the ring came off along the shoulder of I-29.",
              "The grass was thick, and pieces of aluminum were scattered through it. I worked the area with my Nokta Legend, listening to one signal at a time. Two searches came up empty.",
              "I went back after a heavy rain. About half an hour into that third search, I heard a signal I could repeat from another angle. An inch down in the mud were all three bands, still linked together. I got to put that ring back in her hands."],
     "caption": "The Cartier Trinity ring, just as it looked when I found it.", "second": ("cartier-bands", "The recovered Cartier Trinity ring in three colors of gold.", "A closer look at the interlocking bands after recovery.")},
    {"slug": "omaha-keys", "category": "Key recovery", "icon": "key", "place": "Omaha, Nebraska",
     "title": "Keys beneath the fresh mulch", "photo": "keys-returned", "alt": "The Omaha client holding up the keys Alex recovered after a pipe installation.",
     "teaser": "A pipe installation, freshly spread mulch, and a set of keys that took 45 minutes of careful searching to bring back.",
     "when": "April 10, 2026", "iso": "2026-04-10", "social": KEYS_SOCIAL, "source": JOURNAL+"2026/04/lost-keys-recovered-omaha-ne/",
     "intro": "A set of keys went missing during a pipe installation in Omaha. By lunchtime, the owner had a freshly mulched work area to search.",
     "body": ["When he called me, he’d already spent more than two hours looking. We narrowed the most likely stretch to about twenty feet.",
              "The keys and the other metal on the keyring produced a choppy signal under the mulch. I slowed down and checked the uneven sounds as well as the clear ones.",
              "About 45 minutes later, I pulled out the missing keys. The owner could finally put them back in his pocket and get on with his day."],
     "caption": "The owner with his keys after the search in Omaha.", "second": None},
    {"slug": "wedding-band-in-snow", "category": "Snow recovery", "place": "Omaha area",
     "title": "A wedding band lost in the snow", "photo": "winter-wedding-band",
     "alt": "The wedding ring set reunited after the snow search, in a photo supplied with the testimonial.",
     "teaser": "A family’s wedding band disappeared into the snow. The search brought the set back together.",
     "social": DOMAIN + "/site-assets/winter-wedding-band.webp",
     "source": PROFILE + "#:~:text=He%20was%20able%20to%20find%20our%20ring",
     "intro": "A family got in touch after a Celtic wedding band disappeared in the snow. Finding it meant putting their wedding set back together.",
     "body": ["I went out to search the area where they remembered losing it. The snow had hidden the band from view. It took less than an hour to bring it back.",
              "The family shared the photo with their testimonial after the search. Their words sum up what the recovery meant to them: “He was able to find our ring and reunite the set!”"],
     "caption": "The reunited set, photographed by the family.", "second": None},
]


def story_card(s):
    return f'''<a class="story-card {s["slug"]}" aria-labelledby="card-{s["slug"]}" href="/recoveries/{s["slug"]}/">
      <div class="card-image"><img src="/site-assets/{s["photo"]}.webp" loading="lazy" alt="{s["alt"]}">
        <span class="photo-location">{icon("pin")}{s["place"]}</span></div>
      <div class="card-copy"><p class="story-type">{s["category"]}</p><h3 id="card-{s["slug"]}">{s["title"]}</h3>
      <p>{s["teaser"]}</p><span class="card-link">Read the story</span></div>
    </a>'''


def service_card(service):
    return f'''<article class="service-card">
      <div class="service-top"><span class="service-icon">{icon(service["icon"])}</span><span class="service-price">{price_label(service)}</span></div>
      <h3><a href="/{service["slug"]}/">{service["name"]}</a></h3>
      <p>{service["summary"]}</p><a class="service-link" href="/{service["slug"]}/" aria-label="About {service["name"].lower()}">View service</a>
    </article>'''


def faq(question, answer):
    return f'<details class="faq-item"><summary>{question}<span class="plus" aria-hidden="true"></span></summary><p>{answer}</p></details>'


def search_actions(request_href, *, on_dark=False):
    sms_style, request_style = ("button-gold", "button-glass") if on_dark else ("button-green", "button-light-outline")
    return f'''<div class="hero-actions">
      <a class="button {sms_style}" href="{SMS}" aria-describedby="sms-help">{icon("chat")}Text Alex</a>
      <a class="button {request_style}" href="{request_href}">Request a search</a>
    </div><small id="sms-help" class="sms-help">{TEXT_CHECKLIST}</small>'''


def home_content():
    cards = "".join(story_card(s) for s in stories)
    return f'''
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-image"><img src="/site-assets/alex-field-720.webp"
    srcset="/site-assets/alex-field-720.webp 720w, /site-assets/alex-field-1200.webp 1200w"
    sizes="(max-width: 700px) 100vw, 56vw" width="720" height="962" fetchpriority="high"
    alt="Alex sweeping a field with his metal detector in an orange high-visibility vest."></div>
  <div class="wrap hero-inner"><div class="hero-copy">
    {label("Reward-based metal detecting")}
    <h1 id="hero-title">Lost a ring in Nebraska or Iowa? <em>Let's find it.</em></h1>
    <p class="hero-intro">I’m Alex Kaffenberger from Plattsmouth, Nebraska. I search yards, fields, snow, and shallow water for lost rings, keys, and keepsakes.</p>
    {search_actions("#request", on_dark=True)}
  </div></div>
</section>
<div class="credentials" id="experience-title"><div class="wrap credentials-inner">
  <a class="credential" href="/plattsmouth/">{icon("pin")}<span>Plattsmouth-based</span></a>
  <a class="credential" href="/lost-ring-recovery/">{icon("hand")}<span>Reward-based recovery</span></a>
  <a class="credential membership" href="{PROFILE}" aria-label="View Alex’s listing on The Ring Finders">
    <img src="/site-assets/ring-finders.webp" width="48" height="48" alt=""><span>The Ring Finders member</span>
  </a>
</div></div>
<section class="services section-pad" id="services" aria-labelledby="services-title"><div class="wrap">
  <div class="section-heading"><div>{label("Field services")}<h2 id="services-title">Services &amp; pricing</h2></div>
    <p class="service-heading-copy">I confirm any travel fee before heading out.</p></div>
  <div class="service-list">{"".join(service_card(service) for service in SERVICES)}</div>
</div></section>
<section class="journal section-pad" id="recoveries" aria-labelledby="recoveries-title"><div class="wrap" id="work">
  <div class="section-heading"><div>{label("From the field")}<h2 id="recoveries-title">Recovery stories</h2></div>
    <a class="text-link journal-source" href="{JOURNAL}">{icon("book")}The Ring Finders journal</a></div>
  <div class="stories-grid">{cards}</div>
</div></section>
<section class="area section-pad" id="area" aria-labelledby="area-title"><div class="wrap area-layout">
  <div class="area-copy">{label("Service area")}<h2 id="area-title">Local to Plattsmouth.<br><em>Both sides of the river.</em></h2>
    <p>My core service area is the Omaha metro, Council Bluffs, Cass County, and Nebraska City.</p>
    <p>Farther out in Nebraska or Iowa? Text me what you lost, an address or GPS pin, and a photo of the area. We’ll agree on timing and any travel fee before I make the trip.</p>
    <a href="{SMS}" class="button button-paper">{icon("chat")}Text me a map pin</a>
  </div>
  <div><figure class="region-map"><img loading="lazy" src="/site-assets/service-area.webp" width="1120" height="650" alt="Map of the Omaha and Council Bluffs area with Lost Legends based in Plattsmouth, Nebraska, near the Missouri River."></figure>
    {city_links()}</div>
</div></section>
<section class="about section-pad" id="about" aria-labelledby="about-title"><div class="wrap about-layout">
  <figure class="portrait"><img src="/site-assets/alex.webp" width="750" height="795" loading="lazy" alt="Alex Kaffenberger, founder of Lost Legends."></figure>
  <div class="about-copy">{label("Behind the detector")}<h2 id="about-title">Hi, I’m Alex.</h2>
    <p>I’m a dad from Plattsmouth with a love of local history and old maps. Metal detecting started as a way to explore that history. Getting to hand someone their wedding ring back gave me a reason to keep at it.</p>
    <p>I know how local soil and buried scrap affect what I hear through the detector. I pinpoint each signal before digging, refill the hole neatly, and put the turf back when I can. I ask before sharing a customer’s photos or location.</p>
    <a class="text-link" href="/about/">{icon("compass")}More about Alex</a>
  </div>
  <aside class="client-quote"><span class="quote-mark" aria-hidden="true">“</span><blockquote>He was able to find our ring and reunite the set!</blockquote><p>From a family whose wedding band was lost in the snow.</p><a class="text-link" href="{PROFILE}#:~:text=He%20was%20able%20to%20find%20our%20ring">Read the testimonial</a></aside>
</div></section>
<section class="faq-section section-pad" id="faq" aria-labelledby="faq-title"><div class="wrap faq-layout"><div>{label("Before the search")}<h2 id="faq-title">Common questions</h2></div>
  <div class="faq-list">{"".join(faq(*pair) for pair in HOME_FAQS)}
    <a class="text-link faq-more" href="/faq/">See all questions</a>
  </div>
</div></section>
<section class="request section-pad" id="request" aria-labelledby="request-title"><div class="wrap request-layout" id="quote">
  <div class="request-intro">{label("Contact Alex")}<h2 id="request-title">Request a search</h2>
    <p>Tell me what you’re looking for and the nearest town. I’ll get back to you about the search, timing, and any travel fee.</p>
  </div>
  <aside class="direct-contact"><h3>Talk to me directly</h3>
    <a class="direct-number" href="{TEL}">{PHONE}</a>
    <p>For the fastest reply, text me these three things.</p>
    <ul class="contact-checklist" id="contact-checklist"><li>The item you’re looking for</li><li>An address or GPS pin</li><li>A photo of the search area</li></ul>
    <div class="contact-options"><a class="button button-paper" href="{SMS}" aria-describedby="contact-checklist">{icon("chat")}Text Alex</a><a class="text-link" href="https://wa.me/14023096379">WhatsApp</a><a class="text-link" href="mailto:{EMAIL}">Email</a></div>
  </aside>
  <div class="form-panel"><form id="request-form" action="{FORM}" method="post" accept-charset="UTF-8">
    <input type="hidden" name="_next" value="{DOMAIN}/thank-you.html">
    <div class="form-grid"><div class="form-field"><label id="quote-name" for="request-name">Your name <span>*</span></label><input id="request-name" name="name" type="text" autocomplete="name" maxlength="120" required></div>
    <div class="form-field"><label id="quote-phone" for="request-phone">Phone number <span>*</span></label><input id="request-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" minlength="7" maxlength="32" required></div>
    <div class="form-field"><label for="request-service">Service</label><div class="select-wrap"><select id="request-service" name="service"><option>Lost item recovery</option><option>Marker or cover</option><option>Metal cleanup</option><option>Other inquiry</option></select>{icon("chev")}</div></div>
    <div class="form-field"><label id="quote-location" for="request-location">Nearest town or landmark <span>*</span></label><input id="request-location" name="location" type="text" maxlength="240" required></div>
    <div class="form-field full"><label id="quote-item" for="request-item">What should I look for?</label><input id="request-item" type="text" name="item" maxlength="240" placeholder="A gold wedding band, a set of keys…"></div></div>
    <details class="form-extra"><summary>Add timing or search details <span>(optional)</span>{icon("chev")}</summary>
      <div class="form-field"><label id="quote-when" for="request-when">When did it happen?</label><input id="request-when" name="when" type="text" maxlength="160" placeholder="Saturday afternoon, about two weeks ago…"></div>
      <div class="form-field"><label id="quote-message" for="request-details">Anything else I should know?</label><textarea id="request-details" name="message" rows="3" maxlength="3500" placeholder="Where you last had it, what you’ve already searched…"></textarea></div>
    </details>
    <div class="form-submit"><button type="submit" class="button button-green">{icon("chat")}<span>Send request</span></button><small>* Required fields</small></div>
    <p class="form-note" id="quote-privacy">Your request goes to Alex through Formspree.</p>
  </form><div class="form-status" aria-live="polite" aria-atomic="true" tabindex="-1"></div><a class="error-sms text-link" href="{SMS}" hidden>Text Alex instead</a></div>
</div></section>
'''


def story_page(story, other):
    photo = story["second"]
    extra = "" if not photo else f'<figure class="extra-photo"><img src="/site-assets/{photo[0]}.webp" loading="lazy" alt="{photo[1]}"><figcaption>{photo[2]}</figcaption></figure>'
    paragraphs = "".join(f"<p>{p}</p>" for p in story["body"])
    published = ""
    if "iso" in story:
        published = f'<span>{icon("book")}Published <time datetime="{story["iso"]}">{story["when"]}</time></span>'
    source_title = "Original field report" if "iso" in story else "Read the family’s testimonial"
    return f'''<article class="field-note wrap">
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/#recoveries">Recovery stories</a></nav>
      <div class="note-grid"><header class="note-head">{label(story["category"])}<h1>{story["title"]}</h1>
      <p class="note-deck">{story["intro"]}</p>
      <div class="note-meta"><span>{icon("pin")}{story["place"]}</span>{published}</div>
      <div class="note-byline"><img src="/site-assets/alex.webp" alt="" width="42" height="42">By Alex Kaffenberger</div></header>
      <figure class="note-photo {story["slug"]}"><img src="/site-assets/{story["photo"]}.webp" alt="{story["alt"]}" fetchpriority="high"><figcaption>{story["caption"]}</figcaption></figure>
      </div>
      <div class="note-reading">{paragraphs}{extra}<a class="text-link" href="{story["source"]}">{icon("book")}{source_title} on The Ring Finders</a></div>
    </article><section class="note-next"><div class="wrap note-next-inner"><div>{label("Another recovery")}<a class="next-story" href="/recoveries/{other["slug"]}/">{other["title"]}</a></div>
      <div>{search_actions("/#request")}</div></div></section>'''


def city_links():
    links = []
    for core, heading in [(True, "Core service area"), (False, "Farther out, ask me")]:
        towns = "".join(
            f'<li><a href="/{city["slug"]}/">{city["name"]}</a></li>'
            for city in CITIES if city["core"] == core
        )
        links.append(f'<div><h3>{heading}</h3><ul>{towns}</ul></div>')
    return f'<nav class="city-links" aria-label="Service area by city">{"".join(links)}</nav>'


def breadcrumbs(anchor, name):
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#{anchor}">{name}</a></nav>'


def subpage_header(crumbs, eyebrow, title, lead, picture=None, request_href="/#request"):
    photo = ""
    if picture:
        photo = f'<figure class="subpage-photo"><img src="/site-assets/{picture[0]}.webp" alt="{picture[1]}"></figure>'
    return f'''<header class="subpage-head"><div class="wrap">
      {crumbs}<div class="subpage-lead{" with-photo" if photo else ""}">
        <div>{label(eyebrow)}<h1>{title}</h1><p>{lead}</p>
          {search_actions(request_href)}
        </div>{photo}
      </div>
    </div></header>'''


def subpage_contact(title="Ready to plan a search?", href="/#request"):
    return f'''<aside class="note-next"><div class="wrap note-next-inner">
      <p class="next-story">{title}</p><div class="contact-actions">
        <a class="button button-green" href="{href}">{icon("target")}Request a search</a>
        <a class="text-link" href="{TEL}">{icon("phone")}{PHONE}</a>
      </div>
    </div></aside>'''


def service_page(service):
    request_href = "/?" + urlencode({"service": service["value"]}) + "#request"
    picture = (service["photo"], service["alt"]) if "photo" in service else None
    sections = "".join(
        f'<section><h2>{heading}</h2><p>{copy}</p></section>'
        for heading, copy in service["sections"]
    )
    related = "".join(service_card(other) for other in SERVICES if other != service)
    return f'''{subpage_header(breadcrumbs("services", "Services"), price_label(service), service["heading"], service["lead"], picture, request_href)}
    <div class="wrap section-pad subpage-body">
      <div class="subpage-copy">{sections}</div>
      <aside class="subpage-side"><h2>Other services</h2><div class="side-cards">{related}</div></aside>
    </div>{subpage_contact(href=request_href)}'''


def city_page(city):
    local = city.get("story")
    related = next(story for story in stories if story["slug"] == (local or city["related"]))
    coverage = "Core service area" if city["core"] else "Travel by arrangement"
    story_heading = "A recovery from the area" if local else "From the recovery journal"
    nearby = "" if local else f'<p class="related-context">A Lost Legends search from {related["place"]}.</p>'
    city_name = f'{city["name"]}, {city["state"]}'
    return f'''{subpage_header(breadcrumbs("area", "Service area"), coverage, f"Lost item recovery in {city_name}", city["lead"])}
    <div class="wrap section-pad subpage-body city-body">
      <div class="subpage-copy">
        <section><h2>{city["heading"]}</h2><p>{city["copy"]}</p></section>
        <section><h2>Before the search</h2><p>Send what you lost, when it happened, and a location pin. I’ll confirm timing and any travel fee before leaving Plattsmouth.</p>
          <a class="text-link" href="/lost-ring-recovery/">How reward-based recovery works</a>
        </section>
        {city_links()}
      </div>
      <aside class="subpage-side"><h2>{story_heading}</h2>{nearby}{story_card(related)}</aside>
    </div>{subpage_contact("Have a map pin? Let’s talk.")}'''


def about_page():
    return f'''{subpage_header(breadcrumbs("about", "Meet Alex"), "Lost Legends Metal Detection & Recovery", "I’m Alex Kaffenberger.", "I’m a dad from Plattsmouth, a local history buff, and the person who answers when you text Lost Legends.", ("alex", "Alex Kaffenberger, founder of Lost Legends."))}
    <div class="wrap section-pad subpage-body">
      <div class="subpage-copy">
        <section><h2>Why I do it</h2><p>I got into metal detecting through old maps and local history. Helping someone get their wedding ring back gave me another reason to go out with the detector. I help people recover items that carry a story, whether they’re wedding bands, family jewelry, or the keys they need to finish their day.</p></section>
        <section><h2>What a search looks like</h2><p>We start where you last remember having the item. I adjust my detector for the local soil and work in overlapping passes. Along I-29, bits of aluminum made a lost ring hard to hear. Checking the signal from a second direction helped me pick it out.</p>
          <a class="text-link" href="{PROFILE}">{icon("compass")}My listing on The Ring Finders</a></section>
        <section><h2>On your property</h2><p>{YARD_CARE}</p></section>
      </div>
      <aside class="client-quote about-page-quote"><span class="quote-mark" aria-hidden="true">“</span>
        <blockquote>He was able to find our ring and reunite the set!</blockquote><p>From a family whose wedding band was lost in the snow.</p>
        <a class="text-link" href="/recoveries/wedding-band-in-snow/">Read the recovery story</a>
      </aside>
    </div>{subpage_contact("Tell me what you lost.")}'''


def faq_page():
    return f'''{subpage_header(breadcrumbs("services", "Services"), "Before the search", "Frequently asked questions", "What to do after you lose something, how the reward works, and what to expect when I come out.")}
    <div class="wrap section-pad faq-page" id="faq">
      <div class="faq-list">{"".join(faq(*pair) for pair in ALL_FAQS)}</div>
    </div>{subpage_contact("Tell me about your search.")}'''


def build():
    OUT.mkdir(exist_ok=True)
    indexed = []

    def write(path, title, description, body, **options):
        folder = OUT / path.strip("/")
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(
            shell(title, description, body, path=path, **options), encoding="utf-8"
        )
        if options.get("index", True):
            indexed.append(path)

    write("/", "Lost Ring Recovery in Nebraska & Iowa | Lost Legends Metal Detection",
          "Lost a ring, jewelry, or keys? Text Alex Kaffenberger in Plattsmouth for reward-based metal detecting near Omaha, Council Bluffs, and Cass County. No find, no recovery reward.",
          home_content(), faqs=HOME_FAQS)
    for service in SERVICES:
        write(f'/{service["slug"]}/', service["title"] + " | Lost Legends", service["description"],
              service_page(service), service=service)
    for city in CITIES:
        write(f'/{city["slug"]}/', f'Lost Item Recovery in {city["name"]}, {city["state"]} | Lost Legends',
              city["description"], city_page(city), index=bool(city.get("story")))
    for position, story in enumerate(stories):
        other = stories[(position + 1) % len(stories)]
        write(f'/recoveries/{story["slug"]}/', story["title"] + " | Lost Legends Recovery Stories",
              story["teaser"], story_page(story, other), og_image=story["social"], article=True)
    write("/about/", "About Alex Kaffenberger, Plattsmouth Detectorist | Lost Legends",
          "Meet Alex Kaffenberger, the Plattsmouth dad behind Lost Legends Metal Detection & Recovery and a member of The Ring Finders.",
          about_page())
    write("/faq/", "Lost Ring Recovery FAQ | Pricing, Snow & Water Searches | Lost Legends",
          "Answers about reward-based metal detecting, detector rentals, shallow water and snow searches, property pin pricing, and what happens if your item stays missing.",
          faq_page(), faqs=ALL_FAQS)

    # Keep the first published story link working.
    legacy = OUT / "recoveries" / "cartier-trinity"
    legacy.mkdir(parents=True, exist_ok=True)
    story_path = "/recoveries/cartier-ring-roadside/"
    (legacy / "index.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>A Cartier Ring on the Roadside</title>
<meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={story_path}">
<link rel="canonical" href="{DOMAIN}{story_path}"></head><body>
<p><a href="{story_path}">Read A Cartier Ring on the Roadside</a></p></body></html>
''', encoding="utf-8")
    urls = "".join(f"  <url><loc>{DOMAIN}{path}</loc></url>\n" for path in indexed)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n", encoding="utf-8"
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build()
