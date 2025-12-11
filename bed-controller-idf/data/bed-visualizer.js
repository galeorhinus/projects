(function () {
  var headMaxSec = 28;
  var footMaxSec = 43;
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
  const SHOW_CONNECTORS = false;

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

  const BED_TOP_PAIRS = [
    [0, 1],
    [5, 6],
    [9, 10],
    [11, 12],
    [15, 16]
  ];

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

  function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
  }

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

  function mapToVanish(point) {
    return {
      x: point.x + ((VANISHING_POINT_X - point.x) * VANISH_LINE_FRACTION),
      y: point.y + ((VANISHING_POINT_Y - point.y) * VANISH_LINE_FRACTION)
    };
  }

  function setPolygonPoints(el, points) {
    if (!el) return;
    var pts = points.map(function (p) {
      return p.x + ',' + p.y;
    }).join(' ');
    el.setAttribute('points', pts);
  }

  function calculateIconPoints(headPosMs, footPosMs) {
    var headPos = headPosMs / 1000;
    var footPos = footPosMs / 1000;
    var headPercent = clamp((headPos / headMaxSec) * 100, 0, 100);
    var footPercent = clamp((footPos / footMaxSec) * 100, 0, 100);
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

  function updateBedPolygons(bedBaseEl, vanishBedBaseEl, bedTopEls) {
    setPolygonPoints(bedBaseEl, BED_BASE_POINTS);
    setPolygonPoints(
      vanishBedBaseEl,
      BED_BASE_POINTS.map(mapToVanish)
    );
    bedTopEls.forEach(function (el, idx) {
      if (!el) return;
      var pair = BED_TOP_PAIRS[idx];
      var a = BED_BASE_POINTS[pair[0]];
      var b = BED_BASE_POINTS[pair[1]];
      var va = mapToVanish(a);
      var vb = mapToVanish(b);
      setPolygonPoints(el, [a, b, vb, va]);
    });
  }

  function updateMattressRects(nodes, mattressElements) {
    var elementNodePairs = [
      [0, 1],
      [2, 3],
      [4, 5],
      [6, 7]
    ];
    elementNodePairs.forEach(function (pair, index) {
      var element = mattressElements[index];
      if (!element) return;
      var start = nodes[pair[0]];
      var end = nodes[pair[1]];
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
  }

  function updateVanishRects(vanishNodes, vanishElements) {
    var vanishPairs = [
      [0, 1],
      [2, 3],
      [4, 5],
      [6, 7]
    ];
    vanishPairs.forEach(function (pair, index) {
      var element = vanishElements[index];
      if (!element) return;
      var start = vanishNodes[pair[0]];
      var end = vanishNodes[pair[1]];
      if (!start || !end) return;
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
  }

  function updateVanishTops(vals, vanishNodes, vanishTops, headPosContainerEl, footPosContainerEl) {
    var topLift = 0;
    var topPairs = [
      [0, 1],
      [2, 3],
      [4, 5],
      [6, 7]
    ];
    topPairs.forEach(function (pair, index) {
      var poly = vanishTops[index];
      if (!poly) return;
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
      setPolygonPoints(poly, lifted);
      var centroid = polygonCentroid(lifted);
      if (index === 0 && headPosContainerEl) {
        headPosContainerEl.setAttribute('x', centroid.x - 7);
        headPosContainerEl.setAttribute('y', centroid.y - 12);
      }
      if (index === 3 && footPosContainerEl) {
        footPosContainerEl.setAttribute('x', centroid.x - 43);
        footPosContainerEl.setAttribute('y', centroid.y - 12);
      }
    });
  }

  function updateConnectors(vals, vanishNodes, connectors) {
    vanishNodes.forEach(function (vNode, index) {
      var connector = connectors[index];
      if (!connector) return;
      connector.style.display = SHOW_CONNECTORS ? 'inline' : 'none';
      var baseNode = vals.nodes[index];
      connector.setAttribute('x1', baseNode.x);
      connector.setAttribute('y1', baseNode.y - (ELEMENT_THICKNESS / 6));
      connector.setAttribute('x2', vNode.x);
      connector.setAttribute('y2', vNode.y - (ELEMENT_THICKNESS / 6));
    });
  }

  function updateBedVisualizer(headSec, footSec, headMoving, footMoving) {
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
    var bedTopEls = [
      document.getElementById('bed-top'),
      document.getElementById('bed-top-1'),
      document.getElementById('bed-top-2'),
      document.getElementById('bed-top-3'),
      document.getElementById('bed-top-4')
    ];
    var vanishConnectors = VANISH_CONNECTOR_IDS.map(function (id) {
      return document.getElementById(id);
    });
    var bedBaseEl = document.getElementById('bed-base');
    var vanishBedBaseEl = document.getElementById('vanish-bed-base');

    updateBedPolygons(bedBaseEl, vanishBedBaseEl, bedTopEls);

    var vals = calculateIconPoints(headSec * 1000, footSec * 1000);
    var vanishNodes = vals.nodes.map(mapToVanish);

    updateMattressRects(vals.nodes, mattressElements);
    updateVanishRects(vanishNodes, vanishElements);
    updateConnectors(vals, vanishNodes, vanishConnectors);
    updateVanishTops(vals, vanishNodes, vanishTops, headPosContainerEl, footPosContainerEl);

    // Pulse active segments: 0=head, 1=fixed, 2&3=foot
    if (headMoving) {
      if (vanishTops[0]) vanishTops[0].classList.add('pulse');
      if (vanishElements[0]) vanishElements[0].classList.add('pulse');
      if (mattressElements[0]) mattressElements[0].classList.add('pulse');
    } else {
      if (vanishTops[0]) vanishTops[0].classList.remove('pulse');
      if (vanishElements[0]) vanishElements[0].classList.remove('pulse');
      if (mattressElements[0]) mattressElements[0].classList.remove('pulse');
    }
    if (footMoving) {
      if (vanishTops[2]) vanishTops[2].classList.add('pulse');
      if (vanishTops[3]) vanishTops[3].classList.add('pulse');
      if (vanishElements[2]) vanishElements[2].classList.add('pulse');
      if (vanishElements[3]) vanishElements[3].classList.add('pulse');
      if (mattressElements[2]) mattressElements[2].classList.add('pulse');
      if (mattressElements[3]) mattressElements[3].classList.add('pulse');
    } else {
      if (vanishTops[2]) vanishTops[2].classList.remove('pulse');
      if (vanishTops[3]) vanishTops[3].classList.remove('pulse');
      if (vanishElements[2]) vanishElements[2].classList.remove('pulse');
      if (vanishElements[3]) vanishElements[3].classList.remove('pulse');
      if (mattressElements[2]) mattressElements[2].classList.remove('pulse');
      if (mattressElements[3]) mattressElements[3].classList.remove('pulse');
    }

    headPosTextEl.textContent = headSec.toFixed(0) + 's';
    footPosTextEl.textContent = footSec.toFixed(0) + 's';
    headPosTextEl.style.visibility = headSec > 0 ? 'visible' : 'hidden';
    footPosTextEl.style.visibility = footSec > 0 ? 'visible' : 'hidden';
  }

  function setTravelLimits(headSec, footSec) {
    if (typeof headSec === 'number') headMaxSec = headSec;
    if (typeof footSec === 'number') footMaxSec = footSec;
  }

  window.updateBedVisualizer = updateBedVisualizer;
  window.setTravelLimits = setTravelLimits;
})();
