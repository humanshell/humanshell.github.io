#!/usr/bin/env python3
"""Replace tags in Jekyll post front matter with curated tags."""
import re, sys, pathlib

TAGS = {
    "2010-11-14-plah.markdown": ["life", "struggle", "perseverance", "motivation"],
    "2010-11-14-themthey.markdown": ["inner-demons", "struggle", "endurance"],
    "2010-11-14-why.markdown": ["killing", "morality", "human-nature", "perception"],
    "2010-12-01-2.markdown": ["love", "romance", "longing"],
    "2010-12-01-4---what.markdown": ["enlightenment", "rebellion", "individuality"],
    "2010-12-01-beginning-end.markdown": ["existence", "love", "death", "god"],
    "2010-12-01-boss.markdown": ["work", "learning", "perseverance", "dreams"],
    "2010-12-01-misunderstanding.markdown": ["perception", "religion", "love", "understanding"],
    "2010-12-01-religion.markdown": ["god", "faith", "hypocrisy", "prayer"],
    "2010-12-01-running.markdown": ["responsibility", "burden", "reality", "mortality"],
    "2010-12-01-untitled-5.markdown": ["perception", "unconsciousness", "death"],
    "2010-12-01-untitled-6.markdown": ["love", "admiration", "consciousness"],
    "2010-12-13-ask-yourself.markdown": ["introspection", "self-reflection", "questions"],
    "2010-12-13-combinations.markdown": ["life", "love", "experience", "philosophy"],
    "2010-12-13-demand.markdown": ["change", "happiness", "impermanence"],
    "2010-12-13-divine.markdown": ["god", "religion", "war", "skepticism"],
    "2010-12-13-dreams.markdown": ["dreams", "survival", "pain", "wonder"],
    "2010-12-13-einstein.markdown": ["time", "relativity", "present-moment", "philosophy"],
    "2010-12-13-flight.markdown": ["freedom", "oppression", "imagination", "perspective"],
    "2010-12-13-fournow.markdown": ["time", "music", "turmoil", "pain"],
    "2010-12-13-from-below.markdown": ["faith", "belief", "perception", "god"],
    "2010-12-13-from-me.markdown": ["solitude", "existence", "transcendence", "enlightenment"],
    "2010-12-13-go.markdown": ["space", "exploration", "unknown", "imagination"],
    "2010-12-13-god-bless-u.markdown": ["silence", "language", "provocation", "faith"],
    "2010-12-13-hold-me.markdown": ["freedom", "barriers", "acceptance", "nature"],
    "2010-12-13-i-don't-mean-to-imply.markdown": ["truth", "illusion", "simplicity", "mortality"],
    "2010-12-13-if.markdown": ["touch", "senses", "infinity", "universe"],
    "2010-12-13-imagine.markdown": ["mirrors", "identity", "self-image"],
    "2010-12-13-in-and-out.markdown": ["identity", "self", "mirror"],
    "2010-12-13-in-some-ways.markdown": ["indulgence", "tenderness", "conflict", "fate"],
    "2010-12-13-mutherfuker.markdown": ["youth", "justice", "violence", "society"],
    "2010-12-13-needs-wants.markdown": ["desire", "dreams", "needs", "aspiration"],
    "2010-12-13-no-it-can't-be.markdown": ["belief", "truth", "doubt", "perception"],
    "2010-12-13-o.markdown": ["love", "connection", "time", "longing"],
    "2010-12-13-on-a-dead-horse-about-town.markdown": ["people", "truth", "impermanence", "observation"],
    "2010-12-13-on-top-of-it.markdown": ["emptiness", "existence", "thought", "emotion"],
    "2010-12-13-patriotic-love.markdown": ["patriotism", "unity", "love", "memory"],
    "2010-12-13-prescriptions.markdown": ["pain", "voyeurism", "media", "suffering"],
    "2010-12-13-questions.markdown": ["darkness", "evil", "fear", "questions"],
    "2010-12-13-remember.markdown": ["time", "friendship", "loyalty", "hope"],
    "2010-12-13-speak-with-a-sensation.markdown": ["existence", "eternity", "chaos", "life"],
    "2010-12-13-temptation.markdown": ["senses", "synesthesia", "nature", "curiosity"],
    "2010-12-13-to-be-read-like-a-novel.markdown": ["journal", "solitude", "introspection", "prose"],
    "2010-12-13-to-yesterday.markdown": ["change", "nostalgia", "resistance", "unity"],
    "2010-12-13-truth.markdown": ["elements", "dreams", "imagination", "truth"],
    "2010-12-13-untitled-2.markdown": ["power", "god-complex", "destiny", "mankind"],
    "2010-12-13-untitled-3.markdown": ["solitude", "harmony", "escapism"],
    "2010-12-13-untitled-4.markdown": ["unrequited-love", "longing", "isolation"],
    "2010-12-13-untitled.markdown": ["future", "change", "adversity", "resilience"],
    "2010-12-13-wake-up.markdown": ["awareness", "perspective", "truth", "mindfulness"],
    "2010-12-13-warmth.markdown": ["loneliness", "self-belief", "independence"],
    "2010-12-13-who.markdown": ["enlightenment", "pain", "acceptance", "self-discovery"],
    "2010-12-13-would-you.markdown": ["fate", "chance", "caution", "resilience"],
    "2011-03-11-pain-and-suffering.markdown": ["pain", "suffering", "philosophy", "happiness", "utilitarianism"],
    "2011-05-11-reality-vs-non-reality.markdown": ["reality", "perception", "imagination", "relativity", "glass-menagerie"],
    "2011-05-11-state-of-affairs.markdown": ["change", "humanity", "unity", "mortality"],
    "2011-05-18-global-water-resources.markdown": ["water", "scarcity", "global-health", "energy", "sustainability"],
    "2012-03-17-globalization-affects-dictators-too.markdown": ["globalization", "syria", "assad", "sociology"],
    "2012-04-06-societal-thoughts-from-a-tv-writer.markdown": ["television", "chuck-lorre", "society", "culture"],
    "2012-04-09-sociological-entropy.markdown": ["entropy", "sociology", "thermodynamics", "society"],
    "2012-04-13-those-poor-poor-people.markdown": ["poverty", "class", "stigma", "society"],
    "2012-04-23-people-like-us.markdown": ["class", "stratification", "socialization", "america"],
    "2012-05-03-playing-the-political-slots.markdown": ["native-americans", "casinos", "lobbying", "sovereignty", "politics"],
    "2012-08-03-the-culture-makers.markdown": ["corporations", "culture", "media", "advertising", "globalization"],
    "2013-09-24-deploying-ghost-to-heroku.markdown": ["ghost", "heroku", "nodejs", "deployment", "blogging"],
    "2013-09-25-dynamic-character-arrays-in-c.markdown": ["c", "pointers", "dynamic-memory", "arrays", "data-structures"],
}

posts_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_posts")
updated = missing = 0
for fname, tags in TAGS.items():
    path = posts_dir / fname
    if not path.exists():
        print(f"MISSING: {fname}")
        missing += 1
        continue
    text = path.read_text(encoding="utf-8")
    new_line = "tags: [" + ", ".join(tags) + "]"
    new_text, n = re.subn(r"(?m)^tags:\s*\[.*\]\s*$", new_line, text, count=1)
    if n != 1:
        print(f"NO TAGS LINE MATCHED: {fname}")
        missing += 1
        continue
    path.write_text(new_text, encoding="utf-8")
    updated += 1

print(f"updated={updated} problems={missing}")
