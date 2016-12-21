$(function(){
  $.get('/graph', {id: 'Robin', password: '123456'}, function(result) {

    //接受服务端返回的json数据
    var result = JSON.parse(JSON.stringify(result));
    var root = result.elements;
    console.log(JSON.stringify(root));

    //把边的source和target转换成序号连接的
    var edges = [];
    root.edges.forEach(function(e) {
        // Get the source and target nodes
        var sourceNode = root.nodes.filter(function(n) { return n.name === e.source; })[0],
            targetNode = root.nodes.filter(function(n) { return n.name === e.target; })[0];
            relationShip = e.relation;

        // Add the edge to the array
        edges.push({source: sourceNode, target: targetNode, relation: relationShip, left: false, right: true});
    });

    nodes = root.nodes;
    links = edges;
    force.nodes(nodes)
        .links(links);

    //入口
    setAppMode(MODE.EDIT);

  }, 'json');
});




/****************************************************************************/
// 模式：编辑和浏览
var MODE = {
      EDIT: 0,
      EVAL: 1
    },
    appMode = MODE.EDIT;

// set up initial MPL model (loads saved model if available, default otherwise)
var propvars = ['p','q','r','s','t'],
    varCount = 2;

var model = new MPL.Model(),
    modelString = 'AS1;ApS1,2;AqS;';

var modelParam = window.location.search.match(/\?model=(.*)/);
if(modelParam) modelString = modelParam[1];

model.loadFromModelString(modelString);

// 初始化节点和边, based on MPL model
var lastNodeId = 0,
    nodes = [],
    links = [];

// 生成节点数据
//var states = model.getStates();
//states.forEach(function(state) {
//  if(!state) { lastNodeId++; return; }
//
//  var defaultVals = propvars.map(function() { return false; }),
//      node = {id: ++lastNodeId, vals: defaultVals, reflexive: false};
//
//  for(var propvar in state) {
//    var index = propvars.indexOf(propvar);
//    if(index !== -1) node.vals[index] = true;
//  }
//
//  nodes.push(node);
//});

// 生成边的数据
//nodes.forEach(function(source) {
//  var sourceId = source.id,
//      successors = model.getSuccessorsOf(sourceId);
//
//  successors.forEach(function(targetId) {
//    if(sourceId === targetId) {
//      source.reflexive = true;
//      return;
//    }
//
//    var target = nodes.filter(function(node) { return node.id === targetId; })[0];
//
//    if(sourceId < targetId) {
//      links.push({source: source, target: target, left: false, right: true });
//      return;
//    }
//
//    var link = links.filter(function(l) { return (l.source === target && l.target === source); })[0];
//
//    if(link) link.left = true;
//    else links.push({source: target, target: source, left: true, right: false });
//  });
//});

//nodes = root.nodes;
//links = edges;

// set up SVG for D3
var width  = 800,
    height = 800,
    colors = d3.scale.category10();

var svg = d3.select('#app-body .graph')
  .append('svg')
  .attr('oncontextmenu', 'return false;')
  .attr('width', width)
  .attr('height', height);

// 初始化d3力导向布局
var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .size([width, height])
    .linkDistance(150)
    .charge(-500)
    .on('tick', tick);

// 箭头连接线
svg.append('svg:defs').append('svg:marker')
    .attr('id', 'end-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 6)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#000');

svg.append('svg:defs').append('svg:marker')
    .attr('id', 'start-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 4)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M10,-5L0,0L10,5')
    .attr('fill', '#000');

// 编辑：拖拽节点出来的边
var drag_line = svg.append('svg:path')
  .attr('class', 'link dragline hidden')
  .attr('d', 'M0,0L0,0');

// link组 node组
var path = svg.append('svg:g').selectAll('path'),
    circle = svg.append('svg:g').selectAll('g');

// 鼠标事件
var selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null;

function resetMouseVars() {
  mousedown_node = null;
  mouseup_node = null;
  mousedown_link = null;
}

// 右上角 'Link to Model' dialog
var backdrop = d3.select('.modal-backdrop'),
    linkDialog = d3.select('#link-dialog'),
    linkInputElem = linkDialog.select('input').node();

function showLinkDialog() {
  linkInputElem.value = 'http://rkirsling.github.com/modallogic/?model=' + model.getModelString();

  backdrop.classed('inactive', false);
  setTimeout(function() { backdrop.classed('in', true); linkDialog.classed('inactive', false); }, 0);
  setTimeout(function() { linkDialog.classed('in', true); }, 150);
}

