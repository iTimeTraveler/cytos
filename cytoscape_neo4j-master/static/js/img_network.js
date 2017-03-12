// d3 4.0版本
$(function(){
  $.get('/'+projectId+'/editor/graph', function(result) {

    //接受服务端返回的整个图谱的json数据
    var result = JSON.parse(JSON.stringify(result));//把json格式的字符串解析为json对象(层层嵌套的格式)让js识别
    var root = result.elements;

    console.log(JSON.stringify(root));
    //SVG 是用来描述二维图形和绘图程序的语言，SVG 用来定义用于网络的基于矢量的图形，可缩放但是图片失真较小
    //svg窗口的宽高
    var width = window.screen.availWidth;
    var height = window.screen.availHeight - 200;
    //人物图片的宽高
    var img_w = 60;
    var img_h = 70;
    var radius = 25;	//圆形半径
    var line_width = 2; //连线粗细


    //把边的source和target由只是name连接转换成整个节点连接
    var edges = [];
    root.edges.forEach(function(e) {
        // Get the source and target nodes
        var sourceNode = root.nodes.filter(function(n) { return n.id === e.source; })[0],
            targetNode = root.nodes.filter(function(n) { return n.id === e.target; })[0];
            relationShip = e.relation;

        // Add the edge to the array
        edges.push({source: sourceNode, target: targetNode, relation: relationShip});
    });


//    console.log(JSON.stringify(edges));
    var colors = d3.scale.category10(); // 创建头像边框的10种颜色 d3.scale.category()--d3固定函数
    var avatars = ["chanyou", "guixie", "lingsha", "mengli", "suyao", "suyu", "taiqing", "tianhe", "tianqing", "xizhong" ];


    //生成力导向布局
    var drawNetworks = function(){
        var force = d3.layout.force()
                        .nodes(root.nodes)
                        .links(edges) // elements.edges
                        .size([width,height])
                        .linkDistance(200) // 线长
                        .charge(-1000)  // 斥力大小
                        .start();

        //创建缩放行为
        var zoomListener = d3.behavior.zoom()
                        .scaleExtent([0.3, 5])  // 缩放比例区间
                        .on("zoom", null); // zoomed是后文定义的函数:缩放规律

       //创建一个svg变量
        var svg = d3.select("#imgnetwork_content").append("svg") //选中#imgnetwork_content容器添加svg控件
                        .attr("id", "mysvg") // attr添加定义属性
                        .attr("width",width)
                        .attr("height",height)
					    .call(zoomListener);

        //边
        var edges_line = svg.selectAll("line")
                            .data(force.links())
                            .enter()
                            .append("line")
                            .style("stroke","#ccc") // stroke() 方法绘制当前路径的边框
                            .style("stroke-width", line_width);

        //边的文字
        var edges_text = svg.selectAll(".linetext")
                            .data(force.links())
                            .enter()
                            .append("text")
                            .attr("class","linetext")
                            .text(function(d){
                                return d.relation;
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
                                var defs = svg.append("defs").attr("id", "imgdefs") //在svg里面添加defs字段
                                var catpattern = defs.append("pattern") //在defs内层嵌套添加pattern字段
                                                    .attr("id", "catpattern" + i)
                                                    .attr("height", 1)
                                                    .attr("width", 1)
                                catpattern.append("image")
                                    .attr("x", - (img_w / 2 - radius))
                                    .attr("y", - (img_h / 2 - radius))
                                    .attr("width", img_w)
                                    .attr("height", img_h)
                                    .attr("xlink:href", function(which){
                                        if(d.avatar){
                                            return d.avatar;
                                        }else{
                                            var community = d.community==null ? 0 : d.community;
                                            return "/static/img/" + avatars[community] + ".png";
                                        }
                                    })
                                return "url(#catpattern" + i + ")";
                            })
                            .on("click",function(d,i){
                                relateIds.clear();

                                //如果点击了新的节点
                                if (highlight != i) {
                                    highlight = i;
                                    edges_line.style("stroke-width", 4); // 突出连接线，加粗
                                    edges_line.style("stroke-opacity",function(edge){
                                        if( edge.source.id === d.id || edge.target.id === d.id ){
                                            relateIds.add((edge.source.id === d.id) ? edge.target : edge.source);
                                            return 1; // 显示。添加与当前节点相连的其他节点的id到relateIds里面
                                        } else {
                                            return 0; // 隐藏
                                        }
                                    });
                                    //显示连接线上的文字
                                    edges_text.style("fill-opacity",function(edge){
                                        if( edge.source.id === d.id || edge.target.id === d.id ){
                                            return 1;
                                        }
                                    });
                                    nodes_img.style("opacity", function(node){
                                        return dealwithOpacity(node, d, relateIds); // 转到下面的dealwithOpacity函数
                                    });
                                    nodes_text.style("opacity", function(node){
                                        return dealwithOpacity(node, d, relateIds);
                                    });

                                } else {   //如果点击了之前点击的节点=点击两次：即最初的样式
                                    highlight = -1;
                                    //隐去连接线上的文字
                                    edges_text.style("fill-opacity", 0); // opacity不透明性为0=隐藏
                                    //恢复显示所有的连接线、节点、节点文字
                                    edges_line.style("stroke-opacity", 1);// 显示
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
                            // 设置名字的x.y轴起始坐标
                            .attr("dx",function(d){
                                return d.name ? d.name.length * -7 : 0;
                            })
                            .attr("dy",text_dy)
                            .text(function(d){
                                return d.name;
                            });

        //处理节点的显示与隐藏 分三档显示：当前节点全显示，相关节点半透明度显示，无关节点全隐藏
        var dealwithOpacity = function(every, d, relateIds){
            if( every.id === d.id ) {
                return 1;
            } else if (relateIds.has(every)){
                return 0.5;
            } else {
                return 0;
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

            //不断刷新连接线的位置
             edges_line.attr("x1",function(d){ return d.source.x; });
             edges_line.attr("y1",function(d){ return d.source.y; });
             edges_line.attr("x2",function(d){ return d.target.x; });
             edges_line.attr("y2",function(d){ return d.target.y; });

             //不断刷新连接线上文字的位置
             edges_text.attr("x",function(d){ return (d.source.x + d.target.x) / 2 ; });
             edges_text.attr("y",function(d){ return (d.source.y + d.target.y) / 2 ; });


             //不断刷新结点图片和文字
             nodes_img.attr("cx",function(d){ return d.x });
             nodes_img.attr("cy",function(d){ return d.y });

             nodes_text.attr("x",function(d){ return d.x });
             nodes_text.attr("y",function(d){ return d.y + radius; });
        });
        // 定义缩放规律，节点先移动（translate）位置，再缩放
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