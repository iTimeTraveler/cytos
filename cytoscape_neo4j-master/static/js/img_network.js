$(function(){
  $.get('/graph', function(result) {

    //接受服务端返回的json数据
    var result = JSON.parse(JSON.stringify(result));
    var root = result.elements;

    console.log(JSON.stringify(root));

    //svg窗口的宽高
    var width = window.screen.availWidth;
    var height = window.screen.availHeight - 200;
    //人物图片的宽高
    var img_w = 77;
    var img_h = 90;
    var radius = 35;	//圆形半径
    var line_width = 1;


    //把边的source和target转换成序号连接的
    var edges = [];
    root.edges.forEach(function(e) {
        // Get the source and target nodes
        var sourceNode = root.nodes.filter(function(n) { return n.name === e.source; })[0],
            targetNode = root.nodes.filter(function(n) { return n.name === e.target; })[0];
            relationShip = e.relation;

        // Add the edge to the array
        edges.push({source: sourceNode, target: targetNode, relation: relationShip});
    });


//    console.log(JSON.stringify(edges));
    var colors = d3.scale.category10();
    var avatars = ["chanyou", "guixie", "lingsha", "mengli", "suyao", "suyu", "taiqing", "tianhe", "tianqing", "xizhong" ];


    //生成力导向布局
    var drawNetworks = function(){
        var force = d3.layout.force()
                        .nodes(root.nodes)
                        .links(edges)
                        .size([width,height])
                        .linkDistance(400)
                        .charge(-3000)
                        .start();

        //缩放监听
        var zoomListener = d3.behavior.zoom()
                        .scaleExtent([0.3, 5])  //缩放比例区间
                        .on("zoom", zoomed);


        var svg = d3.select("body").append("svg")
                        .attr("id", "mysvg")
                        .attr("width",width)
                        .attr("height",height)
					    .call(zoomListener);

        //边
        var edges_line = svg.selectAll("line")
                            .data(force.links())
                            .enter()
                            .append("line")
                            .style("stroke","#ccc")
                            .style("stroke-width", line_width);

        //边的文字
        var edges_text = svg.selectAll(".linetext")
                            .data(force.links())
                            .enter()
                            .append("text")
                            .attr("class","linetext")
                            .text(function(d){
                                return d.relation;
                                //return "君臣";
                            });


        //节点,图片
        var highlight = -1;  //当前点亮的节点
        var relateIds = new Set();      //点击以后所有相关联的节点
        var nodes_img = svg.selectAll("image")
                            .data(force.nodes())
                            .enter()
                            .append("circle")
                            .attr("class", "circleImg")
                            .attr("stroke", function(d) { return colors(d.community); })
                            .attr("r", radius)
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
                                        //return "static/img/"+d.image;
                                        var community = d.community==null ? 0 : d.community;
                                        return "/static/img/" + avatars[community] + ".png";
                                    })
                                return "url(#catpattern" + i + ")";
                            })
                            .on("click",function(d,i){
                                relateIds.clear();

                                //如果选中了新的节点
                                if (highlight != i) {
                                    highlight = i;
                                    //突出连接线
                                    edges_line.style("stroke-width", 2);
                                    edges_line.style("stroke-opacity",function(edge){
                                        if( edge.source.name === d.name || edge.target.name === d.name ){
                                            relateIds.add((edge.source.name === d.name) ? edge.target : edge.source);
                                            return 1;
                                        } else {
                                            return 0;
                                        }
                                    });
                                    //显示连接线上的文字
                                    edges_text.style("fill-opacity",function(edge){
                                        if( edge.source.name === d.name || edge.target.name === d.name ){
                                            return 1.0;
                                        }
                                    });
                                    nodes_img.style("opacity", function(node){
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
                                    edges_line.style("stroke-width", line_width);
                                    nodes_img.style("opacity", 1);
                                    nodes_text.style("opacity", 1);
                                }
                            })
                            .call(force.drag);


        //节点文字
        var text_dy = 25;
        var nodes_text = svg.selectAll(".nodetext")
                            .data(force.nodes())
                            .enter()
                            .append("text")
                            .attr("class","nodetext")
                            .attr("dx",function(d){
                                return d.name.length * -4;
                            })
                            .attr("dy",text_dy)
                            .text(function(d){
                                return d.name;
                            });

        //处理节点的显示与隐藏
        var dealwithOpacity = function(every, d, relateIds){
            if( every.name === d.name ) {
                return 1.0;
            } else if (relateIds.has(every)){
                return 0.5;
            } else {
                return 0.03;
            }
        }

        force.on("tick", function(){

            //限制结点的边界
//            root.nodes.forEach(function(d,i){
//                d.x = d.x - img_w/2 < 0     ? img_w/2 : d.x ;
//                d.x = d.x + img_w/2 > width ? width - img_w/2 : d.x ;
//                d.y = d.y - img_h/2 < 0      ? img_h/2 : d.y ;
//                d.y = d.y + img_h/2 + text_dy > height ? height - img_h/2 - text_dy : d.y ;
//            });

            //更新连接线的位置
             edges_line.attr("x1",function(d){ return d.source.x; });
             edges_line.attr("y1",function(d){ return d.source.y; });
             edges_line.attr("x2",function(d){ return d.target.x; });
             edges_line.attr("y2",function(d){ return d.target.y; });

             //更新连接线上文字的位置
             edges_text.attr("x",function(d){ return (d.source.x + d.target.x) / 2 ; });
             edges_text.attr("y",function(d){ return (d.source.y + d.target.y) / 2 ; });


             //更新结点图片和文字
             nodes_img.attr("cx",function(d){ return d.x });
             nodes_img.attr("cy",function(d){ return d.y });

             nodes_text.attr("x",function(d){ return d.x });
             nodes_text.attr("y",function(d){ return d.y + radius; });
        });

        function zoomed() {
            var sc = "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")";

            edges_line.attr("transform", sc);
            edges_text.attr("transform",  sc);
            nodes_img.attr("transform",  sc);
            nodes_text.attr("transform",  sc);
        }
    }

    drawNetworks();

  }, 'json');
});