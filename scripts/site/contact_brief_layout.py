"""PARKED (2026-10-07): The Brief, kept for later. Builds the contact page with The Brief; a built copy is
Furnishiq.net/contact-brief-draft.dc.html (noindex). Contact page, studio-desk layout with The Brief.

Replaces the dark statement hero, the channel strip, the form section, the next-steps cards and the visit band with:
a white first screen that is The Brief (brief.js): the questions one at a time on the left, and beside them, on a Stone
mat, a project brief that drafts itself as the answers come in; then the direct lines in one row, the three next
steps on one hairline, and the studio visit beside a framed map toned to the palette. The Brief sends to the same
/api/send-email (formType "contact", the brief written into the message) or opens WhatsApp with the brief pre-written.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/site/contact_layout.py
"""
import io, re

PAGE = "contact.dc.html"
EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>'
ARROW_UR = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>'
MAP_CID = "2079283542092448688"

CSS = """  <style>
    /* ── contact: the studio desk ── */
    .ct,.cn,.cv{--ease:%(e)s;}
    .ct-wrap,.cn-wrap,.cv-wrap{max-width:1280px;margin:0 auto;box-sizing:border-box;}
    .ct{background:#FFFFFF;}
    .ct-wrap{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:32px;align-items:start;padding:clamp(120px,15vh,150px) 0 clamp(72px,9vw,120px);}
    .ct-intro{grid-column:1/6;position:sticky;top:112px;}
    .c-label{display:flex;align-items:center;gap:16px;margin-bottom:clamp(16px,2.4vh,24px);font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.3em;text-transform:uppercase;color:#8B6B4A;}
    .c-label i{display:block;width:32px;height:1px;background:currentColor;}
    .ct-h1{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(44px,5.4vw,88px);line-height:0.98;letter-spacing:-0.04em;color:#1F1F1F;}
    .ct-h1 span{display:block;color:#8B6B4A;}
    .ct-lede{margin:clamp(20px,3vh,28px) 0 0;max-width:30em;font-family:'Lama Sans',sans-serif;font-size:16px;line-height:1.75;color:#5B4636;}
    .ct-ch{margin:clamp(32px,5vh,48px) 0 0;padding:0;list-style:none;border-top:1px solid #E8DFD8;}
    .ct-ch a,.ct-ch div{display:grid;grid-template-columns:96px 1fr auto;gap:16px;align-items:baseline;padding:16px 0;border-bottom:1px solid #E8DFD8;text-decoration:none;color:inherit;}
    .ct-ch small{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .ct-ch b{display:block;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:16px;color:#1F1F1F;transition:color 0.3s var(--ease);}
    .ct-ch em{display:block;margin-top:3px;font-style:normal;font-family:'Lama Sans',sans-serif;font-size:12.5px;color:#8B7A6B;}
    .ct-ch svg{color:#B8A08C;transition:transform 0.4s var(--ease),color 0.3s var(--ease);}
    .ct-ch a:hover b,.ct-ch a:focus-visible b{color:#8B6B4A;}
    .ct-ch a:hover svg,.ct-ch a:focus-visible svg{color:#8B6B4A;transform:translate(3px,-3px);}
    .ct-facts{display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:20px;font-family:'Lama Sans',sans-serif;font-size:12.5px;color:#8B7A6B;}
    .ct-facts span b{font-weight:500;color:#1F1F1F;}
    .ct-panel{grid-column:7/13;background:#F5F2ED;padding:clamp(32px,3.6vw,56px);}
    .ct-panel-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:clamp(28px,3vw,40px);padding-bottom:20px;border-bottom:1px solid #E2D7CA;}
    .ct-panel-head h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(22px,1.8vw,28px);letter-spacing:-0.02em;color:#1F1F1F;}
    .ct-panel-head span{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.2em;text-transform:uppercase;color:#8B6B4A;white-space:nowrap;}
    .ct-in{opacity:0;transform:translateY(18px);transition:opacity 0.9s var(--ease) var(--d,0s),transform 0.9s var(--ease) var(--d,0s);}
    .ct.is-ready .ct-in{opacity:1;transform:none;}
    .rv{opacity:0;transform:translateY(18px);transition:opacity 0.8s %(e)s,transform 0.8s %(e)s;}
    /* the brief: questions */
    .bf{grid-template-columns:repeat(12,minmax(0,1fr));align-items:start;}
    .bf-stage{grid-column:1/7;}
    .bf-h1{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(40px,4.4vw,72px);line-height:0.98;letter-spacing:-0.04em;color:#1F1F1F;}
    .bf-h1 span{display:block;color:#8B6B4A;}
    .bf-status{display:flex;align-items:center;gap:12px;margin:clamp(18px,2.6vh,26px) 0 0;font-family:'Lama Sans',sans-serif;font-size:13.5px;line-height:1.6;color:#5B4636;}
    .bf-status::before{content:"";flex:none;width:7px;height:7px;border:1px solid #8B6B4A;}
    .bf-status.is-open::before{background:#8B6B4A;}
    .bf-root{margin-top:clamp(32px,5vh,52px);}
    .bq-progress{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;}
    .bq-progress i{display:block;height:2px;background:#E8DFD8;transition:background 0.5s var(--ease);}
    .bq-progress i.is-done{background:#B8A08C;}
    .bq-progress i.is-on{background:#1F1F1F;}
    .bq{opacity:0;transform:translateY(14px);transition:opacity 0.6s var(--ease),transform 0.6s var(--ease);}
    .bq.is-in{opacity:1;transform:none;}
    .bq-top{display:flex;justify-content:space-between;align-items:center;min-height:34px;margin:22px 0 14px;}
    .bq-n{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.14em;color:#8B6B4A;}
    .bq-back{display:inline-flex;align-items:center;gap:10px;padding:8px 0;background:none;border:0;cursor:pointer;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:#5B4636;transition:color 0.3s var(--ease),gap 0.3s var(--ease);}
    .bq-back:hover,.bq-back:focus-visible{color:#1F1F1F;gap:14px;}
    .bq-q{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(28px,2.6vw,42px);line-height:1.12;letter-spacing:-0.03em;color:#1F1F1F;outline:none;}
    .bq-hint{margin:10px 0 0;font-family:'Lama Sans',sans-serif;font-size:14px;color:#8B7A6B;}
    .bq-opts{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px;}
    .bq-opt{display:inline-flex;align-items:center;gap:12px;padding:16px 22px;background:transparent;border:1px solid #D9CDBF;cursor:pointer;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;transition:background 0.3s var(--ease),color 0.3s var(--ease),border-color 0.3s var(--ease);}
    .bq-opt:hover,.bq-opt:focus-visible{border-color:#1F1F1F;}
    .bq-opt[aria-pressed="true"]{background:#1F1F1F;border-color:#1F1F1F;color:#F5F2ED;}
    .bq-opts.is-many .bq-opt::before{content:"";flex:none;width:9px;height:9px;border:1px solid currentColor;}
    .bq-opts.is-many .bq-opt[aria-pressed="true"]::before{background:#D6C2A8;border-color:#D6C2A8;}
    .bq-next,.bq-send{display:inline-flex;align-items:center;gap:14px;margin-top:32px;padding:17px 30px;background:#1F1F1F;border:1px solid #1F1F1F;color:#F5F2ED;cursor:pointer;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;white-space:nowrap;transition:background 0.4s var(--ease),color 0.4s var(--ease),gap 0.4s var(--ease),opacity 0.3s;}
    .bq-next:hover,.bq-next:focus-visible,.bq-send:hover,.bq-send:focus-visible{background:#3A2D25;gap:20px;}
    .bq-next:disabled,.bq-send:disabled{opacity:0.35;cursor:default;gap:14px;background:#1F1F1F;}
    .bq-size{margin-top:26px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(34px,3.2vw,52px);letter-spacing:-0.03em;color:#1F1F1F;}
    .bq-range{margin-top:22px;}
    .bq-range input{-webkit-appearance:none;appearance:none;width:100%;height:24px;margin:0;padding:0;border:0;box-shadow:none;background:transparent;cursor:pointer;}
    .bq-range input::-webkit-slider-runnable-track{height:1px;background:#1F1F1F;}
    .bq-range input::-moz-range-track{height:1px;background:#1F1F1F;}
    .bq-range input::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;margin-top:-9px;background:#1F1F1F;border:4px solid #F5F2ED;outline:1px solid #1F1F1F;}
    .bq-range input::-moz-range-thumb{width:12px;height:12px;background:#1F1F1F;border:4px solid #F5F2ED;border-radius:0;outline:1px solid #1F1F1F;}
    .bq-range input:focus-visible{outline:1px solid #8B6B4A;outline-offset:6px;}
    .bq-scale{display:flex;justify-content:space-between;margin-top:8px;font-family:'Lama Sans',sans-serif;font-size:11px;color:#8B7A6B;}
    .bq-form{margin-top:26px;}
    .bq-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px 28px;}
    .bq-field{display:flex;flex-direction:column;gap:6px;}
    .bq-form>.bq-field{margin-top:22px;}
    .bq-label{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .bq-label i{font-style:normal;text-transform:none;letter-spacing:0;color:#B8A08C;}
    .bq-field input,.bq-field textarea,.bq-phone{width:100%;box-sizing:border-box;background:transparent;border:0;border-bottom:1px solid #D6C2A8;border-radius:0;padding:11px 0;outline:none;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;transition:border-color 0.3s var(--ease);}
    .bq-field textarea{resize:vertical;min-height:72px;line-height:1.6;}
    .bq-field input:focus,.bq-field textarea:focus,.bq-phone:focus-within{border-bottom-color:#1F1F1F;}
    .bq-field input.is-bad,.bq-phone:has(.is-bad){border-bottom-color:#C0392B;}
    .bq-phone{display:flex;align-items:center;gap:12px;padding:0;}
    .bq-phone select{flex:none;background:transparent;border:0;border-right:1px solid #D6C2A8;padding:11px 12px 11px 0;font-family:'Lama Sans',sans-serif;font-size:15px;color:#5B4636;outline:none;cursor:pointer;}
    .bq-phone input{border:0!important;padding:11px 0;}
    .bq-err{min-height:0;font-family:'Lama Sans',sans-serif;font-size:11px;color:#C0392B;}
    .bq-acts{display:flex;align-items:center;flex-wrap:wrap;gap:12px 28px;}
    .bq-wa{position:relative;display:inline-flex;align-items:center;gap:12px;margin-top:32px;padding-bottom:6px;color:#1F1F1F;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:color 0.3s var(--ease),gap 0.4s var(--ease);}
    .bq-wa::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:#8B6B4A;}
    .bq-wa:hover,.bq-wa:focus-visible{color:#8B6B4A;gap:18px;}
    .bq-fine{margin:16px 0 0;font-family:'Lama Sans',sans-serif;font-size:11px;color:#B8A08C;}
    .bq-hp,.bq-live{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
    /* the brief: the sheet, on a Stone mat */
    .bf-side{grid-column:8/13;position:sticky;top:112px;background:#F5F2ED;padding:clamp(20px,2.2vw,32px);}
    .bs{position:relative;background:#FFFFFF;border:1px solid #1F1F1F;}
    .bs::before{content:"";position:absolute;inset:6px;border:1px solid #E2D7CA;pointer-events:none;}
    .bs-head{position:relative;display:flex;justify-content:space-between;align-items:flex-end;gap:16px;padding:22px 24px 18px;border-bottom:1px solid #1F1F1F;}
    .bs-kicker{display:block;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.26em;text-transform:uppercase;color:#8B6B4A;}
    .bs-ref{display:block;margin-top:6px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(17px,1.4vw,21px);letter-spacing:-0.01em;color:#1F1F1F;}
    .bs-date{font-family:'Lama Sans',sans-serif;font-size:11px;color:#8B7A6B;white-space:nowrap;}
    .bs-body{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 36%;}
    .bs-rows{padding:6px 24px 10px;}
    .bs-row{display:grid;grid-template-columns:104px minmax(0,1fr);gap:12px;align-items:baseline;padding:11px 0;border-bottom:1px dashed #E2D7CA;}
    .bs-row:last-child{border-bottom:0;}
    .bs-k{font-family:'Lama Sans',sans-serif;font-size:9px;letter-spacing:0.16em;white-space:nowrap;text-transform:uppercase;color:#C4B3A2;transition:color 0.5s var(--ease);}
    .bs-v{font-family:'Lama Sans',sans-serif;font-size:14px;line-height:1.45;color:#1F1F1F;}
    .bs-row:not(.is-set) .bs-v::after{content:"";display:block;width:62%;height:1px;margin-top:7px;background:#EFE8DF;}
    .bs-row.is-set .bs-k{color:#8B6B4A;}
    .bs-row.is-set .bs-v{animation:bs-in 0.6s var(--ease) both;}
    .bs-v.is-new{animation:bs-in 0.6s var(--ease) both;}
    @keyframes bs-in{from{opacity:0;transform:translateY(5px);}to{opacity:1;transform:none;}}
    .bs-plan{padding:20px 18px 18px;border-left:1px solid #E2D7CA;display:flex;flex-direction:column;justify-content:flex-end;}
    .bs-plan-field{position:relative;aspect-ratio:1/1;border:1px dashed #E2D7CA;}
    .bs-plan-rect{position:absolute;left:-1px;bottom:-1px;width:0;height:0;border:1px solid #1F1F1F;background:rgba(139,107,74,0.08);box-sizing:border-box;opacity:0;transition:width 0.8s var(--ease),height 0.8s var(--ease),opacity 0.5s var(--ease);}
    .bs-plan.is-set .bs-plan-rect{opacity:1;}
    .bs-plan-dim{display:flex;align-items:center;gap:8px;margin-top:10px;}
    .bs-plan-dim i{flex:1;height:5px;border:solid #8B6B4A;border-width:0 0 1px 1px;}
    .bs-plan-dim i:last-child{border-width:0 1px 1px 0;}
    .bs-plan-label{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.1em;color:#8B6B4A;white-space:nowrap;}
    .bs-foot{position:relative;display:flex;justify-content:space-between;gap:16px;padding:13px 24px;border-top:1px solid #1F1F1F;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.18em;text-transform:uppercase;color:#8B7A6B;}
    .bs.is-complete .bs-count{color:#8B6B4A;}
    .bs-like{display:grid;grid-template-columns:104px minmax(0,1fr);gap:16px;align-items:center;margin-top:18px;text-decoration:none;color:inherit;}
    .bs-like[hidden],.bs-empty[hidden]{display:none;}
    .bs-empty{display:flex;align-items:center;gap:12px;margin:16px 0 0;font-family:'Lama Sans',sans-serif;font-size:13px;line-height:1.6;color:#8B7A6B;}
    .bs-empty::before{content:"";flex:none;width:20px;height:1px;background:#B8A08C;}
    .bs-like-img{position:relative;display:block;aspect-ratio:4/3;overflow:hidden;background:#E8DFD8;}
    .bs-like-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1s var(--ease);}
    .bs-like:hover img,.bs-like:focus-visible img{transform:scale(1.05);}
    .bs-like small{display:block;font-family:'Lama Sans',sans-serif;font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#8B6B4A;}
    .bs-like b{display:block;margin-top:5px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:15px;color:#1F1F1F;}
    .bs-like em{display:inline-flex;align-items:center;gap:8px;margin-top:6px;font-style:normal;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.18em;text-transform:uppercase;color:#5B4636;transition:gap 0.4s var(--ease);}
    .bs-like:hover em,.bs-like:focus-visible em{gap:14px;}
    /* direct lines */
    .cd{background:#FFFFFF;--ease:%(e)s;}
    .cd-wrap{max-width:1280px;margin:0 auto;box-sizing:border-box;padding:0 0 clamp(64px,8vw,104px);}
    .cd-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px;margin:0;padding:0;list-style:none;}
    .cd-list a,.cd-list div{display:grid;grid-template-columns:1fr auto;gap:6px 12px;padding-top:18px;border-top:1px solid #1F1F1F;text-decoration:none;color:inherit;}
    .cd-list small{grid-column:1/-1;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .cd-list b{display:block;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:16px;color:#1F1F1F;transition:color 0.3s var(--ease);}
    .cd-list em{display:block;margin-top:3px;font-style:normal;font-family:'Lama Sans',sans-serif;font-size:12.5px;color:#8B7A6B;}
    .cd-list svg{color:#B8A08C;transition:transform 0.4s var(--ease),color 0.3s var(--ease);}
    .cd-list a:hover b,.cd-list a:focus-visible b{color:#8B6B4A;}
    .cd-list a:hover svg,.cd-list a:focus-visible svg{color:#8B6B4A;transform:translate(3px,-3px);}
    .cd-facts{display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:24px;font-family:'Lama Sans',sans-serif;font-size:12.5px;color:#8B7A6B;}
    .cd-facts b{font-weight:500;color:#1F1F1F;}
    /* next steps */
    .cn{background:#FFFFFF;border-top:1px solid #E8DFD8;}
    .cn-wrap{padding:clamp(72px,9vw,128px) 0;}
    .cn-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(44px,5vw,72px);}
    .cn-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(32px,3.8vw,60px);line-height:1;letter-spacing:-0.035em;color:#1F1F1F;}
    .cn-note{max-width:26em;margin:0;font-family:'Lama Sans',sans-serif;font-size:14px;line-height:1.7;color:#8B7A6B;}
    .cn-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;margin:0;padding:0;list-style:none;}
    .cn-step{position:relative;padding-top:32px;border-top:1px solid #1F1F1F;}
    .cn-step::before{content:"";position:absolute;top:-4px;left:0;width:7px;height:7px;background:#8B6B4A;}
    .cn-n{font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.12em;color:#8B6B4A;}
    .cn-step h3{margin:14px 0 6px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(24px,2.2vw,32px);letter-spacing:-0.02em;color:#1F1F1F;}
    .cn-tag{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .cn-step p{margin:16px 0 0;max-width:24em;font-family:'Lama Sans',sans-serif;font-size:15px;line-height:1.75;color:#5B4636;}
    /* visit */
    .cv{background:#1E1610;}
    .cv-wrap{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:32px;align-items:center;padding:clamp(72px,9vw,128px) 0;}
    .cv-text{grid-column:1/6;}
    .cv .c-label{color:#D6C2A8;}
    .cv-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(32px,3.8vw,60px);line-height:1;letter-spacing:-0.035em;color:#F5F2ED;}
    .cv-h2 span{display:block;color:rgba(214,194,168,0.75);}
    .cv-p{margin:22px 0 0;max-width:30em;font-family:'Lama Sans',sans-serif;font-size:15px;line-height:1.8;color:rgba(245,242,237,0.62);}
    .cv-facts{margin:32px 0 0;border-top:1px solid rgba(214,194,168,0.18);}
    .cv-facts div{display:grid;grid-template-columns:132px 1fr;gap:16px;padding:15px 0;border-bottom:1px solid rgba(214,194,168,0.18);}
    .cv-facts small{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:rgba(214,194,168,0.6);}
    .cv-facts span{font-family:'Lama Sans',sans-serif;font-size:15px;color:#F5F2ED;}
    .cv-acts{display:flex;align-items:center;flex-wrap:wrap;gap:18px 28px;margin-top:34px;}
    .cv-btn{display:inline-flex;align-items:center;gap:14px;padding:18px 30px;background:#D6C2A8;border:1px solid #D6C2A8;color:#1F1F1F;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;white-space:nowrap;transition:background 0.4s var(--ease),color 0.4s var(--ease),gap 0.4s var(--ease);}
    .cv-btn:hover,.cv-btn:focus-visible{background:transparent;color:#D6C2A8;gap:20px;}
    .cv-link{position:relative;display:inline-flex;align-items:center;gap:10px;padding-bottom:6px;color:#F5F2ED;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:color 0.3s var(--ease);}
    .cv-link::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:rgba(214,194,168,0.45);}
    .cv-link:hover,.cv-link:focus-visible{color:#D6C2A8;}
    .cv-map{grid-column:7/13;position:relative;margin:0;}
    .cv-frame{position:relative;overflow:hidden;aspect-ratio:5/4;background:#2A2019;}
    /* the iframe runs 160px past the frame top and bottom: Google's place card sits in that top margin, out of view, and the pin stays centred */
    .cv-frame iframe{position:absolute;left:0;top:-160px;width:100%;height:calc(100% + 320px);border:0;filter:grayscale(1) sepia(0.28) contrast(0.92) brightness(0.96);}
    .cv-cap{display:flex;align-items:center;gap:12px;margin-top:14px;font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.04em;color:rgba(214,194,168,0.7);}
    .cv-cap::before{content:"";display:block;width:20px;height:1px;background:rgba(214,194,168,0.5);}
    @media(max-width:1360px){.ct-wrap,.cn-wrap,.cv-wrap,.cd-wrap{max-width:none;padding-left:clamp(24px,5vw,80px);padding-right:clamp(24px,5vw,80px);}}
    @media(max-width:960px){
      .ct-wrap,.cv-wrap{grid-template-columns:1fr;gap:48px;}
      .ct-intro,.ct-panel,.cv-text,.cv-map{grid-column:1;}
      .ct-intro{position:static;}
      .bf-stage,.bf-side{grid-column:1;}
      .bf-side{position:static;margin:0 calc(-1 * clamp(24px,5vw,80px));}
      .bf-root{min-height:0;}
      .bq-grid{grid-template-columns:1fr;}
      .cd-list{grid-template-columns:1fr 1fr;gap:28px 24px;}
      .ct-panel{margin:0 calc(-1 * clamp(24px,5vw,80px));}
      .cn-steps{grid-template-columns:1fr;gap:40px;}
      .cv-frame{aspect-ratio:4/3;}
    }
    @media(max-width:600px){
      .ct-ch a,.ct-ch div{grid-template-columns:1fr auto;}
      .ct-ch small{grid-column:1/-1;}
      .cv-facts div{grid-template-columns:1fr;gap:4px;}
      .ct-panel-head{flex-direction:column;gap:8px;}
      .bs-body{grid-template-columns:1fr;}
      .bs-plan{border-left:0;border-top:1px solid #E2D7CA;flex-direction:row;align-items:flex-end;gap:16px;}
      .bs-plan-field{width:96px;flex:none;}
      .bs-plan-dim{flex:1;}
      .cd-list{grid-template-columns:1fr;}
      .bq-opt{padding:14px 18px;font-size:14px;}
    }
    @media(prefers-reduced-motion:reduce){
      .ct-in,.rv{opacity:1;transform:none;transition:none;}
      .bq,.bs-plan-rect{transition:none;}
      .bs-row.is-set .bs-v,.bs-v.is-new{animation:none;}
    }
  </style>
""".replace("%(e)s", EASE)


