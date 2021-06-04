"use strict"
var utilObj = {
    hidePara : function(divId) {
        document.getElementById(divId).style.display = "none";
    },
    showBlockPara : function(divId) {
        document.getElementById(divId).style.display = "inline-block";
    },
    setBackgroundColor : function(divId, color) {
        document.getElementById(divId).style.backgroundColor = color;
    },
    clone : function(obj) {
        if (null == obj || "object" != typeof obj) return obj;
        if (obj instanceof Array) {
            var copy = [];
            var i, len;
            for (i = 0, len = obj.length; i < len; ++i) {
                copy[i] = utilObj.clone(obj[i]);
            }
            return copy;
        }
        if (obj instanceof Object) {
            var copy = {};
            for (var attr in obj) {
                if (obj.hasOwnProperty(attr)) copy[attr] = utilObj.clone(obj[attr]);
            }
            return copy;
        }
        throw new Error("Unable to copy obj! Its type isn't supported.");
    },
    purge : function(d) {
        var a = d.attributes, i, l, n;
        if (a) {
            for (i = a.length - 1; i >= 0; i -= 1) {
                n = a[i].name;
                if (typeof d[n] === 'function') {
                    d[n] = null;
                }
            }
        }
        a = d.childNodes;
        if (a) {
            l = a.length;
            for (i = 0; i < l; i += 1) {
                utilObj.purge(d.childNodes[i]);
            }
        }
    },
    extendInstance : function (child, parent) {
        let F = function() {};
        F.prototype = parent.prototype;
        child.prototype = new F();
        child.prototype.constructor = child;
        child.prototype.uber = parent.prototype;
    },
    clearContent : function(tag_Name) {
        var tagRef = document.getElementById(tag_Name);
        utilObj.purge(tagRef);
        tagRef.innerHTML = "";
    },
    setContent : function(tag_Name, content) {
        if (typeof content !== "string") {
            utilObj.clearContent(tag_Name);
        } else {
            var tagRef = document.getElementById(tag_Name);
            utilObj.purge(tagRef);
            tagRef.innerHTML = content;
        }
    },
    //Define the function of adding event listener to element
    addEventMethod : function(ele, evnt, funct) {
        if (typeof ele.addEventListener === "function") {
            utilObj.addEventMethod = function(ele, evnt, funct) {
                ele.addEventListener(evnt, funct, false);
            }
        } else if (ele.attachEvent === "function") {
            utilObj.addEvent = function(evnt, funct) {
                ele.attachEvent('on'+evnt, funct);
            }
        } else {
            utilObj.addEvent = function(evnt, funct) {
                ele['on'+evnt] = funct;
            }
        };
        utilObj.addEvent(ele, evnt, funct);
    },
    addEvent : function(divName, evnt, funct){
        var thElement = document.getElementById(divName);
        if (typeof thElement.addEventListener === "function") {
            utilObj.addEvent = function(divName, evnt, funct) {
                var sElement = document.getElementById(divName);
                sElement.addEventListener(evnt, funct, false);
            }
        } else if (thElement.attachEvent === "function") {
            utilObj.addEvent = function(divName, evnt, funct) {
                var sElement = document.getElementById(divName);
                sElement.attachEvent('on'+evnt, funct);
            }
        } else {
            utilObj.addEvent = function(divName, evnt, funct) {
                var sElement = document.getElementById(divName);
                sElement['on'+evnt] = funct;
            }
        };
        utilObj.addEvent(divName, evnt, funct);
    },
    //add submit event listener to search request button
    addFormListener : function(divName, method) {
        utilObj.addEvent(divName, "submit", function(event) {  
            event.preventDefault();
            method(this.elements);
        })
    },
    addClickFunc : function(divName, funct) {
        var tagName = document.getElementById(divName);
        tagName.onclick = funct;
    },
    requestData : function(med, sendData, callBack, isSyn) {
        var xhttp, textData;
        textData = JSON.stringify(sendData);
        if (window.XMLHttpRequest) {
            xhttp = new XMLHttpRequest();
        } else {
            xhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var res = [];
                try {
                    res = JSON.parse(xhttp.responseText);
                    callBack(res);
                } catch(err) {
                    //console.log(xhttp.responseText);
                    console.log("can't process response data.", err);
                }
            }
        };
        xhttp.open("POST", med, isSyn);
        xhttp.setRequestHeader("Content-type", "application/json;charsetUTF-8")
        xhttp.send(textData);
    }
}

function oneDoc(docTitle, docContent, timeInfo, videoInfo, captions) {
    this.docTitle = docTitle;
    this.docContent = docContent;
    this.videoInfo = timeInfo;
    this.videoFile = videoInfo;
    this.captions = captions;
}

oneDoc.prototype.contentList = function() {
    var ctForAnalysing = this.docContent;

    return ctForAnalysing.split(';');
}

function findSentance(source, topic) {
    var docList = myVsearch.termGraph.term2Doc[topic];
    if (!docList) {
        return -1;
    }
    var index, oneDoc, result, len, reTopic, sentance, allSents, posiRdm, posi;
    sentance = -1;
    len = docList.length;
    for (index = 0; index < len; index += 1) {
        posiRdm = Math.floor(Math.random() * len);
        posi = docList[posiRdm];
        if (source != "title") {
            oneDoc = myVsearch.searchResults[posi].docContent;
        } else {
            oneDoc = myVsearch.searchResults[posi].docTitle;
        }
        reTopic = new RegExp(topic, "i");
        result = oneDoc.search(reTopic);
        if (result != -1) {
            if (source != "title") {
                allSents = oneDoc.split(".");
                for (var i = 0; i < allSents.length; i += 1) {
                    if (allSents[i].search(reTopic) != -1) {
                        sentance = allSents[i];
                        break;
                    }
                }
            } else {
                sentance = oneDoc;
            }
            break;
        }
    }
    return sentance;
}