function hideLinkDialog() {
  linkDialog.classed('in', false);
  setTimeout(function() { linkDialog.classed('inactive', true); backdrop.classed('in', false); }, 150);
  setTimeout(function() { backdrop.classed('inactive', true); }, 300);
}

// handles for dynamic content in panel
var varCountButtons = d3.selectAll('#edit-pane .var-count button'),
    varTable = d3.select('#edit-pane table.propvars'),
    varTableBody = d3.select('#edit-pane table.propvars tbody'),
    varTableRows = varTable.selectAll('tr'),
    selectedNodeLabel = d3.select('#edit-pane .selected-node-id'),
    evalInput = d3.select('#eval-pane .eval-input'),
    evalOutput = d3.select('#eval-pane .eval-output'),
    currentFormula = d3.select('#app-body .current-formula');

function evaluateFormula() {
  // 确保已经输入了公式
  var formula = evalInput.select('input').node().value;
  if(!formula) {
    evalOutput
      .html('<div class="alert">No formula!</div>')
      .classed('inactive', false);
    return;
  }

  // 检查公式 check formula for bad vars
  var varsInUse = propvars.slice(0, varCount);
  var badVars = (formula.match(/\w+/g) || []).filter(function(v) {
    return varsInUse.indexOf(v) === -1;
  });
  if(badVars.length) {
    evalOutput
      .html('<div class="alert">Invalid variables in formula!</div>')
      .classed('inactive', false);
    return;
  }

  // 解析公式 and catch bad input
  var wff = null;
  try {
    wff = new MPL.Wff(formula);
  } catch(e) {
    evalOutput
      .html('<div class="alert">Invalid formula!</div>')
      .classed('inactive', false);
    return;
  }

  // 评估公式 at each state in model
  var trueStates  = [],
      falseStates = [];
  nodes.forEach(function(node, index) {
    var id = node.id,
        truthVal = MPL.truth(model, id, wff);

    if(truthVal) trueStates.push(id);
    else falseStates.push(id);

    d3.select(circle[0][index])
      .classed('waiting', false)
      .classed('true', truthVal)
      .classed('false', !truthVal);
  });

  // display evaluated formula
  currentFormula
    .html('<strong>Current formula:</strong><br>$' + wff.latex() + '$')
    .classed('inactive', false);

  // display truth evaluation
  var latexTrue  =  trueStates.length ? '$w_{' +  trueStates.join('},$ $w_{') + '}$' : '$\\varnothing$',
      latexFalse = falseStates.length ? '$w_{' + falseStates.join('},$ $w_{') + '}$' : '$\\varnothing$';
  evalOutput
    .html('<div class="alert alert-success"><strong>True:</strong><div><div>' + latexTrue + '</div></div></div>' +
          '<div class="alert alert-error"><strong>False:</strong><div><div>' + latexFalse + '</div></div></div>')
    .classed('inactive', false);

  // 重新渲染 LaTeX
  MathJax.Hub.Queue(['Typeset', MathJax.Hub, currentFormula.node()]);
  MathJax.Hub.Queue(['Typeset', MathJax.Hub, evalOutput.node()]);
}


function setSelectedNodeOrLink(node, link) {
  if (node != null && link != null) {
    return;
  }

  if (node) {       // 选中节点、更新编辑面板
      selected_node = node;

      // 更新选中节点标签
      selectedNodeLabel.html(selected_node ? '<strong>选中了人物：'+selected_node.id+'</strong>' : '未选中人物');

      // 更新左侧变量面板
//      if(selected_node) {
//        var vals = selected_node.vals;
//        varTableRows.each(function(d,i) {
//          d3.select(this).select('.var-value .btn-success').classed('active', vals[i]);
//          d3.select(this).select('.var-value .btn-danger').classed('active', !vals[i]);
//        });
//      }
      varTable.classed('inactive', !selected_node);

      //生成左侧变量表
      if(selected_node){
          var htmlStr = "";
          var nodeKeys = Object.keys(selected_node);
          for(var key in nodeKeys){
            htmlStr += ' <tr class=""><td class="var-name">' + nodeKeys[key] + ':</td><td class="var-value"><div class="btn-group">' +
                        '<input type="text" value="' + selected_node[nodeKeys[key]] + '"> </div></td></tr>';
          }
          varTableBody.empty();
          varTableBody.html(htmlStr);
      }
  /*==============================================================================================================*/
  } else if (link) {    // 选中连线，更新编辑面板
      selected_link = link;

      // 更新选中节点标签
      selectedNodeLabel.html(selected_node ? '<strong>选中了关系：'+'</strong>' : '未选中关系');

      //生成左侧变量表
      if(selected_link){
          var htmlStr = "";
          var linkKeys = Object.keys(selected_link);
          for(var key in linkKeys){
            htmlStr += ' <tr class=""><td class="var-name">' + linkKeys[key] + ':</td><td class="var-value"><div class="btn-group">' +
                        '<input type="text" value="' + selected_link[linkKeys[key]] + '"> </div></td></tr>';
          }
          varTableBody.empty();
          varTableBody.html(htmlStr);
      }
  } else {
      selected_node = null;
      selected_link = null;
      // 更新选中节点标签
      selectedNodeLabel.html('未选中任何东西');
      varTableBody.html('');
  }

}

