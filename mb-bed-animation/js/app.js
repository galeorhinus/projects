const HEAD_MAX_SEC = 28;
const FOOT_MAX_SEC = 43;
const SVG_VIEWBOX_TRAVEL_HEIGHT = 108;
const MATTRESS_Y_BASE = 116;
const HEAD_LENGTH = 120;
const FIXED_LENGTH = 50;
const FOOT1_LENGTH = 90;
const FOOT2_LENGTH = 90;
const HEAD_NODE_START_X = 0;
const HEAD_NODE_END_X = HEAD_NODE_START_X + HEAD_LENGTH;
const FIXED_NODE_START_X = HEAD_NODE_END_X;
const FIXED_NODE_END_X = FIXED_NODE_START_X + FIXED_LENGTH;
const FOOT1_NODE_START_X = FIXED_NODE_END_X;
const FOOT1_NODE_END_X = FOOT1_NODE_START_X + FOOT1_LENGTH;
const FOOT2_NODE_START_X = FOOT1_NODE_END_X;
const FOOT2_NODE_END_X = FOOT2_NODE_START_X + FOOT2_LENGTH;
const MATTRESS_ELEMENT_IDS = [
  'mattress-element-0',
  'mattress-element-1',
  'mattress-element-2',
  'mattress-element-3'
];
const MATTRESS_ELEMENT_NAMES = ['head', 'fixed', 'foot1', 'foot2'];

function calculateIconPoints(headPosMs, footPosMs) {
  var headPos = headPosMs / 1000;
  var footPos = footPosMs / 1000;
  var headPercent = (headPos / HEAD_MAX_SEC) * 100;
  var footPercent = (footPos / FOOT_MAX_SEC) * 100;
  headPercent = Math.max(0, Math.min(100, headPercent));
  footPercent = Math.max(0, Math.min(100, footPercent));
  var headY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (headPercent / 100));
  var footY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (footPercent / 100) * 0.5);
  var nodes = [
    { x: HEAD_NODE_START_X, y: headY },
    { x: HEAD_NODE_END_X, y: MATTRESS_Y_BASE },
    { x: FIXED_NODE_START_X, y: MATTRESS_Y_BASE },
    { x: FIXED_NODE_END_X, y: MATTRESS_Y_BASE },
    { x: FOOT1_NODE_START_X, y: MATTRESS_Y_BASE },
    { x: FOOT1_NODE_END_X, y: footY },
    { x: FOOT2_NODE_START_X, y: footY },
    { x: FOOT2_NODE_END_X, y: footY }
  ];
  return { headY, footY, nodes };
}

function updateVisualizer(headSec, footSec) {
  var headPosTextEl = document.getElementById('head-pos-text');
  var footPosTextEl = document.getElementById('foot-pos-text');
  var headPosContainerEl = document.getElementById('head-pos-text-container');
  var footPosContainerEl = document.getElementById('foot-pos-text-container');
  var mattressElements = MATTRESS_ELEMENT_IDS.map(function (id) {
    return document.getElementById(id);
  });

  var vals = calculateIconPoints(headSec * 1000, footSec * 1000);
  headPosContainerEl.setAttribute('y', vals.headY - 10);
  footPosContainerEl.setAttribute('y', vals.footY - 10);

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
    element.setAttribute('x1', start.x);
    element.setAttribute('y1', start.y);
    element.setAttribute('x2', end.x);
    element.setAttribute('y2', end.y);
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