function oneDocFactory(docTitle, docContent, timeInfo, videoInfo, captions) {
    return new oneDoc(docTitle, docContent, timeInfo, videoInfo, captions);
}

var videoControl = {
    ele: document.getElementById('vpBoard'),
    video : document.getElementById('vid'),
    tiemInfoPane: document.getElementById('vpTimeInfo'),
    endTime: 0,
    isShowed: false,
    language: 'English',
    initialPalyer: function() {
        $('#vplanguage').dropdown({
            onChange: function(index, val) {
                videoControl.language = val;
                $(this).children().eq(0).html(val);
            }
        });
        
        /*update player tune(lan)*/
    }(),
    updateVPlayerTimeInfo: function(info) {
        this.tiemInfoPane.innerHTML = info;
    },
    showPlayer: function() {
        if (!this.isShowed) {
            this.ele.style.display = 'inline-block';
            this.isShowed = true;
        }
    },
    hidePlayer: function() {
        if (this.isShowed) {
            this.ele.style.display = 'none';
            this.isShowed = true;
        }
    },
    endChecker: function() {
        if (videoControl.video.currentTime >= videoControl.endTime) {
            videoControl.video.pause();
        }
    },
    showVideo: function(vidsource) { 

        this.video.removeEventListener('timeupdate', this.endChecker);

        this.video.innerHTML = '<source src="' + vidsource.videoFile + '">';

        this.video.pause();

        this.video.load();

        this.video.currentTime = vidsource.videoInfo['begin_sec'];

        this.endTime = vidsource.videoInfo['end_sec'];

        function getMinute(t) {
            let minute = parseInt(t/60);
            let sec = t%60;
            return '<mark>' + minute + 'm' + sec + 's</mark>';
        }

        this.updateVPlayerTimeInfo('From ' + getMinute(vidsource.videoInfo['begin_sec']) + ' to ' + getMinute(vidsource.videoInfo['end_sec']));
        if (this.audiocontext) {
            this.audiocontext.close();
        }

        this.audiocontext = new (window.AudioContext || window.webkitAudioContext)();
        this.splitter = this.audiocontext.createChannelSplitter(2);
 
        this.gainNode_left = this.audiocontext.createGain();
        this.gainNode_right = this.audiocontext.createGain();

        this.merger = this.audiocontext.createChannelMerger(2);
 
        this.video.onplay = (function(ctxt){
            return function(){
            console.log("we are onplay")
                //ctxt.audiosource = ctxt.audiocontext.createMediaElementSource(document.getElementById('vid'));
                /*
                ctxt.audiosource.connect(ctxt.splitter);
                
                ctxt.splitter.connect(ctxt.gainNode_left, 0, 0);
                ctxt.splitter.connect(ctxt.gainNode_right, 1, 0);
            
            
                ctxt.gainNode_right.connect(ctxt.merger, 0, 1);
                ctxt.gainNode_left.connect(ctxt.merger, 0, 1);

                ctxt.gainNode_left.gain.value = 0.1;
                ctxt.merger.connect(ctxt.audiocontext.destination);            
                */
            }
        })(this)

        this.video.play();
        this.video.onseeking = function() {
            videoControl.video.removeEventListener('timeupdate', videoControl.endChecker);
        }

        this.video.addEventListener('timeupdate', this.endChecker);


        // this.audiocontext = new (window.AudioContext || window.webkitAudioContext)();
        // var splitter = this.audiocontext.createChannelSplitter(2);
        // var gainNode_left = this.audiocontext.createGain();
        // var gainNode_right = this.audiocontext.createGain();
        // var merger = this.audiocontext.createChannelMerger(2);
        // var audio_initialized = false;
        // audiosource = this.audiocontext.createMediaElementSource(video);
        // audiosource.connect(splitter);
        // audio_initialized = true;

        // splitter.connect(gainNode_left, 0, 0);
        // splitter.connect(gainNode_right, 1, 0);
                    
        // gainNode_right.connect(merger, 0, 1);
        // gainNode_left.connect(merger, 0, 1);
        
        // merger.connect(this.audiocontext.destination);
        // gainNode_left.gain.value = 0.1;
    }
}

