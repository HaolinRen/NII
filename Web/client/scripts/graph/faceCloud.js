

"use strict"

;(function() {

const BORDER_SIZE = 8;
let faceCloudPara = {
    paraTag : "tpp",
    graphPara : {
        tagId : "tppg",
        toggleId: 'gs1',
        formTagID : "tfw",
        scale : "log",
        maxTagsNum : 100,
        showImageLabel : false,
    },
    groupPara : {
        toggleId: 'gps1',
        tagId : "tppgo",
        isGroupColor : true,
        isGroupFilter : false,
        formTagID : "gppw",
        groupNum : 5,
    },
    'font-family': 'impact',
    biggestSize : 46,
    smallSize : 16,
    isHeatView : false,
    isListView : false,
};

const FEEBLE_OPACITY = 0.1;

function myFaceCloud(divName) {

    if (!(this instanceof myFaceCloud)) {
        return new myFaceCloud(divName);
    }

    this.tagID = divName;
    this.parameters = faceCloudPara;
    this.isDisplayed = false;
};

utilObj.extendInstance(myFaceCloud, OneWindow);

myFaceCloud.fn = myFaceCloud.prototype;

myFaceCloud.fn.initialMethod = function(tagID) {

    this.uber.initialMethod.call(this, tagID);
    
    this.heatColorScale = ["#FF1400","#FF2800","#FF3200","#FF4600","#FF5a00","#FF6e00","#FF8200","#FF9600","#FFaa00",
                            "#FFbe00","#FFd200","#FFe600","#FFfa00","#fdff00","#d7ff00","#b0ff00","#8aff00","#65ff00",
                            "#17ff00","#00ff36","#00ff83","#00ffd0","#00fff4", "#00e4ff"];
    this.colorHeat = d3.scale.quantile().range(this.heatColorScale.reverse());
    this.groupFill = d3.scale.category10();

    this.getData();

    this.height = parseInt(Math.max(Math.max(this.width * 0.5, 500) * (this.myData.sizeOfMatrix/80), 400));
    this.initGraphBoard();
   
    let that = this;
    notifyier.subscribe('filterTerms', 0, function(terms) {
        if (that.isShowing) {
            that.isFiltered = true;
            that.feebleTerms(terms);
        }
    })
    notifyier.subscribe('clearTermsFilter', 0, function() {
        if (that.isShowing) {
            that.isFiltered = false;
            that.fadeOut();
        }
    })
};
myFaceCloud.fn.getData = function(instance) {
    if (!instance) {
        this.myData = getTheGraphs(this.parameters.graphPara.maxTagsNum);
    } else {
        this.myData = instance;
    }
    this.groupMyGraph();
    this.initData();
}

myFaceCloud.fn.groupMyGraph = function() {
    makeGroup.groupTheGraph(this.myData, this.parameters.groupPara.groupNum);
};

myFaceCloud.fn.hideListPane = function() {
    if (this.parameters.isListView) {
        this.parameters.isListView = false;
        if (this.hasHeatData) {
            $("#htmap").removeClass('disabled');
        }
    }
};

myFaceCloud.fn.formListener = function() {
    this.uber.formListener.call(this);
    let that = this;

    $('#fontfm').dropdown({
        'onChange': d=>{
            that.parameters['font-family'] = d;
            that.updateWords();
        }
    })

    $('#aspratio').dropdown({
        'onChange': d=>{
            if (d === '0') {
                that.width = that.height;
            } else if (d === '1') {
                that.width = parseInt((4/3) * that.height);
            } else if (d === '2') {
                that.width = parseInt((16/9) * that.height);
            } else if (d === '3') {
                that.width = parseInt((16/10) * that.height);
            } else if (d === '4') {
                that.width = parseInt((21/9) * that.height);
            } else {
                that.width = this.originalWidth;
                that.height = parseInt(Math.max(Math.max(that.width * 0.5, 500) * (that.myData.sizeOfMatrix/80), 400));
            }
            that.removeGraphBoard();
            that.initData();
            that.initGraphBoard();
            that.showMethod();
        }
    })

    let formArr = this.graphFormElements.find('.checkbox');
    formArr.eq(0).checkbox({
        'onChecked': function() {
            if (this.value !== that.parameters.groupPara.scale) {
                that.parameters.graphPara.scale = this.value;
                that.updateWords();
            }
        }
    });
    formArr.eq(1).checkbox({
        'onChecked': function() {
            if (this.value !== that.parameters.groupPara.scale) {
                that.parameters.graphPara.scale = this.value;
                that.updateWords();
            }
        }
    })
    formArr.eq(2).checkbox({
        'onChecked': function() {
            if (this.value !== that.parameters.groupPara.scale) {
                that.parameters.graphPara.scale = this.value;
                that.updateWords();
            }
        }
    })
    formArr.eq(3).checkbox({
        'onChange': function() {
            that.parameters.graphPara.showImageLabel = !that.parameters.graphPara.showImageLabel;
            that.updateWords();
        }
    });

    formArr = this.groupFormElements.find('.checkbox');
    formArr.eq(1).checkbox();
    formArr.eq(0).checkbox({
        'onChange': function() {
            that.parameters.groupPara.isGroupFilter = !that.parameters.groupPara.isGroupFilter;
        }
    });

    let rg = this.graphFormElements.find('#p1');

    rg.change(function(d) {
        that.parameters.graphPara.maxTagsNum = +that.graphFormElements.find('output').html();
        
        that.getData();
        that.removeGraphBoard();
        that.height = parseInt(Math.max(Math.max(that.width * 0.5, 500) * (that.myData.sizeOfMatrix/80), 400));

        that.initGraphBoard();
        that.showMethod();
    });

    $("#wlst").on("click", function() {
        if (!that.parameters.isListView) {
            that.reListWords();
        } else {
            that.reCloud();
        }
    });

    d3.select("#gnrw").on('change', function() {
        if (that.parameters.isListView) {
            that.reCloud();
        }
        that.hideHeat();
        if (this.value !== that.parameters.groupPara.groupNum) {
            that.parameters.groupPara.groupNum = this.value;
            that.groupMyGraph();
            that.updateWordsCloud();
        }
    });

    d3.select("#htmap").on("click", function() {
        if (that.parameters.isListView) {
            that.reCloud();  
        }
        if (!that.parameters.isHeatView && that.hasHeatData) {
            that.parameters.isHeatView = true;
            that.giveHeat();
        } else {
            that.hideHeat();
        }
        that.updateWordsCloud();
    });
};

myFaceCloud.fn.clearGraphContent = function() {
    this.hideListPane();
    this.hideHeat();
    
    this.wordPane.selectAll('*').remove();
    this.borderPane.selectAll('*').remove();
    this.clearImages();
    this.hasGraph = false;
}

myFaceCloud.fn.initData = function() {

    wordCluster.dendrogramPosition(this.width, this.height, this.myData);
    myVsearch.checkFaceHasImage(this.myData);
    let that = this;
    let wordDict = this.myData;
    try {
        utilObj.requestData("/get", wordDict.matrix, function(data) {
            let eigenInfo = data;
            that.heatUpper = function() {
                let mxv = Math.max.apply(null, eigenInfo[1]);
                return Math.sqrt(mxv);
            }();
            that.colorHeat.domain([0, that.heatUpper])
            wordDict.nodes.forEach(function(d, i) {
                d.entangIndex = eigenInfo[1][i] !== 0 ? eigenInfo[1][i] : 0.00001;
            });
            that.hasHeatData = true;
        }, false);
    } catch (err) {
        that.hasHeatData = fasle;
        alert("Can't connect to server, some function can't accomplish!");
    };
}

myFaceCloud.fn.removeGraphBoard = function() {
    $("#gwicl").empty();
    $('#heatBK').empty();
}

myFaceCloud.fn.initGraphBoard = function() {
    let width = this.width,
        height = this.height,
        middleX = width >> 1,
        middleY = height >> 1;
    this.svg = d3.select("#gwicl").append("svg")
                .attr("width", width)
                .attr("height", height);
    
    this.heatContext = d3.select("#heatBK")
                            .append("canvas")
                            .attr("width", width)
                            .attr("height", height)
                            .style("width", width + "px")
                            .style("height", height + "px")
                            .node()
                            .getContext("2d");

    this.heatMap = this.svg.append("g").attr("id", "heatMapBack");
 
    this.wordPane = this.svg.append("g")
                    .attr("transform", "translate("
                        + middleX + ", " + middleY + ")");

    this.borderPane = this.svg.append("g")
                    .attr("transform", "translate("
                        + middleX + ", " + middleY + ")");

    this.imagesPane = this.svg.append("g")
                    .attr("transform", "translate("
                        + middleX + ", " + middleY + ")");
}

myFaceCloud.fn.reCloud = function() {
    this.hideListPane();
    this.wordPane.selectAll(".windex").remove();
    this.wordPane.selectAll(".ental").remove();
    this.updateWordsCloud();
    this.showImages();
}

myFaceCloud.fn.formatColorDict = function() {
    this.groupColorDict = {};
    let that = this;
    this.myData.nodes.forEach(function(n) {
        that.groupColorDict[n.text] = n.group;
    })
}

myFaceCloud.fn.keepColorStable = function() {
    let groupMapper = {};
    let inverseMapper = {};
    const MAX_NUM = 10;

    for (let oneTerm of this.myData.nodes) {
        if (groupMapper[this.groupColorDict[oneTerm.text]] === undefined) {
            groupMapper[this.groupColorDict[oneTerm.text]] = [oneTerm.group];
        } else {
            if (groupMapper[this.groupColorDict[oneTerm.text]].indexOf(oneTerm.group) === -1) {
                groupMapper[this.groupColorDict[oneTerm.text]].push(oneTerm.group);
            }
        }
    }

    for (let oneGroup in groupMapper) {
        let arr = groupMapper[oneGroup];
        let lg = arr.length;
        inverseMapper[arr[0]] = +oneGroup;
        for (let i = 1; i < lg; i += 1) {
            if (groupMapper[arr[i]] !== undefined) {
                inverseMapper[arr[i]] = groupMapper[arr[i]][0];
            } else {
                inverseMapper[arr[i]] = arr[i];
            }
        }
    }
    for (let oneTerm of this.myData.nodes) {
        oneTerm.group = inverseMapper[oneTerm.group];
    }
    this.formatColorDict();
}

myFaceCloud.fn.updateWordsCloud = function() {
    this.keepColorStable();
    let that = this;
    const DEMI_BORDER_SIZE = 4;
    this.wordPane.selectAll("text")
        .transition()
        .duration(600)
        .attr("transform", function(d) {
            if (!d.isImage) {
                return "translate(" + [d.x, d.y] + ")rotate(0)";
            } else {
                return "translate(" + [d.x+20, d.y] + ")rotate(0)";
            }
        })
        .attr("class", "words")
        .attr("font-family", this.parameters['font-family'])
        .attr("text-anchor", "middle")
        .style("fill", function(d) {
            return that.fillControl(d);
        })
        .style("font-size", function(d) { 
            if (d.isImage) {
                return '14px';
            } else {
                return d.size + "px";
            }
        })
        .attr('display', function(d, j) {
            if (d.isImage) {
                that.borderDict[j].attr('x', d.x)
                                    .attr('y', d.y)
                                    .attr('width', d.y1)
                                    .attr('height', d.y1)
                                    .attr('fill', function() {
                                        return that.fillControl(d);
                                    });
                that.imagesDict[j].attr('x', d.x + DEMI_BORDER_SIZE)
                                    .attr('y', d.y + DEMI_BORDER_SIZE)
                                    .attr('width', d.y1 - BORDER_SIZE)
                                    .attr('height', d.y1 - BORDER_SIZE);
            }
            
            if (that.parameters.graphPara.showImageLabel) {
                return null;
            } else {
                return d.isImage ? 'none' : null;
            }
        });

}

myFaceCloud.fn.spritTags = function() {
    let that = this;
    d3.layout.cloud()
            .size([this.width-20, this.height])
            .words(this.myData.nodes)
            .font(this.parameters['font-family'])
            .rotate(0)
            .showImageLabel(this.parameters.graphPara.showImageLabel)
            .fontSize(function(d) {
                return that.optimiseSize(d.termIndex, 200); })
            .start();
}

myFaceCloud.fn.drawWords = function() {
    let that = this;
    that.imagesDict = {};
    that.borderDict = {};

    this.wordPane.selectAll("text")
        .data(this.myData.nodes)
        .enter()
        .append("text")
        .style("font-size", function(d) { 
            if (d.isImage) {
                return '14px';
            } else {
                return d.size + "px";
            }
        })
        .style("fill", function(d) {
            return that.fillControl(d);
        })
        .attr("font-family", this.parameters['font-family'])
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
            if (!d.isImage) {
                return "translate(" + [d.x, d.y] + ")rotate(0)";
            } else {
                return "translate(" + [d.x+20, d.y] + ")rotate(0)";
            }
        })
        .attr("class", "words")
        .on("mouseover", function(d, i) {
            that.fadeIn(d, i);
        })
        .on("mouseout", function(d) {
            that.fadeOut(d);
        })
        .text(function(d) { return d.text; })
        .on("click", function(d) {
            that.termClickEvent(d);
        })
        .attr('display', function(d, i) {
            if (d.isImage) {
                const DEMI_BORDER_SIZE = 4;
                that.borderDict[i] = that.borderPane.append('rect')
                                        .attr('x', d.x)
                                        .attr('y', d.y)
                                        .attr('width', d.y1)
                                        .attr('height', d.y1)
                                        .attr('fill', function() {
                                            return that.fillControl(d);
                                        })
                                        .attr('class', 'imageBorder');

                that.imagesDict[i] = that.imagesPane.append('svg:image')
                                        .attr('x', d.x + DEMI_BORDER_SIZE)
                                        .attr('y', d.y + DEMI_BORDER_SIZE)
                                        .attr('width', d.y1 - BORDER_SIZE)
                                        .attr('height', d.y1 - BORDER_SIZE)
                                        .attr('xlink:href', d.imageHref)
                                        .on('mouseover', function() {
                                            that.fadeIn(d, i);
                                        })
                                        .on("mouseout", function() {
                                            that.fadeOut(d);
                                        })
                                        .on("click", function() {
                                            that.termClickEvent(d);
                                        });
                return that.parameters.graphPara.showImageLabel ? null : 'none';
            }
            return null;
        });
}