//节点旁边的text
function makeAssignmentString(node) {
    return "";
}

//左侧面板变量 set # of vars currently in use and notify panel of changes
function setVarCount(count) {
  varCount = count;

  // update variable count button states
  varCountButtons.each(function(d,i) {
    if(i !== varCount-1) d3.select(this).classed('active', false);
    else d3.select(this).classed('active', true);
  });

  //更新节点旁文字
  circle.selectAll('text:not(.id)').text(makeAssignmentString);

  //update variable table rows
  varTableRows.each(function(d,i) {
    if(i < varCount) d3.select(this).classed('inactive', false);
    else d3.select(this).classed('inactive', true);
  });
}

function setVarForSelectedNode(varnum, value) {
  //update node in graph and state in model
  selected_node.vals[varnum] = value;
  var update = {};
  update[propvars[varnum]] = value;
  model.editState(selected_node.id, update);

  //update buttons
  var row = d3.select(varTableRows[0][varnum]);
  row.select('.var-value .btn-success').classed('active', value);
  row.select('.var-value .btn-danger').classed('active', !value);

  //update graph text
  circle.selectAll('text:not(.id)').text(makeAssignmentString);
}

// 力引导布局刷新 (called automatically each iteration)
function tick() {
  // draw directed edges with proper padding from node centers
  path.attr('d', function(d) {
    var deltaX = d.target.x - d.source.x,
        deltaY = d.target.y - d.source.y,
        dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
        normX = deltaX / dist,
        normY = deltaY / dist,
        sourcePadding = d.left ? 17 : 12,
        targetPadding = d.right ? 17 : 12,
        sourceX = d.source.x + (sourcePadding * normX),
        sourceY = d.source.y + (sourcePadding * normY),
        targetX = d.target.x - (targetPadding * normX),
        targetY = d.target.y - (targetPadding * normY);
    return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
  });

  circle.attr('transform', function(d) {
    return 'translate(' + d.x + ',' + d.y + ')';
  });
}