var displayMethod = {
    listTag : document.getElementById("resultsList"),
    infoTag : document.getElementById("ri"),
    groupShowed : false,
    singleShowed : false,
    changeInfoTag : function(numToShow) {
        this.infoTag.innerHTML = numToShow + " results";
    },
    listOneResult : function(results, query) {
        var re = new RegExp(query, "gi");
        var tableOutput = '';
        
        var i, len;
        var cut_size = 200;

        var replace_with_image = function(text){
            let mini_size = 24;
            let concepts=text.split(';');
            let concept_list = [];
            let textWithImg = '';
            for (let i = 0; i < concepts.length; i++)
            {
                if (myVsearch.isFace(concepts[i])) {
                    let img_path = '/data/faces/' + concepts[i] + '.jpg';
                    textWithImg += '<a class="ui image label faceIcon keywords"><img src="'+img_path+'">';
                    textWithImg += concepts[i] + '</a>';
                } else{
                    textWithImg += '<a class="ui label keywords">' + concepts[i] + '</a>';
                }
                // textWithImg += '; ';
            }
            return textWithImg;
        }
        
        for (i = 0, len = results.length; i < len; i++) {
            tableOutput += '<div class="item oneDoc">'
                // + '<div class="ui tiny image"><img  src=/data/thumbnails/thumb-'+results[i].docTitle+'.png></div>'
                + '<div class="content"><a class="header" id="link_'+results[i].docTitle+'">'
                + results[i].docTitle + " [Play] </a>"
                + '<div class="ui labels">';

            tableOutput += replace_with_image(results[i].docContent);
            tableOutput += '</div><div class="ui right floated avatars image"><img src="/data/thumbnails/thumb-'+results[i].docTitle+'.png"></div>';
            tableOutput += '<div class="captions" id="'+results[i].docTitle+'">' + results[i].captions.substring(0,cut_size);
            tableOutput += '<a class="more">[...]</a>'+'</div></div>';
            tableOutput += '</div>';
        }
        this.listTag.innerHTML = tableOutput;

        let lbs = this.listTag.getElementsByClassName('keywords');
        let lbSize = lbs.length;
        for (i = 0; i < lbSize; i += 1) {
            
            lbs[i].addEventListener('click', function() {
                let clickedTerm = this.innerText || this.textContent;
                // myVsearch.searchKeyword(clickedTerm);
                let matchingSnippetsNum = reOrderList.whichElement(clickedTerm);
                myTimeline.updateTitleInfo(clickedTerm);
                let matchingSnippets = reOrderList.findSubDocs(clickedTerm);
                myTimeline.showHoverLine(matchingSnippets);
                // myTimeline.processData(matchingSnippetsNum);
            })
        }

        let ls = this.listTag.getElementsByClassName('header');
        let lg = ls.length;
        for (i = 0; i < lg; i += 1) {
            ls[i].addEventListener('click', (function(source) {
                return function() {
                    videoControl.showPlayer();
                    videoControl.showVideo(source);
                }
            })(results[i]))
        }

        let tb = this.listTag.getElementsByClassName('avatars');
        let tbl = tb.length;
        for (i = 0; i < tbl; i += 1) {
            tb[i].addEventListener('click', (function(source) {
                return function() {
                    videoControl.showPlayer();
                    videoControl.showVideo(source);
                }
            })(results[i]))
        }

        let ls2 = this.listTag.getElementsByClassName('captions');
        let lg2 = ls2.length;
        for (i = 0; i < lg2; i += 1) {

            var open_captions = (function(source, htmltarget) {
                return function() {
                    htmltarget.innerHTML=source.captions;
                }
            })(results[i], ls2[i])

            ls2[i].getElementsByClassName('more')[0].addEventListener('click', open_captions);
            ls2[i].addEventListener('mouseleave', 
                (function(source) {
                    return function() {
                    
                        this.innerHTML=source.captions.substring(0,cut_size) + '<a class="more">[...]</a>';
                        
                        this.getElementsByClassName('more')[0].addEventListener('click', 
                            (function(htmltarget){
                                return function(){
                                    htmltarget.innerHTML=source.captions;
                                };
                            })(this));
                    }
                })(results[i]));
        }

    }
}

function Vsearch_fd(para) {
    
    windowControl.clearGraph();
    para.maxSnpNum = sidebarPane.maxSnippetsNum;

    utilObj.requestData('/ben', para, function(data) {
        let try_fit = [];

        for (let ind of data)
        {
            let doc = oneDocFactory(ind.title, ind.content, ind.time_info, ind.video_file, ind.captions);
            try_fit.push(doc);
        }
        reOrderList.sortRes(try_fit);
        myVsearch.searchResults = try_fit;
        myTimeline.clearBrush();
        myVsearch.totalNum = myVsearch.searchResults.length;
        if (myVsearch.totalNum > 0) {
            myVsearch.hasData = true;
            myVsearch.getTermsTitleDict();
            myVsearch.countTitleDict();

            myTimeline.processData(myVsearch.titleDict, true);

            //test part

            let faceName = para.faceNames[0];
            if (faceName) {

                faceName = faceName.text;
                if (TEST_DATA[faceName]) {
                    let personArr = TEST_DATA[faceName];
                    let temp = {}
                    for (let e of personArr) {
                        temp[e] = 1
                    }
                    myTimeline.processTestData(temp)
                }
            }

            //

            reOrderList.allData();
            windowControl.reopenWindow();
        } else {
            myVsearch.showInfoPane();
        }
    }, true);
};

var reOrderList = {
    newOrderList : [],
    clickedTerm : "",
    numEachPage: 8,
    cloneResult : function() {
        this.newOrderList = myVsearch.searchResults;
    },
    displayTheOrder : function(startP, query) {
        var endP = startP + reOrderList.numEachPage;
        if (endP > this.newOrderList.length) {
            endP = this.newOrderList.length;
        }
        displayMethod.listOneResult(this.newOrderList.slice(startP, endP), query);
    },
    allData : function() {
        if (!myVsearch.hasData) {
            return 0;
        }
        reOrderList.cloneResult();
        displayMethod.changeInfoTag(myVsearch.totalNum);
        reOrderList.clickedTerm = "";
        reOrderList.displayTheOrder(0, reOrderList.clickedTerm);
        pageBar.resetPageNum(Math.ceil(myVsearch.totalNum/reOrderList.numEachPage));
    }
}

reOrderList.sortRes = function(data) {
    data.sort(function(a, b) {
        if (a.docTitle > b.docTitle) {
            return 1;
        } else {
            return -1;
        }
    })
}

