"""Contact page: the letter, and the studio visit.

The first screen is a letter to the studio, laid over mashrabiya light on a limewash wall (contact-letter.js fills
#letter-root): its blanks are the form, choices open in place, the "feel" line takes material swatches cut from the
project photography, and it is sent as written (POST /api/send-email, formType "contact") or on WhatsApp. Then the
direct lines, the three next steps, and the visit: a full-width live Google map with the studio's pin in its right
half, and over its left side a glass panel with the visit details and a request for a day and a time of day, sent by
WhatsApp or email (contact-letter.js fills #visit-root). The Brief, an earlier first screen, is parked in
contact_brief_layout.py.
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
    /* the letter */
    .ct.lw-sec{position:relative;z-index:2;overflow-x:clip;overflow-y:visible;background:#F5F2ED;min-height:100svh;display:flex;flex-direction:column;justify-content:center;}
    .lw-sec .ct-wrap{width:100%;padding-top:clamp(96px,12vh,128px);padding-bottom:clamp(24px,4vh,48px);}
    /* mashrabiya light on limewash: the letter lies in it; the light drifts as slowly as the sun would. The photo has a
       soft vertical shaft of light about 38% across: at 132% wide from the left it falls behind the glass letter, not beside it */
    .lw-bg{position:absolute;inset:0;z-index:0;overflow:hidden;}
    .lw-bg img{position:absolute;left:-2%;top:-6%;width:132%;height:112%;max-width:none;object-fit:cover;object-position:left 40%;animation:lw-drift 48s var(--ease) infinite alternate;}
    .lw-bg::after{content:"";position:absolute;inset:0;background:rgba(245,242,237,0.32);}
    @keyframes lw-drift{from{transform:translate3d(0,0,0);}to{transform:translate3d(-2%,1.2%,0);}}
    .lw{position:relative;z-index:1;}
    .lw{align-items:start;}
    .lw-intro{grid-column:1/5;position:sticky;top:112px;}
    .lw-h1{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(40px,4.2vw,68px);line-height:0.98;letter-spacing:-0.04em;color:#1F1F1F;}
    .lw-h1 span{display:block;color:#8B6B4A;}
    .lw-status{display:flex;align-items:flex-start;gap:12px;margin:clamp(20px,3vh,28px) 0 0;font-family:'Lama Sans',sans-serif;font-size:13.5px;line-height:1.6;color:#5B4636;}
    .lw-status::before{content:"";flex:none;width:7px;height:7px;margin-top:6px;border:1px solid #8B6B4A;}
    .lw-status.is-open::before{background:#8B6B4A;}
    .lw-how{margin:18px 0 0;padding-top:18px;border-top:1px solid rgba(91,70,54,0.25);font-family:'Lama Sans',sans-serif;font-size:13.5px;line-height:1.7;color:#5B4636;}
    .lw-letter{grid-column:5/13;position:relative;}
    .lt-sheet{position:relative;background:rgba(255,255,255,0.62);-webkit-backdrop-filter:blur(22px) saturate(1.15);backdrop-filter:blur(22px) saturate(1.15);border:1px solid rgba(255,255,255,0.75);padding:clamp(24px,min(3.6vw,5vh),56px);box-shadow:0 24px 80px rgba(58,45,37,0.16),inset 0 1px 0 rgba(255,255,255,0.6);}
    .lt-head{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:clamp(18px,3.2vh,40px);padding-bottom:clamp(12px,2vh,18px);border-bottom:1px solid #E8DFD8;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.24em;text-transform:uppercase;color:#8B6B4A;}
    .lt-p,.lt-ruler{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(16px,min(1.42vw,2.5vh),23px);letter-spacing:-0.01em;}
    .lt-p{margin:0 0 0.7em;line-height:1.75;color:#5B4636;}
    .lt-salute{color:#1F1F1F;}
    .lt-ruler{position:absolute;left:-9999px;top:0;visibility:hidden;white-space:pre;}
    .lt-blank,.lt-input,.lt-code,.lt-notes{font:inherit;letter-spacing:inherit;color:#1F1F1F;background:transparent;border:0;border-bottom:1px solid #B8A08C;border-radius:0;padding:0 2px;margin:0;box-shadow:none;outline:none;transition:border-color 0.3s var(--ease),color 0.3s var(--ease);}
    .lt-blank{cursor:pointer;color:#A08770;text-align:left;line-height:1.25;}
    .lt-blank.is-set{color:#1F1F1F;border-bottom-color:#1F1F1F;}
    .lt-blank:hover,.lt-blank[aria-expanded="true"]{border-bottom-color:#8B6B4A;color:#8B6B4A;}
    .lt-blank:focus-visible,.lt-input:focus,.lt-code:focus-visible,.lt-notes:focus{border-bottom-color:#1F1F1F;outline:1px solid #D6C2A8;outline-offset:4px;}
    .lt-input{min-width:2ch;max-width:100%;height:auto;line-height:1.25;vertical-align:baseline;}
    .lt-code{line-height:1.25;}
    .lt-input::placeholder,.lt-notes::placeholder{color:#AE9883;opacity:1;}
    .lt-blank.is-missing,.lt-input.is-missing{border-bottom-color:#C0392B;color:#C0392B;}
    .lt-input.is-missing::placeholder{color:#C0392B;}
    .lt-chip{display:inline-flex;align-items:center;gap:0.3em;white-space:nowrap;}
    .lt-chip img{width:0.95em;height:0.95em;object-fit:cover;border:1px solid rgba(31,31,31,0.12);}
    .lt-phone{white-space:nowrap;}
    .lt-code{-webkit-appearance:none;appearance:none;padding:0 4px 0 2px;margin-right:8px;color:#5B4636;cursor:pointer;}
    .lt-ps{display:flex;gap:0.5em;align-items:baseline;}
    .lt-ps-k{flex:none;color:#8B6B4A;}
    .lt-notes{flex:1;min-width:0;width:100%;resize:none;overflow:hidden;line-height:1.75;border-bottom-style:dashed;border-bottom-color:#D9CDBF;}
    .lt-sign{display:flex;flex-direction:column;align-items:flex-start;gap:4px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(16px,min(1.42vw,2.5vh),23px);color:#5B4636;}
    .lt-end{display:flex;justify-content:space-between;align-items:flex-end;gap:20px 32px;flex-wrap:wrap;margin-top:clamp(14px,2.6vh,32px);}
    .lt-end-acts{display:flex;flex-direction:column;align-items:flex-end;gap:10px;}
    .lt-sign .lt-name{font-size:1.45em;letter-spacing:-0.025em;}
    .lt-company .lt-input{font-size:0.62em;letter-spacing:0.02em;color:#5B4636;}
    .lt-menu{position:absolute;z-index:30;min-width:260px;max-width:min(560px,calc(100% - 32px));background:#FFFFFF;border:1px solid #1F1F1F;padding:10px;box-shadow:0 24px 80px rgba(58,45,37,0.20);opacity:0;transform:translateY(8px);transition:opacity 0.3s var(--ease),transform 0.3s var(--ease);}
    .lt-menu.is-in{opacity:1;transform:none;}
    .lt-menu-hint{margin:4px 6px 10px;font-family:'Lama Sans',sans-serif;font-size:12px;color:#8B7A6B;}
    .lt-opts{display:flex;flex-direction:column;}
    .lt-opt{display:flex;align-items:center;gap:12px;width:100%;padding:11px 12px;background:transparent;border:0;border-bottom:1px solid #F0EAE2;cursor:pointer;text-align:left;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;transition:background 0.2s var(--ease),color 0.2s var(--ease);}
    .lt-opt:last-child{border-bottom:0;}
    .lt-opt:hover,.lt-opt:focus-visible{background:#F5F2ED;outline:none;}
    .lt-opt[aria-pressed="true"]{background:#1F1F1F;color:#F5F2ED;}
    .lt-menu.is-swatches{width:min(520px,calc(100% - 32px));}
    .is-swatches .lt-opts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;}
    .is-swatches .lt-opt{flex-direction:column;align-items:stretch;gap:8px;padding:6px;border:1px solid transparent;}
    .is-swatches .lt-opt[aria-pressed="true"]{background:transparent;color:#1F1F1F;border-color:#1F1F1F;}
    .lt-sw{display:block;aspect-ratio:4/3;overflow:hidden;background:#E8DFD8;}
    .lt-sw img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 0.6s var(--ease);}
    .is-swatches .lt-opt:hover .lt-sw img{transform:scale(1.06);}
    .lt-opt-t{font-size:14px;}
    .lt-done{display:inline-flex;align-items:center;gap:12px;margin:10px 6px 4px;padding:12px 20px;background:#1F1F1F;border:0;color:#F5F2ED;cursor:pointer;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;}
    .lt-acts{display:flex;align-items:center;flex-wrap:wrap;justify-content:flex-end;gap:14px 28px;}
    .lt-send{display:inline-flex;align-items:center;gap:14px;padding:19px 34px;background:#1F1F1F;border:1px solid #1F1F1F;color:#F5F2ED;cursor:pointer;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;white-space:nowrap;transition:background 0.4s var(--ease),gap 0.4s var(--ease),opacity 0.3s;}
    .lt-send:hover,.lt-send:focus-visible{background:#3A2D25;gap:20px;}
    .lt-send:disabled{opacity:0.4;cursor:default;}
    .lt-wa{position:relative;display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;color:#1F1F1F;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:color 0.3s var(--ease),gap 0.4s var(--ease);}
    .lt-wa::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:#8B6B4A;}
    .lt-wa:hover,.lt-wa:focus-visible{color:#8B6B4A;gap:18px;}
    .lt-note{margin:0;font-family:'Lama Sans',sans-serif;font-size:13px;color:#C0392B;text-align:right;}
    .lt-note:not(:empty){margin-top:14px;}
    .lt-fine{margin:0;font-family:'Lama Sans',sans-serif;font-size:11px;color:#8B7A6B;}
    .lt-hp{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;}
    /* direct lines: the studio's clock, and its card */
    .cd{background:#FFFFFF;--ease:%(e)s;}
    .cd-wrap{max-width:1280px;margin:0 auto;box-sizing:border-box;padding:clamp(72px,9vw,128px) 0;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:32px;align-items:center;}
    .cd-clock{grid-column:1/6;}
    .cd-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(32px,3.6vw,56px);line-height:1;letter-spacing:-0.035em;color:#1F1F1F;}
    .cd-h2 span{display:block;color:#8B6B4A;}
    .ck{margin-top:clamp(32px,4vw,52px);padding-top:28px;border-top:1px solid #1F1F1F;}
    .ck-time{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;}
    .ck-time b{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(64px,7vw,112px);line-height:0.9;letter-spacing:-0.05em;color:#1F1F1F;font-variant-numeric:tabular-nums;}
    .ck-time span{font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.24em;text-transform:uppercase;color:#8B6B4A;}
    .ck-state{display:flex;align-items:center;gap:12px;margin:18px 0 0;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;}
    .ck-state::before{content:"";flex:none;width:8px;height:8px;border:1px solid #8B6B4A;}
    .ck-state.is-open::before{background:#8B6B4A;}
    .ck-week{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px;margin-top:28px;}
    .ck-day{display:flex;flex-direction:column;align-items:center;gap:6px;padding:10px 0 9px;border:1px solid #E2D7CA;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:#1F1F1F;}
    .ck-day small{font-size:9px;letter-spacing:0.1em;text-transform:none;color:#8B7A6B;}
    .ck-day.is-off{border-style:dashed;color:#B8A08C;}
    .ck-day.is-off small{color:#C4B3A2;}
    .ck-day.is-today{background:#1F1F1F;border-color:#1F1F1F;color:#F5F2ED;}
    .ck-day.is-today small{color:#D6C2A8;}
    .ck-ruler{position:relative;height:30px;margin-top:26px;}
    .ck-ruler i{position:absolute;top:10px;left:0;right:0;height:1px;background:#E2D7CA;}
    .ck-ruler em{position:absolute;top:7px;height:7px;background:#D6C2A8;left:37.5%;width:37.5%;}
    .ck-ruler u{position:absolute;top:0;width:1px;height:22px;background:#1F1F1F;text-decoration:none;transition:left 1s var(--ease);}
    .ck-ruler u::before{content:"";position:absolute;top:-3px;left:-3px;width:7px;height:7px;background:#1F1F1F;}
    .ck-scale{position:relative;height:14px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.08em;color:#8B7A6B;}
    .ck-scale span{position:absolute;top:0;transform:translateX(-50%);white-space:nowrap;}
    .ck-scale span:first-child{transform:none;}
    .ck-scale span:last-child{transform:translateX(-100%);}
    .cd-card{grid-column:7/13;position:relative;background:#1F1F1F;color:#F5F2ED;padding:clamp(32px,3.6vw,56px);box-shadow:0 24px 80px rgba(58,45,37,0.2);}
    .cd-card::before{content:"";position:absolute;inset:10px;border:1px solid rgba(214,194,168,0.22);pointer-events:none;}
    .cd-card-head{position:relative;display:flex;justify-content:space-between;align-items:center;gap:16px;padding-bottom:clamp(20px,2.4vw,32px);border-bottom:1px solid rgba(214,194,168,0.22);}
    .cd-card-head img{display:block;height:34px;width:auto;}
    .cd-card-head span{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.26em;text-transform:uppercase;color:rgba(214,194,168,0.75);}
    .cd-lines{position:relative;margin:0;padding:0;list-style:none;}
    .cd-line{display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:8px 20px;align-items:center;padding:clamp(16px,1.8vw,22px) 0;border-bottom:1px solid rgba(214,194,168,0.16);}
    .cd-line small{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:rgba(214,194,168,0.65);}
    .cd-line a.cd-v{min-width:0;color:#F5F2ED;text-decoration:none;}
    .cd-v b{display:block;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(19px,1.7vw,26px);letter-spacing:-0.015em;line-height:1.2;overflow-wrap:anywhere;transition:color 0.3s var(--ease);}
    .cd-v em{display:block;margin-top:4px;font-style:normal;font-family:'Lama Sans',sans-serif;font-size:12.5px;color:rgba(245,242,237,0.55);}
    .cd-v:hover b,.cd-v:focus-visible b{color:#D6C2A8;}
    .cd-act{display:inline-flex;align-items:center;gap:10px;padding:10px 0;background:none;border:0;cursor:pointer;color:#D6C2A8;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;white-space:nowrap;transition:color 0.3s var(--ease),gap 0.3s var(--ease);}
    .cd-act:hover,.cd-act:focus-visible{color:#F5F2ED;gap:14px;}
    .cd-card-foot{position:relative;display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:clamp(18px,2vw,26px);font-family:'Lama Sans',sans-serif;font-size:12.5px;color:rgba(245,242,237,0.55);}
    .cd-card-foot b{font-weight:500;color:#F5F2ED;}
    /* next steps: a staircase drawn in section, one hairline that treads and rises from the first conversation to the proposal */
    .cn{background:#F5F2ED;--rise:clamp(56px,7vw,104px);}
    .cn-wrap{padding:clamp(72px,9vw,128px) 0;}
    .cn-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(40px,5vw,72px);}
    .cn-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(32px,3.8vw,60px);line-height:1;letter-spacing:-0.035em;color:#1F1F1F;}
    .cn-note{max-width:24em;margin:0;font-family:'Lama Sans',sans-serif;font-size:14px;line-height:1.7;color:#5B4636;}
    .cn-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;align-items:start;margin:0;padding:0;list-style:none;}
    .cn-step{position:relative;padding-top:26px;}
    .cn-step:nth-child(1){margin-top:calc(var(--rise) * 2);}
    .cn-step:nth-child(2){margin-top:var(--rise);}
    /* the tread: across the step and half the gap either side; the riser: down to the step before */
    .cn-step::before{content:"";position:absolute;top:0;left:-16px;right:-16px;height:1px;background:#1F1F1F;}
    .cn-step:first-child::before{left:0;}
    .cn-step:last-child::before{right:0;}
    .cn-step + .cn-step::after{content:"";position:absolute;top:0;left:-16px;width:1px;height:var(--rise);background:#1F1F1F;}
    .cn-node{position:absolute;top:-4px;left:0;width:9px;height:9px;background:#8B6B4A;}
    .cn-meta{display:flex;align-items:baseline;gap:14px;margin-bottom:18px;}
    .cn-n{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(40px,3.6vw,60px);line-height:0.9;letter-spacing:-0.04em;color:transparent;-webkit-text-stroke:1px #8B6B4A;}
    .cn-tag{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .cn-frame{position:relative;overflow:hidden;aspect-ratio:4/3;background:#E8DFD8;}
    .cn-frame img{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;transition:transform 1.2s var(--ease);}
    .cn-step:hover .cn-frame img{transform:scale(1.04);}
    .cn-step h3{margin:22px 0 0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(24px,2.2vw,34px);letter-spacing:-0.025em;color:#1F1F1F;}
    .cn-step p{margin:12px 0 0;max-width:26em;font-family:'Lama Sans',sans-serif;font-size:15px;line-height:1.75;color:#5B4636;}
    /* visit: a live map across the section, the studio's pin in its right half, the words on glass to the left */
    .cv{position:relative;overflow:hidden;background:#1E1610;}
    .cv-map-bg{position:absolute;inset:0;z-index:0;}
    /* 150% wide from the left edge puts the map's centre, and the pin, at three quarters of the section's width;
       220px past the top and bottom keeps Google's place card out of view and the pin centred in height */
    .cv-map-bg iframe{position:absolute;left:0;top:-220px;width:150%;height:calc(100% + 440px);border:0;filter:grayscale(0.85) sepia(0.22) contrast(0.95);}
    .cv-wrap{position:relative;z-index:1;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:32px;align-items:start;padding:clamp(72px,9vw,128px) 0;pointer-events:none;}
    .cv-text{grid-column:1/6;pointer-events:auto;background:rgba(30,22,16,0.66);-webkit-backdrop-filter:blur(18px) saturate(1.1);backdrop-filter:blur(18px) saturate(1.1);border:1px solid rgba(214,194,168,0.22);padding:clamp(32px,3.4vw,52px);box-shadow:0 24px 80px rgba(0,0,0,0.35);}
    .cv .c-label{color:#D6C2A8;}
    .cv-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(32px,3.8vw,60px);line-height:1;letter-spacing:-0.035em;color:#F5F2ED;}
    .cv-h2 span{display:block;color:rgba(214,194,168,0.75);}
    .cv-p{margin:22px 0 0;max-width:30em;font-family:'Lama Sans',sans-serif;font-size:15px;line-height:1.8;color:rgba(245,242,237,0.62);}
    .cv-facts{margin:28px 0 0;border-top:1px solid rgba(214,194,168,0.18);}
    .cv-facts div{display:grid;grid-template-columns:132px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid rgba(214,194,168,0.18);}
    .cv-facts small{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:rgba(214,194,168,0.6);}
    .cv-facts span{font-family:'Lama Sans',sans-serif;font-size:15px;color:#F5F2ED;}
    .vs-label{margin:30px 0 12px;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.24em;text-transform:uppercase;color:rgba(214,194,168,0.65);}
    .vs-days{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;}
    .vs-day,.vs-slot{display:flex;flex-direction:column;align-items:center;gap:2px;padding:12px 6px;background:transparent;border:1px solid rgba(214,194,168,0.25);color:#F5F2ED;cursor:pointer;font-family:'Lama Sans',sans-serif;transition:background 0.3s var(--ease),color 0.3s var(--ease),border-color 0.3s var(--ease);}
    .vs-day small{font-size:9.5px;letter-spacing:0.18em;text-transform:uppercase;color:rgba(214,194,168,0.75);}
    .vs-day b{font-weight:500;font-size:26px;line-height:1.1;letter-spacing:-0.02em;}
    .vs-day span,.vs-slot span{font-size:11px;color:rgba(245,242,237,0.55);}
    .vs-slots{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;}
    .vs-slot b{font-weight:500;font-size:15px;}
    .vs-day:hover,.vs-slot:hover,.vs-day:focus-visible,.vs-slot:focus-visible{border-color:#D6C2A8;outline:none;}
    .vs-day[aria-pressed="true"],.vs-slot[aria-pressed="true"]{background:#D6C2A8;border-color:#D6C2A8;color:#1F1F1F;}
    .vs-day[aria-pressed="true"] small,.vs-day[aria-pressed="true"] span,.vs-slot[aria-pressed="true"] span{color:#5B4636;}
    .vs-slot:disabled{opacity:0.28;cursor:default;border-color:rgba(214,194,168,0.25);}
    .vs-acts{display:flex;align-items:center;flex-wrap:wrap;gap:16px 28px;margin-top:28px;}
    .vs-cta{display:inline-flex;align-items:center;gap:14px;padding:18px 30px;background:#D6C2A8;border:1px solid #D6C2A8;color:#1F1F1F;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:background 0.4s var(--ease),color 0.4s var(--ease),gap 0.4s var(--ease);}
    .vs-cta:not(.is-off):hover,.vs-cta:not(.is-off):focus-visible{background:transparent;color:#D6C2A8;gap:20px;}
    .vs-cta.is-off{background:transparent;border-style:dashed;border-color:rgba(214,194,168,0.35);color:rgba(214,194,168,0.6);cursor:default;}
    .vs-mail{position:relative;padding-bottom:5px;color:#F5F2ED;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;}
    .vs-mail::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:rgba(214,194,168,0.45);}
    .vs-mail[hidden]{display:none;}
    .vs-mail:hover,.vs-mail:focus-visible{color:#D6C2A8;}
    .vs-fine{margin:14px 0 0;font-family:'Lama Sans',sans-serif;font-size:12px;color:rgba(214,194,168,0.55);}
    .cv-maplink{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-top:26px;padding-top:20px;border-top:1px solid rgba(214,194,168,0.18);}
    .cv-cap{display:flex;align-items:center;gap:12px;font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.04em;color:rgba(214,194,168,0.7);}
    .cv-cap::before{content:"";display:block;width:20px;height:1px;background:rgba(214,194,168,0.5);}
    .cv-link{position:relative;display:inline-flex;align-items:center;gap:10px;padding-bottom:6px;color:#F5F2ED;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:color 0.3s var(--ease);}
    .cv-link::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:rgba(214,194,168,0.45);}
    .cv-link:hover,.cv-link:focus-visible{color:#D6C2A8;}
    @media(max-width:1360px){.ct-wrap,.cn-wrap,.cv-wrap,.cd-wrap{max-width:none;padding-left:clamp(24px,5vw,80px);padding-right:clamp(24px,5vw,80px);}}
    @media(max-width:960px){
      .ct-wrap,.cv-wrap{grid-template-columns:1fr;gap:48px;}
      .ct-intro,.ct-panel,.cv-text,.cv-map,.lw-intro,.lw-letter{grid-column:1;}
      .lw-intro{position:static;}
      .ct.lw-sec{min-height:0;display:block;}
      .lt-end,.lt-end-acts{align-items:flex-start;}
      .lt-acts{justify-content:flex-start;}
      .lt-note{text-align:left;}
      .cv-map-bg{position:relative;height:360px;}
      .cv-map-bg iframe{width:100%;}
      .cv-wrap{padding-top:0;}
      .cv-text{margin:-48px 0 0;}
      .lw-letter{margin:0 calc(-1 * clamp(24px,5vw,80px));}
      .lt-sheet{border-left:0;border-right:0;}
      .ct-intro{position:static;}
      .cd-wrap{grid-template-columns:1fr;gap:48px;}
      .cd-clock,.cd-card{grid-column:1;}
      .cd-card{margin:0 calc(-1 * clamp(24px,5vw,80px));}
      .ct-panel{margin:0 calc(-1 * clamp(24px,5vw,80px));}
      .cn-steps{grid-template-columns:1fr;gap:48px;}
      .cn-step:nth-child(n){margin-top:0;}
      .cn-step::before{left:0;right:0;}
      .cn-step + .cn-step::after{display:none;}
    }
    @media(max-width:600px){
      .ct-ch a,.ct-ch div{grid-template-columns:1fr auto;}
      .ct-ch small{grid-column:1/-1;}
      .cv-facts div{grid-template-columns:1fr;gap:4px;}
      .ct-panel-head{flex-direction:column;gap:8px;}
      .cd-line{grid-template-columns:1fr auto;}
      .cd-line small{grid-column:1/-1;}
      .vs-day b{font-size:21px;}
      .is-swatches .lt-opts{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;}
      .is-swatches .lt-opt{padding:4px;}
      .lt-opt-t{font-size:12.5px;}
    }
    @media(prefers-reduced-motion:reduce){
      .ct-in,.rv{opacity:1;transform:none;transition:none;}
      .cn-frame img{transition:none;}
      .lt-menu{transition:none;}
      .lw-bg img{animation:none;}
    }
  </style>
""".replace("%(e)s", EASE)


