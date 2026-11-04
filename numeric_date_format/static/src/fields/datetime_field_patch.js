import { patch } from "@web/core/utils/patch";
import { DateTimeField } from "@web/views/fields/datetime/datetime_field";

/**
 * Date, datetime and date range widgets (form, list, kanban, also the
 * read-only value and the tooltip) always use the numeric format.
 * Subclasses (list widget, remaining days, ...) inherit this.
 */
patch(DateTimeField.prototype, {
    getFormattedValue(valueIndex) {
        return super.getFormattedValue(valueIndex, true);
    },
});