reOrderList.findSubDocs = function(event_ID) {
    let res = {};
    if (typeof event_ID == "string") {
        if (myVsearch.termGraph.term2Doc.hasOwnProperty(event_ID)) {
            var i, len, index;
            for (i = 0, len = myVsearch.termGraph.term2Doc[event_ID].length; i < len; i++) {
                index = myVsearch.termGraph.term2Doc[event_ID][i];
                let tempSnippet = myVsearch.searchResults[index];
                if (res[tempSnippet.docTitle] === undefined) {
                    res[tempSnippet.docTitle] = 1;
                } else {
                    res[tempSnippet.docTitle] += 1;
                }
            }
        }
    }
    return res;
}

reOrderList.whichElement = function(event_ID) {
    let res = {};
    if (typeof event_ID == "string") {
        if (myVsearch.termGraph.term2Doc.hasOwnProperty(event_ID)) {
            var i, len, index;
            this.newOrderList = [];
            for (i = 0, len = myVsearch.termGraph.term2Doc[event_ID].length; i < len; i++) {
                index = myVsearch.termGraph.term2Doc[event_ID][i];
                let tempSnippet = myVsearch.searchResults[index];
                this.newOrderList.push(tempSnippet);
                if (res[tempSnippet.docTitle] === undefined) {
                    res[tempSnippet.docTitle] = 1;
                } else {
                    res[tempSnippet.docTitle] += 1;
                }
            }
            this.clickedTerm = event_ID;
            pageBar.resetPageNum(this.newOrderList.length / this.numEachPage);

            displayMethod.changeInfoTag(len);
            this.displayTheOrder(0, event_ID);
        }
    }
    return res;
}

reOrderList.dateFilter = function(d1, d2) {
    let termsArrs = [];
    if (d1 === d2) {
        this.allData();
        return false;
    } else {
        this.newOrderList = myVsearch.getResultsInterval(d1, d2);
        pageBar.resetPageNum(this.newOrderList.length / this.numEachPage);
        displayMethod.changeInfoTag(this.newOrderList.length);
        this.clickedTerm = '';
        this.displayTheOrder(0, '');
        termsArrs = this.newOrderList.map(function(n) {
            return n.contentList();
        });
    }
    return termsArrs;
}

var notifyier = {
    topics: {},
    subscribe: function(topic, id, func) {
      if (this.topics[topic] === undefined) {
        this.topics[topic] = [];
      }
      this.topics[topic].push({
        id: id,
        method: func
      });
    },
    update: function(topic, paras) {
      let oneTopic = this.topics[topic];
      if (oneTopic !== undefined) {
        let lg = oneTopic.length;
        for (let i = 0; i < lg; i += 1) {
          oneTopic[i].method(paras);
        }
      }
    },
    removeSubscriber: function(topic, id, func) {
      let oneTopic = this.topics[topic];
      if (oneTopic !== undefined) {
        if (id === undefined && func === undefined) {
          delete this.topics[topic];
        } else {
          for (let i = 0, j = oneTopic.length; i < j; i += 1) {
            if (oneTopic[i].id === id || oneTopic[i].method === func) {
              oneTopic.splice(i, 1);
              i -= 1;
              j -= 1;
            }
          }
        }
      }
    }
};