def reveal(delay=None):
    return ' data-reveal%s' % ((' data-reveal-delay="%s"' % delay) if delay else "")


def build():
    h = []
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->')
    h.append('<!-- The letter: the blanks are the form (contact-letter.js fills #letter-root) -->')
    h.append('<section id="form" data-screen-label="Contact" class="ct lw-sec" data-contact-hero>')
    h.append(CSS)
    h.append('  <div class="lw-bg" aria-hidden="true"><img src="uploads/mashrabiya-light-limewash-wall-texture-1920.webp" alt="" fetchpriority="high" decoding="async"></div>')
    h.append('  <div class="ct-wrap lw">')
    h.append('    <div class="lw-intro">')
    h.append('      <div class="c-label ct-in" style="--d:0.05s;"><i></i>Contact FurnishIQ</div>')
    h.append('      <h1 class="lw-h1 ct-in" style="--d:0.12s;">Write to <span>the studio.</span></h1>')
    h.append('      <p class="lw-status ct-in" id="letter-status" style="--d:0.2s;">A senior consultant replies within one working day.</p>')
    h.append('      <p class="lw-how ct-in" style="--d:0.28s;">Tap a blank to choose, type where it asks, and send the letter as it reads. Nothing more to fill in.</p>')
    h.append('    </div>')
    h.append('    <div id="letter-root" class="lw-letter ct-in" style="--d:0.3s;"></div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ DIRECT LINES ━━━━━━━━━━━━ -->')
    h.append('<!-- The studio, right now: its clock in Riyadh (contact-letter.js fills #direct-clock), and its card -->')
    h.append('<section data-screen-label="Direct" class="cd">')
    h.append('  <div class="cd-wrap">')
    h.append('    <div class="cd-clock">')
    h.append('      <div class="c-label rv"%s><i></i>Prefer to talk directly?</div>' % reveal())
    h.append('      <h2 class="cd-h2 rv"%s>The studio, <span>right now.</span></h2>' % reveal("0.08"))
    h.append('      <div id="direct-clock" class="ck rv"%s><p class="ck-state">Sunday to Thursday, 9:00 to 18:00, Riyadh time.</p></div>' % reveal("0.14"))
    h.append('    </div>')
    h.append('    <div class="cd-card rv"%s>' % reveal("0.12"))
    h.append('      <div class="cd-card-head"><img src="assets/logo-default.png" width="264" height="90" alt="FurnishIQ" loading="lazy"><span>Studio · Riyadh</span></div>')
    h.append('      <ul class="cd-lines">')
    h.append('        <li class="cd-line"><small>Email</small><a class="cd-v" href="mailto:info@furnishiq.net"><b>info@furnishiq.net</b><em>Briefs, drawings &amp; RFPs</em></a><button type="button" class="cd-act" data-copy="info@furnishiq.net">Copy</button></li>')
    h.append('        <li class="cd-line"><small>Phone</small><a class="cd-v" href="tel:+966580330627"><b>+966 58 033 0627</b><em>Ibrahim Al Ali, Projects</em></a><a class="cd-act" href="tel:+966580330627">Call %s</a></li>' % ARROW_UR)
    h.append('        <li class="cd-line"><small>WhatsApp</small><a class="cd-v" href="https://wa.me/966580330627" target="_blank" rel="noopener" id="id-contact-wa"><b>Message us directly</b><em>Fastest first response</em></a><a class="cd-act" href="https://wa.me/966580330627" target="_blank" rel="noopener">Open %s</a></li>' % ARROW_UR)
    h.append('      </ul>')
    h.append('      <div class="cd-card-foot"><span>Coverage <b>All regions of Saudi Arabia</b></span><span>Languages <b>English &amp; <span lang="ar" dir="rtl" style="font-family:\'GE SS Two\',\'Arial\',sans-serif;">العربية</span></b></span></div>')
    h.append('    </div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ WHAT HAPPENS NEXT ━━━━━━━ -->')
    h.append('<!-- A staircase in section: each step treads and rises, from the first conversation to the proposal -->')
    h.append('<section data-screen-label="Next Steps" class="cn">')
    h.append('  <div class="cn-wrap">')
    h.append('    <div class="cn-head">')
    h.append('      <div><div class="c-label rv"%s><i></i>After you reach out</div><h2 class="cn-h2 rv"%s>What happens next.</h2></div>' % (reveal(), reveal("0.08")))
    h.append('      <p class="cn-note rv"%s>No obligation at any step: the proposal comes before any commitment.</p>' % reveal("0.12"))
    h.append('    </div>')
    h.append('    <ol class="cn-steps">')
    steps = [
        ("01", "We listen", "Within one working day", "A senior consultant, not a call centre, reviews your inquiry and schedules a discovery conversation at a time that suits you.",
         "executive-floors-client-majlis-1280.webp", "A majlis set for a conversation"),
        ("02", "We visit", "Site &amp; scope", "We survey the space, understand how you'll use it, and align on ambition, constraints and timeline, face to face where possible.",
         "fitout-pillar-brand-led-planning-site-plan-1280.webp", "A site under survey, its plan pinned to a column"),
        ("03", "We propose", "Plan &amp; roadmap", "You receive a clear proposal: scope, photoreal direction and a comprehensive budget roadmap, before committing to anything.",
         "interior-design-pillar-visual-certainty-render-review-1280.webp", "A client and a designer reviewing a render"),
    ]
    for k, (n, t, tag, p, img, alt) in enumerate(steps):
        h.append('      <li class="cn-step rv"%s>' % reveal("%.2f" % (0.12 * k) if k else None))
        h.append('        <span class="cn-node" aria-hidden="true"></span>')
        h.append('        <div class="cn-meta"><span class="cn-n">%s</span><span class="cn-tag">%s</span></div>' % (n, tag))
        h.append('        <div class="cn-frame"><img src="uploads/%s" alt="%s" loading="lazy" decoding="async"></div>' % (img, alt))
        h.append('        <h3>%s</h3>' % t)
        h.append('        <p>%s</p>' % p)
        h.append('      </li>')
    h.append('    </ol>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ VISIT ━━━━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Visit" class="cv">')
    h.append('  <div class="cv-map-bg"><iframe src="https://www.google.com/maps?cid=%s&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="FurnishIQ studio on Google Maps"></iframe></div>' % MAP_CID)
    h.append('  <div class="cv-wrap">')
    h.append('    <div class="cv-text rv"%s>' % reveal())
    h.append('      <div class="c-label"><i></i>Visit the studio</div>')
    h.append('      <h2 class="cv-h2">See materials. <span>Touch finishes.</span></h2>')
    h.append('      <p class="cv-p">Some decisions deserve to be made in person. Book a studio session to explore material libraries, finish samples and past project work.</p>')
    h.append('      <div class="cv-facts"><div><small>Address</small><span>Al Takhassousi, Riyadh</span></div><div><small>By appointment</small><span>Sunday – Thursday · 9:00 – 18:00</span></div></div>')
    h.append('      <div id="visit-root"></div>')
    h.append('      <div class="cv-maplink"><span class="cv-cap">The studio is marked on the map</span><a href="https://www.google.com/maps?cid=%s" target="_blank" rel="noopener" class="cv-link">Open in Google Maps %s</a></div>' % (MAP_CID, ARROW_UR))
    h.append('    </div>')
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
    // contact-letter.js: the letter and the visit request. It may load after this render: then it starts itself on these flags
    if (window.FIQLetter) window.FIQLetter(); else window.FIQLetterPending = true;
    if (window.FIQVisit) window.FIQVisit(); else window.FIQVisitPending = true;
    if (window.FIQDirect) window.FIQDirect(); else window.FIQDirectPending = true;

""" + s[b:]
    # the old form's channel hover, phone focus and country lookup (contact-letter.js has its own)
    a = s.index("    // ── CHANNEL CARD HOVER")
    b = s.index("\n  }\n}\n</script>", a)
    s = s[:a].rstrip() + "\n" + s[b:]
    # contact-letter.js alongside the page's other shared scripts
    o = '<script src="./newsletter.js" defer></script>'
    assert s.count(o) == 1
    s = s.replace(o, o + '\n<script src="./contact-letter.js" defer></script>')
    io.open(PAGE, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(PAGE, "rebuilt")


if __name__ == "__main__":
    main()
