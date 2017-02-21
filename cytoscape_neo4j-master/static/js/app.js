$(function(){
  $.get('/editor/graph', {id: 'Robin', password: '123456'}, function(result) {

    //接受服务端返回的json数据
    var result = JSON.parse(JSON.stringify(result));
    var root = result.elements;
    //console.log(JSON.stringify(root));

    //把边的source和target转换成序号连接的
    var edges = [];
    root.edges.forEach(function(e) {
        // Get the source and target nodes
        var sourceNode = root.nodes.filter(function(n) { return n.name === e.source; })[0],
            targetNode = root.nodes.filter(function(n) { return n.name === e.target; })[0];

        // Add the edge to the array
        edges.push({source: sourceNode, target: targetNode, relation: e.relation, weight: e.weight, id: e.id, left: false, right: true});
    });

    nodes = root.nodes;
    links = edges;
    force.nodes(nodes)
        .links(links);

    //入口
    setAppMode(MODE.EDIT);
    setTotalPeople(nodes.length);

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
var model = new MPL.Model();
var showCommunty = false;
var varCount = 2;


// 初始化节点和边, based on MPL model
var lastNodeIndex = 0,
    nodes = [],
    links = [];


// set up SVG for D3
var width  = 1200,
    height = 800,
    colors = d3.scale.category20();


//人物图片的宽高
var img_w = 70,
    img_h = 80,
    radius = 30;	//圆形半径


var svg = d3.select('#app-body .graph')
    .append('svg')
    .attr('oncontextmenu', 'return false;')
    .attr('width', '100%')
    .attr('height', height);

//缩放监听
var zoomListener = d3.behavior.zoom()
    .scale(1.0)
    .scaleExtent([0.3, 5])  //缩放比例区间
    .on("zoom", function() {
        var centerX = width / 2,
            centerY = height / 2,
            scale = d3.event.scale;
        // 绕整个svg的中心缩放
        var sc = "translate(" + -centerX*(scale-1) + "," + -centerY*(scale-1)  + ")scale(" + scale + ")";
        path.attr("transform", sc);
        pathtext.selectAll('textPath').attr("transform",  sc);
        circle.selectAll('g').attr("transform",  sc);
        circle.selectAll('circle').attr("transform",  sc);
        circle.selectAll('text').attr("transform",  sc);

    });

var unzoomListener = d3.behavior.zoom()
    .scale(1.0)
    .on("zoom", null);

// 初始化d3力导向布局
var force = d3.layout.force()
    .size([width, height])
    .linkDistance(200)
    .charge(-1000)
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
    .attr('d', 'M0,-5L10,0L0,5');

svg.append('svg:defs').append('svg:marker')
    .attr('id', 'start-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 4)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M10,-5L0,0L10,5');

// 编辑：拖拽节点出来的边
var drag_line = svg.append('svg:path')
  .attr('class', 'link dragline hidden')
  .attr('d', 'M0,0L0,0');

// link组 node组
var path = svg.append('svg:g').selectAll('path'),
    pathtext = svg.append('svg:g').selectAll('text'),
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

// 左侧面板动态内容区 handles for dynamic content in panel
var varCountButtons = d3.selectAll('#edit-pane .var-count button'),
    varTable = d3.select('#edit-pane table.propvars'),
    varTableBody = d3.select('#edit-pane table.propvars tbody'),
    varSubmmit = d3.select('#model-submmit'),
    varTableRows = varTable.selectAll('tr'),
    varAvatarRow = d3.select('#avatar-content'),
    selectedNodeLabel = d3.select('#edit-pane .selected-node-id'),
    evalInput = d3.select('#eval-pane .eval-input'),
    evalOutput = d3.select('#eval-pane .eval-output'),
    currentFormula = d3.select('#app-body .current-formula');


//节点旁边的text
function makeAssignmentString(node) {
    return "";
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

  //path.attr('d', function(d) {
  //  return 'M' + d.source.x + ',' + d.source.y + 'L' + d.target.x + ',' + d.target.y;
  //});

  circle.selectAll('circle')
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

  circle.selectAll('text')
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y + 4; });

//  circle.attr('transform', function(d) {
//    return 'translate(' + d.x + ',' + d.y + ')';
//  });
}




// 更新整个svg布局 (called when needed)
function restart() {

  //link
  path = path.data(links);

  // 更新已存在的link
  path.classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; });

  // 添加新link
  path.enter().append('svg:path')
    .attr('class', 'link')
    .attr("id", function(d) { return "edgepath" + d.id; })
    .attr("stroke-width", function(d) { return appMode == MODE.EDIT ? "8px" : Math.sqrt(d.weight); })
    .classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; })
    .on('mousedown', function(d) {
      if(appMode !== MODE.EDIT || d3.event.ctrlKey) return;

      //选中边
      mousedown_link = d;
      if(mousedown_link === selected_link) setSelectedNodeOrLink(null, null);
      else setSelectedNodeOrLink(null, mousedown_link);
      restart();
    });

  // 删除旧的link
  path.exit().remove();


  // 边上的文字
  pathtext = pathtext.data(links);

  //更新已存在的边上的文字
  pathtext.selectAll('text')
    .text(function(d) { return d.relation; });

  // 添加边上的文字
  var text = pathtext.enter()
    .append("text")
    .attr('class', 'edgetext')
    .attr("x", 6)
    .attr("dy", -5)
    .append('textPath')
    .attr('xlink:href', function(d) { return "#edgepath" + d.id; })
    .style("text-anchor","middle")
    .attr("startOffset","50%")
    .text(function(d) { return d.relation; });

  // 删除旧的link上的文字
  pathtext.exit().remove();



  // 节点
  circle = circle.data(nodes, function(d) { return d.temp_index; });

  // 更新已存在的nodes (reflexive & selected visual states)
  circle.selectAll('circle')
    .style('stroke', function(d) {
        return (d === selected_node) ? d3.rgb(colors(showCommunty ? d.community : d.temp_index)).brighter().toString() : colors(showCommunty ? d.community : d.temp_index);
    })
    .classed('reflexive', function(d) { return d.reflexive; });

  // 添加新节点
  var g = circle.enter().append('svg:g');

  //节点图片
  g.append('svg:circle')
    .attr('class', 'node')
    .attr('r', radius)
    .attr("fill", function(d, i){

        //创建圆形图片
        var defs = svg.append("defs").attr("id", "imgdefs")
        var catpattern = defs.append("pattern")
                            .attr("id", "catpattern" + i)
                            .attr("height", 1)
                            .attr("width", 1)
        catpattern.append("image")
            .attr("x", - (img_w / 2 - radius))
            .attr("y", - (img_h / 2 - radius))
            .attr("width", img_w)
            .attr("height", img_h)
            .attr("xlink:href", function(which){
                return d.avatar == null ? "/static/img/suyu.png" : d.avatar;
            })
        return "url(#catpattern" + i + ")";
    })
    .style('stroke', function(d) {
        return (d === selected_node) ? d3.rgb(colors(showCommunty ? d.community : d.temp_index)).brighter().toString() : colors(showCommunty ? d.community : d.temp_index);
     })
    .classed('reflexive', function(d) { return d.reflexive; })
    .on('mouseover', function(d) {
      if(appMode !== MODE.EDIT || !mousedown_node || d === mousedown_node) return;
      //d3.select(this).attr('transform', 'scale(1.1)');
    })
    .on('mouseout', function(d) {
      if(appMode !== MODE.EDIT || !mousedown_node || d === mousedown_node) return;
      // unenlarge target node
      d3.select(this).attr('transform', '');
    })
    .on('mousedown', function(d) {
      if(appMode !== MODE.EDIT || d3.event.ctrlKey) return;

      // 选中节点
      mousedown_node = d;
      if(mousedown_node === selected_node) setSelectedNodeOrLink(null, null);
      else setSelectedNodeOrLink(mousedown_node, null);

      // reposition drag line
      drag_line
        .attr("stroke-width", "7px")
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
      model.addTransition(mousedown_node.temp_index, mouseup_node.temp_index);

      //生成新的连线 (update if exists)
      // note: links are strictly source < target; arrows separately specified by booleans
      var source = mousedown_node,
          target = mouseup_node;

      var link = links.filter(function(l) {
        return (l.source === source && l.target === target);
      })[0];

      if(link == null) {
        link = {source: source, target: target, relation: 'INTERACTS', left: false, right: true};
        links.push(link);
        submmitModifyLink(link, ModifyAction.ADD);
      }

      // 同时选中这条线
      setSelectedNodeOrLink(null, link);
      restart();
    });


  // 更新已存在的节点文字 (reflexive & selected visual states)
  circle.selectAll('text')
    .style('fill', function(d) {
          return colors(showCommunty ? d.community : d.temp_index);
      })

  //显示 node Name
  g.append('svg:text')
      .attr('x', 0)
      .attr('y', 4)
      .attr("dx",function(d){
        return d.name.length * -0.5;
      })
      .attr("dy",radius + 7)
      .attr('class', 'id')
      .style('fill', function(d) {
        return colors(showCommunty ? d.community : d.temp_index);
      })
      .text(function(d) { return d.name == null ? d.temp_index : d.name; });

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
    ++lastNodeIndex;
    for(i in nodes) {
        if(nodes[i].temp_index == lastNodeIndex) exist = true;
    }
  }while(exist)

  //添加新节点
  var point = d3.mouse(this),
      node = {temp_index: lastNodeIndex+"", "label":"Character", "name": lastNodeIndex+"", "weight":1};
  node.x = point[0];
  node.y = point[1];
  nodes.push(node);
  submmitModifyNode(node, ModifyAction.ADD);
  setSelectedNodeOrLink(node, null);    //选中新加的节点

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
  submmitModifyLink(link, ModifyAction.DELETE);
  var sourceId = link.source.temp_index,
      targetId = link.target.temp_index;

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
    submmitModifyLink(l, ModifyAction.DELETE);
  });
  submmitModifyNode(node, ModifyAction.DELETE);
}

