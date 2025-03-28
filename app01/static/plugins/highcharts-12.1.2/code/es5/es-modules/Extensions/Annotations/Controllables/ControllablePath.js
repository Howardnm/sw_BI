/* *
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 * */
'use strict';
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
import Controllable from './Controllable.js';
import ControllableDefaults from './ControllableDefaults.js';
var defaultMarkers = ControllableDefaults.defaultMarkers;
import H from '../../../Core/Globals.js';
import U from '../../../Core/Utilities.js';
var addEvent = U.addEvent, defined = U.defined, extend = U.extend, merge = U.merge, uniqueKey = U.uniqueKey;
/* *
 *
 *  Constants
 *
 * */
var markerEndSetter = createMarkerSetter('marker-end');
var markerStartSetter = createMarkerSetter('marker-start');
// See TRACKER_FILL in highcharts.src.js
var TRACKER_FILL = 'rgba(192,192,192,' + (H.svg ? 0.0001 : 0.002) + ')';
/* *
 *
 *  Functions
 *
 * */
/**
 * @private
 */
function createMarkerSetter(markerType) {
    return function (value) {
        this.attr(markerType, 'url(#' + value + ')');
    };
}
/**
 * @private
 */
function onChartAfterGetContainer() {
    this.options.defs = merge(defaultMarkers, this.options.defs || {});
    ///  objectEach(this.options.defs, function (def): void {
    //     const attributes = def.attributes;
    //     if (
    //         def.tagName === 'marker' &&
    //         attributes &&
    //         attributes.id &&
    //         attributes.display !== 'none'
    //     ) {
    //         this.renderer.addMarker(attributes.id, def);
    //     }
    // }, this);
}
/**
 * @private
 */
function svgRendererAddMarker(id, markerOptions) {
    var options = { attributes: { id: id } };
    var attrs = {
        stroke: markerOptions.color || 'none',
        fill: markerOptions.color || 'rgba(0, 0, 0, 0.75)'
    };
    options.children = (markerOptions.children &&
        markerOptions.children.map(function (child) {
            return merge(attrs, child);
        }));
    var ast = merge(true, {
        attributes: {
            markerWidth: 20,
            markerHeight: 20,
            refX: 0,
            refY: 0,
            orient: 'auto'
        }
    }, markerOptions, options);
    var marker = this.definition(ast);
    marker.id = id;
    return marker;
}
/* *
 *
 *  Class
 *
 * */
/**
 * A controllable path class.
 *
 * @requires modules/annotations
 *
 * @private
 * @class
 * @name Highcharts.AnnotationControllablePath
 *
 * @param {Highcharts.Annotation}
 * Related annotation.
 *
 * @param {Highcharts.AnnotationsShapeOptions} options
 * A path's options object.
 *
 * @param {number} index
 * Index of the path.
 */
