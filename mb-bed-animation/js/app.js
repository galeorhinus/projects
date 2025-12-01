const HEAD_MAX_SEC = 28;
const FOOT_MAX_SEC = 43;
const MATTRESS_Y_BASE = 116;
const HEAD_NODE_VERTICAL_TRAVEL = MATTRESS_Y_BASE - 8;
const FOOT_NODE_VERTICAL_TRAVEL = HEAD_NODE_VERTICAL_TRAVEL * 0.5;
const HEAD_LENGTH = 124;
const FIXED_LENGTH = 54;
const FOOT1_LENGTH = 80;
const FOOT2_LENGTH = 80;
const HEAD_TO_FIXED_GAP = 4;
const FIXED_TO_FOOT1_GAP = 4;
const FOOT1_TO_FOOT2_GAP = 4;
const ELEMENT_THICKNESS = 12;
const ELEMENT_RADIUS = 4;
const VANISHING_POINT_X = 169;
const VANISHING_POINT_Y = -60;
const VANISH_LINE_FRACTION = 0.3;
const VANISH_ELEMENT_THICKNESS = 12;
const VANISH_ELEMENT_RADIUS = 4;
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
  var vanishConnectors = VANISH_CONNECTOR_IDS.map(function (id) {
    return document.getElementById(id);
  });

  var vals = calculateIconPoints(headSec * 1000, footSec * 1000);
  var headNode = vals.nodes[0];
  var footNode = vals.nodes[7];
  headPosContainerEl.setAttribute('x', headNode.x + 5);
  headPosContainerEl.setAttribute('y', headNode.y - 6);
  footPosContainerEl.setAttribute('x', footNode.x - 55);
  footPosContainerEl.setAttribute('y', footNode.y - 8);

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
    var baseNode = vals.nodes[index];
    connector.setAttribute('x1', baseNode.x);
    connector.setAttribute('y1', baseNode.y);
    connector.setAttribute('x2', vNode.x);
    connector.setAttribute('y2', vNode.y);
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
