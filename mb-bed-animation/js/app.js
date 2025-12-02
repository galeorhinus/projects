const HEAD_MAX_SEC = 28;
const FOOT_MAX_SEC = 43;
const MATTRESS_Y_BASE = 116;
const HEAD_NODE_VERTICAL_TRAVEL = MATTRESS_Y_BASE - 8;
const FOOT_NODE_VERTICAL_TRAVEL = HEAD_NODE_VERTICAL_TRAVEL * 0.5;
const HEAD_LENGTH = 121;
const FIXED_LENGTH = 51;
const FOOT1_LENGTH = 80;
const FOOT2_LENGTH = 80;
const HEAD_TO_FIXED_GAP = 6;
const FIXED_TO_FOOT1_GAP = 6;
const FOOT1_TO_FOOT2_GAP = 6;
const ELEMENT_THICKNESS = 12;
const ELEMENT_RADIUS = 4;
const VANISHING_POINT_X = 169;
const VANISHING_POINT_Y = -60;
const VANISH_LINE_FRACTION = 0.3;
const VANISH_ELEMENT_THICKNESS = 12;
const VANISH_ELEMENT_RADIUS = 4;
const BED_BASE_POINTS = [
  { x: 0, y: 126 },
  { x: 350, y: 126 },
  { x: 350, y: 132 },
  { x: 324, y: 132 },
  { x: 324, y: 151 },
  { x: 316, y: 151 },
  { x: 316, y: 132 },
  { x: 244, y: 132 },
  { x: 244, y: 151 },
  { x: 236, y: 151 },
  { x: 236, y: 132 },
  { x: 114, y: 132 },
  { x: 114, y: 151 },
  { x: 106, y: 151 },
  { x: 106, y: 132 },
  { x: 34, y: 132 },
  { x: 34, y: 151 },
  { x: 26, y: 151 },
  { x: 26, y: 132 },
  { x: 0, y: 132 }
];
const SHOW_CONNECTORS = false;
const HEAD_NODE_START_X = 0;
const HEAD_NODE_END_X = HEAD_NODE_START_X + HEAD_LENGTH;
const FIXED_NODE_START_X = HEAD_NODE_END_X + HEAD_TO_FIXED_GAP;
const FIXED_NODE_END_X = FIXED_NODE_START_X + FIXED_LENGTH;
const FOOT1_NODE_START_X = FIXED_NODE_END_X + FIXED_TO_FOOT1_GAP;
const FOOT1_NODE_END_X = FOOT1_NODE_START_X + FOOT1_LENGTH;
const FOOT2_NODE_START_X = FOOT1_NODE_END_X + FOOT1_TO_FOOT2_GAP;
const FOOT2_NODE_END_X = FOOT2_NODE_START_X + FOOT2_LENGTH;
const MATTRESS_ELEMENT_IDS = [
  'mattress-element-0',
  'mattress-element-1',
  'mattress-element-2',
  'mattress-element-3'
];
const MATTRESS_ELEMENT_NAMES = ['head', 'fixed', 'foot1', 'foot2'];
const VANISH_ELEMENT_IDS = [
  'vanish-element-0',
  'vanish-element-1',
  'vanish-element-2',
  'vanish-element-3'
];
const VANISH_TOP_IDS = [
  'vanish-top-0',
  'vanish-top-1',
  'vanish-top-2',
  'vanish-top-3'
];
const VANISH_CONNECTOR_IDS = [
  'vanish-connector-0',
  'vanish-connector-1',
  'vanish-connector-2',
  'vanish-connector-3',
  'vanish-connector-4',
  'vanish-connector-5',
  'vanish-connector-6',
  'vanish-connector-7'
];

