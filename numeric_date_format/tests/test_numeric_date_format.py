from datetime import datetime, time

from odoo import fields
from odoo.tests import HttpCase, tagged

# Polls the page until every element matching `selector` shows a value, then
# logs "test successful" if one of them starts with the expected numeric date
# and none of them contains a month name ("Nov 4").
CHECK_FIELD_JS = """
(async () => {
    const expected = %(expected)r;
    const readValue = (el) => {
        const input = el.matches("input") ? el : el.querySelector("input");
        return ((input ? input.value : el.textContent) || "").trim();
    };
    const deadline = Date.now() + 30000;
    let values = [];
    while (Date.now() < deadline) {
        values = [...document.querySelectorAll(%(selector)r)].map(readValue);
        if (values.length && values.every(Boolean)) {
            break;
        }
        await new Promise((resolve) => setTimeout(resolve, 200));
    }
    const ok = values.some((v) => v.startsWith(expected))
        && !values.some((v) => /[A-Za-z]{3}/.test(v));
    if (ok) {
        console.log("test successful");
    } else {
        const el = document.querySelector(%(selector)r);
        console.error(`%(label)s: expected "${expected}...", got ${JSON.stringify(values)}`
            + ` / html: ${el ? el.outerHTML.slice(0, 400) : "no element"}`);
    }
})();
"""

# Calls the "date" and "datetime" formatters directly, as list, kanban,
# calendar and pivot views do. Waits for the user's language settings first.
CHECK_FORMATTERS_JS = """
(async () => {
    const get = (name) => odoo.loader.modules.get(name);
    while (!get("@numeric_date_format/formatters/numeric_formatters")
            || !get("@web/core/l10n/translation")) {
        await new Promise((resolve) => setTimeout(resolve, 100));
    }
    await get("@web/core/l10n/translation").translationIsReady;
    const { registry } = get("@web/core/registry");
    const formatters = registry.category("formatters");
    const day = luxon.DateTime.local().set({ hour: 12, minute: 0, second: 0 });
    const date = formatters.get("date")(day);
    const datetime = formatters.get("datetime")(day);
    const expected = %(expected)r;
    if (date === expected && datetime.startsWith(expected)) {
        console.log("test successful");
    } else {
        console.error(`formatters: expected "${expected}", got "${date}" / "${datetime}"`);
    }
})();
"""

@tagged('post_install', '-at_install')
class TestNumericDateFormat(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lang = cls.env['res.lang']._lang_get(cls.env.ref('base.user_admin').lang or 'en_US')
        # Today, current year: standard Odoo 19 would show it as "Nov 4".
        cls.today = fields.Date.context_today(cls.env.ref('base.user_admin'))
        cls.expected = cls.today.strftime(cls.lang.date_format)
        # Noon, so the day stays the same in any user timezone. All crons, so
        # the first row of the list view has this value too.
        crons = cls.env['ir.cron'].search([])
        crons.nextcall = datetime.combine(cls.today, time(12, 0))
        cls.cron = crons[0]

    def test_formatters(self):
        self.browser_js(
            "/odoo",
            CHECK_FORMATTERS_JS % {'expected': self.expected},
            login='admin',
        )

    def test_form_datetime_field(self):
        self.browser_js(
            f"/odoo/action-base.ir_cron_act/{self.cron.id}",
            CHECK_FIELD_JS % {
                'expected': self.expected,
                'selector': '.o_form_view .o_field_widget[name="nextcall"]',
                'label': 'Form view',
            },
            login='admin',
        )

    def test_list_datetime_column(self):
        self.browser_js(
            "/odoo/action-base.ir_cron_act",
            CHECK_FIELD_JS % {
                'expected': self.expected,
                'selector': '.o_data_row td[name="nextcall"]',
                'label': 'List view',
            },
            login='admin',
        )
