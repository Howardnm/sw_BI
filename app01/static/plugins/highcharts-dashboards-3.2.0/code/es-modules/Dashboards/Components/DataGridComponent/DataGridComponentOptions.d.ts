import type { GridOptions } from '../../Plugins/DataGridTypes';
import type Component from '../Component';
import type Sync from '../Sync/Sync';
/**
 * Options to control the DataGrid component.
 */
export interface Options extends Component.Options {
    /**
     * Connector options
     */
    connector?: Component.ConnectorOptions;
    /**
     * The style class to add to the rendered data grid container. This option
     * is now deprecated, and moved to [gridClassName](#gridClassName).
     *
     * @deprecated
     */
    dataGridClassName?: string;
    /**
     * The style class to add to the rendered data grid container.
     *
     */
    gridClassName?: string;
    /**
     * The identifier for the rendered data grid container. This option is now
     * deprecated, and moved to [gridID](#gridID).
     *
     * @deprecated
     */
    dataGridID?: string;
    /**
     * The identifier for the rendered data grid container.
     */
    gridID?: string;
    /**
     * Callback to use when a change in the data grid occurs.
     *
     * @private
     *
     * @param e
     * Related keyboard event of the change.
     *
     * @param connector
     * Relate store of the change.
     */
    onUpdate(e: KeyboardEvent, connector: Component.ConnectorTypes): void;
    type: 'DataGrid' | 'Grid';
    /**
     * Generic options to adjust behavior and styling of the rendered data
     * grid.
     */
    gridOptions?: GridOptions;
    /**
     * Generic options to adjust behavior and styling of the rendered data
     * grid. This option is now deprecated, and moved to
     * [gridOptions](#gridOptions).
     *
     * @deprecated
     */
    dataGridOptions?: GridOptions;
    /** @private */
    tableAxisMap?: Record<string, string | null>;
    /**
     * Defines which elements should be synced.
     * ```
     * Example:
     * {
     *     highlight: true
     * }
     * ```
     * Try it:
     *
     * {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/dashboards/demo/sync-extremes/ | Extremes Sync }
     *
     * {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/dashboards/component-options/sync-highlight/ | Highlight Sync }
     *
     * {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/dashboards/component-options/sync-visibility/ | Visibility Sync }
     *
     */
    sync?: SyncOptions;
    /**
     * Sync options for the component.
     */
    syncHandlers?: Sync.OptionsRecord;
}
/**
 * Sync options available for the DataGrid component.
 *
 * Example:
 * ```
 * {
 *     highlight: true
 * }
 * ```
 */
export interface SyncOptions extends Sync.RawOptionsRecord {
    /**
     * Extremes sync is available for Highcharts, KPI, DataGrid and
     * Navigator components. Sets a common range of displayed data. For the
     * KPI Component sets the last value.
     *
     * Try it:
     *
     * {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/dashboards/demo/sync-extremes/ | Extremes Sync }
     *
     * @default false
     */
    extremes?: boolean | Sync.OptionsEntry;
    /**
     * Highlight sync is available for Highcharts and DataGrid components.
     * It allows to highlight hovered corresponding rows in the table and
     * chart points.
     *
     * Try it:
     *
     * {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/dashboards/component-options/sync-highlight/ | Highlight Sync }
     *
     * @default false
     */
    highlight?: boolean | Sync.OptionsEntry;
    /**
     * Visibility sync is available for Highcharts and DataGrid components.
     * Synchronizes the visibility of data from a hidden/shown series.
     *
     * Try it:
     *
     * {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/dashboards/component-options/sync-visibility/ | Visibility Sync }
     *
     * @default false
     */
    visibility?: boolean | Sync.OptionsEntry;
}
/**
 * Datagrid component highlight sync options.
 *
 * Example:
 * ```
 * {
 *     enabled: true,
 *     autoScroll: true
 * }
 * ```
 */
export interface DataGridHighlightSyncOptions extends Sync.OptionsEntry {
    /**
     * Whether to scroll the data grid to the highlighted row automatically.
     *
     * @default false
     */
    autoScroll?: boolean;
}
export default Options;