function calculateIconPoints(headPosMs, footPosMs) {
  var headPos = headPosMs / 1000;
  var footPos = footPosMs / 1000;
  var headPercent = (headPos / HEAD_MAX_SEC) * 100;
  var footPercent = (footPos / FOOT_MAX_SEC) * 100;
  headPercent = Math.max(0, Math.min(100, headPercent));
  footPercent = Math.max(0, Math.min(100, footPercent));
  var headTargetY = MATTRESS_Y_BASE - (HEAD_NODE_VERTICAL_TRAVEL * (headPercent / 100));
  var headTheta = Math.atan2(MATTRESS_Y_BASE - headTargetY, HEAD_LENGTH);
  var headNodeX = HEAD_NODE_END_X - (HEAD_LENGTH * Math.cos(headTheta));
  var headNodeY = MATTRESS_Y_BASE - (HEAD_LENGTH * Math.sin(headTheta));
  var footTargetY = MATTRESS_Y_BASE - (FOOT_NODE_VERTICAL_TRAVEL * (footPercent / 100));
  var footTheta = Math.atan2(MATTRESS_Y_BASE - footTargetY, FOOT1_LENGTH);
  var foot1EndX = FOOT1_NODE_START_X + (FOOT1_LENGTH * Math.cos(footTheta));
  var foot1EndY = MATTRESS_Y_BASE - (FOOT1_LENGTH * Math.sin(footTheta));
  var footDeltaX = foot1EndX - FOOT1_NODE_END_X;
  var footDeltaY = foot1EndY - MATTRESS_Y_BASE;
  var foot2StartX = FOOT2_NODE_START_X + footDeltaX;
  var foot2EndX = FOOT2_NODE_END_X + footDeltaX;
  var foot2Y = MATTRESS_Y_BASE + footDeltaY;
  var nodes = [
    { x: headNodeX, y: headNodeY },
    { x: HEAD_NODE_END_X, y: MATTRESS_Y_BASE },
    { x: FIXED_NODE_START_X, y: MATTRESS_Y_BASE },
    { x: FIXED_NODE_END_X, y: MATTRESS_Y_BASE },
    { x: FOOT1_NODE_START_X, y: MATTRESS_Y_BASE },
    { x: foot1EndX, y: foot1EndY },
    { x: foot2StartX, y: foot2Y },
    { x: foot2EndX, y: foot2Y }
  ];
  return { headY: headNodeY, footY: foot1EndY, nodes };
}