var myVsearch = {
    termGraph : {},
    searchResults : [],
    documentGraph : {},
    interactGraph: {},
    lastQuery : "",
    hasData : false,
    totalNum : 0,
    infoPane: $('#msgPane'),
    searchInputs: $('#searchInput').find('input'),
    showInfoPane: function() {
        this.infoPane.css('display', 'flex');
        setTimeout(function() {
            myVsearch.infoPane.hide();
        }, 2000);
    },
    isFace: function (text) {
        return (this.faceDict[text] !== undefined);
    },
    checkFaceHasImage: function(data) {

        for (let oneNode of data.nodes) {
            if (this.isFace(oneNode.text)) {
            //if (this.faceDict[oneNode.text] !== undefined) {
                oneNode.isImage = true;
                oneNode.imageHref = 'data/faces/' + this.faceDict[oneNode.text];
            }
        }
    },
    clearSearch : function() {
        myVsearch.searchInputs.val('');
    },
    setSearchKeyword: function(word) {
        myVsearch.searchInputs.eq(3).focus().attr('placeholder','').val(word);
    },
    searchKeyword: function(word) {
        myVsearch.clearSearch();
        myVsearch.setSearchKeyword(word);
        myVsearch.searchRequest();
    },
    clearSearchDate : function() {
        myVsearch.searchInputs.eq(0).val('').attr('placeholder', 'Start date');
        myVsearch.searchInputs.eq(1).val('').attr('placeholder', 'End date');
    },
    setSearchDate: function(d1, d2) {
        if (d1 && d1.length > 0) {
            myVsearch.searchInputs.eq(0).attr('placeholder', '').val(d1);
        }
        if (d2 && d2.length > 0) {
            myVsearch.searchInputs.eq(1).attr('placeholder', '').val(d2);
        }
    },
    getSearhContent : function() {
        return {
            startDate: myVsearch.searchInputs.eq(0).val(),
            endDate: myVsearch.searchInputs.eq(1).val(),
            faceName: myVsearch.searchInputs.eq(2).val(),
            keywords: myVsearch.searchInputs.eq(3).val().toLowerCase()
        }
    },
    searchRequest: function() {
        /* Start of the program */
        let searchBoxContent = myVsearch.getSearhContent();

        let startDate = searchBoxContent.startDate.replace('_', '');

        let endDate = searchBoxContent.endDate.replace('_', '');

        let faceName = searchBoxContent.faceName;

        let keywords = searchBoxContent.keywords;

        let input = startDate + '-' + endDate + '-' + faceName + '-' + keywords;

        if (input == "---") return false;

        // windowControl.clearGraph();
        // if (input !== myVsearch.lastQuery) {
        let faceNameArr = [];

        if (faceName.length > 0) {
            faceNameArr.push({'text': faceName});
        }

        let keywordArr = [];

        if (keywords.length > 0) {
            keywordArr.push({'text': keywords});
        }

        let para = {
            'dates': [startDate + '-' + endDate],
            'faceNames': faceNameArr,
            'keywords': keywordArr,
            'fkconj': 'AND',
        }

        Vsearch_fd(para);

        searchBox.resetQueryBox();
        searchBox.hideQueryBox();
        // Vsearch_fd(startDate, endDate, faceName, keywords);
            // myVsearch.lastQuery = input;
        // } else {
        //     myVsearch.showInfoPane();
        //     myVsearch.updateInfoPane('Same input, please try something else...');
        //     setTimeout(function() {
        //         myVsearch.hideInfoPane();
        //     }, 1000);
        // }
        return false;
    },
    getTermsTitleDict: function() {
        //console.log("here we are constructing the graph", myVsearch.searchResults)
        
        myVsearch.termGraph = benterm2Document(myVsearch.searchResults);

        myVsearch.termsAllArrs = myVsearch.getCloudTerms(myVsearch.termGraph.term2Doc);
        popModal.updateTermsList(myVsearch.termsAllArrs);
        // myVsearch.documentGraph = doc2Document(myVsearch.termGraph.term2Doc);
        // myVsearch.interactGraph = interactionGraph(myVsearch.documentGraph);
        // myVsearch.checkFaceHasImage(myVsearch.interactGraph);
    },
    getCloudTerms: function(termDict) {
        let termsArrs = [];
        for (let oneTerm in termDict) {
            let dictSize = termDict[oneTerm].length;
            if (dictSize > popModal.miniTermDocNum) {
                termsArrs.push({
                    'text': oneTerm,
                    'doc': termDict[oneTerm],
                    'val': dictSize 
                })
            }
        };

        termsArrs.sort(function(a, b) {
            return b.val - a.val;
        })
        return termsArrs;
    },
    getResultsInterval: function(d1, d2) {
        let docsDuringD1D2 = [];
        for (let oneSnippet of myVsearch.searchResults) {
            if (oneSnippet.docTitle >= d1 && oneSnippet.docTitle <= d2) {
                docsDuringD1D2.push(oneSnippet);
            }
        };
        reOrderList.sortRes(docsDuringD1D2);
        return docsDuringD1D2;
    },
    countTitleDict: function() {
        this.titleDict = {};
        for (let oneSnippet of this.searchResults) {
            if (this.titleDict[oneSnippet.docTitle] === undefined) {
                this.titleDict[oneSnippet.docTitle] = 1;
            } else {
                this.titleDict[oneSnippet.docTitle] += 1;
            }
        }
    }
}

var popModal = {
    myModal : $('.modal'),
    miniTermDocNum : 3,
    showModal: function() {
        popModal.myModal.modal({
            onApprove: function() {
                windowControl.updateTermsFromCheckList();
            }
        }).modal('show');
    },
    updateTermsList: function(compareDict) {
        let listPane = popModal.myModal.find('.list');
        let arrs = myVsearch.termsAllArrs;
        let arrsSize = arrs.length;
        let onePieceSize = Math.ceil(arrsSize/3);
        let twoPieceSize = onePieceSize * 2;
        
        function addOneCheck(text, val, isChecked) {
            let res = '<div class="item"><div class="ui checkbox"><input type="checkbox"'
            if (isChecked) {
               res += ' checked="true"><label>';
            } else {
                res += '><label>';
            }
            res += text + '</label></div><div class="right floated content">' + val + '</div></div>';
            return res;
        }

        let preList = '';
        let sedList = '';
        let tedList = '';

        for (let i = 0; i < arrsSize; i += 1) {
            let tempText = arrs[i].text;
            let isShowed = false;
            if (compareDict[tempText] !== undefined) {
                isShowed = true;
            }
            if (i < onePieceSize) {
                preList += addOneCheck(tempText, arrs[i].val, isShowed);
            } else if (i < twoPieceSize) {
                sedList += addOneCheck(tempText, arrs[i].val, isShowed);
            } else {
                tedList += addOneCheck(tempText, arrs[i].val, isShowed);
            }
        }
        listPane.eq(0).html(preList);
        listPane.eq(1).html(sedList);
        listPane.eq(2).html(tedList);
        let ckbs = listPane.find('.checkbox');

        popModal.myModal.find('.master.checkbox').checkbox({
            onChecked: function() {
                ckbs.checkbox('check')
            },
            onUnchecked: function() {
                ckbs.checkbox('uncheck')
            }
        })
        ckbs.checkbox();
    },
    getCheckedTerms: function() {
        let cks = popModal.myModal.find('.checkbox');
        let lg = cks.length;
        let checkedTermsDict = {};
        for (let i = 1; i < lg; i += 1) {
            let tempElement = cks.eq(i);
            if (tempElement.checkbox('is checked')) {
                checkedTermsDict[tempElement.text()] = 0;
            }
        }

        return checkedTermsDict;
    },
    initial: function() {
        
        $('#mdlToggle').on('click', function() {
            windowControl.showTermsCheckList();
        })
    }
}

