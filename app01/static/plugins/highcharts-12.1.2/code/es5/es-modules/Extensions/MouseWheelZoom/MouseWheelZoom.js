/* *
 *
 *  (c) 2023 Torstein Honsi, Askel Eirik Johansson
 *
 *  License: www.highcharts.com/license
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 * */
'use strict';
import U from '../../Core/Utilities.js';
var addEvent = U.addEvent, isObject = U.isObject, pick = U.pick, defined = U.defined, merge = U.merge;
import NBU from '../Annotations/NavigationBindingsUtilities.js';
var getAssignedAxis = NBU.getAssignedAxis;
/* *
 *
 *  Constants
 *
 * */
var composedClasses = [], defaultOptions = {
    enabled: true,
    sensitivity: 1.1
};
var wheelTimer;
/* *
 *
 *  Functions
 *
 * */
/**
 * @private
 */
var optionsToObject = function (options) {
    if (!isObject(options)) {
        options = {
            enabled: options !== null && options !== void 0 ? options : true
        };
    }
    return merge(defaultOptions, options);
};
/**
 * @private
 */
var zoomBy = function (chart, howMuch, xAxis, yAxis, mouseX, mouseY, options) {
    var type = pick(options.type, chart.zooming.type, '');
    var axes = [];
    if (type === 'x') {
        axes = xAxis;
    }
    else if (type === 'y') {
        axes = yAxis;
    }
    else if (type === 'xy') {
        axes = chart.axes;
    }
    var hasZoomed = chart.transform({
        axes: axes,
        // Create imaginary reference and target rectangles around the mouse
        // point that scales up or down with `howMuch`;
        to: {
            x: mouseX - 5,
            y: mouseY - 5,
            // Must use 10 to get passed the limit for too small reference.
            // Below this, the transform will default to a pan.
            width: 10,
            height: 10
        },
        from: {
            x: mouseX - 5 * howMuch,
            y: mouseY - 5 * howMuch,
            width: 10 * howMuch,
            height: 10 * howMuch
        },
        trigger: 'mousewheel'
    });
    if (hasZoomed) {
        if (defined(wheelTimer)) {
            clearTimeout(wheelTimer);
        }
        // Some time after the last mousewheel event, run drop. In case any of
        // the affected axes had `startOnTick` or `endOnTick`, they will be
        // re-adjusted now.
        wheelTimer = setTimeout(function () {
            var _a;
            (_a = chart.pointer) === null || _a === void 0 ? void 0 : _a.drop();
        }, 400);
    }
    return hasZoomed;
};
/**
 * @private
 */
function onAfterGetContainer() {
    var _this = this;
    var wheelZoomOptions = optionsToObject(this.zooming.mouseWheel);
    if (wheelZoomOptions.enabled) {
        addEvent(this.container, 'wheel', function (e) {
            var _a, _b;
            e = ((_a = _this.pointer) === null || _a === void 0 ? void 0 : _a.normalize(e)) || e;
            var pointer = _this.pointer, allowZoom = pointer && !pointer.inClass(e.target, 'highcharts-no-mousewheel');
            // Firefox uses e.detail, WebKit and IE uses deltaX, deltaY, deltaZ.
            if (_this.isInsidePlot(e.chartX - _this.plotLeft, e.chartY - _this.plotTop) && allowZoom) {
                var wheelSensitivity = wheelZoomOptions.sensitivity || 1.1, delta = e.detail || ((e.deltaY || 0) / 120), xAxisCoords = getAssignedAxis(pointer.getCoordinates(e).xAxis), yAxisCoords = getAssignedAxis(pointer.getCoordinates(e).yAxis);
                var hasZoomed = zoomBy(_this, Math.pow(wheelSensitivity, delta), xAxisCoords ? [xAxisCoords.axis] : _this.xAxis, yAxisCoords ? [yAxisCoords.axis] : _this.yAxis, e.chartX, e.chartY, wheelZoomOptions);
                // Prevent page scroll
                if (hasZoomed) {
                    (_b = e.preventDefault) === null || _b === void 0 ? void 0 : _b.call(e);
                }
            }
        });
    }
}
/**
 * @private
 */
function compose(ChartClass) {
    if (composedClasses.indexOf(ChartClass) === -1) {
        composedClasses.push(ChartClass);
        addEvent(ChartClass, 'afterGetContainer', onAfterGetContainer);
    }
}
/* *
 *
 *  Default Export
 *
 * */
var MouseWheelZoomComposition = {
    compose: compose
};
export default MouseWheelZoomComposition;
/* *
 *
 *  API Options
 *
 * */
/**
 * The mouse wheel zoom is a feature included in Highcharts Stock, but is also
 * available for Highcharts Core as a module. Zooming with the mouse wheel is
 * enabled by default in Highcharts Stock. In Highcharts Core it is enabled if
 * [chart.zooming.type](chart.zooming.type) is set. It can be disabled by
 * setting this option to `false`.
 *
 * @type      {boolean|object}
 * @since 11.1.0
 * @requires  modules/mouse-wheel-zoom
 * @sample    {highcharts} highcharts/mouse-wheel-zoom/enabled
 *            Enable or disable
 * @sample    {highstock} stock/mouse-wheel-zoom/enabled
 *            Enable or disable
 * @apioption chart.zooming.mouseWheel
 */
/**
 * Zooming with the mouse wheel can be disabled by setting this option to
 * `false`.
 *
 * @type      {boolean}
 * @default   true
 * @since 11.1.0
 * @requires  modules/mouse-wheel-zoom
 * @apioption chart.zooming.mouseWheel.enabled
 */
/**
 * Adjust the sensitivity of the zoom. Sensitivity of mouse wheel or trackpad
 * scrolling. `1` is no sensitivity, while with `2`, one mouse wheel delta will
 * zoom in `50%`.
 *
 * @type      {number}
 * @default   1.1
 * @since 11.1.0
 * @requires  modules/mouse-wheel-zoom
 * @sample    {highcharts} highcharts/mouse-wheel-zoom/sensitivity
 *            Change mouse wheel zoom sensitivity
 * @sample    {highstock} stock/mouse-wheel-zoom/sensitivity
 *            Change mouse wheel zoom sensitivity
 * @apioption chart.zooming.mouseWheel.sensitivity
 */
/**
 * Decides in what dimensions the user can zoom scrolling the wheel. Can be one
 * of `x`, `y` or `xy`. In Highcharts Core, if not specified here, it will
 * inherit the type from [chart.zooming.type](chart.zooming.type). In Highcharts
 * Stock, it defaults to `x`.
 *
 * Note that particularly with mouse wheel in the y direction, the zoom is
 * affected by the default [yAxis.startOnTick](#yAxis.startOnTick) and
 * [endOnTick]((#yAxis.endOnTick)) settings. In order to respect these settings,
 * the zoom level will adjust after the user has stopped zooming. To prevent
 * this, consider setting `startOnTick` and `endOnTick` to `false`.
 *
 * @type      {string}
 * @default   {highcharts} undefined
 * @default   {highstock} x
 * @validvalue ["x", "y", "xy"]
 * @since 11.1.0
 * @requires  modules/mouse-wheel-zoom
 * @apioption chart.zooming.mouseWheel.type
 */
(''); // Keeps doclets above in JS file
