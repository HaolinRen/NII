"use strict"
var paraBB = {
    paraTag : "bpp",
    graphPara : {
        toggleId: 'gs4',
        tagId : "bppgp",
        formTagID : "bcw",
        scale : "log",
        maxBubbleNum : 80, 
    },
    groupPara : {
        toggleId: 'gps4',
        tagId : "bppgo",
        formTagID : "gppb",
        groupNum : 10,
        isUpdate : true,
    },
    biggestSize : 36,
    smallSize : 14,
};
var paraHM = {
    paraTag : "mpp",
    graphPara : {
        toggleId: 'gs3',
        tagId : "mppgp",
        
        formTagID : "pcw",
        maxMatrixSize : 30,
    },
    groupPara : {
        toggleId: 'gps3',
        tagId : "mppgo",
        formTagID : "gmp",
        groupNum : 0
    },
    biggestSize : 0,
    smallSize : 0,
};

var paraFN = {
    paraTag : "spp",
    graphPara : {
        toggleId: 'gs2',
        tagId : "sppgp",
        formTagID : "nfw",
        scale : "log",
        maxNodesNum : 20,
        nodesDist : 200,
    },
    groupPara : {
        toggleId: 'gps2',
        tagId : "sppgo",
        isGroupColor : true,
        isGroupFilter : true,
        formTagID : "gfp",
        groupNum : 4,
    },
    biggestSize : 14,
    smallSize : 3,
};

function getTermIndex(termText, inGraph) {
    var re = -1;
    var len = inGraph.sizeOfMatrix;
    for (var temp1 = 0; temp1 < len; temp1 += 1) {
        if (termText === inGraph.nodes[temp1].text) {
            re = temp1;
            break;
        }
    }
    return re;
}

function testNeighbour(a, b, inGraph) {
    var i1, i2;
    if (typeof a == "number") {
        if (i1 >= inGraph.sizeOfMatrix || i2 >= inGraph.sizeOfMatrix) {
            return false;
        }
        i1 = a;
        i2 = b;
    } else {
        i1 = getTermIndex(a, inGraph);
        i2 = getTermIndex(b, inGraph);
        if (i1 === -1 || i2 === -1) {
            return false;
        }
    }
    return inGraph.matrix[i1][i2] !== 0;
}

