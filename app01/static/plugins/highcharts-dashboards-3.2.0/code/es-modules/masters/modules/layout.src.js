/**
 * @license Highcharts Dashboards Layout 3.2.0 (2025-03-26)
 * @module dashboards/modules/layout
 * @requires dashboards
 *
 * (c) 2009-2024 Highsoft AS
 *
 * License: www.highcharts.com/license
 */
'use strict';
/* *
 *
 *  Imports
 *
 * */
import Globals from '../../Dashboards/Globals.js';
// Fill registries
import '../../Dashboards/EditMode/EditMode.js';
import '../../Dashboards/EditMode/Fullscreen.js';
import EditMode from '../../Dashboards/EditMode/EditMode.js';
import Fullscreen from '../../Dashboards/EditMode/Fullscreen.js';
/* *
 *
 *  Namespace
 *
 * */
const G = Globals;
G.EditMode = EditMode;
G.Fullscreen = Fullscreen;
/* *
 *
 *  Default Export
 *
 * */
export default G;