var pageBar = {
    pageNow : 0,
    firstCall : true,
    pageNumEle: $('#pa2'),
    setPage : function(pageNum) {
        this.pageNumEle.dropdown('set selected', pageNum);
    },
    initPageNum: function() {
        this.pageNumEle.dropdown({
            onChange(val, tx) {
                pageBar.changePage(+tx);
            }
        });
    },
    setPageText: function(num) {
        this.pageNow = num;
        this.pageNumEle.dropdown('set text', num);
    },
    resetPageNum: function(number) {
        this.pageNow = 1;
        this.setPageText(this.pageNow);
        let res = '';
        for (let i = 1; i <= number; i += 1) {
            res += '<div class="item">' + i + '</div>'; 
        }
        this.pageNumEle.find('.menu').html(res);
    },
    previousPage : function() {
        pageBar.setPage(pageBar.pageNow-1);
    },
    nextPage : function() {
        pageBar.setPage(pageBar.pageNow+1);
    },
    changePage : function(val) {
        if (val == 0 || pageBar.pageNow === val || typeof val !== 'number') {
            return;
        } else {
            var skip2 = reOrderList.numEachPage * (val - 1);
            if (skip2 > reOrderList.newOrderList.length || skip2 < 0) {
                return 0;
            }
            reOrderList.displayTheOrder(skip2, reOrderList.clickedTerm);
            this.pageNow = parseInt(val);
        }
    }
}

