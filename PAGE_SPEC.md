# Agents for Agents — page build spec

Every page on this site is one self contained `index.html` inside its own folder, linked to the
shared stylesheet. Never write a `<style>` block. Never restate the design system. If a page
needs a component that does not exist yet, add it to `assets/brand.css` under a clearly
commented section rather than inlining it.

## File shape (copy this exactly)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><PAGE TITLE> · Agents for Agents</title>
<meta name="description" content="<ONE SENTENCE, UNDER 155 CHARS>">
<meta property="og:title" content="<PAGE TITLE>">
<meta property="og:description" content="<SAME ONE SENTENCE>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/brand.css">
</head>
<body>

<nav id="nav">
  <div class="wrap">
    <a class="brand" href="/"><span class="mk"></span> Agents for Agents</a>
    <div class="nl">
      <a href="/">Home</a>
      <a href="#<SECTION>">…</a>
      <a class="cta-sm" href="#<CTA ANCHOR>"><CTA LABEL></a>
    </div>
  </div>
</nav>

<main>
  … sections …
</main>

<footer>
  <div class="wrap">
    <div>&copy; 2026 Agents for Agents. Built in Massachusetts by a working agent.</div>
    <div><a href="https://instagram.com/henryhandleshomes">Instagram</a> &nbsp; · &nbsp; <a href="mailto:henry@serhant.com">Email</a></div>
  </div>
</footer>

<script>
const io = new IntersectionObserver((es) => {
  es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { rootMargin: '0px 0px -8% 0px', threshold: .12 });
document.querySelectorAll('.rv').forEach((el, i) => {
  el.style.transitionDelay = Math.min(i % 6, 5) * 55 + 'ms';
  io.observe(el);
});
const nav = document.getElementById('nav');
addEventListener('scroll', () => nav.classList.toggle('stuck', scrollY > 12), { passive: true });
</script>
</body>
</html>
```

## Components available in brand.css

Layout: `.wrap` (1160 max), `.narrow` (760 max, for reading), `section` (120px vertical rhythm)
Type: `.serif`, `.mono`, `h1.display`, `h2.display`, `.eyebrow`, `.tag`, `.copy`, `.lede`
Emphasis: wrap a phrase in `<em>` inside any `.display` heading to set it in italic accent violet
Hero: `header.hero` > `.eyebrow`, `h1.display.serif`, `.lede`, `.acts` with `.btn.btn-fill` / `.btn.btn-line`, `.hero-note`
Bands: `.strip` (thin fact row, must be a plain div, never a section), `.moment` (full bleed dark, `.big` `.cap` `.fine`), `.out` and `.safe` (tinted section wrappers)
Grids: `.dom` + `.d` (3 col capability tiles), `.figs` + `.fig` (4 stat columns), `.deliv` + `.dv` (numbered deliverable rows), `.index` + `.row` (numbered index with right margin meta), `.entry` + `.paths` (route list)
Editorial: `.story` + `blockquote`, `.method` + `.mrow` (label + heading + paragraph rows), `.probs` + `.prob` (quote left, outcome right), `.olist` (two column outcome list)
Commerce: `.buy` (bordered price card), `.faq` + `.q`, `.paths` (list of routes)
Device: `.phone` > `.scr` > `.card` (approval card mock)
Reveal: add class `rv` to anything that should fade up on scroll. Every meaningful block gets it.

## Voice rules, non negotiable

- Henry is a practicing agent, never a coach or a guru. Agent to agent.
- NEVER use em dashes or double hyphens anywhere. Commas, colons, periods only.
- No hype vocabulary: no "game changer", "unlock", "10x", "revolutionary", "supercharge".
- No income claims, no guarantees, no fake urgency, no invented testimonials or logos.
- Sell the outcome and the pain. Withhold the mechanism. A visitor should finish a page
  convinced it works and still not know exactly how it is built.
- Short sentences carry weight. Long ones carry nuance. Alternate.
- Compliance is a selling point, not a disclaimer. Fair housing, Do Not Call, opt out,
  and "nothing sends without you" get stated plainly wherever they are relevant.
- Where a claim uses a number, that number must be real and its assumptions shown.
  Approved real figures: 1,314 contacts audited, 370 dark past ninety days, 909 never called,
  $222,000 estimated at a 2 percent reactivation rate and $30,000 average commission,
  the expired pipeline has run every morning since April, 13 packs, 263 skills.

## Every page ends the same way

A `.close` section: one `h2.display.serif` with an `<em>` phrase, one line of `.copy`, one
`.btn.btn-fill`, and a link back to `/`.

## Known gotchas

- `.strip` is a `div`. Wrapping it in `<section>` doubles its padding.
- Titles use a middle dot, never an em dash. The no dash rule applies to markup too.
- If you need a component that is not listed above, add it to `assets/brand.css` in a commented section and note it in your report. Do not inline a `<style>` block.
