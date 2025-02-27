!/**
 * Highcharts JS v12.1.2 (2025-01-09)
 * @module highcharts/modules/marker-clusters
 * @requires highcharts
 *
 * Marker clusters module for Highcharts
 *
 * (c) 2010-2024 Wojciech Chmiel
 *
 * License: www.highcharts.com/license
 */function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e(t._Highcharts):"function"==typeof define&&define.amd?define("highcharts/modules/marker-clusters",["highcharts/highcharts"],function(t){return e(t)}):"object"==typeof exports?exports["highcharts/modules/marker-clusters"]=e(t._Highcharts):t.Highcharts=e(t.Highcharts)}("undefined"==typeof window?this:window,t=>(()=>{"use strict";let e;var i={944:e=>{e.exports=t}},s={};function o(t){var e=s[t];if(void 0!==e)return e.exports;var a=s[t]={exports:{}};return i[t](a,a.exports,o),a.exports}o.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return o.d(e,{a:e}),e},o.d=(t,e)=>{for(var i in e)o.o(e,i)&&!o.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},o.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e);var a={};o.d(a,{default:()=>tx});var r=o(944),n=o.n(r);let l={cluster:{enabled:!1,allowOverlap:!0,animation:{duration:500},drillToCluster:!0,minimumClusterSize:2,layoutAlgorithm:{gridSize:50,distance:40,kmeansThreshold:100},marker:{symbol:"cluster",radius:15,lineWidth:0,lineColor:"#ffffff"},dataLabels:{enabled:!0,format:"{point.clusterPointsAmount}",verticalAlign:"middle",align:"center",style:{color:"contrast"},inside:!0}},tooltip:{clusterFormat:"<span>Clustered points: {point.clusterPointsAmount}</span><br/>"}},{fireEvent:p,isArray:h,objectEach:u,uniqueKey:d}=n(),c=class{constructor(t={}){this.autoId=!t.id,this.columns={},this.id=t.id||d(),this.modified=this,this.rowCount=0,this.versionTag=d();let e=0;u(t.columns||{},(t,i)=>{this.columns[i]=t.slice(),e=Math.max(e,t.length)}),this.applyRowCount(e)}applyRowCount(t){this.rowCount=t,u(this.columns,e=>{h(e)&&(e.length=t)})}getColumn(t,e){return this.columns[t]}getColumns(t,e){return(t||Object.keys(this.columns)).reduce((t,e)=>(t[e]=this.columns[e],t),{})}getRow(t,e){return(e||Object.keys(this.columns)).map(e=>this.columns[e]?.[t])}setColumn(t,e=[],i=0,s){this.setColumns({[t]:e},i,s)}setColumns(t,e,i){let s=this.rowCount;u(t,(t,e)=>{this.columns[e]=t.slice(),s=t.length}),this.applyRowCount(s),i?.silent||(p(this,"afterSetColumns"),this.versionTag=d())}setRow(t,e=this.rowCount,i,s){let{columns:o}=this,a=i?this.rowCount+1:e+1;u(t,(t,r)=>{let n=o[r]||s?.addColumns!==!1&&Array(a);n&&(i?n.splice(e,0,t):n[e]=t,o[r]=n)}),a>this.rowCount&&this.applyRowCount(a),s?.silent||(p(this,"afterSetRows"),this.versionTag=d())}},{animObject:m}=n(),{cluster:f}=l,{addEvent:g,defined:x,error:y,isArray:C,isFunction:k,isObject:I,isNumber:M,merge:b,objectEach:S,relativeLength:w,syncTimeout:A}=n(),X={grid:function(t,e,i,s){let o,a,r,n,l;let p={},h=this.getGridOffset(),u=this.getScaledGridSize(s);for(l=0;l<t.length;l++){let s=Q(this,{x:t[l],y:e[l]});o=s.x-h.plotLeft,a=s.y-h.plotTop,r=Math.floor(o/u),p[n=Math.floor(a/u)+":"+r]??(p[n]=[]),p[n].push({dataIndex:i[l],x:t[l],y:e[l]})}return p},kmeans:function(t,e,i,s){let o=[],a=[],r={},n=s.processedDistance||f.layoutAlgorithm.distance,l=s.iterations,p=0,h=!0,u=0,d=0,c,m=[];s.processedGridSize=s.processedDistance;let g=this.markerClusterAlgorithms?this.markerClusterAlgorithms.grid.call(this,t,e,i,s):{};for(let t in g)g[t].length>1&&(c=T(g[t]),o.push({posX:c.x,posY:c.y,oldX:0,oldY:0,startPointsLen:g[t].length,points:[]}));for(;h;){for(let t of o)t.points.length=0;a.length=0;for(let s=0;s<t.length;s++)u=t[s],d=e[s],(m=this.getClusterDistancesFromPoint(o,u,d)).length&&m[0].distance<n?o[m[0].clusterIndex].points.push({x:u,y:d,dataIndex:i[s]}):a.push({x:u,y:d,dataIndex:i[s]});for(let t=0;t<o.length;t++)1===o[t].points.length&&(m=this.getClusterDistancesFromPoint(o,o[t].points[0].x,o[t].points[0].y))[1].distance<n&&(o[m[1].clusterIndex].points.push(o[t].points[0]),o[m[0].clusterIndex].points.length=0);h=!1;for(let t=0;t<o.length;t++)c=T(o[t].points),o[t].oldX=o[t].posX,o[t].oldY=o[t].posY,o[t].posX=c.x,o[t].posY=c.y,(o[t].posX>o[t].oldX+1||o[t].posX<o[t].oldX-1||o[t].posY>o[t].oldY+1||o[t].posY<o[t].oldY-1)&&(h=!0);l&&(h=p<l-1),p++}for(let t=0,e=o.length;t<e;++t)r["cluster"+t]=o[t].points;for(let t=0,e=a.length;t<e;++t)r["noise"+t]=[a[t]];return r},optimizedKmeans:function(t,e,i,s){let o=s.processedDistance||f.layoutAlgorithm.gridSize,a=this.getRealExtremes(),r=(this.options.cluster||{}).marker,n,l={},p,h;if(!this.markerClusterInfo||this.initMaxX&&this.initMaxX<a.maxX||this.initMinX&&this.initMinX>a.minX||this.initMaxY&&this.initMaxY<a.maxY||this.initMinY&&this.initMinY>a.minY)this.initMaxX=a.maxX,this.initMinX=a.minX,this.initMaxY=a.maxY,this.initMinY=a.minY,l=this.markerClusterAlgorithms?this.markerClusterAlgorithms.kmeans.call(this,t,e,i,s):{},this.baseClusters=null;else{for(let t of(this.baseClusters??(this.baseClusters={clusters:this.markerClusterInfo.clusters,noise:this.markerClusterInfo.noise}),this.baseClusters.clusters)){for(let e of(t.pointsOutside=[],t.pointsInside=[],t.data)){let i=Q(this,e),s=Q(this,t);n=Math.sqrt(Math.pow(i.x-s.x,2)+Math.pow(i.y-s.y,2)),p=o-(h=t.clusterZone?.marker?.radius?t.clusterZone.marker.radius:r?.radius?r.radius:f.marker.radius)>=0?o-h:h,n>h+p&&x(t.pointsOutside)?t.pointsOutside.push(e):x(t.pointsInside)&&t.pointsInside.push(e)}t.pointsInside.length&&(l[t.id]=t.pointsInside);let e=0;for(let i of t.pointsOutside)l[t.id+"_noise"+e++]=[i]}for(let t of this.baseClusters.noise)l[t.id]=t.data}return l}},Y,P=[],L=0;function z(t,e,i){t.attr({opacity:e}).animate({opacity:1},i)}function D(t,e,i,s){for(let o of(O(t,s,i,!0,!0),e))o.point?.destroy?.()}function O(t,e,i,s,o){t.point&&(s&&t.point.graphic&&(t.point.graphic.show(),z(t.point.graphic,e,i)),o&&t.point.dataLabel&&(t.point.dataLabel.show(),z(t.point.dataLabel,e,i)))}function T(t){let e=t.length,i=0,s=0;for(let o=0;o<e;o++)i+=t[o].x,s+=t[o].y;return{x:i/e,y:s/e}}function v(t,e){let i=[];return i.length=e,t.clusters.forEach(function(t){t.data.forEach(function(t){i[t.dataIndex]=t})}),t.noise.forEach(function(t){i[t.data[0].dataIndex]=t.data[0]}),i}function V(){return Math.random().toString(36).substring(2,7)+"-"+L++}function R(t,e,i){t.point&&(e&&t.point.graphic&&t.point.graphic.hide(),i&&t.point.dataLabel&&t.point.dataLabel.hide())}function E(t){(t.point||t.target).firePointEvent("drillToCluster",t,function(t){let e=t.point||t.target,i=e.series,{xAxis:s,yAxis:o,chart:a}=i,{inverted:r,mapView:n,pointer:l}=a;if(i.options.cluster?.drillToCluster&&e.clusteredData){let t=e.clusteredData.map(t=>t.x).sort((t,e)=>t-e),i=e.clusteredData.map(t=>t.y).sort((t,e)=>t-e),p=t[0],h=t[t.length-1],u=i[0],d=i[i.length-1],c=Math.abs((h-p)*.1),m=Math.abs((d-u)*.1),f=Math.min(p,h)-c,g=Math.max(p,h)+c,x=Math.min(u,d)-m,y=Math.max(u,d)+m;if(n)n.fitToBounds({x1:f,x2:g,y1:x,y2:y});else if(s&&o){let t=s.toPixels(f),e=s.toPixels(g),i=o.toPixels(x),n=o.toPixels(y);r&&([t,e,i,n]=[i,n,t,e]),t>e&&([t,e]=[e,t]),i>n&&([i,n]=[n,i]),l&&(l.zoomX=!0,l.zoomY=!0),a.transform({from:{x:t,y:i,width:e-t,height:n-i}})}}})}function j(t,e){let{chart:i,xAxis:s,yAxis:o}=t;return i.mapView?i.mapView.pixelsToProjectedUnits(e):{x:s?s.toValue(e.x):0,y:o?o.toValue(e.y):0}}function G(t){let e=this.chart,i=e.mapView,s=m(this.options.cluster?.animation),o=s.duration||500,a=this.markerClusterInfo?.pointsState,r=a?.newState,n=a?.oldState,l=[],p,h,u,d=0,c=0,f=0,g=!1,x=!1;if(n&&r){let a=Q(this,h=r[t.stateId]);c=a.x-(i?0:e.plotLeft),f=a.y-(i?0:e.plotTop),1===h.parentsId.length?(p=n[r?.[t.stateId].parentsId[0]],h.point?.graphic&&p.point?.plotX&&p.point.plotY&&(p.point.plotX!==h.point.plotX||p.point.plotY!==h.point.plotY)&&(u=h.point.graphic.getBBox(),d=h.point.graphic?.isImg?0:u.width/2,h.point.graphic.attr({x:p.point.plotX-d,y:p.point.plotY-d}),h.point.graphic.animate({x:c-(h.point.graphic.radius||0),y:f-(h.point.graphic.radius||0)},s,function(){x=!0,p.point?.destroy?.()}),h.point.dataLabel?.alignAttr&&p.point.dataLabel?.alignAttr&&(h.point.dataLabel.attr({x:p.point.dataLabel.alignAttr.x,y:p.point.dataLabel.alignAttr.y}),h.point.dataLabel.animate({x:h.point.dataLabel.alignAttr.x,y:h.point.dataLabel.alignAttr.y},s)))):0===h.parentsId.length?(R(h,!0,!0),A(function(){O(h,.1,s,!0,!0)},o/2)):(R(h,!0,!0),h.parentsId.forEach(function(t){n?.[t]&&(p=n[t],l.push(p),p.point?.graphic&&(g=!0,p.point.graphic.show(),p.point.graphic.animate({x:c-(p.point.graphic.radius||0),y:f-(p.point.graphic.radius||0),opacity:.4},s,function(){x=!0,D(h,l,s,.7)}),p.point.dataLabel&&-9999!==p.point.dataLabel.y&&h.point?.dataLabel?.alignAttr&&(p.point.dataLabel.show(),p.point.dataLabel.animate({x:h.point.dataLabel.alignAttr.x,y:h.point.dataLabel.alignAttr.y,opacity:.4},s))))}),A(function(){x||D(h,l,s,.85)},o),g||A(function(){D(h,l,s,.1)},o/2))}}function F(){this.markerClusterSeriesData?.forEach(t=>{t?.destroy?.()}),this.markerClusterSeriesData=null}function H(){let t,e,i,s,o,a,r,n,l,p,h,u,d,m,y;let C=this,{chart:I}=C,b=I.mapView,S=C.getColumn("x"),A=C.getColumn("y"),X=C.options.cluster,P=C.getRealExtremes(),L=[],z=[],D=[];if(b&&C.is("mappoint")&&S&&A&&C.options.data?.forEach((t,e)=>{let i=C.projectPoint(t);i&&(S[e]=i.x,A[e]=i.y)}),X?.enabled&&S?.length&&A?.length&&!I.polar){h=X.layoutAlgorithm.type,(m=X.layoutAlgorithm).processedGridSize=w(m.gridSize||f.layoutAlgorithm.gridSize,I.plotWidth),m.processedDistance=w(m.distance||f.layoutAlgorithm.distance,I.plotWidth),s=m.kmeansThreshold||f.layoutAlgorithm.kmeansThreshold;let b=m.processedGridSize/2,O=j(C,{x:0,y:0}),T=j(C,{x:b,y:b});o=Math.abs(O.x-T.x),a=Math.abs(O.y-T.y);for(let t=0;t<S.length;t++)!C.dataMaxX&&(x(n)&&x(r)&&x(p)&&x(l)?M(A[t])&&M(p)&&M(l)&&(n=Math.max(S[t],n),r=Math.min(S[t],r),p=Math.max(A[t]||p,p),l=Math.min(A[t]||l,l)):(n=r=S[t],p=l=A[t])),S[t]>=P.minX-o&&S[t]<=P.maxX+o&&(A[t]||P.minY)>=P.minY-a&&(A[t]||P.maxY)<=P.maxY+a&&(L.push(S[t]),z.push(A[t]),D.push(t));x(n)&&x(r)&&M(p)&&M(l)&&(C.dataMaxX=n,C.dataMinX=r,C.dataMaxY=p,C.dataMinY=l),u=(d=(k(h)?h:C.markerClusterAlgorithms?h&&C.markerClusterAlgorithms[h]?C.markerClusterAlgorithms[h]:L.length<s?C.markerClusterAlgorithms.kmeans:C.markerClusterAlgorithms.grid:()=>!1).call(this,L,z,D,m))?C.getClusteredData(d,X):d,X.animation&&C.markerClusterInfo?.pointsState?.oldState?(function(t){for(let e of Object.keys(t))t[e].point?.destroy?.()}(C.markerClusterInfo.pointsState.oldState),t=C.markerClusterInfo.pointsState.newState):t={},e=S.length,i=C.markerClusterInfo,u&&(C.dataTable.modified=new c({columns:{x:u.groupedXData,y:u.groupedYData}}),C.hasGroupedData=!0,C.markerClusterInfo=u,C.groupMap=u.groupMap),Y.apply(this),u&&C.markerClusterInfo&&(C.markerClusterInfo.clusters?.forEach(t=>{(y=C.points[t.index]).isCluster=!0,y.clusteredData=t.data,y.clusterPointsAmount=t.data.length,t.point=y,g(y,"click",E)}),C.markerClusterInfo.noise?.forEach(t=>{t.point=C.points[t.index]}),X.animation&&C.markerClusterInfo&&(C.markerClusterInfo.pointsState={oldState:t,newState:C.getPointsState(u,i,e)}),X.animation?this.hideClusteredData():this.destroyClusteredData(),this.markerClusterSeriesData=this.hasGroupedData?this.points:null)}else Y.apply(this)}function W(t,e,i){let s=[];for(let o=0;o<t.length;o++){let a=Q(this,{x:e,y:i}),r=Q(this,{x:t[o].posX,y:t[o].posY}),n=Math.sqrt(Math.pow(a.x-r.x,2)+Math.pow(a.y-r.y,2));s.push({clusterIndex:o,distance:n})}return s.sort((t,e)=>t.distance-e.distance)}function Z(t,e){let i=this.options.data,s=[],o=[],a=[],r=[],n=[],l=Math.max(2,e.minimumClusterSize||2),p=0,h,u,d,c,m,g,x,M,S,w,A,X;if(k(e.layoutAlgorithm.type)&&!this.isValidGroupedDataObject(t))return y("Highcharts marker-clusters module: The custom algorithm result is not valid!",!1,this.chart),!1;for(let y in t)if(t[y].length>=l){if(d=t[y],h=V(),m=d.length,e.zones)for(let t=0;t<e.zones.length;t++)m>=e.zones[t].from&&m<=e.zones[t].to&&((A=e.zones[t]).zoneIndex=t,w=e.zones[t].marker,X=e.zones[t].className);S=T(d),"grid"!==e.layoutAlgorithm.type||e.allowOverlap?x={x:S.x,y:S.y}:(g=this.options.marker||{},x=this.preventClusterCollisions({x:S.x,y:S.y,key:y,groupedData:t,gridSize:this.getScaledGridSize(e.layoutAlgorithm),defaultRadius:g.radius||3+(g.lineWidth||0),clusterRadius:w&&w.radius?w.radius:(e.marker||{}).radius||f.marker.radius}));for(let t=0;t<m;t++)d[t].parentStateId=h;if(a.push({x:x.x,y:x.y,id:y,stateId:h,index:p,data:d,clusterZone:A,clusterZoneClassName:X}),s.push(x.x),o.push(x.y),n.push({options:{formatPrefix:"cluster",dataLabels:e.dataLabels,marker:b(e.marker,{states:e.states},w||{})}}),i?.length)for(let t=0;t<m;t++)I(i[d[t].dataIndex])&&(d[t].options=i[d[t].dataIndex]);p++,w=null}else for(let e=0;e<t[y].length;e++)u=t[y][e],h=V(),M=null,c=i?.[u.dataIndex],s.push(u.x),o.push(u.y),u.parentStateId=h,r.push({x:u.x,y:u.y,id:y,stateId:h,index:p,data:t[y]}),M=c&&"object"==typeof c&&!C(c)?b(c,{x:u.x,y:u.y}):{userOptions:c,x:u.x,y:u.y},n.push({options:M}),p++;return{clusters:a,noise:r,groupedXData:s,groupedYData:o,groupMap:n}}function _(){let{chart:t,xAxis:e,yAxis:i}=this,s=0;return{plotLeft:e&&this.dataMinX&&this.dataMaxX?e.reversed?e.toPixels(this.dataMaxX):e.toPixels(this.dataMinX):t.plotLeft,plotTop:i&&this.dataMinY&&this.dataMaxY?i.reversed?i.toPixels(this.dataMinY):i.toPixels(this.dataMaxY):t.plotTop}}function B(t,e,i){let s,o;let a=e?v(e,i):[],r=v(t,i),n={};P=[],t.clusters.forEach(t=>{n[t.stateId]={x:t.x,y:t.y,id:t.stateId,point:t.point,parentsId:[]}}),t.noise.forEach(t=>{n[t.stateId]={x:t.x,y:t.y,id:t.stateId,point:t.point,parentsId:[]}});for(let t=0;t<r.length;t++)s=r[t],o=a[t],s?.parentStateId&&o?.parentStateId&&n[s.parentStateId]?.parentsId.indexOf(o.parentStateId)===-1&&(n[s.parentStateId].parentsId.push(o.parentStateId),-1===P.indexOf(o.parentStateId)&&P.push(o.parentStateId));return n}function q(){let t=this.chart,e=t.mapView?0:t.plotLeft,i=j(this,{x:e,y:t.mapView?0:t.plotTop}),s=j(this,{x:e+t.plotWidth,y:e+t.plotHeight}),o=i.x,a=s.x,r=i.y,n=s.y;return{minX:Math.min(o,a),maxX:Math.max(o,a),minY:Math.min(r,n),maxY:Math.max(r,n)}}function N(t){let e=this.xAxis,i=this.chart.mapView,s=t.processedGridSize||f.layoutAlgorithm.gridSize,o=!0,a=1,r=1;this.gridValueSize||(i?this.gridValueSize=s/i.getScale():this.gridValueSize=Math.abs(e.toValue(s)-e.toValue(0)));let n=+(s/(i?this.gridValueSize*i.getScale():e.toPixels(this.gridValueSize)-e.toPixels(0))).toFixed(14);for(;o&&1!==n;){let t=Math.pow(2,a);n>.75&&n<1.25?o=!1:n>=1/t&&n<1/t*2?(o=!1,r=t):n<=t&&n>t/2&&(o=!1,r=1/t),a++}return s/r/n}function U(){let t=this.markerClusterSeriesData,e=this.markerClusterInfo?.pointsState?.oldState,i=P.map(t=>e?.[t].point?.id||"");t?.forEach(t=>{t&&i.indexOf(t.id)!==-1?(t.graphic&&t.graphic.hide(),t.dataLabel&&t.dataLabel.hide()):t?.destroy?.()})}function K(t){let e=!1;return!!I(t)&&(S(t,t=>{if(e=!0,!C(t)||!t.length){e=!1;return}for(let i=0;i<t.length;i++)if(!I(t[i])||!t[i].x||!t[i].y){e=!1;return}}),e)}function J(t){let[e,i]=t.key.split(":").map(parseFloat),s=t.gridSize,o=t.groupedData,a=t.defaultRadius,r=t.clusterRadius,n=i*s,l=e*s,p=Q(this,t),h=[],u=this.options.cluster?.marker,d=this.options.cluster?.zones,c=this.getGridOffset(),m=p.x,g=p.y,y=0,C=0,k,I,M,b,S,w,A,X,Y,P,L,z;m-=c.plotLeft,g-=c.plotTop;for(let o=1;o<5;o++)for(A=0,M=o%2?-1:1,b=o<3?-1:1,S=Math.floor((m+M*r)/s),z=[(w=Math.floor((g+b*r)/s))+":"+S,w+":"+i,e+":"+S];A<z.length;A++)-1===h.indexOf(z[A])&&z[A]!==t.key&&h.push(z[A]);for(let t of h)if(o[t]){o[t].posX||(P=T(o[t]),o[t].posX=P.x,o[t].posY=P.y);let p=Q(this,{x:o[t].posX||0,y:o[t].posY||0});if(k=p.x-c.plotLeft,I=p.y-c.plotTop,[Y,X]=t.split(":").map(parseFloat),d){y=o[t].length;for(let t=0;t<d.length;t++)y>=d[t].from&&y<=d[t].to&&(C=x(d[t].marker?.radius)?d[t].marker.radius||0:u?.radius?u.radius:f.marker.radius)}o[t].length>1&&0===C&&u?.radius?C=u.radius:1===o[t].length&&(C=a),L=r+C,C=0,X!==i&&Math.abs(m-k)<L&&(m=X-i<0?n+r:n+s-r),Y!==e&&Math.abs(g-I)<L&&(g=Y-e<0?l+r:l+s-r)}let D=j(this,{x:m+c.plotLeft,y:g+c.plotTop});return o[t.key].posX=D.x,o[t.key].posY=D.y,D}function Q(t,e){let{chart:i,xAxis:s,yAxis:o}=t;return i.mapView?i.mapView.projectedUnitsToPixels(e):{x:s?s.toPixels(e.x):0,y:o?o.toPixels(e.y):0}}let $={compose:function(t,e){let i=e.prototype;!i.markerClusterAlgorithms&&(Y=i.generatePoints,i.markerClusterAlgorithms=X,i.animateClusterPoint=G,i.destroyClusteredData=F,i.generatePoints=H,i.getClusterDistancesFromPoint=W,i.getClusteredData=Z,i.getGridOffset=_,i.getPointsState=B,i.getRealExtremes=q,i.getScaledGridSize=N,i.hideClusteredData=U,i.isValidGroupedDataObject=K,i.preventClusterCollisions=J,g(e,"destroy",i.destroyClusteredData),t.plotOptions&&(t.plotOptions.series=b(t.plotOptions.series,l)))}},{animObject:tt}=n(),{defaultOptions:te}=n(),{composed:ti}=n(),{addEvent:ts,defined:to,error:ta,isFunction:tr,merge:tn,pushUnique:tl,syncTimeout:tp}=n();function th(){let t=this.chart,e=0;for(let i of t.series)i.markerClusterInfo&&(e=tt((i.options.cluster||{}).animation).duration||0);tp(()=>{t.tooltip&&t.tooltip.destroy()},e)}function tu(){for(let t of this.series||[])if(t.markerClusterInfo){let e=t.options.cluster,i=((t.markerClusterInfo||{}).pointsState||{}).oldState;if((e||{}).animation&&t.markerClusterInfo&&0===(t.chart.pointer?.pinchDown||[]).length&&"pan"!==((t.xAxis||{}).eventArgs||{}).trigger&&i&&Object.keys(i).length){for(let e of t.markerClusterInfo.clusters)t.animateClusterPoint(e);for(let e of t.markerClusterInfo.noise)t.animateClusterPoint(e)}}}function td(t){let e=(((t.point||t.target).series.options.cluster||{}).events||{}).drillToCluster;tr(e)&&e.call(this,t)}function tc(){if(this.dataGroup)return ta("Highcharts marker-clusters module: Running `Point.update` when point belongs to clustered series is not supported.",!1,this.series.chart),!1}function tm(){let t=(this.options.cluster||{}).drillToCluster;if(this.markerClusterInfo&&this.markerClusterInfo.clusters)for(let e of this.markerClusterInfo.clusters)e.point&&e.point.graphic&&(e.point.graphic.addClass("highcharts-cluster-point"),t&&e.point&&(e.point.graphic.css({cursor:"pointer"}),e.point.dataLabel&&e.point.dataLabel.css({cursor:"pointer"})),to(e.clusterZone)&&e.point.graphic.addClass(e.clusterZoneClassName||"highcharts-cluster-zone-"+e.clusterZone.zoneIndex))}function tf(t,i,s,o){let a=s/2,r=o/2,n=e.arc(t+a,i+r,a-4,r-4,{start:.5*Math.PI,end:2.5*Math.PI,open:!1}),l=e.arc(t+a,i+r,a-3,r-3,{start:.5*Math.PI,end:2.5*Math.PI,innerR:a-2,open:!1});return e.arc(t+a,i+r,a-1,r-1,{start:.5*Math.PI,end:2.5*Math.PI,innerR:a,open:!1}).concat(l,n)}(te.plotOptions||{}).series=tn((te.plotOptions||{}).series,l);let tg=n();({compose:function(t,e,i,s){if(tl(ti,"MarkerClusters")){let o=s.prototype.pointClass,{scatter:a}=s.types;ts(t,"setExtremes",th),ts(e,"render",tu),ts(o,"drillToCluster",td),ts(o,"update",tc),ts(s,"afterRender",tm),a&&$.compose(i,a)}}}).compose(tg.Axis,tg.Chart,tg.defaultOptions,tg.Series),({compose:function(t){(e=t.prototype.symbols).cluster=tf}}).compose(tg.SVGRenderer);let tx=n();return a.default})());