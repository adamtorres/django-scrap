// TODO: cache responses?  seems fast at the moment.  Put cache on a later list.
var autocomplete_keypress_timer;
var autocomplete_url = "set from page as it likely uses django template tags.";
var autocomplete_fields = ["list", "of", "fields", "to", "include", "in", "dropdown"];
var autocomplete_display_field = "name of the field to use when clicking on a dropdown item";
var autocomplete_copy_values = {}; // dict of autocomplete_column:form_field pairs to copy when an item is selected.
var autocomplete_li_template_id = "id of li to use as a template";
var autocomplete_remove_decimal_fields = []
var autocomplete_container_id = "line_item_list";

$( document ).ready(function() {
    ac_no_results();
})
function ac_start_timer(caller) {
    window.clearTimeout(autocomplete_keypress_timer);
    autocomplete_keypress_timer = setTimeout(ac_timer_elapsed_func, 750, caller);
}
function ac_no_results() {
    $(".dropdown-menu").each(function() {
        $(this).empty();
        $(this).append($("<li><a class='dropdown-item disabled'>No results</a></li>"));
    });
}
function ac_new_dropdown_item(data) {
    var ac_li_template = $(`#${autocomplete_li_template_id}`);
    console.log(ac_li_template);
    var new_ac_li = ac_li_template.clone();
    new_ac_li.attr('id', null);
    $(new_ac_li.find('a')).attr("data-id", data['id']);
    new_ac_li.find('div').each(function() {
        var e = $(this);
        var key = e.attr('name');
        if (key === undefined){
            return true;
        }
        if (autocomplete_fields.includes(key)) {
            let v = data[key];
            if (autocomplete_remove_decimal_fields.includes(key)) {
                // The data from the server includes decimal places when not needed.  This seems to work to only show
                // decimal places when needed.
                v = Math.round(v * 100) / 100;
            }
            // TODO: need to get date_str.js into scrap and the media class.
            if (is_date_value(v) && is_date_field(key)){
                e.text(format_date_str(v));
            } else {
                e.text(v);
            }
        }
    });
    new_ac_li.removeClass("hidden");
    return new_ac_li;
}
function ac_timer_elapsed_func(caller_obj) {
    var caller = $(caller_obj);
    var t = ac_get_dropdown_textbox(caller);
    var text_value = t.val().trim();

    if (text_value === "") {
        // don't want to send empty requests.
        ac_no_results();
        return;
    }
    logit(`timer: ${t.prop('id')} send &quot;${text_value}&quot; to ${autocomplete_url}`);
    var jqxhr = $.ajax({
        url: autocomplete_url,
        type: "get",
        data: {
            terms: text_value,
            field: "cryptic_name",
        },
        caller_id: caller.prop('id'),
        terms: text_value
    })
    .done(function(data) {
        var d_caller = $(document.getElementById(this.caller_id));
        console.log(d_caller);
        var d_ddl = ac_get_dropdown_list(d_caller)
        d_ddl.empty();
        var count = 0;
        $.each(data, function(index){
            d_ddl.append(ac_new_dropdown_item(this));
            count++;
        });
        if (count === 0) {
            ac_no_results();
        }
        logit(`Got ${count} results for "${this.terms}".`)
        if (d_caller.find('.dropdown-menu').is(":hidden")){
            // logit("dropdown is hidden, toggling dropdown");
            // TODO: toggle doesn't work.
            // d_caller.dropdown('toggle');
        } else {
            logit("NOT toggling dropdown");
        }
    })
    .fail(function() {
        logit("ajax fail");
    })
    .always(function() {
        logit("ajax complete");
    });
}
function ac_get_dropdown_parent(e) {
    // Given any element within a dropdown tree, return the top-most element.
    return $(e).parents(".dropdown");
}
function ac_get_dropdown_div(p) {
    return p.children(".dropdown");
}
function ac_get_dropdown_textbox(p) {
    return p.children("input[type='text']");
}
function ac_get_dropdown_list(p) {
    return p.children(".dropdown-menu");
}
function ac_get_hidden_model_field(p) {
    id_text = p.prop("id");
    id_text = id_text.substring(0, id_text.length - "-dropdown".length);
    return $(document.getElementById(id_text));
}
function ac_get_autocomplete_field(e, field_name) {
    return e.find(`div[name="${field_name}"]`);
}
function ac_get_form_field(field_name){
    //field_name = id=id_items-0-unit_size, name=items-0-unit_size
}
function ac_get_form_prefix(p) {
    // "id_items-0-item-dropdown"
    // returns "id_items-0-"
    let id_text = p.prop("id");
    return id_text.substring(0, id_text.length - "item-dropdown".length);
}
function ac_get_form_field(p, form_prefix, form_field) {
    // return $(document.getElementById(`${form_prefix}${form_field}`));
    return $(`#${form_prefix}${form_field}`);
}
function autocomplete_setup_events() {
    $(`#${autocomplete_container_id}`).on("click", "button", function(e) {
        logit("Log of jquery events.", true);
    });
    $(`#${autocomplete_container_id}`).on("keypress", "input", function(e) {
        ac_start_timer(ac_get_dropdown_parent(this));
    })
    $(`#${autocomplete_container_id}`).on("keydown", "input", function(e) {
        switch (e.keyCode) {
            case 8: // Backspace
                ac_start_timer(ac_get_dropdown_parent(this));
                break;
            case 9: // Tab
            case 13: // Enter
            case 37: // Left
            case 38: // Up
            case 39: // Right
            case 40: // Down
                break;
            default:
                break;
        }
    });
    $(`#${autocomplete_container_id}`).on("focusout", "input", function() {
        window.clearTimeout(autocomplete_keypress_timer);
    })
    $(`#${autocomplete_container_id}`).on('click', 'a.dropdown-item', function() {
        // $( "div" ).data( "role" ) === "page";
        var e = $(this);
        var p = ac_get_dropdown_parent(e);
        var n = ac_get_autocomplete_field(e, autocomplete_display_field);
        var selected_item = n.text();
        var t = ac_get_dropdown_textbox(p);
        var h = ac_get_hidden_model_field(p);
        let form_prefix = ac_get_form_prefix(p);

        for (const [key, value] of Object.entries(autocomplete_copy_values)) {
            copy_field = ac_get_autocomplete_field(e, key);
            form_field = ac_get_form_field(p, form_prefix, value);
            form_field.val(copy_field.text());
        }
        logit(`clicked dropdown item: &quot;${selected_item}&quot; ${e.data("id")} and setting ${t.prop("id")} AND ${h.prop("id")}`);
        t.val(n.text());
        h.val(e.data("id"));
        // $("#jquery-example-2-text").val(n.text());
    })
    $(`#${autocomplete_container_id}`).on('show.bs.dropdown', 'div.dropdown', function () {
        // logit("show.bs.dropdown");
    })
    $(`#${autocomplete_container_id}`).on('shown.bs.dropdown', 'div.dropdown', function () {
        // logit("shown.bs.dropdown");
    })
    $(`#${autocomplete_container_id}`).on('hide.bs.dropdown', 'div.dropdown', function () {
        // logit("hide.bs.dropdown");
    })
    $(`#${autocomplete_container_id}`).on('hidden.bs.dropdown', 'div.dropdown', function () {
        // logit("hidden.bs.dropdown");
    })
}
