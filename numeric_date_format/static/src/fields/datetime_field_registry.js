import { registry } from "@web/core/registry";
import { withNumericViewOption } from "../core/numeric_options";

/**
 * The field definitions read the `numeric` view option to compute the
 * placeholder and the list column width. Wrap them so both match the numeric
 * format and dates are not cut off in list views.
 */
const FIELD_KEYS = [
    "date",
    "datetime",
    "daterange",
    "list.date",
    "list.datetime",
    "list.daterange",
];

const fieldsRegistry = registry.category("fields");

for (const key of FIELD_KEYS) {
    if (!fieldsRegistry.contains(key)) {
        continue;
    }
    const definition = fieldsRegistry.get(key);
    const { extractProps, listViewWidth } = definition;
    const numericDefinition = { ...definition };
    if (typeof extractProps === "function") {
        numericDefinition.extractProps = (fieldInfo, dynamicInfo) =>
            extractProps(withNumericViewOption(fieldInfo), dynamicInfo);
    }
    if (typeof listViewWidth === "function") {
        numericDefinition.listViewWidth = (fieldInfo) =>
            listViewWidth(withNumericViewOption(fieldInfo));
    }
    fieldsRegistry.add(key, numericDefinition, { force: true });
}
