async function loadJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

function getValue(obj, path) {
  return path.split('.').reduce((acc, key) => (acc && key in acc ? acc[key] : null), obj);
}

function fmtValue(val) {
  if (val === null || val === undefined) return '';
  if (typeof val === 'number' && !Number.isInteger(val)) return val.toFixed(1);
  return String(val);
}

function mapTimeToX(t, x0, x1, ticks) {
  if (!ticks || ticks.length === 0) return x0;
  const idx = ticks.indexOf(t);
  if (idx >= 0) return x0 + (x1 - x0) * idx / Math.max(1, ticks.length - 1);
  return x0;
}

function mapValToY(v, y0, y1, vmin, vmax) {
  if (vmax === vmin) return y1;
  const t = (v - vmin) / (vmax - vmin);
  return y1 - t * (y1 - y0);
}

function el(tag, attrs = {}, text = null) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
  if (text !== null) node.textContent = text;
  return node;
}

async function render() {
  const layout = await loadJson('../layout.json');
  const frame = await loadJson('../frame.json');

  const { width, height, viewBox } = layout.canvas;
  const svg = el('svg', { width, height, viewBox });

  if (layout.styles) {
    const defs = el('defs');
    const style = el('style');
    style.textContent = layout.styles;
    defs.appendChild(style);
    svg.appendChild(defs);
  }

  // rects
  layout.static.rects.forEach(r => {
    const attrs = { x: r.x, y: r.y, width: r.w, height: r.h };
    if (r.class) attrs.class = r.class;
    if (r.fill) attrs.fill = r.fill;
    svg.appendChild(el('rect', attrs));
  });

  // lines
  layout.static.lines.forEach(l => {
    const attrs = { x1: l.x1, y1: l.y1, x2: l.x2, y2: l.y2 };
    if (l.class) attrs.class = l.class;
    if (l.strokeWidth) attrs['stroke-width'] = l.strokeWidth;
    svg.appendChild(el('line', attrs));
  });

  // ticks
  layout.static.ticks.x.forEach(x => {
    svg.appendChild(el('line', { class: 'divider', x1: x, y1: layout.static.ticks.y1, x2: x, y2: layout.static.ticks.y2 }));
  });

  // text
  layout.text.forEach(t => {
    const text = t.bind ? fmtValue(getValue(frame, t.bind)) : t.text || '';
    const attrs = { x: t.x, y: t.y };
    if (t.class) attrs.class = t.class;
    if (t.anchor) attrs['text-anchor'] = t.anchor;
    svg.appendChild(el('text', attrs, text));
  });

  // time labels
  layout.time_labels.labels.forEach((lbl, i) => {
    const x = layout.time_labels.x[i];
    const cls = x >= 530 ? 'label-inv' : 'label-xs';
    svg.appendChild(el('text', { class: cls, x, y: layout.time_labels.y }, lbl));
  });

  // forecast
  layout.forecast && frame.forecast.daily.slice(0, layout.forecast.rows).forEach((d, i) => {
    const y = layout.forecast.start_y + i * layout.forecast.row_h;
    svg.appendChild(el('text', { class: layout.forecast.class, x: layout.forecast.dow_x, y, 'text-anchor': 'end' }, d.dow));
    svg.appendChild(el('text', { class: layout.forecast.class, x: layout.forecast.temp_x, y, 'text-anchor': 'start' }, `${d.high}/${d.low}`));
  });

  // charts
  const ticks = frame.charts.xaxis.ticks;
  const temp = layout.charts.temp;
  const moon = layout.charts.moon;

  const drawPolyline = (pts, stroke, extra = {}) => {
    if (pts.length < 2) return;
    const path = pts.map(p => `${Math.round(p[0])},${Math.round(p[1])}`).join(' ');
    svg.appendChild(el('polyline', {
      points: path,
      fill: 'none',
      stroke,
      'stroke-width': extra.strokeWidth || 3,
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
      ...(extra.dash ? { 'stroke-dasharray': extra.dash } : {})
    }));
  };

  const actualPts = frame.charts.temp.actual.map(p => [
    mapTimeToX(p.t, temp.x0, temp.x1, ticks),
    mapValToY(p.v, temp.y0, temp.y1, temp.min, temp.max)
  ]);
  drawPolyline(actualPts, '#000');

  const forecastPts = frame.charts.temp.forecast.map(p => [
    mapTimeToX(p.t, temp.x0, temp.x1, ticks),
    mapValToY(p.v, temp.y0, temp.y1, temp.min, temp.max)
  ]);
  drawPolyline(forecastPts, '#000', { dash: '8,6' });

  const moonPts = frame.charts.moon.curve.map(p => [
    mapTimeToX(p.t, moon.x0, moon.x1, ticks),
    mapValToY(p.elev, moon.y0, moon.y1, moon.min, moon.max)
  ]);
  const dayPts = moonPts.filter(p => p[0] <= 530);
  const nightPts = moonPts.filter(p => p[0] >= 530);
  drawPolyline(dayPts, '#000');
  drawPolyline(nightPts, '#fff', { strokeWidth: 5 });

  const container = document.getElementById('frame');
  container.innerHTML = '';
  container.appendChild(svg);
}

render().catch(err => {
  console.error(err);
  const container = document.getElementById('frame');
  container.textContent = 'Failed to render preview.';
});
