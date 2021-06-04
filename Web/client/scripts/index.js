$(function() {

    $('#submitSearch').on('click', myVsearch.searchRequest);

    $('#kdInput').submit(function() {
        setTimeout(myVsearch.searchRequest, 20);
        return false;
    }).find('input').focus();

    let myFaceInput = $('#faceInput'); 
    myFaceInput.submit(function() {
        setTimeout(myVsearch.searchRequest, 20);
        return false;
    })

    $('.tl').on("click", function() {
        if (myVsearch.hasData) {
            $(this).siblings().removeClass('active');

            if (this.id !== 'hd') {
                $(this).addClass('active');
            }
        }
        try {
            windowControl.changeWindow(this.id);
        } catch (e) {
            console.log(e);
        }
    })
    
    let topEle = document.getElementById('searchResult');
    let isVpSticky = false;
    let myVideoPlayer = $('#vpBoard');
    const TOP_BOARD = 10;
    
    window.onscroll = function() {
       
        var ReTop = topEle.getBoundingClientRect().top;

        if (ReTop < TOP_BOARD && !isVpSticky) {
            isVpSticky = true;
            myVideoPlayer.removeClass('moveVp').addClass('stickyVp');
        } else if (ReTop > TOP_BOARD && isVpSticky) {
            isVpSticky = false;
            myVideoPlayer.removeClass('stickyVp').addClass('moveVp');
        }
    }

    utilObj.addEvent("pf1", "click", pageBar.previousPage);
    utilObj.addEvent("pf2", "click", pageBar.nextPage);
    
    pageBar.initPageNum();

    myTimeline = myTimeline.initial();

    searchBox.initial();

    sidebarPane.initial();

    popModal.initial();

    utilObj.requestData('/face', {}, function(data) {
        myVsearch.faceDict = data;
        let tempArr = [];
        for (let oneFace in data) {
            tempArr.push({'title': oneFace});
        };
        myFaceInput.search({
            source: tempArr
        });
    }, true);
});