myFaceCloud.fn.clearImages = function() {
    this.imagesPane.selectAll('image').remove();
}

myFaceCloud.fn.showImages = function() {
    this.imagesPane.selectAll('image').attr('display', null);
    this.borderPane.selectAll('rect').attr('display', null);
}

myFaceCloud.fn.hideImges = function() {
    this.imagesPane.selectAll('image').attr('display', 'none');
    this.borderPane.selectAll('rect').attr('display', 'none');
}

myFaceCloud.fn.reListWords = function() {
    this.hideHeat();
    
    $("#htmap").addClass('disabled');
    
    var cordX, cordY, tranResult;
    var colorForOrder = ["#6363FF", "#6373FF", "#63A3FF", "#63E3FF", "#63FFFB", "#63FFCB",
                       "#63FF9B", "#63FF6B", "#7BFF63", "#BBFF63", "#DBFF63", "#FBFF63", 
                       "#FFD363", "#FFB363", "#FF8363", "#FF7363", "#FF6364"]; 

    let that = this;
    let middleX = this.width >> 1;
    let middleY = this.height >> 1;

    if (this.listOrdered.length == 0) {
        this.listOrdered = utilObj.clone(that.myData.nodes);
        this.listOrdered.sort(function(a, b) {
            return b.entangIndex - a.entangIndex;
        });
    }
    var arrayForIndex = [];
    for (let i = 0, len = this.listOrdered.length; i < len; i += 1) {
        arrayForIndex.push(this.listOrdered[i].text);
    }
    var maxRectWidth = 100, minRectWidth = 15, tempWidth, scaleM = arrayForIndex.length;
    var colorScale = d3.scale.quantile()
                        .domain([0, scaleM])
                        .range(colorForOrder);
    
    this.parameters.isListView = true;

    let perRow = middleY / 10;

    this.hideImges();

    let X_DIST = 260,
        Y_DIST = 16;

    this.wordPane.selectAll(".words")
        .transition()
        .duration(600)
        .attr("class", "liW")
        .style("font-size", "14px")
        .attr("text-anchor", "end")
        .style("fill", "black")
        .attr('display', null)
        .attr("transform", function(d, i) {
            cordX = Math.floor(arrayForIndex.indexOf(d.text) / perRow) * X_DIST - middleX + X_DIST;
            cordY = Math.floor(arrayForIndex.indexOf(d.text) % perRow) * Y_DIST - middleY + 38;
            tranResult = "translate(" + [cordX, cordY] + ")rotate(0)";
            return tranResult;
        })
        .attr('display', null);

    this.wordPane.selectAll(".windex")
        .data(arrayForIndex)
        .enter()
        .append("rect")
        .transition()
        .duration(600)
        .attr("transform", function(d, i) {
            cordX = Math.floor( i / perRow) * X_DIST - middleX + X_DIST;
            cordY = Math.floor( i % perRow) * Y_DIST - middleY + 26;
            tranResult = "translate(" + [cordX, cordY] + ")rotate(0)";
            return tranResult;
        })
        .attr("class", "windex")
        .attr("height", 14)
        .attr("width", function(d, i) {
            if (that.listOrdered[0].termIndex !== 1) {
                tempWidth = (Math.log(that.listOrdered[i].termIndex) / Math.log(that.listOrdered[0].termIndex))
                                * (maxRectWidth - minRectWidth) + minRectWidth;
            } else {
                tempWidth = minRectWidth;
            }

            return tempWidth;
        })
        .attr("fill", function(d, i) {
            return colorScale(scaleM - i);
        });

    this.wordPane.selectAll(".ental")
        .data(that.myData.nodes)
        .enter().append("text")
        .transition()
        .duration(800)
        .attr("class","ental")
        .attr("text-anchor", "start")
        .attr("font-size", 11)
        .text(function(d) { return d.entangIndex.toFixed(4); })
        .attr("transform", function(d, i) {
            cordX = Math.floor(arrayForIndex.indexOf(d.text) / perRow) * X_DIST - middleX + X_DIST;
            cordY = Math.floor(arrayForIndex.indexOf(d.text) % perRow) * Y_DIST - middleY + 38;
            tranResult = "translate(" + [cordX, cordY] + ")rotate(0)";
            return tranResult;
        });
}

