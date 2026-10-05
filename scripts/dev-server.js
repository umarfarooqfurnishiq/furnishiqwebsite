// Local preview server that behaves like the Vercel deployment.
// Reads vercel.json and applies its redirects, filesystem and rewrites in the same order Vercel does,
// so clean URLs (/projects, /ar/contact, /project-detail?project=...) work locally.
// Serves byte ranges so video seeking works. Form posts to /api/* are logged, never emailed.
//
// Usage: npm run serve            (http://localhost:3000)
//        PORT=4000 npm run serve

const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PORT = Number(process.env.PORT) || 3000;

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.avif': 'image/avif', '.gif': 'image/gif', '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.webm': 'video/webm',
  '.pdf': 'application/pdf', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf',
};

// Re-read vercel.json on every request so edits apply without a restart
function loadConfig() {
  try { return JSON.parse(fs.readFileSync(path.join(ROOT, 'vercel.json'), 'utf8')); } catch (e) { return {}; }
}

// Vercel path patterns: literal segments, ":name" (one segment) and ":name*" (rest of the path)
function match(source, pathname) {
  const names = [];
  const re = source.split('(.*)').map((part) => part
    .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
    .replace(/\/:(\w+)(\*)?/g, (_, name, star) => {
      names.push(name);
      return star ? '(?:/(.*))?' : '/([^/]+)';
    })).join('(.*)');
  const m = new RegExp('^' + re + '$').exec(pathname);
  if (!m) return null;
  const params = {};
  names.forEach((n, i) => { params[n] = m[i + 1] || ''; });
  return params;
}

function fill(dest, params) {
  return dest.replace(/:(\w+)\*?/g, (_, n) => (n in params ? params[n] : '')).replace(/\/+$/, '') || '/';
}

function fileFor(pathname) {
  const p = path.normalize(path.join(ROOT, decodeURIComponent(pathname)));
  if (!p.startsWith(ROOT)) return null;
  try { if (fs.statSync(p).isFile()) return p; } catch (e) {}
  return null;
}

function send(req, res, file, extraHeaders) {
  const stat = fs.statSync(file);
  const headers = {
    'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream',
    'Accept-Ranges': 'bytes',
    'Cache-Control': 'no-store',
    ...extraHeaders,
  };
  const range = /bytes=(\d*)-(\d*)/.exec(req.headers.range || '');
  if (range) {
    let start = range[1] === '' ? stat.size - Number(range[2]) : Number(range[1]);
    let end = range[1] !== '' && range[2] !== '' ? Number(range[2]) : stat.size - 1;
    end = Math.min(end, stat.size - 1);
    if (start > end || start < 0) {
      res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` });
      return res.end();
    }
    res.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${stat.size}`, 'Content-Length': end - start + 1 });
    if (req.method === 'HEAD') return res.end();
    return fs.createReadStream(file, { start, end }).pipe(res);
  }
  res.writeHead(200, { ...headers, 'Content-Length': stat.size });
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(file).pipe(res);
}

function notFound(res, pathname) {
  res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<!doctype html><meta charset="utf-8"><title>404</title><body style="font-family:sans-serif;padding:48px;background:#F5F2ED;color:#3A2D25"><h1>404</h1><p>No page or file at <code>${pathname.replace(/</g, '&lt;')}</code>.</p><p><a href="/">Home</a></p>`);
}

function handleApi(req, res, pathname) {
  let body = '';
  req.on('data', (c) => { body += c; });
  req.on('end', () => {
    console.log(`[api] ${req.method} ${pathname} (local preview, nothing sent)\n${body}`);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, local: true }));
  });
}

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const pathname = url.pathname;
  const cfg = loadConfig();

  for (const r of cfg.redirects || []) {
    const params = match(r.source, pathname);
    if (params) {
      res.writeHead(r.permanent ? 308 : 307, { Location: fill(r.destination, params) + url.search });
      return res.end();
    }
  }

  if (pathname.startsWith('/api/')) return handleApi(req, res, pathname);

  let file = pathname !== '/' && fileFor(pathname);
  if (!file) {
    for (const r of cfg.rewrites || []) {
      const params = match(r.source, pathname);
      if (params) { file = fileFor(fill(r.destination, params)); break; }
    }
  }
  if (!file) return notFound(res, pathname);

  const extra = {};
  for (const h of cfg.headers || []) {
    if (match(h.source, pathname)) h.headers.forEach(({ key, value }) => { if (key.toLowerCase() !== 'cache-control') extra[key] = value; });
  }
  send(req, res, file, extra);
}).listen(PORT, () => {
  console.log(`FurnishIQ local site: http://localhost:${PORT}  (Arabic: http://localhost:${PORT}/ar)`);
});