// only respond once per keydown
var lastKeyDown = -1;
var keyitems = [17, //Ctrl
                8,  // backspace键
                46, // delete键
                66, // B键
                76, // L键
                82 // R键
                ];

//键盘按键事件
function keydown() {
  if (document.activeElement.nodeName == "INPUT") {
    return;
  }

  if(keyitems.indexOf(d3.event.keyCode) > 0){
    d3.event.preventDefault();      //阻止默认按键行为
  }

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
        model.removeState(selected_node.temp_index);
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
        var sourceId = selected_link.source.temp_index,
            targetId = selected_link.target.temp_index;
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
        var sourceId = selected_link.source.temp_index,
            targetId = selected_link.target.temp_index;
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
          model.removeTransition(selected_node.temp_index, selected_node.temp_index);
        } else {
          selected_node.reflexive = true;
          model.addTransition(selected_node.temp_index, selected_node.temp_index);
        }
      } else if(selected_link) {
        var sourceId = selected_link.source.temp_index,
            targetId = selected_link.target.temp_index;
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



var hideKeys = new Set(['x', 'y', 'px', 'py', 'id', 'index', 'temp_index', 'left', 'right', 'hash']);

function setSelectedNodeOrLink(node, link) {
  if (node != null && link != null) {
    return;
  }
  selected_node = node;
  selected_link = link;

  if (node) {       // 选中节点、更新编辑面板
      // 更新选中节点标签
      selectedNodeLabel.html(selected_node ? '<strong>选中了人物：'+selected_node.temp_index+'</strong>' : '未选中人物');

      // 更新左侧变量面板
      varTable.classed('inactive', !selected_node);
      varSubmmit.classed('inactive', !selected_node);

      //生成左侧变量表
      if(selected_node){
          var htmlStr = "";
          var nodeKeys = Object.keys(selected_node);
          for(var key in nodeKeys){
            if(!hideKeys.has(nodeKeys[key])){
                switch(nodeKeys[key]) {
                    // 不能修改的字段使用lable显示
                    case 'avatar':
                        break;
                    case 'pagerank':
                    case 'community':
                    case 'fixed':
                        htmlStr += '<tr class="m-b-sm"><td class="var-name">' + nodeKeys[key] + ':</td><td class="var-value"><div class="btn-group">' +
                            '<label for="">' + selected_node[nodeKeys[key]] + '</label> </div></td></tr>';
                        break;
                    default:
                        htmlStr += '<tr class="m-b-sm"><td class="var-name">' + nodeKeys[key] + ':</td><td class="var-value"><div class="btn-group">' +
                            '<input id="' + nodeKeys[key] + '_value" type="text" class="form-control" value="' + selected_node[nodeKeys[key]] + '"> </div></td></tr>';
                        break;
                }
            }
          }

          htmlStr += '<tr class="m-b-sm"><td class="var-name">avatar:</td><td class="var-value"><div class="btn-group">' +
                            varAvatarRow.html() + '</div></td></tr>';

          varTableBody.empty();
          varTableBody.html(htmlStr);

          if(nodeKeys.indexOf('avatar') > -1){
                $('#avatar_value').val(selected_node['avatar']);
          }
      }
  /*==============================================================================================================*/
  } else if (link) {    // 选中连线，更新编辑面板
      // 更新选中节点标签
      selectedNodeLabel.html(selected_link ? '<strong>选中了关系：'+'</strong>' : '未选中关系');
      varTable.classed('inactive', !selected_link);
      varSubmmit.classed('inactive', !selected_link);

      //生成左侧变量表
      if(selected_link){
          var htmlStr = "",
              linkKeys = Object.keys(selected_link);
          for(var key in linkKeys){
            if(!hideKeys.has(linkKeys[key])){
                switch(linkKeys[key]) {
                    // 不能修改的字段使用lable显示
                    case 'source':
                    case 'target':
                        htmlStr += '<tr class=""><td class="var-name">' + linkKeys[key] + ':</td><td class="var-value"><div class="btn-group">' +
                            '<label for="">' + selected_link[linkKeys[key]]['name'] + '</label> </div></td></tr>';
                        break;
                    default:
                        htmlStr += '<tr class=""><td class="var-name">' + linkKeys[key] + ':</td><td class="var-value"><div class="btn-group">' +
                            '<input id="' + linkKeys[key] + '_value" type="text" class="form-control" value="' + selected_link[linkKeys[key]] + '"> </div></td></tr>';
                        break;
                }
            }
          }
          varTableBody.empty();
          varTableBody.html(htmlStr);
      }
  } else {
      // 更新选中节点标签
      varTable.classed('inactive', true);
      varSubmmit.classed('inactive', true);
      selectedNodeLabel.html('未选中');
      varTableBody.html('');
  }
}


function setAppMode(newMode) {
  // mode-specific settings
  if(newMode === MODE.EDIT) {
    // 启用listeners
    svg.classed('edit', true)
      .style('background', '#252d47')
      .on('mousedown', mousedown)
      .on('mousemove', mousemove)
      .on('mouseup', mouseup)
      .call(unzoomListener);
    d3.select(window)
      .on('keydown', keydown)
      .on('keyup', keyup);

    var zoom = d3.behavior.zoom()
    zoom.scale(zoom.scale()*2 ).translate(zoom.translate());
    //// 绕整个svg的中心缩放
    //var centerX = width / 2,
    //    centerY = height / 2,
    //    scale = 1.0;
    //var sc = "translate(" + -centerX*(scale-1) + "," + -centerY*(scale-1)  + ")scale(" + scale + ")";
    //path.attr("transform", sc);
    //circle.selectAll('g').attr("transform",  sc);
    //circle.selectAll('circle').attr("transform",  sc);
    //circle.selectAll('text').attr("transform",  sc);

    // remove eval classes
    circle
      .classed('waiting', false)
      .classed('true', false)
      .classed('false', false);
    currentFormula.classed('inactive', true);

    circle
      .on('mousedown.drag', null)
      .on('touchstart.drag', null);
    svg.classed('ctrl', false);

    path.attr("stroke-width", "8px");
  } else if(newMode === MODE.EVAL) {
    // 禁用listeners (except for I-bar prevention)
    svg.classed('edit', false)
      .style('background', '#fff')
      .on('mousedown', function() { d3.event.preventDefault(); })
      .on('mousemove', null)
      .on('mouseup', null)
      .call(zoomListener);
    d3.select(window)
      .on('keydown', null)
      .on('keyup', null);

    // 启用节点可拖拽
    circle.call(force.drag);
    svg.classed('ctrl', true);
    lastKeyDown = -1;

    path.attr("stroke-width", function(d) { return Math.sqrt(d.weight); });

    // in case still dragging
    drag_line
      .classed('hidden', true)
      .style('marker-end', '');

    // clear mouse vars
    setSelectedNodeOrLink(null, null);
    resetMouseVars();

    // reset eval state
    circle.classed('waiting', false);
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

/**
 * 显示社区区分的颜色
 */
function setShowCommunities() {
    showCommunty = !showCommunty;
    restart();
}

function setTotalPeople(total) {
    d3.select('#peopleCount').html(total);
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




var ModifyAction ={
  ADD:1,
  DELETE:2,
  ALTER:3
}
//编辑：仅修改节点或关系
function updateNodeOrLink() {
  if(selected_node) {
    // 读取左侧表格节点的数据
    var posi = nodes.indexOf(selected_node);
    var nodeKeys = Object.keys(selected_node);
    for(var i in nodeKeys){
        var input = document.getElementById(nodeKeys[i]+'_value');
        if(input != null){
            selected_node[nodeKeys[i]] = input.value;
        }
    }
    if($('#avatar_value').val()){
        selected_node['avatar'] = $('#avatar_value').val();
    }
    submmitModifyNode(selected_node, ModifyAction.ALTER);

    // 先删除再添加
    nodes.splice(posi, 1);
    restart();
    nodes.splice(posi, 0, selected_node);
    restart();

  }else if(selected_link) {
    // 读取左侧表格边的数据
    var pos_l = links.indexOf(selected_link);
    var linkKeys = Object.keys(selected_link);
    for(var i in linkKeys){
        var input = document.getElementById(linkKeys[i]+'_value');
        if(input != null){
            selected_link[linkKeys[i]] = input.value;
        }
    }
    submmitModifyLink(selected_link, ModifyAction.ALTER);

    // 先删除再添加
    links.splice(pos_l, 1);
    restart();
    links.splice(pos_l, 0, selected_link);
    restart();
  }
}
//编辑节点：增、删、改
function submmitModifyNode(node, action) {
  $.post("/editor/post", {
        type: "node",
        node: JSON.stringify(node),
        act: action
    }, function(data){
        if(action === ModifyAction.ADD) {
            // 添加服务端返回的id
            temp = node;
            temp['id'] = data.result.uid;
            nodes.splice(nodes.indexOf(node), 1, temp);
            restart();
        }else if(action === ModifyAction.ALTER){
        }
  })
}
//编辑关系：增、删、改
function submmitModifyLink(link, action) {
  $.post("/editor/post", {
        type: "link",
        link: JSON.stringify(link),
        act: action
    }, function(data){
  })
}