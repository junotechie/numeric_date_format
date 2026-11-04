import { registry } from "@web/core/registry";
import { formatDate, formatDateTime } from "@web/views/fields/formatters";
import { numericOptions } from "../core/numeric_options";

/**
 * Formatters are used wherever a value is displayed without a field widget:
 * read-only list cells, group headers, kanban, calendar, pivot, ...
 */

export function formatDateNumeric(value, options = {}) {
    return formatDate(value, numericOptions(options));
}
formatDateNumeric.extractOptions = (fieldInfo) =>
    numericOptions(formatDate.extractOptions(fieldInfo));

export function formatDateTimeNumeric(value, options = {}) {
    // Some callers (e.g. dynamic placeholders) pass no options: use the same
    // defaults as datetime fields (time shown, seconds hidden).
    return formatDateTime(
        value,
        numericOptions({
            ...options,
            showTime: options.showTime ?? true,
            showSeconds: options.showSeconds ?? false,
        })
    );
}
formatDateTimeNumeric.extractOptions = (fieldInfo) =>
    numericOptions(formatDateTime.extractOptions(fieldInfo));

registry
    .category("formatters")
    .add("date", formatDateNumeric, { force: true })
    .add("datetime", formatDateTimeNumeric, { force: true });
