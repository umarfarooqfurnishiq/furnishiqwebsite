const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);
const TO_EMAIL = process.env.TO_EMAIL || 'info@furnishiq.net';
const FROM_EMAIL = process.env.FROM_EMAIL || 'FurnishIQ Website <website@furnishiq.net>';

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderRows(rows) {
  return rows
    .filter((row) => row && row.value)
    .map(
      (row) => `
        <tr>
          <td style="padding:14px 0;border-bottom:1px solid #E4DED4;font-family:'Helvetica Neue',Arial,sans-serif;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;color:#8B6B4A;width:160px;vertical-align:top;">${escapeHtml(row.label)}</td>
          <td style="padding:14px 0;border-bottom:1px solid #E4DED4;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;color:#1F1F1F;vertical-align:top;white-space:pre-wrap;">${escapeHtml(row.value)}</td>
        </tr>`
    )
    .join('');
}

function renderEmail(heading, rows) {
  return `
  <div style="background:#F5F2ED;padding:40px 20px;font-family:'Helvetica Neue',Arial,sans-serif;">
    <div style="max-width:560px;margin:0 auto;background:#FFFFFF;">
      <div style="background:#3A2D25;padding:28px 32px;">
        <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:11px;letter-spacing:0.24em;text-transform:uppercase;color:#D6C2A8;">FurnishIQ</div>
      </div>
      <div style="padding:32px;">
        <h1 style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:20px;font-weight:600;color:#1F1F1F;margin:0 0 24px;">${escapeHtml(heading)}</h1>
        <table style="width:100%;border-collapse:collapse;">
          ${renderRows(rows)}
        </table>
      </div>
      <div style="padding:20px 32px;background:#F5F2ED;">
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:11px;color:#8B6B4A;margin:0;">Sent automatically from the FurnishIQ website.</p>
      </div>
    </div>
  </div>`;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    res.status(405).json({ ok: false, error: 'Method not allowed' });
    return;
  }

  let data = req.body;
  if (typeof data === 'string') {
    try { data = JSON.parse(data); } catch (e) { data = {}; }
  }
  data = data || {};

  const formType = data.formType;
  const replyTo = (data.email || '').trim() || undefined;

  let subject;
  let heading;
  let rows;

  if (formType === 'contact') {
    const name = (data.name || '').trim();
    subject = `New Project Inquiry — ${name || 'Website Visitor'}`;
    heading = 'New Project Inquiry';
    rows = [
      { label: 'Name', value: name },
      { label: 'Company', value: data.company },
      { label: 'Email', value: data.email },
      { label: 'Phone', value: data.phone },
      { label: 'Interested In', value: data.service },
      { label: 'Estimated Budget', value: data.budget },
      { label: 'Project Details', value: data.message },
    ];
  } else if (formType === 'brochure') {
    const name = (data.name || '').trim();
    subject = `Brochure Request — ${name || 'Website Visitor'}`;
    heading = 'Brochure / Consultation Request';
    rows = [
      { label: 'Name', value: name },
      { label: 'Email', value: data.email },
      { label: 'Phone', value: data.phone },
      { label: 'Requested', value: data.request },
      { label: 'Source Page', value: data.sourcePage },
    ];
  } else {
    res.status(400).json({ ok: false, error: 'Unknown form type' });
    return;
  }

  try {
    await resend.emails.send({
      from: FROM_EMAIL,
      to: TO_EMAIL,
      replyTo,
      subject,
      html: renderEmail(heading, rows),
    });
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Resend send failed:', err);
    res.status(502).json({ ok: false, error: 'Email send failed' });
  }
};
