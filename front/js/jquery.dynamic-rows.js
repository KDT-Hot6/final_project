/*
 * ssdDynamicRows jQuery plugin
 * Examples and documentation at: https://github.com/sebastiansulinski/dynamic-rows
 * Copyright (c) 2015 Sebastian Sulinski <info@ssdtutorials.com>
 * Version: 3.0.2 (23-DEC-2015)
 * Licensed under the MIT.
 * Requires: jQuery v1.9 or later
 */
(function ($) {

    $.fn.ssdDynamicRows = function (options) {

        "use strict";

        var settings = $.extend({

            event_type: 'click',

            hide_css_class: 'dn',
            row: '[data-ssd-dynamic-row]',

            button_add: '[data-ssd-dynamic-add]',
            button_remove: '[data-ssd-dynamic-remove]',

            other_elements: {},

            divider: '-',

            clear_warning: function (row) {}

        }, options);


        function preventStop(event) {

            "use strict";

            event.preventDefault();
            event.stopPropagation();

        }

        function removeButton(container, items) {

            "use strict";

            container.find(settings.button_remove)
                     .removeClass(settings.hide_css_class);

            if (items.length < 2) {

                items.last()
                     .find(settings.button_remove)
                     .addClass(settings.hide_css_class);

            }

        }

        function addButton(container, items) {

            "use strict";

            container.find(settings.button_add)
                     .addClass(settings.hide_css_class);

            items.last()
                 .find(settings.button_add)
                 .removeClass(settings.hide_css_class);

        }

        function buttons(container) {

            "use strict";

            var items = container.children(settings.row);

            removeButton(container, items);
            addButton(container, items);

        }

        function setUp(container) {

            "use strict";

            buttons(container);

        }



        function amendAttributes(row) {

            "use strict";

            var inputs = row.find(':input'),
                labels = row.find('label');

            $.each(inputs, function () {

                var id = $(this).prop('id').split(settings.divider),
                    new_index = (parseInt(id[1], 10) + 1),
                    new_id = id[0] + settings.divider + new_index;

                $(this).prop('name', new_id)
                       .prop('id', new_id)
                       .val('');

            });

            $.each(labels, function () {

                var attr_for = $(this).prop('for').split(settings.divider),
                    new_index = (parseInt(attr_for[1], 10) + 1),
                    new_attr_for = attr_for[0] + settings.divider + new_index;

                $(this).prop('for', new_attr_for);

            });

            $.each(settings.other_elements, function(obj, attr) {

                var other = row.find(obj);

                $.each(other, function() {

                    var old_attr = $(this).attr(attr).split(settings.divider),
                        new_index = (parseInt(old_attr[1], 10) + 1),
                        new_attr = old_attr[0] + settings.divider + new_index;

                    $(this).attr(attr, new_attr);

                });

            });

            settings.clear_warning(row);

            return row;

        }

        function cloneRow(row) {

            "use strict";

            return amendAttributes(row.closest(settings.row).clone());

        }

        function add(container) {

            "use strict";

            container.on(
                settings.event_type,
                settings.button_add,
                function (event) {

                    preventStop(event);

                    var row = $(this).closest(settings.row),
                        new_row = cloneRow(row);

                    container.append(new_row);

                    buttons(container);

                }
            );

        }

        function remove(container) {

            "use strict";

            container.on(
                settings.event_type,
                settings.button_remove,
                function (event) {

                    preventStop(event);

                    var row = $(this).closest(settings.row);

                    row.fadeOut(200, function () {

                        $(this).remove();

                        buttons(container);

                    });

                }
            );

        }

        return this.each(function () {

            "use strict";

            setUp($(this));
            add($(this));
            remove($(this));

        });


    }

})(window.jQuery);