var searchBox = {
    dateArr: [],
    faceArr: [],
    keywordsArr: [],
    faceOrKeyword: 'AND',
    showQueryBox: function() {
        $('#multiQueryBox').show();
    },
    hideQueryBox: function() {
        $('#multiQueryBox').hide();
    },
    getQueryBoxDate: function() {
        let resArr = [];
        for (let oneDate of searchBox.dateArr) {
            resArr.push(oneDate.eq(1).text().replace('_', ''));
        }
        return resArr;
    },
    getOneQueryText: function(posi, $ele) {
        let resArr = [];
        if (posi !== 0) {
            resArr.push({
                'conj': $ele.eq(0).text()
            });
        }
        let startBracket = $ele.eq(1).find('span').text();
        let startBracketSize = startBracket.length;
        if (startBracketSize === 1) { 
            resArr.push({
                'bracket':startBracket
            });
        } else if (startBracketSize > 1) {
            for (let i = 0; i < startBracketSize; i += 1) {
                resArr.push({
                    'bracket': startBracket[0]
                })
            }
        }
        let labelText = $ele.eq(2).text();
        resArr.push({
            'text': labelText
        });
        
        let endBracket = $ele.eq(3).find('span').text();
        let endBracketSize = endBracket.length;
        if (endBracketSize === 1) { 
            resArr.push({
                'bracket':endBracket
            });
        } else if (endBracketSize > 1) {
            for (let i = 0; i < endBracketSize; i += 1) {
                resArr.push({
                    'bracket': endBracket[0]
                }) 
            }
        }

        return resArr;
    },
    getFaceQueryText: function() {
        let resArr = [];
        let lg = searchBox.faceArr.length;

        for (let i = 0; i < lg; i += 1) {
            let oneFaceItem = searchBox.faceArr[i];
            let oneItemArr = searchBox.getOneQueryText(i, oneFaceItem);

            resArr = resArr.concat(oneItemArr);
        }
        return resArr;
    },
    getKeywordsText: function() {
        let resArr = [];
        let lg = searchBox.keywordsArr.length;

        for (let i = 0; i < lg; i += 1) {
            let oneFaceItem = searchBox.keywordsArr[i];
            let oneItemArr = searchBox.getOneQueryText(i, oneFaceItem);

            resArr = resArr.concat(oneItemArr);
        }
        return resArr;
    },
    resetQueryBox: function() {
        $('.searchContent').empty();
        searchBox.dateArr = [];
        searchBox.faceArr = [];
        searchBox.keywordsArr = [];
    },
    formatLabel: function(labelText) {
        let tempText = '<a class="ui green circular label">AND</a>';
        tempText += '<div class="ui icon inline dropdown button">';
        tempText += '<span class="text"></span>';
        tempText += '<div class="menu"><div class="item"></div>';
        tempText += '<div class="item"><b>(</b></div>';
        tempText += '<div class="item"><b>((</b></div>';
        tempText += '<div class="item"><b>(((</b></div>';
        tempText += '<div class="item"><b>)</b></div>';
        tempText += '<div class="item"><b>))</b></div>';
        tempText += '<div class="item"><b>)))</b></div></div>';
        tempText += '</div><div class="ui label queryTag">';
        tempText += labelText;
        tempText += '<i class="delete icon"></i></div>';
        tempText += '<div class="ui icon inline dropdown button">';
        tempText += '<span class="text"></span>';
        tempText += '<div class="menu"><div class="item"></div>';
        tempText += '<div class="item"><b>(</b></div>';
        tempText += '<div class="item"><b>((</b></div>';
        tempText += '<div class="item"><b>(((</b></div>';
        tempText += '<div class="item"><b>)</b></div>';
        tempText += '<div class="item"><b>))</b></div>';
        tempText += '<div class="item"><b>)))</b></div></div></div>';
        return tempText;
    },
    addFaceQuery: function(faceName) {
        if (faceName === '') {
            return;
        }
        
        let tempText = searchBox.formatLabel(faceName);
        let tempElement = $(tempText);
        if (searchBox.faceArr.length === 0) {
            tempElement.eq(0).hide();
        }

        tempElement.eq(1).dropdown();
        tempElement.eq(3).dropdown();

        tempElement.eq(0).on('click', function() {
            if (this.innerHTML === 'AND') {
                $(this).removeClass('green')
                        .addClass('blue')
                        .text('OR');
            } else {
                $(this).removeClass('blue')
                        .addClass('green')
                        .text('AND');
            }
        })

        tempElement.find('i').on('mouseover', function() {
            tempElement.addClass('red');
        }).on('mouseleave', function() {
            tempElement.removeClass('red');
        }).on('click', function() {
            tempElement.remove();
            let lg = searchBox.faceArr.length;
            for (let i = 0; i < lg; i += 1) {
                if (searchBox.faceArr[i] === tempElement) {
                    if (i === 0) {
                        if (lg > 1) {
                            searchBox.faceArr[1].eq(0).hide();
                        }
                    }
                    tempElement.remove();
                    searchBox.faceArr.splice(i, 1);
                    break;
                }
            }
        });
        searchBox.faceArr.push(tempElement);
        $('#faceQueryBox').append(tempElement);
    },
    addKeywordQuery: function(keywords) {

        let wordsList = keywords.split(',');
        let lg = wordsList.length;
        if (lg === 0) {
            return;
        }
        for (let i = 0; i < lg; i += 1) {
            if (wordsList[i] === '') {
                continue;
            }
            let tempText = searchBox.formatLabel(wordsList[i]);
            let tempElement = $(tempText);
            if (searchBox.keywordsArr.length === 0) {
                tempElement.eq(0).hide();
            }

            tempElement.eq(1).dropdown();
            tempElement.eq(3).dropdown();

            tempElement.eq(0).on('click', function() {
                if (this.innerHTML === 'AND') {
                    $(this).removeClass('green')
                            .addClass('blue')
                            .text('OR');
                } else {
                    $(this).removeClass('blue')
                            .addClass('green')
                            .text('AND');
                }
            })

            tempElement.find('i').on('mouseover', function() {
                tempElement.addClass('red');
            }).on('mouseleave', function() {
                tempElement.removeClass('red');
            }).on('click', function() {
                tempElement.remove();
                let lg = searchBox.keywordsArr.length;
                for (let i = 0; i < lg; i += 1) {
                    if (searchBox.keywordsArr[i] === tempElement) {
                        if (i === 0) {
                            if (lg > 1) {
                                searchBox.keywordsArr[1].eq(0).hide();
                            }
                        }
                        tempElement.remove();
                        searchBox.keywordsArr.splice(i, 1);
                        break;
                    }
                }
            });
            searchBox.keywordsArr.push(tempElement);
            $('#keywordQueryBox').append(tempElement);
        }
    },
    addDateQuery: function(d1, d2) {
        if (d1.replace(' ', '') === '' && d2.replace(' ', '') === '') {
            return;
        }

        let dateStr = d1 + '-' + d2;

        for (let oneDateEle of searchBox.dateArr) {
            if (dateStr === oneDateEle.eq(1).text()) {
                return;
            }
        }

        let tempText = '<a class="ui blue circular label">OR</a><div class="ui label queryTag">';
            tempText += dateStr;
            tempText += '<i class="delete icon"></i></div>';
        
        let tempElement = $(tempText);

        if (searchBox.dateArr.length === 0) {
            tempElement.eq(0).hide();
        };
        tempElement.find('i').on('mouseover', function() {
            tempElement.addClass('red');
        }).on('mouseleave', function() {
            tempElement.removeClass('red');
        }).on('click', function() {
            tempElement.remove();
            let lg = searchBox.dateArr.length;
            for (let i = 0; i < lg; i += 1) {
                if (searchBox.dateArr[i] === tempElement) {
                    if (i === 0) {
                        if (lg > 1) {
                            searchBox.dateArr[1].eq(0).hide();
                        }
                    }
                    tempElement.remove();
                    searchBox.dateArr.splice(i, 1);
                    break;
                }
            }
        });
        
        searchBox.dateArr.push(tempElement);

        $('#dateQueryBox').append(tempElement);
    },
    initial: function() {
        let self = searchBox;
        // $('#multiQueryBox .dropdown').dropdown();
        $('#clearSearchBox').on('click', function() {
            self.resetQueryBox();
        });
        $('#faceOrKeyword').on('click', function() {
            if (this.innerHTML === 'AND') {
                $(this).removeClass('green')
                        .addClass('blue')
                        .text('OR');
                self.faceOrKeyword = 'OR';
            } else {
                $(this).removeClass('blue')
                        .addClass('green')
                        .text('AND');
                self.faceOrKeyword = 'AND';
            }
        });
        $('#addToBox').on('click', function() {
            let searchBoxContent = myVsearch.getSearhContent();
            self.addDateQuery(searchBoxContent.startDate, searchBoxContent.endDate);
            self.addFaceQuery(searchBoxContent.faceName)
            self.addKeywordQuery(searchBoxContent.keywords);
            self.showQueryBox();
            myVsearch.clearSearch();
        });
        $('#commitBoxSearch').on('click', function() {
            let dates = self.getQueryBoxDate();
            let faces = self.getFaceQueryText();
            let keywords = self.getKeywordsText();
            let para = {
                dates: dates,
                faceNames: faces,
                keywords: keywords,
                fkconj: self.faceOrKeyword
            };
            console.log(para);
            Vsearch_fd(para);
        })
    }
}