function forceLayout(pointer) {
    var termGraph = pointer.myData;
   
    var winWidth = pointer.width;
    var winHeight = parseInt(winWidth*0.6);

    var subInterGraph = "undefined";
    var color = d3.scale.category20();
    var groupFill = d3.scale.category10();
    var svg = d3.select("#gfl")
                .append("svg:svg")
                .attr("height", winHeight)
                .attr("width", winWidth);

    var force = d3.layout.force()
                    .nodes(termGraph.nodes)
                    .links(termGraph.links)
                    .charge(-200)
                    .friction(0.5)
                    .linkDistance(pointer.parameters.graphPara.nodesDist)
                    .size([winWidth, winHeight])
                    .start();

    var link = svg.selectAll("line.link")
                .data(termGraph.links)
                .enter().append("svg:line")
                .attr("class", "link")
                .attr("x1", function(d){ return d.source.x; })
                .attr("y1", function(d){ return d.source.y; })
                .attr("x2", function(d){ return d.target.x; })
                .attr("y2", function(d){ return d.target.y; })
                .style("strock-width", 0.2);

    function dragstart(d, i) {
        force.stop();
        svg.selectAll("g.node").on("mouseover", null).on("mouseout", null);
        d3.selectAll(".glabel").on("mouseover", null).on("mouseout", null);
    }

    function dragmove(d, i) {
        d.px += d3.event.dx;
        d.py += d3.event.dy;
        d.x += d3.event.dx;
        d.y += d3.event.dy;
        d.px = Math.max(20, Math.min(winWidth - 20, d.px));
        d.py = Math.max(20, Math.min(winHeight - 20, d.py));
        d.x = Math.max(20, Math.min(winWidth - 20, d.x));
        d.y = Math.max(20, Math.min(winHeight - 20, d.y));
        tick();
    }

    function dragend(d, i) {
        svg.selectAll("g.node").on("mouseover", fadeIn).on("mouseout", fadeOut);
    }

    var node_drag = d3.behavior.drag()
                .on("dragstart", dragstart)
                .on("drag", dragmove)
                .on("dragend", dragend);

    var node = svg.selectAll("g.node")
                .data(termGraph.nodes)
                .enter().append("svg:g")
                .attr("class","node")
                .on("mouseover", fadeIn)
                .on("mouseout", fadeOut)
                .on("click", function(d) {
                    reOrderList.whichElement(d.text);
                })
                .call(node_drag);

    node.append("circle")
        .attr("class", "circle")
        .attr("r", function(d) {
            d.nodeSize = pointer.optimiseSize(d.termIndex, 200);
            return d.nodeSize; })
        .style("fill", function(d, i) {                
            return color(d.group);
        });

    node.append("svg:text")
        .attr("class","glabel")
        .attr("dx", 8)
        .attr("text-anchor", "start")
        .attr("dy", ".35em")
        .text(function(d) { return d.text; })
        // .style("display", function() {
        //     // return termGraph.sizeOfMatrix > 30 ? "none" : "inline";
        // });

    function tick() {
        link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) {
            d.x = Math.max(20, Math.min(winWidth - 20, d.x));
            d.y = Math.max(20, Math.min(winHeight - 20, d.y));
            return "translate(" + d.x + "," + d.y + ")";});
    }

    force.on("tick", tick);

    function fadeIn(d, i) {
        var sameGroupTerms = [];
        var clickedOrder, cOrder, index, c1, c2;
        node.transition()
            .duration(400)
            .style("opacity", 0.1)
            .filter(function(g, j) {
                if (pointer.parameters.groupPara.isGroupFilter) {
                    if (g.group === d.group) {
                        sameGroupTerms.push(j);
                        return true;
                    } else {
                        return false;
                    }
                } else {
                    if (g.group === d.group) {
                        sameGroupTerms.push(j);
                    };
                    if (testNeighbour(i, j, termGraph)) {
                        return true;
                    } else {
                        return false;
                    }} 
                })
            .style("opacity", 1)
            .select("circle")
            .attr("r", function(g, k) {
                if (pointer.parameters.groupPara.isGroupFilter) {
                    if (k !== i) {
                        return 20 * (0.5 + termGraph.matrix[i][k] * termGraph.matrix[k][i]);
                    } else {
                        return 20;
                    }
                } else {
                    if (g.text === d.text) {
                        return d.nodeSize;
                    } else {
                        if (subInterGraph === "undefined") {
                            subInterGraph = getSubInterGraph(termGraph.neighbourDict[i], termGraph);
                            clickedOrder = getTermIndex(d.text, subInterGraph);
                        }
                        cOrder = getTermIndex(g.text, subInterGraph);
                        index  = subInterGraph.matrix[clickedOrder][cOrder] * subInterGraph.matrix[cOrder][clickedOrder];
                        return 20 * (0.5 + index);
                    }
                }
            });

        if (pointer.parameters.groupPara.isGroupFilter) {
            subInterGraph = getSubInterGraph(sameGroupTerms, termGraph);
        } else {
            var sameGroupInterGraph = getSubInterGraph(sameGroupTerms, termGraph);
        };

        link.transition()
            .duration(400)
            .style("opacity", function (o) {
                if (testNeighbour(o.source.text, o.target.text, subInterGraph)) {
                    return 1;
                } else {
                    return 0.1;
                }
            });

        node.select(".glabel").transition()
            .duration(400)
            .style("display", "none")
            .filter(function(o) {
                if (pointer.parameters.groupPara.isGroupFilter) {
                    if (o.group == d.group) {
                        return true;
                    } else {
                        return false;
                    }
                } else {
                    return testNeighbour(d.text, o.text, subInterGraph) != 0;
                }
            })
            .style("display", "inline");
    }

    function fadeOut(d) {
        subInterGraph = "undefined";
        node.transition()
            .duration(400)
            .style("opacity", 1)
            .select("circle")
            .attr("r", function(d) { 
                return pointer.optimiseSize(d.termIndex, 200); 
            });

        link.transition().style("opacity", 1);

        node.select(".glabel")
            .transition()
            .style("display", function() {
                return termGraph.sizeOfMatrix > 30 ? "none" : "inline";
            });
    }

    d3.select("#gnrn").on("change", function() {
        pointer.parameters.groupPara.groupNum = +this.value;
        makeGroup.groupTheGraph(termGraph, +this.value);
        node.select("circle")
            .style("fill", function(d, i) {
                return color(d.group);
            });
    });
}