// 更新整个svg布局 (called when needed)
function restart() {

  //link
  path = path.data(links);

  // 更新link
  path.classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; });

  // 添加新link
  path.enter().append('svg:path')
    .attr('class', 'link')
    .classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; })
    .on('mousedown', function(d) {
      if(appMode !== MODE.EDIT || d3.event.ctrlKey) return;

      // select link
      mousedown_link = d;
      if(mousedown_link === selected_link) setSelectedNodeOrLink(null, null);
      else setSelectedNodeOrLink(null, mousedown_link);
      restart();
    });

  // 删除旧的link
  path.exit().remove();

  // 节点
  // NB: the function arg is crucial here! nodes are known by id, not by index!
  circle = circle.data(nodes, function(d) { return d.id; });

  // update existing nodes (reflexive & selected visual states)
  circle.selectAll('circle')
    .style('fill', function(d) { return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id); })
    .classed('reflexive', function(d) { return d.reflexive; });

  // 添加新节点
  var g = circle.enter().append('svg:g');

  g.append('svg:circle')
    .attr('class', 'node')
    .attr('r', 12)
    .style('fill', function(d) {return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id); })
    .style('stroke', function(d) { return d3.rgb(colors(d.id)).darker().toString(); })
    .classed('reflexive', function(d) { return d.reflexive; })
    .on('mouseover', function(d) {
      if(appMode !== MODE.EDIT || !mousedown_node || d === mousedown_node) return;
      // enlarge target node
      d3.select(this).attr('transform', 'scale(1.1)');
    })
    .on('mouseout', function(d) {
      if(appMode !== MODE.EDIT || !mousedown_node || d === mousedown_node) return;
      // unenlarge target node
      d3.select(this).attr('transform', '');
    })
    .on('mousedown', function(d) {
      if(appMode !== MODE.EDIT || d3.event.ctrlKey) return;

      // select node
      mousedown_node = d;
      if(mousedown_node === selected_node) setSelectedNodeOrLink(null, null);
      else setSelectedNodeOrLink(mousedown_node, null);

      // reposition drag line
      drag_line
        .style('marker-end', 'url(#end-arrow)')
        .classed('hidden', false)
        .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);

      restart();
    })
    .on('mouseup', function(d) {
      if(appMode !== MODE.EDIT || !mousedown_node) return;

      // needed by FF
      drag_line
        .classed('hidden', true)
        .style('marker-end', '');

      // check for drag-to-self
      mouseup_node = d;
      if(mouseup_node === mousedown_node) { resetMouseVars(); return; }

      // unenlarge target node
      d3.select(this).attr('transform', '');

      // add transition to model
      model.addTransition(mousedown_node.id, mouseup_node.id);

      //生成新的连线 (update if exists)
      // note: links are strictly source < target; arrows separately specified by booleans
      var source, target, direction;
      if(mousedown_node.id < mouseup_node.id) {
        source = mousedown_node;
        target = mouseup_node;
        direction = 'right';
      } else {
        source = mouseup_node;
        target = mousedown_node;
        direction = 'left';
      }

      var link = links.filter(function(l) {
        return (l.source === source && l.target === target);
      })[0];

      if(link) {
        link[direction] = true;
      } else {
        link = {source: source, target: target, relation: 'INTERACTS'};
        link[direction] = true;
        links.push(link);
      }

      // 同时选中这条线
      setSelectedNodeOrLink(null, link);
      restart();
    });

  //显示 node IDs
  g.append('svg:text')
      .attr('x', 0)
      .attr('y', 4)
      .attr('class', 'id')
      .text(function(d) { return d.name == null ? d.id : d.name; });

  //文字阴影
  g.append('svg:text')
      .attr('x', 16)
      .attr('y', 4)
      .attr('class', 'shadow')
      .text(makeAssignmentString);

  //文字前景
  g.append('svg:text')
      .attr('x', 16)
      .attr('y', 4)
      .text(makeAssignmentString);

  //删除旧 node
  circle.exit().remove();

  // set the graph in motion
  force.start();
}

//鼠标按下事件处理
function mousedown() {
  // 阻止 I-bar on drag
  d3.event.preventDefault();

  // because :active only works in WebKit?
  svg.classed('active', true);

  if(d3.event.ctrlKey || mousedown_node || mousedown_link) return;

  var exist;
  do {
    exist = false;
    ++lastNodeId;
    for(i in nodes) {
        if(nodes[i].id == lastNodeId) exist = true;
    }
  }while(exist)

  //添加新节点
  var point = d3.mouse(this),
      node = {id: lastNodeId+"", "label":"Character","name": lastNodeId+"","weight":1};
  node.x = point[0];
  node.y = point[1];
  nodes.push(node);

  // add state to model
  model.addState();

  restart();
}


//鼠标move事件处理
function mousemove() {
  if(!mousedown_node) return;

  // update drag line
  drag_line.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);

  restart();
}

//鼠标弹起事件处理
function mouseup() {
  if(mousedown_node) {
    // hide drag line
    drag_line
      .classed('hidden', true)
      .style('marker-end', '');
  }

  // because :active only works in WebKit?
  svg.classed('active', false);

  // clear mouse event vars
  resetMouseVars();
}

function removeLinkFromModel(link) {
  var sourceId = link.source.id,
      targetId = link.target.id;

  // remove leftward transition
  if(link.left) model.removeTransition(targetId, sourceId);

  // remove rightward transition
  if(link.right) model.removeTransition(sourceId, targetId);
}

//删掉节点时，同时断开边
function spliceLinksForNode(node) {
  var toSplice = links.filter(function(l) {
    return (l.source === node || l.target === node);
  });
  toSplice.map(function(l) {
    links.splice(links.indexOf(l), 1);
  });
}

// only respond once per keydown
var lastKeyDown = -1;