function updateVisualizer(headSec, footSec) {
  var headPosTextEl = document.getElementById('head-pos-text');
  var footPosTextEl = document.getElementById('foot-pos-text');
  var headPosContainerEl = document.getElementById('head-pos-text-container');
  var footPosContainerEl = document.getElementById('foot-pos-text-container');
  var mattressElements = MATTRESS_ELEMENT_IDS.map(function (id) {
    return document.getElementById(id);
  });
  var vanishElements = VANISH_ELEMENT_IDS.map(function (id) {
    return document.getElementById(id);
  });
  var vanishTops = VANISH_TOP_IDS.map(function (id) {
    return document.getElementById(id);
  });
  var bedTopEl = document.getElementById('bed-top');
  var bedTopEl1 = document.getElementById('bed-top-1');
  var bedTopEl2 = document.getElementById('bed-top-2');
  var bedTopEl3 = document.getElementById('bed-top-3');
  var bedTopEl4 = document.getElementById('bed-top-4');
  var vanishConnectors = VANISH_CONNECTOR_IDS.map(function (id) {
    return document.getElementById(id);
  });
  var bedBaseEl = document.getElementById('bed-base');
  var vanishBedBaseEl = document.getElementById('vanish-bed-base');
  function polygonCentroid(points) {
    var area = 0;
    var cx = 0;
    var cy = 0;
    for (var i = 0, len = points.length; i < len; i++) {
      var j = (i + 1) % len;
      var cross = (points[i].x * points[j].y) - (points[j].x * points[i].y);
      area += cross;
      cx += (points[i].x + points[j].x) * cross;
      cy += (points[i].y + points[j].y) * cross;
    }
    area = area / 2;
    if (!area) {
      return { x: points[0].x, y: points[0].y };
    }
    cx = cx / (6 * area);
    cy = cy / (6 * area);
    return { x: cx, y: cy };
  }

  // set bed base polygons
  if (bedBaseEl) {
    var bedFrontPoints = BED_BASE_POINTS.map(function (p) {
      return p.x + ',' + p.y;
    }).join(' ');
    bedBaseEl.setAttribute('points', bedFrontPoints);
  }
  if (vanishBedBaseEl) {
    var bedRearPoints = BED_BASE_POINTS.map(function (p) {
      var vx = p.x + ((VANISHING_POINT_X - p.x) * VANISH_LINE_FRACTION);
      var vy = p.y + ((VANISHING_POINT_Y - p.y) * VANISH_LINE_FRACTION);
      return vx + ',' + vy;
    }).join(' ');
    vanishBedBaseEl.setAttribute('points', bedRearPoints);
  }
  if (bedTopEl) {
    var tl = BED_BASE_POINTS[0];
    var tr = BED_BASE_POINTS[1];
    var vtl = {
      x: tl.x + ((VANISHING_POINT_X - tl.x) * VANISH_LINE_FRACTION),
      y: tl.y + ((VANISHING_POINT_Y - tl.y) * VANISH_LINE_FRACTION)
    };
    var vtr = {
      x: tr.x + ((VANISHING_POINT_X - tr.x) * VANISH_LINE_FRACTION),
      y: tr.y + ((VANISHING_POINT_Y - tr.y) * VANISH_LINE_FRACTION)
    };
    var topPoints = [
      tl.x + ',' + tl.y,
      tr.x + ',' + tr.y,
      vtr.x + ',' + vtr.y,
      vtl.x + ',' + vtl.y
    ].join(' ');
    bedTopEl.setAttribute('points', topPoints);
  }
  if (bedTopEl1) {
    var p5 = BED_BASE_POINTS[5];
    var p6 = BED_BASE_POINTS[6];
    var vp5 = {
      x: p5.x + ((VANISHING_POINT_X - p5.x) * VANISH_LINE_FRACTION),
      y: p5.y + ((VANISHING_POINT_Y - p5.y) * VANISH_LINE_FRACTION)
    };
    var vp6 = {
      x: p6.x + ((VANISHING_POINT_X - p6.x) * VANISH_LINE_FRACTION),
      y: p6.y + ((VANISHING_POINT_Y - p6.y) * VANISH_LINE_FRACTION)
    };
    var topPoints1 = [
      p5.x + ',' + p5.y,
      p6.x + ',' + p6.y,
      vp6.x + ',' + vp6.y,
      vp5.x + ',' + vp5.y
    ].join(' ');
    bedTopEl1.setAttribute('points', topPoints1);
  }
  if (bedTopEl2) {
    var p9 = BED_BASE_POINTS[9];
    var p10 = BED_BASE_POINTS[10];
    var vp9 = {
      x: p9.x + ((VANISHING_POINT_X - p9.x) * VANISH_LINE_FRACTION),
      y: p9.y + ((VANISHING_POINT_Y - p9.y) * VANISH_LINE_FRACTION)
    };
    var vp10 = {
      x: p10.x + ((VANISHING_POINT_X - p10.x) * VANISH_LINE_FRACTION),
      y: p10.y + ((VANISHING_POINT_Y - p10.y) * VANISH_LINE_FRACTION)
    };
    var topPoints2 = [
      p9.x + ',' + p9.y,
      p10.x + ',' + p10.y,
      vp10.x + ',' + vp10.y,
      vp9.x + ',' + vp9.y
    ].join(' ');
    bedTopEl2.setAttribute('points', topPoints2);
  }
  if (bedTopEl3) {
    var p11 = BED_BASE_POINTS[11];
    var p12 = BED_BASE_POINTS[12];
    var vp11 = {
      x: p11.x + ((VANISHING_POINT_X - p11.x) * VANISH_LINE_FRACTION),
      y: p11.y + ((VANISHING_POINT_Y - p11.y) * VANISH_LINE_FRACTION)
    };
    var vp12 = {
      x: p12.x + ((VANISHING_POINT_X - p12.x) * VANISH_LINE_FRACTION),
      y: p12.y + ((VANISHING_POINT_Y - p12.y) * VANISH_LINE_FRACTION)
    };
    var topPoints3 = [
      p11.x + ',' + p11.y,
      p12.x + ',' + p12.y,
      vp12.x + ',' + vp12.y,
      vp11.x + ',' + vp11.y
    ].join(' ');
    bedTopEl3.setAttribute('points', topPoints3);
  }
  if (bedTopEl4) {
    var p15 = BED_BASE_POINTS[15];
    var p16 = BED_BASE_POINTS[16];
    var vp15 = {
      x: p15.x + ((VANISHING_POINT_X - p15.x) * VANISH_LINE_FRACTION),
      y: p15.y + ((VANISHING_POINT_Y - p15.y) * VANISH_LINE_FRACTION)
    };
    var vp16 = {
      x: p16.x + ((VANISHING_POINT_X - p16.x) * VANISH_LINE_FRACTION),
      y: p16.y + ((VANISHING_POINT_Y - p16.y) * VANISH_LINE_FRACTION)
    };
    var topPoints4 = [
      p15.x + ',' + p15.y,
      p16.x + ',' + p16.y,
      vp16.x + ',' + vp16.y,
      vp15.x + ',' + vp15.y
    ].join(' ');
    bedTopEl4.setAttribute('points', topPoints4);
  }

  var vals = calculateIconPoints(headSec * 1000, footSec * 1000);
  var headNode = vals.nodes[0];
  var footNode = vals.nodes[7];
  var elementNodePairs = [
    [0, 1],
    [2, 3],
    [4, 5],
    [6, 7]
  ];
  elementNodePairs.forEach(function (pair, index) {
    var element = mattressElements[index];
    if (!element) {
      return;
    }
    var start = vals.nodes[pair[0]];
    var end = vals.nodes[pair[1]];
    var dx = end.x - start.x;
    var dy = end.y - start.y;
    var length = Math.sqrt((dx * dx) + (dy * dy));
    var angle = Math.atan2(dy, dx) * (180 / Math.PI);
    element.setAttribute('x', start.x);
    element.setAttribute('y', start.y - (ELEMENT_THICKNESS / 2));
    element.setAttribute('width', length);
    element.setAttribute('height', ELEMENT_THICKNESS);
    element.setAttribute('rx', ELEMENT_RADIUS);
    element.setAttribute('ry', ELEMENT_RADIUS);
    element.setAttribute('transform', 'rotate(' + angle + ' ' + start.x + ' ' + start.y + ')');
  });

  var vanishNodes = vals.nodes.map(function (node) {
    return {
      x: node.x + ((VANISHING_POINT_X - node.x) * VANISH_LINE_FRACTION),
      y: node.y + ((VANISHING_POINT_Y - node.y) * VANISH_LINE_FRACTION)
    };
  });

  var vanishPairs = [
    [0, 1],
    [2, 3],
    [4, 5],
    [6, 7]
  ];
  vanishPairs.forEach(function (pair, index) {
    var element = vanishElements[index];
    if (!element) {
      return;
    }
    var start = vanishNodes[pair[0]];
    var end = vanishNodes[pair[1]];
    if (!start || !end) {
      return;
    }
    var dx = end.x - start.x;
    var dy = end.y - start.y;
    var length = Math.sqrt((dx * dx) + (dy * dy));
    var angle = Math.atan2(dy, dx) * (180 / Math.PI);
    element.setAttribute('x', start.x);
    element.setAttribute('y', start.y - (VANISH_ELEMENT_THICKNESS / 2));
    element.setAttribute('width', length);
    element.setAttribute('height', VANISH_ELEMENT_THICKNESS);
    element.setAttribute('rx', VANISH_ELEMENT_RADIUS);
    element.setAttribute('ry', VANISH_ELEMENT_RADIUS);
    element.setAttribute('transform', 'rotate(' + angle + ' ' + start.x + ' ' + start.y + ')');
  });

  vanishNodes.forEach(function (vNode, index) {
    var connector = vanishConnectors[index];
    if (!connector) {
      return;
    }
    connector.style.display = SHOW_CONNECTORS ? 'inline' : 'none';
    var baseNode = vals.nodes[index];
    connector.setAttribute('x1', baseNode.x);
    connector.setAttribute('y1', baseNode.y - (ELEMENT_THICKNESS / 6));
    connector.setAttribute('x2', vNode.x);
    connector.setAttribute('y2', vNode.y - (ELEMENT_THICKNESS / 6));
  });


  // var topLift = ELEMENT_THICKNESS / 4;
  var topLift = 0;
  var topPairs = [
    [0, 1],
    [2, 3],
    [4, 5],
    [6, 7]
  ];
  topPairs.forEach(function (pair, index) {
    var poly = vanishTops[index];
    if (!poly) {
      return;
    }
    var nStart = vals.nodes[pair[0]];
    var nEnd = vals.nodes[pair[1]];
    var vStart = vanishNodes[pair[0]];
    var vEnd = vanishNodes[pair[1]];
    var lifted = [
      { x: nStart.x, y: nStart.y - topLift },
      { x: vStart.x, y: vStart.y - topLift },
      { x: vEnd.x, y: vEnd.y - topLift },
      { x: nEnd.x, y: nEnd.y - topLift }
    ];
    var points = lifted.map(function (p) {
      return p.x + ',' + p.y;
    }).join(' ');
    poly.setAttribute('points', points);
    var centroid = polygonCentroid(lifted);
    if (index === 0) {
      headPosContainerEl.setAttribute('x', centroid.x - 7);
      headPosContainerEl.setAttribute('y', centroid.y - 12);
    }
    if (index === 3) {
      footPosContainerEl.setAttribute('x', centroid.x - 43);
      footPosContainerEl.setAttribute('y', centroid.y - 12);
    }
  });

  headPosTextEl.textContent = headSec.toFixed(0) + 's';
  footPosTextEl.textContent = footSec.toFixed(0) + 's';
  headPosTextEl.style.visibility = headSec > 0 ? 'visible' : 'hidden';
  footPosTextEl.style.visibility = footSec > 0 ? 'visible' : 'hidden';

  var elementLogString = elementNodePairs.map(function (pair, index) {
    var start = vals.nodes[pair[0]];
    var end = vals.nodes[pair[1]];
    var startStr = Math.round(start.x) + ',' + Math.round(start.y);
    var endStr = Math.round(end.x) + ',' + Math.round(end.y);
    var name = MATTRESS_ELEMENT_NAMES[index] || ('e' + index);
    return name + ' (e' + index + ') n' + pair[0] + '-' + pair[1] + ' [' + startStr + ' -> ' + endStr + ']';
  }).join(' | ');
  console.log('Mattress elements: ' + elementLogString);
}

function initControls() {
  var headRange = document.getElementById('head-range');
  var footRange = document.getElementById('foot-range');
  var headVal = document.getElementById('head-val');
  var footVal = document.getElementById('foot-val');

  function sync() {
    var h = parseFloat(headRange.value) || 0;
    var f = parseFloat(footRange.value) || 0;
    headVal.textContent = h;
    footVal.textContent = f;
    updateVisualizer(h, f);
  }

  headRange.addEventListener('input', sync);
  footRange.addEventListener('input', sync);
  sync();
}

window.addEventListener('DOMContentLoaded', initControls);