function matrixHeatMapLayout(pointer) {
    var objectMatrix = pointer.myData;
    var margin = { top: 160, right: 0, bottom: 10, left: 160 },
        mSize = objectMatrix.sizeOfMatrix,
        gridSize = parseInt(18 - (mSize / 10)),
        width = mSize * gridSize + 300,
        height = mSize * gridSize + 160,
        w2 = gridSize * mSize + 40,
        legendElementWidth = 30,
        buckets = 10,
        colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#48D1CC","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"];

    var groupFill = d3.scale.category10();
    var colorScale = d3.scale.quantile()
        .domain([0, 1])
        .range(colors);

    var svg = d3.select("#gmx").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var cordY = svg.selectAll(".cordY")
        .data(objectMatrix.nodes)
        .enter().append("text")
        .text(function (d) { return d.text; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize + 2; })
        .style("font-size", (gridSize-1) + "px")
        .style("fill", "#000")
        .style("text-anchor", "end")
        .attr("transform", "translate(0," + gridSize / 1.5 + ")");

    var cordX = svg.selectAll(".cordX")
        .data(objectMatrix.nodes)
        .enter().append("text")
        .text(function(d) { return d.text; })
        .attr("x", 0)
        .attr("y", function(d, i) { return i * gridSize + 14; })
        .style("font-size", gridSize + "px")
        .style("fill", "#000")
        .style("text-anchor", "start")
        .attr("transform", "translate(" + gridSize / 2 + ', -6)rotate(-90)');

    var heatMap = svg.selectAll(".entangleIndice")
        .data(objectMatrix.heatMatrix)
        .enter().append("rect")
        .attr("x", function(d, i) { return (i%mSize)*gridSize + 10; })
        .attr("y", function(d, i) { return Math.floor(i/mSize)*gridSize; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "entangleIndice bordered")
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("fill", colors[0]);

    function updateHeatValue() {
        heatMap.transition().duration(1600)
            .style("fill", function(d, i) {
                if (d.termIndex === 0) {
                    return "#FFFFFF";
                } else {
                    return colorScale(d); 
                }
            });
        heatMap.select("title").text(function(d) { return d; });
    }

    heatMap.append("title").text(function(d) { return d; });
        
    updateHeatValue();

    var legend = svg.selectAll(".legend")
        .data([0].concat(colorScale.quantiles()), function(d) { return d; })
        .enter().append("g")
        .attr("class", "legend");

    legend.append("rect")
        .attr("x", w2)
        .attr("y", function(d, i) { return legendElementWidth * (i - 1) + 30; })
        .attr("width", 10)
        .attr("height", legendElementWidth)
        .style("fill", function(d, i) { return colors[i]; });

    legend.append("text")
        .attr("class", "mono")
        .style("font-size", gridSize / 2)
        .text(function(d) { return ">" + d.toFixed(2); })
        .attr("x", w2+12)
        .attr("y", function(d, i) { return legendElementWidth * (i - 1) + legendElementWidth/2+38; });

    function updatePosiData() {
        var tempNum = pointer.parameters.groupPara.groupNum;
        makeGroup.groupTheGraph(objectMatrix, tempNum);
        var i, j, tempIndex, tempTerm;
        tempIndex = 0;
        for (i = 1; i <= tempNum; i += 1) {
            for (j = 0; j < mSize; j += 1) {
                if (objectMatrix.nodes[j].group == i) {
                    objectMatrix.nodes[j].gOrder = tempIndex;
                    tempIndex += 1;
                }
            }
        }
    };

    d3.select("#gmrn").on("change", function() {
        pointer.parameters.groupPara.groupNum = this.value;
        updatePosiData();
        cordX.transition().duration(300)
            .style("fill", function(d) {
                return groupFill(d.group);
            })
            .attr("y", function(d, i) {
                return d.gOrder * gridSize + 14;
            });
        cordY.transition().duration(300)
            .style("fill", function(d) {
                return groupFill(d.group); })
            .transition()
            .attr("y", function(d, i) {
                return d.gOrder * gridSize + 2;
            });

        var t0, t1, tX, tY;
        heatMap.transition().duration(300)
            .attr("x", function(d, i) {
                t0 = i%mSize;
                tX = objectMatrix.nodes[t0].gOrder;
                return  tX*gridSize + 10; })
            .transition()
            .attr("y", function(d, i) {
                t1 = Math.floor(i/mSize);
                tY = objectMatrix.nodes[t1].gOrder;
                return tY*gridSize;
            });
    });
}

function bubbleLayout(pointer) {
    var padding = 0, // separation between same-color circles
        clusterPadding = 5, // separation between different-color circles
        maxRadius = 20;
    var n = pointer.myData.sizeOfMatrix,
        m = pointer.parameters.groupPara.groupNum;

    var width = pointer.width,
        height = parseInt(width*0.6);

    var color = d3.scale.category10()
                    .domain(d3.range(m));

    var nodes = [], index, groupNO, oneTerm, rad, name, oneNode, clusters = [];
    for (index = 0; index < n; index += 1) {
        oneTerm = pointer.myData.nodes[index];
        name = oneTerm.text;
        groupNO = oneTerm.group;
        rad = pointer.optimiseSize(oneTerm.termIndex, 200);
        oneNode = {cluster: groupNO, radius: rad, text: name};
        if (!clusters[oneNode.cluster] || (oneNode.radius > clusters[oneNode.cluster].radius)) {
            clusters[oneNode.cluster] = oneNode;
        }
        nodes.push(oneNode);
    }

    function updateCluster() {
        for (index = 0; index < n; index += 1) {
            nodes[index].cluster = makeGroup.groupsInfo[nodes[index].text];
        }
    }

    d3.layout.pack()
        .size([width, height])
        .children(function(d) { return d.values; })
        .value(function(d) { return d.radius * d.radius; })
        .nodes({values: d3.nest()
                .key(function(d) { return d.cluster; })
                .entries(nodes)});

    var force = d3.layout.force()
        .nodes(nodes)
        .size([width, height])
        .gravity(0)
        .charge(0)
        .on("tick", tick)
        .start();

    var tag_Name = "#" + this.tagID;
    var svg = d3.select(tag_Name).append("svg")
        .attr("width", width)
        .attr("height", height);

    var circle = svg.selectAll(".bubble")
        .data(nodes)
        .enter().append("g")
        .attr("class", "bubble")
        .on("mouseover", fadeIn)
        .on('mouseout', fadeOut)
        .on("click", function(d) {
            reOrderList.whichElement(d.text);
        })
        .call(force.drag);

    var tempLen, tempSize;
    circle.append("svg:circle")
            .attr("class", "circle")
            .style("fill", function(d) { return color(d.cluster); })
            .style("fill-opacity", 0.4);

    circle.append("svg:text")
          .text(function(d) { return d.text; })
          .style("font-size", 0)
          .attr("text-anchor", "middle")
          .attr("font-family","sans-serif")
          .attr("dy", function(d) { return d.radius/4; });

    circle.select("circle")
        .transition()
        .duration(500)
        .delay(function(d, i) {return i * 10; })
        .attrTween("r", function(d) {
            var i = d3.interpolate(0, d.radius);
            return function(t) {
                return d.radius = i(t);
            };
        });

    circle.select("text")
        .transition()
        .duration(600)
        .delay(function(d, i) {return i * 10; })
        .style("font-size", function(d) {
                tempLen = d.text.length;
                tempSize = d.radius * 10 / (3 * tempLen);
                tempSize += 2;
                return Math.round(tempSize) + "px"; 
              })

    function tick(e) {
        circle.each(cluster(10 * e.alpha * e.alpha))
                .each(collide(.2))
                .attr("x", function(d) {
                    return d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
                })
                .attr("y", function(d) {
                    return d.y = Math.max(d.radius, Math.min(height - d.radius, d.y));})
                .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"});
    }

    function fadeIn(d) {
        circle.transition()
            .duration(300)
            .style("opacity", 0.1)
            .filter(function(g) {
                if (g.cluster == d.cluster) {
                    return true;
                } else {
                    return false;
                }
                })
            .style("opacity", 1);
    }

    function fadeOut(d) {
        circle.transition()
                .duration(300)
                .style("opacity", 1);
    }

    function cluster(alpha) {
        return function(d) {
            var cluster = clusters[d.cluster],
                k = 1;
            if (cluster === d) {
              cluster = {x: width / 2, y: height / 2, radius: -d.radius};
              k = .1 * Math.sqrt(d.radius);
            }
            var x = d.x - cluster.x,
                y = d.y - cluster.y,
                l = Math.sqrt(x * x + y * y),
                r = d.radius + cluster.radius;
            if (l != r) {
                l = (l - r) / l * alpha * k;
                d.x -= x *= l;
                d.y -= y *= l;
                cluster.x += x;
                cluster.y += y;
            }
        }
    }

    // Resolves collisions between d and all other circles.
    function collide(alpha) {
        var quadtree = d3.geom.quadtree(nodes);
        return function(d) {
            var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
                nx1 = d.x - r,
                nx2 = d.x + r,
                ny1 = d.y - r,
                ny2 = d.y + r;
            quadtree.visit(function(quad, x1, y1, x2, y2) {
                if (quad.point && (quad.point !== d)) {
                    var x = d.x - quad.point.x,
                    y = d.y - quad.point.y,
                    l = Math.sqrt(x * x + y * y),
                    r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
                    if (l < r) {
                        l = (l - r) / l * alpha;
                        d.x -= x *= l;
                        d.y -= y *= l;
                        quad.point.x += x;
                        quad.point.y += y;
                    }
                }
            return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
            });
        };
    }
}

var OneWindow = function(divName, parameter) {
    this.tagID = divName;
    this.parameters = parameter;
    this.isDisplayed = false;
}

OneWindow.prototype.init = function(divName, parameter) {
    this.tagID = divName;
    this.parameters = parameters;
    this.isDisplayed = false;
}
OneWindow.prototype.updateGroupParameters = function() {};
OneWindow.prototype.updateGraphParameters = function() {};

OneWindow.prototype.showMethod = function() {};
OneWindow.prototype.initialMethod = function() {
    this.width = parseInt($('#graphContent').width())-30;
    this.originalWidth = this.width;
    var that = this;
    if (!this.parameters) {
        return;
    }
    if (this.parameters.paraTag) {
        utilObj.showBlockPara(this.parameters.paraTag);
    }
    if (this.parameters.groupPara && this.parameters.graphPara) {
        this.groupParaPane = $('#'+that.parameters.groupPara.tagId);
        this.graphParaPane = $('#'+that.parameters.graphPara.tagId);
        
        if (this.parameters.groupPara) {
            let that = this;
            $('#'+this.parameters.groupPara.toggleId).on('click', function() {
                $(this).addClass('active').siblings().removeClass('active');
                that.groupParaPane.show();
                that.graphParaPane.hide();
            });
        }
        if (this.parameters.graphPara) {
            let that = this;
            $('#'+this.parameters.graphPara.toggleId).on('click', function() {
                $(this).addClass('active').siblings().removeClass('active');
                that.graphParaPane.show();
                that.groupParaPane.hide();
            });
        }
    }
};
OneWindow.prototype.formListener = function() {
    let that = this;
    if (!this.parameters) {
        return;
    }
    if (this.parameters.graphPara) {
        this.graphFormElements = $('#'+this.parameters.graphPara.formTagID);
    }
    if (this.parameters.groupPara) {
        this.groupFormElements = $('#'+this.parameters.groupPara.formTagID);
    }
};

OneWindow.prototype.hideWin = function() {
    utilObj.hidePara(this.tagID);
    this.displayParameters(false);
    this.isShowing = false;
}

OneWindow.prototype.optimiseSize = function(inputSize, upperSize) {
    if (!this.parameters.biggestSize) return 0;
    var preRes, normalSize;
    var upBoundSize = upperSize;
    normalSize = inputSize > upBoundSize ? upBoundSize : inputSize;
    if (inputSize < 1 || upperSize < 1) {
        this.parameters.graphPara.scale = "sqrt";
    }
    switch (this.parameters.graphPara.scale) {
        case "log":
            preRes = Math.log(normalSize)/Math.log(upBoundSize);
            break;
        case "sqrt":
            preRes = Math.sqrt(normalSize)/Math.sqrt(upBoundSize);
            break;
        default :
            preRes = normalSize/upBoundSize;
    }
    return preRes*(this.parameters.biggestSize-this.parameters.smallSize)+this.parameters.smallSize;
}

OneWindow.prototype.displayParameters = function(isShow) {
    if (!this.parameters || !this.parameters.paraTag) return 0;
    if (isShow) {
        utilObj.showBlockPara(this.parameters.paraTag);
    } else {
        utilObj.hidePara(this.parameters.paraTag);
    }
}

OneWindow.prototype.showWin = function() {

    utilObj.showBlockPara(this.tagID);
    this.displayParameters(true);

    if (!this.isDisplayed) {
        this.initialMethod();
        this.formListener();
        this.isDisplayed = true;
    };
    if (!this.hasGraph) {
        this.getData();
        
        this.showMethod(this);
        this.hasGraph = true;
    };
    this.isShowing = true;     
}

OneWindow.prototype.clearGraphContent = function() {
    utilObj.clearContent(this.tagID);
    this.hasGraph = false;
}

OneWindow.prototype.getCheckList = function() {

    let nodesDict = {};
    let lg = this.myData.nodes.length;
    for (let i = 0; i < lg; i += 1) {
        nodesDict[this.myData.nodes[i].text] = 0;
    }

    popModal.updateTermsList(nodesDict);
}

OneWindow.prototype.showCheckData = function(checkedterms) {
   let instance = filterTerm2DocGraph(myVsearch.termGraph.term2Doc, checkedterms);
   this.clearGraphContent();
   this.getData(instance);
   this.showMethod(this);
   this.hasGraph = true;
   this.isShowing = true;
}


function graphRequest(tag_Name) {
    if (tag_Name === "gwi") {
        return new myFaceCloud('gwi');
    } else if (tag_Name === "gfl") {
        return creatForceNodes("gfl");
    } else if (tag_Name === "gmx") {
        return creatHeatMatrix("gmx");
    } else if (tag_Name === "gbg") {
        return creatBubbleTags("gbg");
    } else if (tag_Name === "gdg") {
        return new dendrogram('gdg');
    } else if (tag_Name === 'gpk') {
        return new packGraph('gpk');
    }
}

function creatBubbleTags(tag_Name) {
    var result = new OneWindow(tag_Name, paraBB);

    result.getData = function(instance) {
        if (instance) {
            result.myData = instance
        } else {
            result.myData = getTheGraphs(result.parameters.graphPara.maxBubbleNum);
        }
        makeGroup.groupTheGraph(result.myData, result.parameters.groupPara.groupNum);
    }
    result.formListener = function() {
        result.constructor.prototype.formListener.call(this);
        let formArr = this.graphFormElements.find('.checkbox');
        let that = this;
        formArr.eq(0).checkbox({
            'onChecked': function() {
                that.parameters.graphPara.scale = this.value;
                that.clearGraphContent();
                that.showMethod(that);
            }
        });
        formArr.eq(1).checkbox({
            'onChecked': function() {
                that.parameters.graphPara.scale = this.value;
                that.clearGraphContent();
                that.showMethod(that);
            }
        })
        formArr.eq(2).checkbox({
            'onChecked': function() {
                that.parameters.graphPara.scale = this.value;
                that.clearGraphContent();
                that.showMethod(that);
            }
        });
        let bubblesSizeEle = this.graphFormElements.find('#pb');
        bubblesSizeEle.change(function() {
            result.parameters.graphPara.maxBubbleNum = +this.value;
            result.getData();
            that.clearGraphContent();
            that.showMethod(that);
        });
        let bubblesGroupSizeEle = this.groupFormElements.find('#gnrb');
        bubblesGroupSizeEle.change(function() {
            that.parameters.groupPara.groupNum = +this.value;
            that.clearGraphContent();
            makeGroup.groupTheGraph(that.myData, +this.value);
            that.showMethod(that);
        })
    }
    result.showMethod = bubbleLayout;
    return result;
}

function creatHeatMatrix(tag_Name) {
    var result = new OneWindow(tag_Name, paraHM);
    result.getData = function(instance) {
        if (instance) {
            result.myData = instance;
        } else {
            result.myData = getTheGraphs(result.parameters.graphPara.maxMatrixSize);    
        }
        
        var index1, index2, matrixIndice;
        result.myData.heatMatrix = []
        for (index1 = 0; index1 < result.myData.sizeOfMatrix; index1 += 1) {
            for (index2 = 0; index2 < result.myData.sizeOfMatrix; index2 += 1) {
                matrixIndice = result.myData.matrix[index1][index2];
                result.myData.heatMatrix.push(matrixIndice);
            }
        };
    }
    result.formListener = function() {
        this.constructor.prototype.formListener.call(this);
        let maxtrixSizeRange = this.graphFormElements.find('#mn');
        maxtrixSizeRange.change(function() {
            result.parameters.graphPara.maxMatrixSize = this.value;
            result.getData();
            result.clearGraphContent();
            result.showMethod(result);
        })
    }
    
    result.updateGroupParameters = function() {
        var formElements = this.groupFormElements.get(0).elements;
        var tempValue = formElements.item(1).value;
        if (result.parameters.groupPara.groupNum != tempValue) {
            result.parameters.groupPara.groupNum = tempValue;
            return true;
        } else {
            return false;
        }
    };
    result.showMethod = matrixHeatMapLayout;
    return result;
}

function creatForceNodes(tag_Name) {
    var result = new OneWindow(tag_Name, paraFN);
    result.initialMethod = function() {
        result.constructor.prototype.initialMethod.call(result);
        result.getData();
    };
    result.getData = function(instance) {
        if (instance) {
            this.myData = instance;
        } else {
            this.myData = getTheGraphs(result.parameters.graphPara.maxNodesNum);
        }
        makeGroup.groupTheGraph(this.myData, result.parameters.groupPara.groupNum);
    }
    result.showWin = function() {
        result.constructor.prototype.showWin.call(result);
    };
    result.hideWin = function() {
        result.constructor.prototype.hideWin.call(result);
    }

    result.formListener = function() {
        this.constructor.prototype.formListener.call(this);
        let formArr = this.graphFormElements.find('.checkbox');

        let that = this;
        formArr.eq(0).checkbox({
            'onChecked': function() {
                if (this.value !== that.parameters.groupPara.scale) {
                    that.parameters.graphPara.scale = this.value;
                    result.clearGraphContent();
                    result.showMethod(result);
                }
            }
        });
        formArr.eq(1).checkbox({
            'onChecked': function() {
                if (this.value !== that.parameters.groupPara.scale) {
                    that.parameters.graphPara.scale = this.value;
                    result.clearGraphContent();
                    result.showMethod(result);
                }
            }
        })
        formArr.eq(2).checkbox({
            'onChecked': function() {
                if (this.value !== that.parameters.groupPara.scale) {
                    that.parameters.graphPara.scale = this.value;
                    result.clearGraphContent();
                    result.showMethod(result);
                }
            }
        })

        let nodeSizeRange = this.graphFormElements.find('#dn');
        nodeSizeRange.change(function() {
            that.parameters.graphPara.nodesDist = +this.value;
            result.clearGraphContent();
            result.showMethod(result);
        });

        let nodeDistence = this.graphFormElements.find('#p3');
        nodeDistence.change(function() {
            that.parameters.graphPara.maxNodesNum = +this.value;
            result.clearGraphContent();
            result.getData();
            result.showMethod(result);
        });

        formArr = this.groupFormElements.find('.checkbox');

        let a = true;
        formArr.eq(0).checkbox({
            'onChange': function() {
                that.parameters.groupPara.isGroupFilter = !that.parameters.groupPara.isGroupFilter;
            }
        });
    }

    result.showMethod = forceLayout;
    return result;
}
