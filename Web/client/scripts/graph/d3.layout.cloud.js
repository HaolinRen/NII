var wordCluster = {
  coreData : {},
  // isShowed : false,
  MIN_SIZE : 80,
  MAX_SIZE : 160,
  corePosition : function(nodeID, kind) {
    if (!this.coreData.hasOwnProperty(nodeID)) {
      console.log(nodeID);
      return 0;
    }
    if (kind == 0) {
      return this.coreData[nodeID][0];
    } else {
      return this.coreData[nodeID][1];
    }
  },
  optimiseCorePosition : function(winWidth, winHeight, nodesIn) {
    this.coreData = {};
    function groupSort(a, b) {
      return a.group - b.group;
    }
    d3.layout.pack()
        .size([winWidth, 1.5 * winHeight])
        .children(function(d) { return d.values; })
        .value(function(d) { return d.nodeSize; })
        .nodes({values: d3.nest()
                .key(function(d) { return d.group; })
                .entries(nodesIn)});
    var oneNode, nodeData;
    for (oneNode in nodesIn) {
      nodeData = nodesIn[oneNode];
      this.coreData[nodeData.text] = [parseInt(nodeData.x), parseInt(nodeData.y)];
    }
  },
  dendrogramPosition : function(winWidth, winHeight, interGraph) {
    this.coreData = {};
    var packPos = d3.layout.pack()
                    .size([winWidth, winHeight])
                    .value(function(d) { if (d.text === "") {
                        return 1;
                      } else {
                        return d.degree/10 + 4;
                      }; })
                    .nodes(getDendrogram(interGraph));
    var nodeData, i, len;
    len = packPos.length;
    for (i = 0; i < len; i += 1) {
      if (packPos[i].text != "") {
        nodeData = packPos[i];
        this.coreData[nodeData.text] = [parseInt(nodeData.x), parseInt(nodeData.y)];
      }
    }
    // if (!this.isShowed) {
    //   d3.select('#packPlace').selectAll('*').remove();

    //   var svg = d3.select('#packPlace')
    //             .append('svg')
    //             .attr('width', winHeight)
    //             .attr('height', 800)
    //             .append('g')
    //             .attr('transform', 'translate(10, 10)');

    //   var node = svg.selectAll('.node')
    //                 .data(packPos)
    //                 .enter().append('g')
    //                 .attr('class', function(d) {return d.children ? 'node' : 'leaf node'})
    //                 .attr('transform', function(d) {
    //                   return 'translate(' + d.x + ',' + d.y + ')';
    //                 });
    //   var format = d3.format(', d');

    //   node.append('title')
    //       .text(function(d) { return d.text;})//nodeSize + (d.children ? '' : ' : ' + format(d.nodeSize)); })

    //   node.append('circle')
    //       .attr('class','tcircle')
    //       .attr('r', function(d) {return d.r; });

      // node.append("text")
      //   .attr("dy", ".3em")
      //   .style("text-anchor", "middle")
      //   .text(function(d) { return d.text; });

    // }
  },
  imageSizeScale: function(val) {
    return parseInt(this.sizeScale(val));
  },
  initSizeScale: function(data) {
    this.sizeScale = d3.scale.log().range([this.MIN_SIZE, this.MAX_SIZE]);
    let minSize = 0;
    let maxSize = 0;
    data.forEach(function(n) {
      if (n.isImage) {
        if (n.termIndex < minSize || minSize === 0) {
          minSize = n.termIndex;
        }
        if (n.termIndex > maxSize) {
          maxSize = n.termIndex;
        }
      }
    });
    this.sizeScale.domain([minSize, maxSize]);
  }
};

