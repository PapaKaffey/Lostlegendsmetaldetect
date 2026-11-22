"""Copy for service and coverage pages."""

PIN_DISCLAIMER = (
    "I use a metal detector to identify existing markers only. This is not a land survey "
    "and does not establish, verify, or certify property boundaries."
)
REWARD_TERMS = (
    "You set the reward after I return your item. No find, no fee. "
    "The only exception is a travel fee we agree on before a remote trip."
)
UNSUCCESSFUL_SEARCH = (
    "You’ll get a report of where I searched and practical next steps, such as another spot to check "
    "or whether a return visit makes sense. You pay nothing unless we agreed on a travel fee "
    "for a remote trip in advance."
)
YARD_CARE = (
    "I pinpoint the target before I dig. In a lawn, I cut a clean plug, refill the hole neatly, "
    "and replace the turf whenever conditions allow. I ask before sharing photos or details "
    "that identify you or your property."
)

HOME_FAQS = [
    (
        "What should I do if I just lost a ring?",
        "Mark the last spot where you remember wearing it. For the fastest reply, text me what you lost, "
        "an address or GPS pin, and a photo of the search area. Tell me if the area is about to be mowed or plowed.",
    ),
    ("What does a lost-ring or jewelry search cost?", REWARD_TERMS),
    ("What happens if you don’t find my item?", UNSUCCESSFUL_SEARCH),
    (
        "Is the $75 property pin service a land survey?",
        PIN_DISCLAIMER + " For boundary questions, contact a licensed land surveyor.",
    ),
    (
        "Should I rent a metal detector or hire you?",
        "A rental can work if you know the spot and have time to learn the controls. In ground full of nails "
        "or pull tabs, it takes practice to pick out a ring. I bring my own equipment, search in overlapping "
        "passes, and check signals from more than one direction.",
    ),
    (
        "Can you search in water or snow?",
        "Yes. I use waterproof equipment for shallow-water searches when conditions allow. Tell me how deep "
        "the water was, what the bottom is like, and where you went in. For a snow loss, mark the spot "
        "and tell me where any shoveled or plowed snow ended up.",
    ),
]
ALL_FAQS = HOME_FAQS + [
    (
        "How quickly can you respond?",
        "I check texts frequently. Depending on my schedule and the drive, I may be able to come out the same "
        "day or the next, including evenings and weekends. I’ll confirm a time with you before I head out.",
    ),
    (
        "What are the chances of finding my item?",
        "The best lead is a specific spot where you know you had it. The chances depend on how much time "
        "has passed, whether the item is still there, and how much ground or debris there is to search. "
        "Tell me what’s changed since the loss and I’ll talk through what’s realistic.",
    ),
    (
        "How should I prepare the search area?",
        "Mark the likely spot with a landmark or photo and note the route you took. If possible, hold off "
        "on mowing, raking, shoveling, or moving soil. Tell me where you’ve already looked and arrange "
        "permission if someone else owns or manages the property.",
    ),
    ("How do you protect my yard and privacy?", YARD_CARE),
    (
        "Where do you take jobs?",
        "I’m based in Plattsmouth. My core area is the Omaha metro, Council Bluffs, Cass County, and "
        "Nebraska City. For other parts of Nebraska or Iowa, text your nearest town so I can confirm the trip.",
    ),
    (
        "Can you search on someone else’s property?",
        "We’ll need permission from the property owner or whoever manages the site before I start. If it’s "
        "a park, venue, job site, or rental property, send me the location and let me know who can grant access.",
    ),
    (
        "Can you find keys, watches, or other jewelry?",
        "Yes. Tell me what it’s made of and whether there are other metal pieces attached. A picture helps, "
        "especially for small earrings, pendants, and keys with a plastic fob.",
    ),
    (
        "How much do property pin locating and cleanup cost?",
        "Property pin locating is $75 per detectable marker. Junk metal cleanup is $89 per hour. "
        "I’ll confirm the scope and any travel charge before scheduling.",
    ),
]

