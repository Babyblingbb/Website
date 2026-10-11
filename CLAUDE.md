# Baby Bling — Shopify storefront (babybling.in)

PRIVATE REPO. Contains live credentials (`sp.py`, `.shopify_token.json`, `.fastrr_api.json`). Never make it public.

## What's live
- Store: `ws0twk-ww.myshopify.com` → https://babybling.in
- Live theme: **"Copy of Tinker" id `166532448359`** (old "Tinker" `142438236263` is unpublished, used only for previews).
- Our pages are custom `{% layout none %}` Liquid templates in `shopify/templates/`:
  - `index.liquid` (homepage), `collection.floating.liquid` (all shirts, collection handle `shirts`),
    `page.bb.liquid` (info pages by handle: shipping, size-guide, track-order, about),
    `product.<name>-shirt.liquid` × 11 (product `template_suffix` = `<name>-shirt`).
- Checkout: Shiprocket Fastrr (`snippets/sr-checkout.liquid` in theme); our JS calls `shiprocketCheckoutEvents.buyCart()`, falls back to `/checkout`.

## Shopify API
`python sp.py scopes` — client-credentials token (24h, cached in `.shopify_token.json`).
`sp.call(method, path, payload)` REST 2025-01, `sp.gql(query)`.
Missing scopes (as of 2026-10-12): discounts, content (pages), legal policies.

## Workflow
1. Source HTML pages (`index*.html`) are built by `make-*-page.py` + `add-fabric.py`; `build-liquid.py` turns them into product templates (`ship-all.py` runs the whole chain for all 11).
2. Homepage: `python make-home.py`. Collection: `make-shop-page.py` → `build-shop-liquid.py`. Info page: `make-info-page.py`.
3. **Always run `python patch-layout.py` after any build** — it injects: content_for_header, Fastrr snippet, checkout hook, nav/footer links, mobile burger menu (`menu.py`), size-chart popup (`sizechart.py`), coupons (`coupons.py`), shared CSS (`bbstyle.css`) and pilot CSS (`bbstyle-lab.css`).
4. Upload: `PUT themes/166532448359/assets.json` with `{"asset":{"key":"templates/<file>","value":...}}` (see one-liners in `ship-all.py` / `upload.py`).
5. Verify on phone width (390px): no horizontal overflow, no broken images.

## House rules (from the owner)
- Try design changes on **Sail Away (`product.sail-shirt`) first**; roll out to all pages only after approval. Don't restyle sections nobody asked about.
- Text must stay readable on every sky backdrop; no glow/text-shadow on body text.
- Mobile first; owner writes in Hinglish and prefers short, token-efficient replies.
- Never invent customer reviews on the live site (`reviews-test.py` targets the unpublished theme only, labelled "Sample").

## Images
AI renders via Vertex (`gen*.py` call `~/.claude/scripts/gen-image.py`, model `gemini-3-pro-image`); cut-outs `cutout.py`, grid normalisation `normalise.py`.