(function() {
  function cloud() {
    var size = [256, 256],
        text = cloudText,
        font = cloudFont,
        fontSize = cloudFontSize,
        fontStyle = cloudFontNormal,
        fontWeight = cloudFontNormal,
        rotate = cloudRotate,
        padding = cloudPadding,
        spiral = archimedeanSpiral,
        words = [],
        timeInterval = Infinity,
        event = d3.dispatch("word", "end"),
        timer = null,
        cloud = {};

    cloud.start = function() {
      var board = zeroArray((size[0] >> 5) * size[1]),
          bounds = null,
          n = words.length,
          i = -1,
          tags = [],
          data = words.map(function(d, i) {
            d.text = text.call(this, d, i);
            d.font = font.call(this, d, i);
            d.style = fontStyle.call(this, d, i);
            d.weight = fontWeight.call(this, d, i);
            d.rotate = rotate.call(this, d, i);
            d.size = ~~fontSize.call(this, d, i);
            d.padding = padding.call(this, d, i);
            return d;
          }).sort(function(a, b) { return a.ogod - b.ogod; });
      if (timer) clearInterval(timer);
      timer = setInterval(step, 0);
      wordCluster.initSizeScale(data);
      step();

      return cloud;

      function corePosi(nodeID, kind) {
        if (true) {
          return wordCluster.corePosition(nodeID, kind);
        } else {
          return (size[kind] * (Math.random() + .5)) >> 1;
        }
      }
      function step() {
        var start = +new Date,
            d;
        while (+new Date - start < timeInterval && ++i < n && timer) {
          d = data[i];
          d.x = corePosi(d.text, 0);
          d.y = corePosi(d.text, 1);
          
          cloudSprite(d, data, i);

          if (d.hasText && place(board, d, bounds)) {
            tags.push(d);
            event.word(d);
            if (bounds) cloudBounds(bounds, d);
            else bounds = [{x: d.x + d.x0, y: d.y + d.y0}, {x: d.x + d.x1, y: d.y + d.y1}];

            d.x -= size[0] >> 1;
            d.y -= size[1] >> 1;
          }
        }
        if (i >= n) {
          cloud.stop();
          event.end(tags, bounds);
        }
      }
    }

    cloud.stop = function() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
      return cloud;
    };

    cloud.timeInterval = function(x) {
      if (!arguments.length) return timeInterval;
      timeInterval = x == null ? Infinity : x;
      return cloud;
    };

    function place(board, tag, bounds) {
      var perimeter = [{x: 0, y: 0}, {x: size[0], y: size[1]}],
          startX = tag.x,
          startY = tag.y,
          maxDelta = Math.sqrt(size[0] * size[0] + size[1] * size[1]),
          s = spiral(size),
          dt = Math.random() < .5 ? 1 : -1,
          t = -dt,
          dxdy,
          dx,
          dy;

      while (dxdy = s(t += dt)) {
        dx = ~~dxdy[0];
        dy = ~~dxdy[1];

        if (Math.min(dx, dy) > maxDelta) {
          console.log('out box')
          break
        };

        tag.x = startX + dx;
        tag.y = startY + dy;

        if (tag.x + tag.x0 < 0 || tag.y + tag.y0 < 0 ||
            tag.x + tag.x1 > size[0] || tag.y + tag.y1 > size[1]) continue;
        // TODO only check for collisions within current bounds.
        if (!bounds || !cloudCollide(tag, board, size[0])) {
          if (!bounds || collideRects(tag, bounds)) {
            var sprite = tag.sprite,
                w = tag.width >> 5,
                sw = size[0] >> 5,
                lx = tag.x - (w << 4),
                sx = lx & 0x7f,
                msx = 32 - sx,
                h = tag.y1 - tag.y0,
                x = (tag.y + tag.y0) * sw + (lx >> 5),
                last;
            for (var j = 0; j < h; j++) {
              last = 0;
              for (var i = 0; i <= w; i++) {
                board[x + i] |= (last << msx) | (i < w ? (last = sprite[j * w + i]) >>> sx : 0);
              }
              x += sw;
            }
            delete tag.sprite;
            return true;
          }
        }
      }
      return false;
    }

    cloud.words = function(x) {
      if (!arguments.length) return words;
      words = x;
      return cloud;
    };

    cloud.size = function(x) {
      if (!arguments.length) return size;
      size = [+x[0], +x[1]];
      return cloud;
    };

    cloud.font = function(x) {
      if (!arguments.length) return font;
      font = d3.functor(x);
      return cloud;
    };

    cloud.fontStyle = function(x) {
      if (!arguments.length) return fontStyle;
      fontStyle = d3.functor(x);
      return cloud;
    };

    cloud.showImageLabel = function(x) {
      if (!arguments.length) return false;
      showImageLabel = d3.functor(x);
      return cloud;
    }

    cloud.fontWeight = function(x) {
      if (!arguments.length) return fontWeight;
      fontWeight = d3.functor(x);
      return cloud;
    };

    cloud.rotate = function(x) {
      if (!arguments.length) return rotate;
      rotate = d3.functor(x);
      return cloud;
    };

    cloud.text = function(x) {
      if (!arguments.length) return text;
      text = d3.functor(x);
      return cloud;
    };

    cloud.spiral = function(x) {
      if (!arguments.length) return spiral;
      spiral = spirals[x + ""] || x;
      return cloud;
    };

    cloud.fontSize = function(x) {
      if (!arguments.length) return fontSize;
      fontSize = d3.functor(x);
      return cloud;
    };

    cloud.padding = function(x) {
      if (!arguments.length) return padding;
      padding = d3.functor(x);
      return cloud;
    };

    return d3.rebind(cloud, event, "on");
  }

  function cloudText(d) {
    return d.text;
  }

  function cloudFont() {
    return "serif";
  }

  function cloudFontNormal() {
    return "normal";
  }

  function cloudFontSize(d) {
    return Math.sqrt(d.value);
  }

  function cloudRotate() {
    return (~~(Math.random() * 6) - 3) * 30;
  }

  function cloudPadding() {
    return 1;
  }

  function showImageLabel() {
    return false;
  }

  // Fetches a monochrome sprite bitmap for the specified text.
  // Load in batches for speed.
  function cloudSprite(d, data, di) {
    if (d.sprite) {
      return;
    }
    c.clearRect(0, 0, (cw << 5) / ratio, ch / ratio);
    var x = 0,
        y = 0,
        maxh = 0,
        n = data.length;
    --di;
    while (++di < n) {
      d = data[di];
      c.save();

      if (d.isImage) {
        let tempSize = 14
        c.font = d.style + " " + d.weight + " " + ~~((tempSize + 1) / ratio) + "px " + d.font;
      } else {
        c.font = d.style + " " + d.weight + " " + ~~((d.size + 1) / ratio) + "px " + d.font;
      }
      var w = c.measureText(d.text + "m").width * ratio,
          h = d.size << 1;

      if (d.isImage) {
        w = wordCluster.imageSizeScale(d.termIndex);
      }
      
      if (d.rotate) {
        var sr = Math.sin(d.rotate * cloudRadians),
            cr = Math.cos(d.rotate * cloudRadians),
            wcr = w * cr,
            wsr = w * sr,
            hcr = h * cr,
            hsr = h * sr;
        w = (Math.max(Math.abs(wcr + hsr), Math.abs(wcr - hsr)) + 0x1f) >> 5 << 5;
        h = ~~Math.max(Math.abs(wsr + hcr), Math.abs(wsr - hcr));
      } else {
        w = (w + 0x1f) >> 5 << 5;
      }

      if (d.isImage) {
        h = w;
      }
      if (h > maxh) maxh = h;
      if (x + w >= (cw << 5)) {
        x = 0;
        y += maxh;
        // maxh = 0;
      }
      if (y + h >= ch) break;
      
      c.translate((x + (w >> 1)) / ratio, (y + (h >> 1)) / ratio);

      if (d.rotate) c.rotate(d.rotate * cloudRadians);
      if (d.isImage) {
        c.fillRect(0, 0, w, w);
        if (showImageLabel.call(this)) {
          c.fillText(d.text, 0, 0);
        }
      } else {
        c.fillText(d.text, 0, 0);
      }

      if (d.padding && !d.isImage) {
        c.lineWidth = 2 * d.padding;
        c.strokeText(d.text, 0, 0);
      }
      c.restore();

      d.width = w;
      d.height = h;
      d.xoff = x;
      d.yoff = y;
      d.x1 = w >> 1;
      d.y1 = h >> 1;
      d.x0 = -d.x1;
      d.y0 = -d.y1;
      d.hasText = true;
      x += w;
    }
    var pixels = c.getImageData(0, 0, (cw << 5) / ratio, ch / ratio).data,
        sprite = [];

    while (--di >= 0) {
      d = data[di];
      if (!d.hasText) continue;
      var w = d.width,
          w32 = w >> 5,
          h = d.y1 - d.y0;
      // Zero the buffer

      // if (!d.isImage) {
        for (var i = 0; i < h * w32; i++) sprite[i] = 0;
        x = d.xoff;
        if (x == null) return;
        y = d.yoff;
        var seen = 0,
            seenRow = -1;
        for (var j = 0; j < h; j++) {
          for (var i = 0; i < w; i++) {
            var k = w32 * j + (i >> 5),
                m = pixels[((y + j) * (cw << 5) + (x + i)) << 2] ? 1 << (31 - (i % 32)) : 0;
            sprite[k] |= m;
            seen |= m;
          }
          if (seen) seenRow = j;
          else {
            d.y0++;
            h--;
            j--;
            y++;
            if (d.isImage) {
              d.x0++;
            }
          }
        }
        d.y1 = d.y0 + seenRow;
        if (d.isImage) {
          d.x1 = d.x0 + seenRow;
        }
        // if (d.isImage) {
          d.sprite = sprite.slice(0, (d.y1 - d.y0) * w32);
        // } else {
        //   d.sprite = sprite.slice(0, (d.y1 - d.y0) * w32/2);
        // }
      // } else {
      //   for (var i = 0; i < w32*w32/4; i += 1) {
      //     sprite[i] = -122;
      //   }
      //   d.sprite = sprite;
      // }
    }
  }

  // Use mask-based collision detection.
  function cloudCollide(tag, board, sw) {
    sw >>= 5;
    var sprite = tag.sprite,
        w = tag.width >> 5,
        lx = tag.x - (w << 4),
        sx = lx & 0x7f,
        msx = 32 - sx,
        h =  tag.y1 - tag.y0,
        x = (tag.y + tag.y0) * sw + (lx >> 5),
        last;
    for (var j = 0; j < h; j++) {
      last = 0;
      for (var i = 0; i <= w; i++) {
        if (((last << msx) | (i < w ? (last = sprite[j * w + i]) >>> sx : 0))
            & board[x + i]) return true;
      }
      x += sw;
    }
    return false;
  }

  function cloudBounds(bounds, d) {
    var b0 = bounds[0],
        b1 = bounds[1];
    if (d.x + d.x0 < b0.x) b0.x = d.x + d.x0;
    if (d.y + d.y0 < b0.y) b0.y = d.y + d.y0;
    if (d.x + d.x1 > b1.x) b1.x = d.x + d.x1;
    if (d.y + d.y1 > b1.y) b1.y = d.y + d.y1;
  }

  function collideRects(a, b) {
    return a.x + a.x1 > b[0].x && a.x + a.x0 < b[1].x && a.y + a.y1 > b[0].y && a.y + a.y0 < b[1].y;
  }

  function archimedeanSpiral(size) {
    var e = size[0] / size[1];
    return function(t) {
      return [e * (t *= .1) * Math.cos(t), t * Math.sin(t)];
    };
  }

  function rectangularSpiral(size) {
    var dy = 4,
        dx = dy * size[0] / size[1],
        x = 0,
        y = 0;
    return function(t) {
      var sign = t < 0 ? -1 : 1;
      // See triangular numbers: T_n = n * (n + 1) / 2.
      switch ((Math.sqrt(1 + 4 * sign * t) - sign) & 3) {
        case 0:  x += dx; break;
        case 1:  y += dy; break;
        case 2:  x -= dx; break;
        default: y -= dy; break;
      }
      return [x, y];
    };
  }

  // TODO reuse arrays?
  function zeroArray(n) {
    var a = [],
        i = -1;
    while (++i < n) a[i] = 0;
    return a;
  }

  var cloudRadians = Math.PI / 180,
      cw = 1 << 11 >> 5,
      ch = 1 << 11,
      canvas,
      ratio = 1;

  if (typeof document !== "undefined") {
    canvas = document.createElement("canvas");
    canvas.width = 1;
    canvas.height = 1;
    ratio = Math.sqrt(canvas.getContext("2d").getImageData(0, 0, 1, 1).data.length >> 2);
    canvas.width = (cw << 5) / ratio;
    canvas.height = ch / ratio;
  } else {
    // Attempt to use node-canvas.
    canvas = new Canvas(cw << 5, ch);
  }

  var c = canvas.getContext("2d"),
      spirals = {
        archimedean: archimedeanSpiral,
        rectangular: rectangularSpiral
      };
  c.fillStyle = c.strokeStyle = "red";
  c.textAlign = "center";

  if (typeof module === "object" && module.exports) module.exports = cloud;
  else (d3.layout || (d3.layout = {})).cloud = cloud;
})();


