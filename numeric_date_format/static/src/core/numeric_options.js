/**
 * Odoo 19+ displays date fields in a short locale style ("Nov 4") unless the
 * field has options="{'numeric': True}". This module forces that option on,
 * so dates follow the language date format (e.g. 04/11/2026) as before Odoo 19.
 */

/**
 * Return a copy of formatter options with `numeric` forced on.
 *
 * @param {Object} [options]
 * @returns {Object}
 */
export function numericOptions(options = {}) {
    return { ...options, numeric: true };
}

/**
 * Return a copy of a field node info (`{ options, attrs, ... }`) whose view
 * options have `numeric` forced on.
 *
 * @param {Object} info
 * @returns {Object}
 */
export function withNumericViewOption(info) {
    return { ...info, options: numericOptions(info.options) };
}