SERVICES = [
    {
        "slug": "lost-ring-recovery", "icon": "ring", "name": "Lost ring recovery",
        "price": "Reward basis", "value": "Lost item recovery",
        "title": "Lost Ring Recovery in Nebraska & Iowa",
        "description": "Lost a wedding ring, jewelry, keys, or a keepsake? Alex Kaffenberger offers reward-based metal detecting on land, in snow, and in shallow water near Omaha and Council Bluffs.",
        "summary": REWARD_TERMS + " If your item stays missing, you still get a search report and next steps.",
        "heading": "Lost ring & jewelry recovery",
        "lead": "I search yards, fields, snow, and shallow water for lost rings, jewelry, keys, and other metal keepsakes. I’m based in Plattsmouth and take searches on both sides of the Missouri.",
        "photo": "cartier-in-hand", "alt": "The Cartier Trinity ring Alex recovered near Council Bluffs.",
        "sections": [
            ("How the reward works", REWARD_TERMS),
            ("If I don’t find it", UNSUCCESSFUL_SEARCH),
            ("Water, snow, and other tough searches", "For a ring lost while swimming or wading, mark where you entered the water and where you noticed it was missing. Send me the depth and bottom conditions so I can judge access and equipment. For a snow loss, tell me where the snow was piled and when the area was last plowed or shoveled."),
            ("Before I arrive", "Mark where you last had the item and note any ground or snow that has been moved. If someone else manages the property, we’ll arrange permission before the search."),
            ("Searching your yard", YARD_CARE),
        ],
    },
    {
        "slug": "property-pin-locating", "icon": "marker", "name": "Property pin locating",
        "price": "$75 per marker", "value": "Marker or cover",
        "title": "Property Pin Locating in the Omaha Area | $75 per Marker",
        "description": "Alex Kaffenberger locates existing detectable property pins for $75 per marker near Plattsmouth, Bellevue, Omaha, and Council Bluffs. This is not a land survey.",
        "summary": PIN_DISCLAIMER,
        "heading": "Find existing property pins",
        "lead": PIN_DISCLAIMER,
        "sections": [
            ("$75 per detectable marker", "Send your nearest town, how many corners you’re trying to locate, and anything you know about where the pins should be. A copy of an existing survey or plat can help me narrow the search. Ask separately about locating a metal curb stop or valve cover."),
            ("When you need a surveyor", "If you need a property line confirmed for a fence, construction, or a boundary dispute, contact a licensed land surveyor."),
            ("What I need before the visit", "Share any visible landmarks and tell me about fences, pets, and property access. I’ll confirm the search area and any travel fee with you before the appointment."),
        ],
    },
    {
        "slug": "junk-metal-cleanup", "icon": "magnet", "name": "Junk metal cleanup",
        "price": "$89 per hour", "value": "Metal cleanup",
        "title": "Junk Metal Cleanup Near Omaha & Plattsmouth | $89/hr",
        "description": "Request a metal detector sweep for nails, screws, wire, and scrap in yards, farmsteads, or work areas. Lost Legends charges $89 per hour for cleanup.",
        "summary": "Detector sweeps for nails, wire, and scrap in yards, farmsteads, and work areas.",
        "heading": "Junk metal cleanup",
        "lead": "I sweep yards, farmsteads, and work areas for loose metal such as nails, screws, wire, and scrap, including pieces hidden in grass or just below the surface.",
        "sections": [
            ("$89 per hour", "Send the approximate size of the area and a photo of the site or the debris you’re finding. I’ll confirm the work area, any limits on digging, and travel before we start."),
            ("Where a detector sweep helps", "A sweep can help after a roof tear-off, fence removal, or cleanup around an old shed or work area. Tell me which spots you use most so I can cover those first."),
            ("What to expect afterward", "I’ll tell you which areas I swept and point out any spots where heavy debris or access limited coverage. Soil conditions and the type and depth of the metal affect what I can locate."),
        ],
    },
]