def reveal(delay=None):
    return ' data-reveal%s' % ((' data-reveal-delay="%s"' % delay) if delay else "")


def build():
    h = []
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->')
    h.append('<!-- The Brief: the questions one at a time (brief.js fills #brief-root), and the brief drafting itself beside them (#brief-sheet) -->')
    h.append('<section id="form" data-screen-label="Contact" class="ct" data-contact-hero>')
    h.append(CSS)
    h.append('  <div class="ct-wrap bf">')
    h.append('    <div class="bf-stage">')
    h.append('      <div class="c-label ct-in" style="--d:0.05s;"><i></i>Contact FurnishIQ</div>')
    h.append('      <h1 class="bf-h1 ct-in" style="--d:0.12s;">Start a <span>conversation.</span></h1>')
    h.append('      <p class="bf-status ct-in" id="brief-status" style="--d:0.2s;">A senior consultant replies within one working day.</p>')
    h.append('      <div id="brief-root" class="bf-root ct-in" style="--d:0.3s;"></div>')
    h.append('    </div>')
    h.append('    <div class="bf-side ct-in" style="--d:0.4s;">')
    h.append('      <div id="brief-sheet" class="bs" role="region" aria-label="Your project brief, drafted from your answers"></div>')
    h.append('    </div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ DIRECT LINES ━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Direct" class="cd">')
    h.append('  <div class="cd-wrap">')
    h.append('    <div class="c-label rv"%s><i></i>Prefer to talk directly?</div>' % reveal())
    h.append('    <ul class="cd-list rv"%s>' % reveal("0.08"))
    h.append('      <li><a href="mailto:info@furnishiq.net"><small>Email</small><span><b>info@furnishiq.net</b><em>Briefs, drawings &amp; RFPs</em></span>%s</a></li>' % ARROW_UR)
    h.append('      <li><a href="tel:+966580330627"><small>Phone</small><span><b>+966 58 033 0627</b><em>Ibrahim Al Ali, Projects</em></span>%s</a></li>' % ARROW_UR)
    h.append('      <li><a href="https://wa.me/966580330627" target="_blank" rel="noopener" id="id-contact-wa"><small>WhatsApp</small><span><b>Message us directly</b><em>Fastest first response</em></span>%s</a></li>' % ARROW_UR)
    h.append('      <li><div><small>Hours</small><span><b>Sun – Thu · 9:00 – 18:00</b><em>Riyadh, Saudi Arabia (AST)</em></span></div></li>')
    h.append('    </ul>')
    h.append('    <div class="cd-facts rv"%s><span>Coverage <b>All regions of Saudi Arabia</b></span><span>Languages <b>English &amp; <span lang="ar" dir="rtl" style="font-family:\'GE SS Two\',\'Arial\',sans-serif;">العربية</span></b></span></div>' % reveal("0.12"))
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ WHAT HAPPENS NEXT ━━━━━━━ -->')
    h.append('<section data-screen-label="Next Steps" class="cn">')
    h.append('  <div class="cn-wrap">')
    h.append('    <div class="cn-head">')
    h.append('      <div><div class="c-label rv"%s><i></i>After you reach out</div><h2 class="cn-h2 rv"%s>What happens next.</h2></div>' % (reveal(), reveal("0.08")))
    h.append('      <p class="cn-note rv"%s>No obligation at any step: the proposal comes before any commitment.</p>' % reveal("0.12"))
    h.append('    </div>')
    h.append('    <ol class="cn-steps">')
    steps = [
        ("01", "We listen", "Within one working day", "A senior consultant, not a call centre, reviews your inquiry and schedules a discovery conversation at a time that suits you."),
        ("02", "We visit", "Site &amp; scope", "We survey the space, understand how you'll use it, and align on ambition, constraints and timeline, face to face where possible."),
        ("03", "We propose", "Plan &amp; roadmap", "You receive a clear proposal: scope, photoreal direction and a comprehensive budget roadmap, before committing to anything."),
    ]
    for k, (n, t, tag, p) in enumerate(steps):
        h.append('      <li class="cn-step rv"%s><span class="cn-n">%s</span><h3>%s</h3><div class="cn-tag">%s</div><p>%s</p></li>' % (reveal("%.2f" % (0.08 * k) if k else None), n, t, tag, p))
    h.append('    </ol>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ VISIT ━━━━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Visit" class="cv">')
    h.append('  <div class="cv-wrap">')
    h.append('    <div class="cv-text">')
    h.append('      <div class="c-label rv"%s><i></i>Visit the studio</div>' % reveal())
    h.append('      <h2 class="cv-h2 rv"%s>See materials. <span>Touch finishes.</span></h2>' % reveal("0.08"))
    h.append('      <p class="cv-p rv"%s>Some decisions deserve to be made in person. Book a studio session to explore material libraries, finish samples and past project work.</p>' % reveal("0.14"))
    h.append('      <div class="cv-facts rv"%s><div><small>Address</small><span>Riyadh, Kingdom of Saudi Arabia</span></div><div><small>By appointment</small><span>Sunday – Thursday · 9:00 – 18:00</span></div></div>' % reveal("0.2"))
    h.append('      <div class="cv-acts rv"%s>' % reveal("0.26"))
    h.append('        <a href="#form" id="id-visit-cta" class="cv-btn">Book a studio visit %s</a>' % ARROW)
    h.append('        <a href="https://www.google.com/maps?cid=%s" target="_blank" rel="noopener" class="cv-link">Open in Google Maps %s</a>' % (MAP_CID, ARROW_UR))
    h.append('      </div>')
    h.append('    </div>')
    h.append('    <figure class="cv-map rv"%s>' % reveal("0.18"))
    h.append('      <div class="cv-frame"><iframe src="https://www.google.com/maps?cid=%s&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="FurnishIQ location on Google Maps"></iframe></div>' % MAP_CID)
    h.append('      <figcaption class="cv-cap">The FurnishIQ studio, Riyadh</figcaption>')
    h.append('    </figure>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    return "\n".join(h) + "\n"


NAV_PAIRS = [
    ("      const s = window.scrollY > 60;\n      if (!nav) return;\n",
     "      const s = window.scrollY > 60;\n      if (!nav) return;\n      const dark = s || nav.hasAttribute('data-nav-dark');   // white first screen: dark text from the top\n"),
    ("      if (logoW) logoW.style.opacity = s ? '0' : '1';\n      if (logoD) logoD.style.opacity = s ? '1' : '0';",
     "      if (logoW) logoW.style.opacity = dark ? '0' : '1';\n      if (logoD) logoD.style.opacity = dark ? '1' : '0';"),
    ("        l.style.color = s ? '#1F1F1F' : '#FFFFFF';\n        if (l !== navContactLink) l.style.opacity = s ? '1' : '0.8';",
     "        l.style.color = dark ? '#1F1F1F' : '#FFFFFF';\n        if (l !== navContactLink) l.style.opacity = dark ? '1' : '0.8';"),
    ("        navCta.style.color = s ? '#1F1F1F' : '#FFFFFF';\n        navCta.style.borderColor = s ? 'rgba(91,70,54,0.35)' : 'rgba(214,194,168,0.5)';",
     "        navCta.style.color = dark ? '#1F1F1F' : '#FFFFFF';\n        navCta.style.borderColor = dark ? 'rgba(91,70,54,0.35)' : 'rgba(214,194,168,0.5)';"),
    ("l.style.opacity = window.scrollY > 60 ? '1' : '0.8';",
     "l.style.opacity = (window.scrollY > 60 || nav.hasAttribute('data-nav-dark')) ? '1' : '0.8';"),
    ("navCta.style.background = window.scrollY > 60 ? '#3A2D25' : 'rgba(255,255,255,0.1)';",
     "navCta.style.background = (window.scrollY > 60 || nav.hasAttribute('data-nav-dark')) ? '#3A2D25' : 'rgba(255,255,255,0.1)';"),
]


def main():
    s = io.open(PAGE, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    if 'class="ct"' in s:
        print(PAGE, "already rebuilt")
        return
    a = s.index("<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->")
    b = s.index("<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ FOOTER")
    s = s[:a] + build() + s[b:]
    # styles for the sections that are gone
    a = s.index("    .journey-card {")
    b = s.index("    @media(max-width:960px){", a)
    s = s[:a] + s[b:]
    s = re.sub(r"\n\s*\.(fiq-hero-grid|fiq-hero-side|fiq-channel-strip|fiq-contact-cols|fiq-contact-left|journey-cards-grid|fiq-visit-map)\{[^\n]*", "", s)
    # nav starts dark over the white first screen
    assert s.count('<nav id="id-nav" style=') == 1
    s = s.replace('<nav id="id-nav" style=', '<nav id="id-nav" data-nav-dark style=')
    for o, n in NAV_PAIRS:
        assert s.count(o) == 1, o
        s = s.replace(o, n)
    # script: a plain entrance in place of the word reveal; the channel cards' hover is now CSS
    a = s.index("    // ── HERO ENTRANCE")
    b = s.index("    // ── SCROLL REVEAL")
    s = s[:a] + """    // ── HERO ENTRANCE ──────────────────────────────────────
    const hero = document.querySelector('[data-contact-hero]');
    if (hero) requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
    // brief.js: the questions and the drafting sheet. It may load after this render: then it starts itself on this flag
    if (window.FIQBrief) window.FIQBrief(); else window.FIQBriefPending = true;

""" + s[b:]
    # the old form's channel hover, phone focus and country lookup (brief.js has its own)
    a = s.index("    // ── CHANNEL CARD HOVER")
    b = s.index("\n  }\n}\n</script>", a)
    s = s[:a].rstrip() + "\n" + s[b:]
    # brief.js alongside the page's other shared scripts
    o = '<script src="./newsletter.js" defer></script>'
    assert s.count(o) == 1
    s = s.replace(o, o + '\n<script src="./brief.js" defer></script>')
    io.open(PAGE, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(PAGE, "rebuilt")


if __name__ == "__main__":
    main()
