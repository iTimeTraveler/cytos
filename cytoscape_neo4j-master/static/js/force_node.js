// d3 4.0版本
$(function(){
  $.get('/'+projectId+'/editor/graph', function(result) {

    //接受服务端返回的json数据
    var result = JSON.parse(JSON.stringify(result));
    var root = result.elements;
    console.log(JSON.stringify(root));


    //把边的source和target转换成序号连接的
    var edges = [];
    root.edges.forEach(function(e) {
        // Get the source and target nodes
        var sourceNode = root.nodes.filter(function(n) { return n.id === e.source; })[0],
            targetNode = root.nodes.filter(function(n) { return n.id === e.target; })[0];
            relationShip = e.relation;

        // Add the edge to the array
        edges.push({source: sourceNode, target: targetNode, relation: relationShip});
    });


    //svg窗口的宽高
    var width = window.screen.availWidth - 220;
    var height = window.screen.availHeight - 220;
    var colors = d3.scaleOrdinal(d3.schemeCategory20);
    var radius = 15;


    var svg = d3.select("#force_content").append("svg")
                                .attr("width",width)
                                .attr("height",height);


    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().distance(100).id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width / 2, height / 2));


    // 开始d3画图
    var drawNodeNetwork = function(){

        //边
        var edges_line = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(edges)
            .enter().append("line")
            .attr("stroke-width", 1);

        //边的文字
        var edges_text = svg.append("g").selectAll(".linetext")
            .data(edges)
            .enter()
            .append("text")
            .attr("class","linetext")
            .append('tspan')
            .attr('x',0)
            .attr('y',20)
            .text(function(d){
                return d.relation;
            });

//        var edges_text = svg.append("g").selectAll(".linetext")
//            .data(edges)
//            .enter()
//            .append("text")
//            .attr("class","linetext")
//            .attr('x',0)
//            .attr('y',20)
//            .append('textPath')
//            .attr('xlink:href',function(d,i) {return '#edgepath'+i})
//            .style("pointer-events", "none")
//            .text(function(d){
//                return d.relation;
//            });

        //节点圆圈
        var highlight = -1;  //当前点亮的节点
        var relateIds = new Set();      //点击以后所有相关联的节点
        var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(root.nodes)//表示使用force.nodes数据
            .enter().append("circle")
            .style("fill", function(d) { return colors(d.community); })
            .style('stroke', "#fff")
            .attr("r", radius)  //设置圆圈半径
            .on("click",function(d,i){
                onNodeClick(d, i);
                //d3.select(this).style('stroke-width',2);
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        //节点提示
        node.append("title")
                    .text(function(d) { return d.id; });


        //节点文字
        var nodes_text = svg.append("g")
            .attr("class", "name")
            .selectAll("text")
            .data(root.nodes)
            //返回缺失元素的占位对象（placeholder），指向绑定的数据中比选定元素集多出的一部分元素。
            .enter()
            .append("text")
            .attr("dy", "0.5em")
            .attr("text-anchor", "middle")//在圆圈中加上数据
            .attr('x',function(d){
                var re_en = /[a-zA-Z]+/g;
                //如果是全英文，不换行
                if(!d.name){
                    return 0;
                }
                else if(d.name.match(re_en)){
                     d3.select(this).append('tspan')
                     .attr('x',0)
                     .attr('y',0)
                     .text(function(){return d.name;});
                }
                //如果小于四个字符，不换行
                else if(d.name.length<=4){
                     d3.select(this).append('tspan')
                    .attr('x',0)
                    .attr('y',0)
                    .text(function(){return d.name;});
                }else{
                    var top=d.name.substring(0,4);
                    var bot=d.name.substring(4,d.name.length);

                    d3.select(this).text(function(){return '';});

                    d3.select(this).append('tspan')
                        .attr('x',0)
                        .attr('y',-7)
                        .text(function(){return top;});

                    d3.select(this).append('tspan')
                        .attr('x',0)
                        .attr('y',10)
                        .text(function(){return bot;});
                }
            })
            .on("click",function(d,i){
                onNodeClick(d, i);
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        //节点点击事件
        var onNodeClick = function(d, i) {
                relateIds.clear();

                //如果选中了新的节点
                if (highlight != i) {
                    highlight = i;
                    //突出连接线
                    edges_line.style("stroke-opacity",function(edge){
                        if( edge.source.id === d.id || edge.target.id === d.id ){
                            relateIds.add((edge.source.id === d.id) ? edge.target : edge.source);
                            return 1;
                        } else {
                            return 0;
                        }
                    });
                    //单击时让连接线加粗
                    edges_line.style("stroke-width",function(line){
                        if(line.source.id === d.id || line.target.id === d.id){
                            return 3;
                        }
                    });
                    //显示连接线上的文字
                    edges_text.style("fill-opacity",function(edge){
                        if( edge.source.id === d.id || edge.target.id === d.id ){
                            return 1.0;
                        }
                    });
                    node.style("opacity", function(node){
                        return dealwithOpacity(node, d, relateIds);
                    });
                    nodes_text.style("opacity", function(node){
                        return dealwithOpacity(node, d, relateIds);
                    });

                } else {   //如果点击了已选中的节点
                    highlight = -1;
                    //隐去连接线上的文字
                    edges_text.style("fill-opacity", 0);
                    //恢复显示所有的连接线、节点、节点文字
                    edges_line.style("stroke-opacity", 1);
                    edges_line.style("stroke-width", 1);
                    nodes_text.style("opacity", 1);
                    node.style("opacity", 1);
                }
        }

        //处理节点的显示与隐藏
        var dealwithOpacity = function(every, d, relateIds){
            if( every.id === d.id ) {
                return 1.0;
            } else if (relateIds.has(every)){
                return 0.7;
            } else {
                return 0.03;
            }
        }

        function ticked() {
            edges_line
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });

            //限制结点的边界
            root.nodes.forEach(function(d,i){
                d.x = d.x - radius < 0     ? radius : d.x ;
                d.x = d.x + radius > width ? width - radius : d.x ;
                d.y = d.y - radius < 0      ? radius : d.y ;
                d.y = d.y + radius > height ? height - radius : d.y ;
            });

            //顶点文字位置
            nodes_text.attr("transform", function (d) {
                  return "translate(" + (d.x) + "," + d.y + ")";
            });

            //更新连接线上文字的位置
             edges_text.attr("x",function(d){ return (d.source.x + d.target.x) / 2 ; });
             edges_text.attr("y",function(d){ return (d.source.y + d.target.y) / 2 ; });
        }

        simulation
            .nodes(root.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(edges);
    }
    // 终止d3画图

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    drawNodeNetwork();
//    alert("drawNodeNetwork");

  }, 'json');
});