var ControllablePath = /** @class */ (function (_super) {
    __extends(ControllablePath, _super);
    /* *
     *
     *  Constructors
     *
     * */
    function ControllablePath(annotation, options, index) {
        var _this = _super.call(this, annotation, options, index, 'shape') || this;
        /* *
         *
         *  Properties
         *
         * */
        _this.type = 'path';
        return _this;
    }
    /* *
     *
     *  Static Functions
     *
     * */
    ControllablePath.compose = function (ChartClass, SVGRendererClass) {
        var svgRendererProto = SVGRendererClass.prototype;
        if (!svgRendererProto.addMarker) {
            addEvent(ChartClass, 'afterGetContainer', onChartAfterGetContainer);
            svgRendererProto.addMarker = svgRendererAddMarker;
        }
    };
    /* *
     *
     *  Functions
     *
     * */
    /**
     * Map the controllable path to 'd' path attribute.
     *
     * @return {Highcharts.SVGPathArray|null}
     * A path's d attribute.
     */
    ControllablePath.prototype.toD = function () {
        var dOption = this.options.d;
        if (dOption) {
            return typeof dOption === 'function' ?
                dOption.call(this) :
                dOption;
        }
        var points = this.points, len = points.length, d = [];
        var showPath = len, point = points[0], position = showPath && this.anchor(point).absolutePosition, pointIndex = 0, command;
        if (position) {
            d.push(['M', position.x, position.y]);
            while (++pointIndex < len && showPath) {
                point = points[pointIndex];
                command = point.command || 'L';
                position = this.anchor(point).absolutePosition;
                if (command === 'M') {
                    d.push([command, position.x, position.y]);
                }
                else if (command === 'L') {
                    d.push([command, position.x, position.y]);
                }
                else if (command === 'Z') {
                    d.push([command]);
                }
                showPath = point.series.visible;
            }
        }
        return (showPath && this.graphic ?
            this.chart.renderer.crispLine(d, this.graphic.strokeWidth()) :
            null);
    };
    ControllablePath.prototype.shouldBeDrawn = function () {
        return _super.prototype.shouldBeDrawn.call(this) || !!this.options.d;
    };
    ControllablePath.prototype.render = function (parent) {
        var options = this.options, attrs = this.attrsFromOptions(options);
        this.graphic = this.annotation.chart.renderer
            .path([['M', 0, 0]])
            .attr(attrs)
            .add(parent);
        this.tracker = this.annotation.chart.renderer
            .path([['M', 0, 0]])
            .addClass('highcharts-tracker-line')
            .attr({
            zIndex: 2
        })
            .add(parent);
        if (!this.annotation.chart.styledMode) {
            this.tracker.attr({
                'stroke-linejoin': 'round', // #1225
                stroke: TRACKER_FILL,
                fill: TRACKER_FILL,
                'stroke-width': this.graphic.strokeWidth() +
                    options.snap * 2
            });
        }
        _super.prototype.render.call(this);
        extend(this.graphic, { markerStartSetter: markerStartSetter, markerEndSetter: markerEndSetter });
        this.setMarkers(this);
    };
    ControllablePath.prototype.redraw = function (animation) {
        if (this.graphic) {
            var d = this.toD(), action = animation ? 'animate' : 'attr';
            if (d) {
                this.graphic[action]({ d: d });
                this.tracker[action]({ d: d });
            }
            else {
                this.graphic.attr({ d: 'M 0 ' + -9e9 });
                this.tracker.attr({ d: 'M 0 ' + -9e9 });
            }
            this.graphic.placed = this.tracker.placed = !!d;
        }
        _super.prototype.redraw.call(this, animation);
    };
    /**
     * Set markers.
     * @private
     * @param {Highcharts.AnnotationControllablePath} item
     */
    ControllablePath.prototype.setMarkers = function (item) {
        var itemOptions = item.options, chart = item.chart, defs = chart.options.defs, fill = itemOptions.fill, color = defined(fill) && fill !== 'none' ?
            fill :
            itemOptions.stroke;
        var setMarker = function (markerType) {
            var markerId = itemOptions[markerType];
            var def, predefinedMarker, key, marker;
            if (markerId) {
                for (key in defs) { // eslint-disable-line guard-for-in
                    def = defs[key];
                    if ((markerId === (def.attributes && def.attributes.id) ||
                        // Legacy, for
                        // unit-tests/annotations/annotations-shapes
                        markerId === def.id) &&
                        def.tagName === 'marker') {
                        predefinedMarker = def;
                        break;
                    }
                }
                if (predefinedMarker) {
                    marker = item[markerType] = chart.renderer
                        .addMarker((itemOptions.id || uniqueKey()) + '-' + markerId, merge(predefinedMarker, { color: color }));
                    item.attr(markerType, marker.getAttribute('id'));
                }
            }
        };
        ['markerStart', 'markerEnd']
            .forEach(setMarker);
    };
    /* *
     *
     *  Static Properties
     *
     * */
    /**
     * A map object which allows to map options attributes to element attributes
     *
     * @name Highcharts.AnnotationControllablePath.attrsMap
     * @type {Highcharts.Dictionary<string>}
     */
    ControllablePath.attrsMap = {
        dashStyle: 'dashstyle',
        strokeWidth: 'stroke-width',
        stroke: 'stroke',
        fill: 'fill',
        zIndex: 'zIndex'
    };
    return ControllablePath;
}(Controllable));
/* *
 *
 *  Default Export
 *
 * */
export default ControllablePath;