CITIES = [
    {
        "slug": "omaha", "name": "Omaha", "state": "Nebraska", "core": True,
        "description": "Lost a ring or keys in Omaha? See how Alex recovered keys under fresh mulch and what to send for a reward-based metal detector search.",
        "lead": "Mulch, sod, or cleanup can cover a lost item fast. If you lost something in Omaha, tell me what work was done around it and where the ground was disturbed.",
        "heading": "When the area has been worked on",
        "copy": "Tell me which crews were working, where they stored or moved material, and when the area will be disturbed again. For a park or venue, share the closest entrance and the spot you were standing when you last had the item.",
        "story": "omaha-keys",
    },
    {
        "slug": "council-bluffs", "name": "Council Bluffs", "state": "Iowa", "core": True,
        "description": "Reward-based lost ring recovery in Council Bluffs and southwest Iowa. Read Alex’s Cartier Trinity recovery from an I-29 shoulder in the metro area.",
        "lead": "Council Bluffs is part of my regular service area from Plattsmouth. I take lost-item searches in yards and fields, and I assess access before any roadside or shoreline search.",
        "heading": "Pin down the spot before a trip",
        "copy": "On a long stretch of road or trail, the nearest exit, cross street, or landmark can make a big difference. Send a pin from a safe place and let me know where there’s lawful access. For a river or lake loss, share where you entered the water and how deep you were.",
        "story": "cartier-ring-roadside",
    },
    {
        "slug": "bellevue", "name": "Bellevue", "state": "Nebraska", "core": True,
        "description": "Text Alex for lost ring recovery or existing property pin locating in Bellevue, Nebraska. Lost Legends is based nearby in Plattsmouth.",
        "lead": "Bellevue is in my regular search area. I can look for a wedding band in the yard, a key dropped along a path, or an existing metal property marker you can’t see above ground.",
        "heading": "Yard searches and existing markers",
        "copy": "If a ring slipped off during yard work, retrace where you took off your gloves, moved bags, or set tools down. Looking for a marker? Send me your plat or survey if you have it, along with the corners you want me to check.",
        "related": "omaha-keys",
    },
    {
        "slug": "plattsmouth", "name": "Plattsmouth", "state": "Nebraska", "core": True,
        "description": "Lost Legends is based in Plattsmouth. Contact local detectorist Alex Kaffenberger for lost rings, keys, and keepsakes in Plattsmouth and Cass County.",
        "lead": "Plattsmouth is home. I take searches around town and throughout Cass County, from backyards to farmsteads. Nebraska City is also part of my regular service area.",
        "heading": "Searching a larger property",
        "copy": "If you lost something on an acreage, start with the gates, parking spots, and paths you took. A marked-up screenshot or a couple of landmarks helps me decide where to work first. Tell me about fences, livestock, or equipment that could affect access.",
        "related": "wedding-band-in-snow",
    },
    {
        "slug": "lincoln", "name": "Lincoln", "state": "Nebraska", "core": False,
        "description": "Lost a ring in Lincoln, Nebraska? Text Alex Kaffenberger your map pin and search details to check availability and any travel fee from Plattsmouth.",
        "lead": "I consider Lincoln searches by arrangement. Text me the closest cross streets or an address, how recently it happened, and the size of the area you want me to check.",
        "heading": "When a field or event site is closing",
        "copy": "For a loss at a game, event, or busy field, mark your route from the entrance and the place you first noticed the item was gone. Check who manages the site and when it’s open so we can plan a search around access and my drive from Plattsmouth.",
        "related": "omaha-keys",
    },
    {
        "slug": "des-moines", "name": "Des Moines", "state": "Iowa", "core": False,
        "description": "Ask Lost Legends about lost ring recovery near Des Moines, Iowa. Send the item, timing, and a map pin to confirm travel from Plattsmouth.",
        "lead": "Des Moines is a longer trip from my Plattsmouth base. I review requests individually and confirm timing and any travel fee before heading out.",
        "heading": "What helps me plan a longer trip",
        "copy": "A video or a couple of photos showing the size of the search area can save a back-and-forth. If you visited more than one spot that day, send the places and when you last remember having the item. We can work through where a detector search has the best chance.",
        "related": "cartier-ring-roadside",
    },
]