var myTimeline = {
    initial: function() {
        let timelinePane = $('#timeline');
        let instance = new activityIndex($('#timeline'), timelinePane.width(), 400);
        instance.init();
        // this.myTimeline.processData(myVsearch.titleDict);
        // let that = this;
        instance.callback = function(d1, d2) {
            notifyier.update('selectedDateInterval', d1, d2);
            let termsInterval = reOrderList.dateFilter(d1, d2);
            if (termsInterval) {
                let notRepeatTerms = {};
                for (let oneArr of termsInterval) {
                    for (let oneTerm of oneArr) {
                        if (notRepeatTerms[oneTerm]) {
                            notRepeatTerms[oneTerm] += 1;
                        } else {
                            notRepeatTerms[oneTerm] = 1
                        }
                    }
                }
                notifyier.update('filterTerms', notRepeatTerms);;
            } else {
                notifyier.update('clearTermsFilter');
            }
        }

        return instance;
    },
}

var makeGroup = {
    groupsInfo : {},
    groupNum : 0,
    searchGroups : 3,
    docsGrouped : false,
    groupTheGraph : function(initialInterGraph, groupSize) {
        makeGroup.groupsInfo = {};
        var groupFinal = initialInterGraph;

        if (!initialInterGraph.hasOwnProperty('termsArrs') || initialInterGraph.termsArrs.length < groupSize) {
            getMatrixVertiMax(groupFinal);
            getTermsGroups(groupFinal);
            
            optimiseGroup(groupFinal);
            regroupTerms(groupFinal);
            createTermsArr(groupFinal);
            getOptiGroup(groupFinal);
        } 
        reduceGroup(groupSize, groupFinal);

        var i, j, len, term, len2, leaf, leafList, tempInfo = {};

        for (i = 0, len = groupFinal.termsArrs.length; i < len; i += 1) {
            leafList = groupFinal.termsArrs[i];
            for (j = 0, len2 = leafList.length; j < len2; j += 1) {
                leaf = leafList[j];
                term = groupFinal.nodes[leaf];
                tempInfo[term.text] = i + 1;
                term.group = i + 1;
            }
        }
        makeGroup.groupNum = len;
        makeGroup.groupsInfo = tempInfo;
    }
}

var sidebarPane = {
    mySidebar: $('.ui.sidebar'),
    maxSnippetsNum: 200,
    isShowed: true,
    showSidebar : function() {
        sidebarPane.mySidebar
                    .sidebar('setting', 'transition', 'overlay')
                    .sidebar('toggle');
    },
    submitMethod: function() {
        let snippetsNumEle = sidebarPane.mySidebar.children().eq(1).find('input');
        let snippetsNum = +snippetsNumEle.val();
        if (snippetsNum > 0) {
            sidebarPane.maxSnippetsNum = snippetsNum;
        } else {
            sidebarPane.maxSnippetsNum = 200;
            snippetsNumEle.val(200);
        }

    },
    initial: function() {
        $('#pageID').on('click', function() {
            sidebarPane.showSidebar();
        });
        sidebarPane.mySidebar.find('.checkbox').checkbox({
            'onChange': function(d) {
                if (sidebarPane.isShowed) {
                    sidebarPane.isShowed = false;
                    $('#timeline').hide();
                } else {
                    sidebarPane.isShowed = true;
                    $('#timeline').show();
                }
            }
        })

        sidebarPane.mySidebar.find('#sidebarSettingSubmit').on('click', function() {
            sidebarPane.submitMethod();
            sidebarPane.showSidebar();
        })
    }
}

var windowControl = {
    windowDict : {},
    currentWindow : "",
    lastWindow: '',
    showTermsCheckList: function() {
        if (windowControl.currentWindow !== '') {
            let ctw = windowControl.windowDict[windowControl.currentWindow];
            ctw.getCheckList();
            popModal.showModal();
        }
    },
    reopenWindow: function() {
        if (windowControl.lastWindow !== '') {
            windowControl.changeWindow(windowControl.lastWindow);
        }
    },
    updateTermsFromCheckList: function() {
        if (windowControl.currentWindow !== '') {
            let checkTerms = popModal.getCheckedTerms();
            if (Object.keys(checkTerms).length > 0) {
                let ctw = windowControl.windowDict[windowControl.currentWindow];
                ctw.showCheckData(checkTerms);
            }
        }
    },
    changeWindow : function(tag_Name) {
        let graphPaneName = 'g' + tag_Name;
        if (!myVsearch.hasData) return false;
        if (windowControl.currentWindow === graphPaneName) {
            return false;
        } else if (graphPaneName === "ghd") {
            windowControl.clearGraph();
            windowControl.lastWindow = '';
            return false;
        }
        windowControl.lastWindow = tag_Name;
        if (windowControl.currentWindow !== "") {
            windowControl.windowDict[windowControl.currentWindow].hideWin();
        }
        var result = windowControl.windowDict[graphPaneName];
        if (!result) {
            result = windowControl.addWindow(graphPaneName);
        };
        windowControl.currentWindow = graphPaneName;
        $(graphPaneName).show();
        result.showWin();
    },
    clearGraph : function() {
        for (var item in windowControl.windowDict) {
            if (windowControl.windowDict[item]) {
                windowControl.windowDict[item].clearGraphContent();
                windowControl.windowDict[item].hideWin();
            }
        };
        windowControl.currentWindow = "";
        $('.tl').removeClass('active');
    },
    addWindow : function(windowName) {
        windowControl.windowDict[windowName] = graphRequest(windowName);
        return windowControl.windowDict[windowName];
    }
};