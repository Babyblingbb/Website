BABY BLING — Balloon Bicycle shirt page for Shopify
====================================================
Runs inside your theme on babybling.in. Uses Shopify's own cart + checkout.
No app, no Vercel, no external hosting.

USE THIS ONE  ->  templates/product.balloon-shirt.liquid
   Makes the page THE product page:  babybling.in/products/peach-linen-shirt
   (templates/page.balloon-shirt.liquid is the standalone-page version,
    only needed if you'd rather have it at /pages/... - ignore otherwise.)

INSTALL  (Online Store > Themes > ... > Edit code)

1. ASSETS
   "Assets" folder > "Add a new asset" > Upload file.
   Upload all 7 bb-*.webp files. Keep the names exactly.

2. TEMPLATE
   "Templates" > "Add a new template"
       Template type : product
       Name          : balloon-shirt
       Base          : liquid       <-- IMPORTANT, not json
   Delete what it pre-fills, paste ALL of
   templates/product.balloon-shirt.liquid , then Save.

3. ASSIGN IT TO THE SHIRT
   Admin > Products > "Peach Linen shirt"
   Right sidebar, bottom > "Theme template" > choose  balloon-shirt  > Save.

   Live at:  https://babybling.in/products/peach-linen-shirt

WHY YOU GOT "PAGE NOT FOUND" BEFORE
   /pages/balloon-bicycle-shirt 404s because no Page was ever created in
   Content > Pages. The product route above avoids that step entirely.

HOW IT TALKS TO YOUR STORE
   - Reads the product it is assigned to. Nothing is hardcoded.
   - Price comes from Shopify. While the product is Rs.0 the page shows
     "Price coming soon" instead of a fake number or Rs.0.00.
   - SIZES: if the product has a real "Size" option, the size buttons are
     built from your actual variants - sold-out ones grey out, and picking
     one selects that variant id and its price. If there is no Size option
     (today), the buttons send the chosen size as a line-item property.
   - Add to cart -> POST /cart/add.js      (real Shopify line item)
   - Cart drawer -> /cart.js , remove -> /cart/change.js
   - Checkout    -> /checkout              (your Razorpay + COD)

TO ACTUALLY SELL IT
   "Peach Linen shirt" is Rs.0.00 with no stock and one "Default Title"
   variant. Set a price, add the size variants, add stock. The page picks
   all of it up automatically - no code change.
   Handle: peach-linen-shirt   Variant: 44581189255271