myFaceCloud.fn.getTermIndex = function(termText, inGraph) {
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

myFaceCloud.fn.testNeighbour = function(a, b, inGraph) {
    var i1, i2;
    if (typeof a == "number") {
        if (i1 >= inGraph.sizeOfMatrix || i2 >= inGraph.sizeOfMatrix) {
            return false;
        }
        i1 = a;
        i2 = b;
    } else {
        i1 = this.getTermIndex(a, inGraph);
        i2 = this.getTermIndex(b, inGraph);
        if (i1 === -1 || i2 === -1) {
            return false;
        }
    }
    return inGraph.matrix[i1][i2] !== 0;
}

myFaceCloud.fn.fadeIn = function(g, i) {
    if (this.parameters.isListView ) { return 0; };

    let that = this;
    // var relatedNodes = [];
    // var tempGroupsTerms = [];
    var showNum = 0;
    var maxShowNum = 24;
    let wordDict = this.myData;
    this.isWordHoving = true;
    this.wordPane.selectAll(".words")
        .transition()
        .duration(400)
        .style("opacity", FEEBLE_OPACITY)
        .filter(function(d, j) {
            let res = false;
            if (that.parameters.groupPara.isGroupFilter) {
                if (g.group == d.group) {
                    // tempGroupsTerms.push(d.text);                        
                    res = true;
                }
            } else {
                if (that.testNeighbour(i, j, wordDict) && showNum < maxShowNum) {
                    showNum += 1;
                    // relatedNodes.push(j);
                    d.tempHeat = wordDict.matrix[i][j];
                    res = true;
                } else {
                    d.tempHeat = 0;
                    res = false;
                }
            }
            if (d.isImage) {
                if (res) {
                    that.borderDict[j].transition()
                                .duration(400)
                                .style('opacity', 1);

                    that.imagesDict[j].transition()
                                .duration(400)
                                .style('opacity', 1);
                } else {
                    that.imagesDict[j].transition()
                                .duration(400)
                                .style('opacity', FEEBLE_OPACITY);
                    that.borderDict[j].transition()
                                .duration(400)
                                .style('opacity', FEEBLE_OPACITY);
                }
            }
            return res;
        })
        .style("opacity", 1);

    if (this.parameters.isHeatView && this.hasHeatData) {
        this.createHeatImage(this.updateHeatData('tempHeat'));
    }
    let matchingSnippets = reOrderList.findSubDocs(g.text);
    myTimeline.showHoverLine(matchingSnippets);
}

myFaceCloud.fn.feebleTerms = function(terms) {
    let that = this;
    if (this.isListView) {
        return 0;
    }
    let bgValue = 1;
    for (let oneTerm in terms) {
        if (terms[oneTerm] > bgValue) {
            bgValue = terms[oneTerm];
        }
    }
    this.tempTermsSize = {};
    this.wordPane.selectAll('.words')
                .transition()
                .duration(400)
                .style('opacity', function(d, j) {
                    let isShow = false;
                    if (terms[d.text]) {
                        isShow = true;
                    }

                    if (d.isImage) {
                        if (isShow) {
                            that.borderDict[j].transition()
                                        .duration(400)
                                        .style('opacity', 1);

                            that.imagesDict[j].transition()
                                        .duration(400)
                                        .style('opacity', 1);
                        } else {
                            that.imagesDict[j].transition()
                                        .duration(400)
                                        .style('opacity', FEEBLE_OPACITY);
                            that.borderDict[j].transition()
                                        .duration(400)
                                        .style('opacity', FEEBLE_OPACITY);
                        }
                    }
                    return isShow ? 1 : FEEBLE_OPACITY;
                })
                .style('font-size', function(d, j) {
                    let tvale = that.optimiseSize(terms[d.text], bgValue);

                    if (tvale < d.size && terms[d.text]) {

                        if (d.isImage) {
                            let w = (tvale / d.size) * d.y1;
                            that.borderDict[j].attr('width', w)
                                                .attr('height', w);
                            that.imagesDict[j].attr('width', w - BORDER_SIZE)
                                                .attr('height', w - BORDER_SIZE);
                            that.tempTermsSize[d.text] = 14;
                        } else {
                            that.tempTermsSize[d.text] = tvale;
                        }
                        return tvale;
                    }
                    
                })

}

myFaceCloud.fn.fadeOut = function() {
    let that = this;

    if (this.parameters.isListView) { return 0; };
    this.isWordHoving = false;
    if (this.parameters.isHeatView && this.hasHeatData) {
        setTimeout(function() {
            if (!that.isWordHoving) {
                that.createHeatImage(that.updateHeatData('entangIndex'));
            }
        }, 300);

        this.wordPane.selectAll(".words")
            .transition()
            .duration(400)
            .style("opacity", function(d, j) {
                if (that.isFiltered) {
                    let op = that.tempTermsSize[d.text] ? 1 : FEEBLE_OPACITY;

                    if (d.isImage) {
                        that.imagesDict[j].transition()
                                            .duration(400).style('opacity', op);
                        that.borderDict[j].transition()
                                            .duration(400).style('opacity', op);
                    }
                    return op;
                } else {
                    if (d.isImage) {
                        that.imagesDict[j].transition()
                                            .duration(400).style('opacity', 1);
                        that.borderDict[j].transition()
                                            .duration(400).style('opacity', 1);
                    }
                    return 1;
                }
            })
            .style('font-size', function(d, j) {
                if (that.isFiltered) {
                    if (d.isImage) {
                        return 14;
                    } else {
                        return that.tempTermsSize[d.text] || d.size;
                    }
                } else {
                    if (d.isImage) {
                        that.imagesDict[j]
                            .attr('width', d.y1 - BORDER_SIZE)
                            .attr('height', d.y1 - BORDER_SIZE);

                        that.borderDict[j]
                            .attr('width', d.y1)
                            .attr('height', d.y1);
                    }
                    if (d.isImage) {
                        return 14;
                    } else {
                        return d.size;
                    }
                }
            });
    } else {
        this.wordPane.selectAll(".words")
            .transition()
            .duration(400)
            .style("opacity", function(d, j) {
                if (that.isFiltered) {
                    let op = that.tempTermsSize[d.text] ? 1 : FEEBLE_OPACITY;

                    if (d.isImage) {
                        that.imagesDict[j].transition()
                                            .duration(400)
                                            .style('opacity', op);
                        that.borderDict[j].transition()
                                            .duration(400)
                                            .style('opacity', op);
                    }
                    return op;
                } else {
                    if (d.isImage) {
                        that.imagesDict[j].transition()
                                            .duration(400)
                                            .style('opacity', 1);
                        that.borderDict[j].transition()
                                            .duration(400)
                                            .style('opacity', 1);
                    }
                    return 1;
                }
            })
            .style('font-size', function(d, j) {
                if (that.isFiltered) {
                    if (d.isImage) {
                        return 14;
                    } else {
                        return that.tempTermsSize[d.text] || d.size;
                    }
                } else {
                    if (d.isImage) {
                        that.imagesDict[j]
                            .attr('width', d.y1 - BORDER_SIZE)
                            .attr('height', d.y1 - BORDER_SIZE);
                            
                        that.borderDict[j]
                            .attr('width', d.y1)
                            .attr('height', d.y1);
                    }
                    if (d.isImage) {
                        return 14;
                    } else {
                        return d.size;
                    }
                }
            });
    }
    
    myTimeline.clearHoverLine();
}

myFaceCloud.fn.initHeatData = function() {
    var x0, y0;
    var res = [];
    for (y0 = 0; y0 < this.height; y0 += 1) {
        var tempArr = [];
        for (x0 = 0; x0 < this.width; x0 += 1) {
            tempArr.push(0);
        }
        res.push(tempArr);
    }
    return res;
}

myFaceCloud.fn.updateHeatData = function(heatFormat) {
    var oneTerm, x0, x1, y0, y1, cx, cy, tx,ty,xx, xy, k, coreHeat, mt;
    var border = 26;
    var miBorder = 0;
    var lastValue;
    let heatData = this.initHeatData();
    
    let width = this.width;
    let height = this.height;
    let middleX = width >> 1;
    let middleY = height >> 1;
    function dist(x0, y0, x1, y1) {
        return Math.sqrt((y1-y0)*(y1-y0)+(x1-x0)*(x1-x0));
    }

    for (let i = 0; i < this.myData.sizeOfMatrix; i += 1) {
        oneTerm = this.myData.nodes[i];
        if (oneTerm.isImage) {
            x0 = oneTerm.x + middleX;
            x1 = oneTerm.x + oneTerm.y1 + middleX;
            y0 = oneTerm.y + middleY;
            y1 = oneTerm.y + oneTerm.y1 + middleY;

        } else {
            var tempW = oneTerm.width/3 + 5;
            var tempH = oneTerm.height/3 + 5;
            x0 = Math.floor(Math.max(oneTerm.x + middleX - tempW, 0));
            x1 = Math.floor(Math.min(oneTerm.x + middleX + tempW, width)) ;
            y0 = Math.floor(Math.max(oneTerm.y + middleY - tempH, 0));
            y1 = Math.floor(Math.min(oneTerm.y + middleY + 3, height));
        }
        miBorder = 0;

        coreHeat = Math.cbrt(oneTerm[heatFormat]);

        mt = coreHeat/border;
        if (coreHeat > this.heatUpper) {
            coreHeat = this.heatUpper;
        };
    
        tx = x0-border < 0 ? 0 : x0-border;
        xx = x1+border > width-1 ? width-1 : x1+border;

        ty = y0-border < 0 ? 0 : y0-border;
        xy = y1+border > height-1 ? height-1 : y1+border;

        for (cx = tx; cx <= xx; cx += 1) {
            for (cy = ty; cy <= xy; cy += 1) {
                
                if (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) {
                    if (heatData[cy][cx] < coreHeat) {
                        heatData[cy][cx] = coreHeat;
                    }
                } else {
                    var tempValue;
                    if (cx < x0) {
                        if (cy < y0) {
                            miBorder = dist(cx, cy, x0, y0);
                            tempValue = coreHeat - miBorder*mt;
                        } else if (cy > y1) {
                            miBorder = dist(cx, cy, x0, y1);
                            tempValue = coreHeat - miBorder*mt;
                        } else {
                            miBorder = (x0-cx);
                            tempValue = coreHeat - miBorder*mt;
                        }
                    } else if (cx > x1) {
                        if (cy < y0) {
                            miBorder = dist(cx, cy, x1, y0);
                            tempValue = coreHeat - miBorder*mt;
                        } else if (cy > y1) {
                            miBorder = dist(cx, cy, x1, y1);
                            tempValue = coreHeat - miBorder*mt;
                        } else {
                            miBorder = (cx-x1);
                            tempValue = coreHeat - miBorder*mt;
                        }
                    } else if (cy < y0) {
                        miBorder = (y0-cy);
                        tempValue = coreHeat - miBorder*mt;
                    } else if (cy > y0) {
                        miBorder = (cy-y1);
                        tempValue = coreHeat - miBorder*mt;
                    }
                    k = tempValue;
                    if (coreHeat < 0.1 && miBorder > border/2) {
                        k = 0;
                    }
                    heatData[cy][cx] = k > heatData[cy][cx] ? k :  heatData[cy][cx];
                }
            }
        }
    }
    return heatData;
}

myFaceCloud.fn.createHeatImage = function(heatMat) {
    var image = this.heatContext.createImageData(this.width, this.height);
    

    for (var y = 0, p = -1; y < this.height; y += 1) {
        for (var x = 0; x < this.width; x += 1) {
            var heatVal = heatMat[y][x];

            if (heatVal === 0) {
                image.data[++p] = 255;
                image.data[++p] = 255;
                image.data[++p] = 255;
                image.data[++p] = 102;
            } else {
                var c = d3.rgb(this.colorHeat(heatVal));
                image.data[++p] = c.r;
                image.data[++p] = c.g;
                image.data[++p] = c.b;
                image.data[++p] = 102;
            }
        }
    }

    this.heatContext.putImageData(image, 0, 0);
}

myFaceCloud.fn.hideHeat = function() {
    if (this.parameters.isHeatView) {
        this.heatContext.clearRect(0, 0, this.width, this.height);
        this.heatMap.selectAll(".htIndex").remove();
        this.parameters.isHeatView = false;
    }
}

myFaceCloud.fn.giveHeat = function() {

    this.createHeatImage(this.updateHeatData('entangIndex'));

    var startX = 20,
        startY = 400;
    let that = this;

    this.heatMap.selectAll(".htIndex")
            .data(this.heatColorScale)
            .enter().append("rect")
            .attr("class", "htIndex")
            .attr("width", 20)
            .attr("height", 12)
            .attr("x", startX)
            .attr("y", function(d, i) {
                return startY - i * 12;
            })
            .attr("fill", function(d, i) {
                return that.heatColorScale[i];
            })
            .style("opacity", 0.4);
}

myFaceCloud.fn.fillControl = function(d) {
    var res = this.groupFill(d.group);
    if (res === '#ff7f0e') {
        res = '#17becf'
    }
    return res;
}

myFaceCloud.fn.termClickEvent = function(d) {
    let matchingSnippetsNum = reOrderList.whichElement(d.text);
    myTimeline.updateTitleInfo(d.text);
    // myTimeline.processData(matchingSnippetsNum);
}

myFaceCloud.fn.showMethod = function() {

    this.spritTags();
    this.drawWords();
    let that = this;
    this.formatColorDict();
    this.listOrdered = [];
    // myTimeline.processData(myVsearch.titleDict);
}

myFaceCloud.fn.updateWords = function() {
    this.spritTags();
    this.updateWordsCloud();
}

window.myFaceCloud = myFaceCloud;

}(window))