//键盘按键事件
function keydown() {
  d3.event.preventDefault();

  if(lastKeyDown !== -1) return;
  lastKeyDown = d3.event.keyCode;

  // ctrl键
  if(d3.event.keyCode === 17) {
    circle.call(force.drag);
    svg.classed('ctrl', true);
    return;
  }

  if(!selected_node && !selected_link) return;
  switch(d3.event.keyCode) {
    case 8: // backspace键
    case 46: // delete键
      if(selected_node) {
        model.removeState(selected_node.id);
        nodes.splice(nodes.indexOf(selected_node), 1);
        spliceLinksForNode(selected_node);
      } else if(selected_link) {
        removeLinkFromModel(selected_link);
        links.splice(links.indexOf(selected_link), 1);
      }
      setSelectedNodeOrLink(null, null);
      restart();
      break;
    case 66: // B键
      if(selected_link) {
        var sourceId = selected_link.source.id,
            targetId = selected_link.target.id;
        // 把单向箭头改为双向
        if(!selected_link.left) {
          selected_link.left = true;
          model.addTransition(targetId, sourceId);
        }
        if(!selected_link.right) {
          selected_link.right = true;
          model.addTransition(sourceId, targetId);
        }
      }
      restart();
      break;
    case 76: // L键
      if(selected_link) {
        var sourceId = selected_link.source.id,
            targetId = selected_link.target.id;
        // 把箭头改为指向source
        if(!selected_link.left) {
          selected_link.left = true;
          model.addTransition(targetId, sourceId);
        }
        if(selected_link.right) {
          selected_link.right = false;
          model.removeTransition(sourceId, targetId);
        }
      }
      restart();
      break;
    case 82: // R键
      if(selected_node) {
        // toggle node reflexivity
        if(selected_node.reflexive) {
          selected_node.reflexive = false;
          model.removeTransition(selected_node.id, selected_node.id);
        } else {
          selected_node.reflexive = true;
          model.addTransition(selected_node.id, selected_node.id);
        }
      } else if(selected_link) {
        var sourceId = selected_link.source.id,
            targetId = selected_link.target.id;
        // 把箭头改为指向target
        if(selected_link.left) {
          selected_link.left = false;
          model.removeTransition(targetId, sourceId);
        }
        if(!selected_link.right) {
          selected_link.right = true;
          model.addTransition(sourceId, targetId);
        }
      }
      restart();
      break;
  }
}

function keyup() {
  lastKeyDown = -1;

  // ctrl键
  if(d3.event.keyCode === 17) {
    // "uncall" force.drag
    // see: https://groups.google.com/forum/?fromgroups=#!topic/d3-js/-HcNN1deSow
    circle
      .on('mousedown.drag', null)
      .on('touchstart.drag', null);
    svg.classed('ctrl', false);
  }
}

// handles to mode select buttons and left-hand panel
var modeButtons = d3.selectAll('#mode-select button'),
    panes = d3.selectAll('#app-body .panel .tab-pane');

function setAppMode(newMode) {
  // mode-specific settings
  if(newMode === MODE.EDIT) {
    // 启用listeners
    svg.classed('edit', true)
      .on('mousedown', mousedown)
      .on('mousemove', mousemove)
      .on('mouseup', mouseup);
    d3.select(window)
      .on('keydown', keydown)
      .on('keyup', keyup);

    // remove eval classes
    circle
      .classed('waiting', false)
      .classed('true', false)
      .classed('false', false);
    currentFormula.classed('inactive', true);
  } else if(newMode === MODE.EVAL) {
    // 禁用listeners (except for I-bar prevention)
    svg.classed('edit', false)
      .on('mousedown', function() { d3.event.preventDefault(); })
      .on('mousemove', null)
      .on('mouseup', null);
    d3.select(window)
      .on('keydown', null)
      .on('keyup', null);

    // in case ctrl still held
    circle
      .on('mousedown.drag', null)
      .on('touchstart.drag', null);
    svg.classed('ctrl', false);
    lastKeyDown = -1;

    // in case still dragging
    drag_line
      .classed('hidden', true)
      .style('marker-end', '');

    // clear mouse vars
    setSelectedNodeOrLink(null, null);
    resetMouseVars();

    // reset eval state
    circle.classed('waiting', true);
    evalOutput.classed('inactive', true);
  } else return;

  // switch button and panel states and set new mode
  modeButtons.each(function(d,i) {
    if(i !== newMode) d3.select(this).classed('active', false);
    else d3.select(this).classed('active', true);
  });
  panes.each(function(d,i) {
    if(i !== newMode) d3.select(this).classed('active', false);
    else d3.select(this).classed('active', true);
  });
  appMode = newMode;

  restart();
}

//enter键 to evaluate formula
evalInput.select('input')
  .on('keyup', function() {
    // enter
    if(d3.event.keyCode === 13) evaluateFormula();
  })
  .on('keydown', function() {
    // enter -- needed on IE9
    if(d3.event.keyCode === 13) d3.event.preventDefault();
  });

function submmitGraph() {
  console.log(JSON.stringify(nodes));
  console.log(JSON.stringify(links));
  $.post("/", {
        nodes: JSON.stringify(nodes),
        links: JSON.stringify(links)
    }, function(data){

  })
}

/****************************************************************************/