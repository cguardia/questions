"""Defines constants to be used throughout the code."""

SURVEY_JS_VERSION = "1.8.2"

SURVEY_JS_CDN = f"https://surveyjs.azureedge.net/{SURVEY_JS_VERSION}"

SURVEY_JS_WIDGETS = "surveyjs-widgets.js"

SURVEY_JS_PLATFORMS = (
    "angular",
    "jquery",
    "knockout",
    "react",
    "vue",
)

SUGGESTED_JS_BY_PLATFORM = {
    "angular": [
        "https://npmcdn.com/zone.js",
        "https://npmcdn.com/core-js@2.6.5/client/shim.min.js",
        "https://npmcdn.com/rxjs@5.0.0-beta.6/bundles/Rx.umd.js",
        "https://npmcdn.com/@angular/core@2.0.0-rc.5/bundles/core.umd.js",
        "https://npmcdn.com/@angular/common@2.0.0-rc.5/bundles/common.umd.js",
        "https://npmcdn.com/@angular/compiler@2.0.0-rc.5/bundles/compiler.umd.js",
        "https://npmcdn.com/@angular/platform-browser@2.0.0-rc.5/bundles/platform-browser.umd.js",
        "https://npmcdn.com/@angular/platform-browser-dynamic@2.0.0-rc.5/bundles/platform-browser-dynamic.umd.js",
    ],
    "jquery": [
        "https://unpkg.com/jquery@3.5.1/dist/jquery.js",
    ],
    "knockout": [
        "https://cdnjs.cloudflare.com/ajax/libs/knockout/3.4.0/knockout-min.js",
    ],
    "react": [
        "https://cdnjs.cloudflare.com/ajax/libs/babel-polyfill/7.6.0/polyfill.js",
        "https://unpkg.com/react@15/dist/react.js",
        "https://unpkg.com/react-dom@15/dist/react-dom.js",
        "https://unpkg.com/@babel/standalone@7.2.5/babel.min.js",
    ],
    "vue": [
        "https://unpkg.com/vue/dist/vue.js",
    ],
}

BOOTSTRAP_URL = "https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css"

INCLUDE_KEYS = {
    "pages": {
        "__all__": {
            "name": ...,
            "questions": {
                "__all__": {
                    "accepted_types": ...,
                    "add_row_location": ...,
                    "add_row_text": ...,
                    "allow_add_panel": ...,
                    "allow_add_rows": ...,
                    "allow_remove_panel": ...,
                    "allow_remove_rows": ...,
                    "allow_clear": ...,
                    "allow_images_preview": ...,
                    "allow_multiple": ...,
                    "all_rows_required": ...,
                    "auto_close": ...,
                    "auto_unmask": ...,
                    "bg_emotion": ...,
                    "cells": ...,
                    "cell_type": ...,
                    "choices": ...,
                    "choices_by_url": ...,
                    "choices_enable_if": ...,
                    "choices_max": ...,
                    "choices_min": ...,
                    "choices_order": ...,
                    "choices_step": ...,
                    "choices_visible_if": ...,
                    "clear_button": ...,
                    "columns": ...,
                    "columns_visible_if": ...,
                    "column_col_count": ...,
                    "column_layout": ...,
                    "column_min_width": ...,
                    "cols": ...,
                    "col_count": ...,
                    "config": ...,
                    "confirm_delete": ...,
                    "confirm_delete_text": ...,
                    "content_mode": ...,
                    "correct_answer": ...,
                    "currency": ...,
                    "date_format": ...,
                    "days_of_week_highlighted": ...,
                    "default_row_value": ...,
                    "default_value": ...,
                    "default_value_from_last_panel": ...,
                    "default_value_from_last_row": ...,
                    "description": ...,
                    "description_location": ...,
                    "direction": ...,
                    "disable_touch_keyboard": ...,
                    "display_style": ...,
                    "elements": ...,
                    "emotion_color": ...,
                    "emotion_size": ...,
                    "emotions": ...,
                    "emotions_count": ...,
                    "empty_text": ...,
                    "enable_if": ...,
                    "end_date": ...,
                    "expression": ...,
                    "expression_format": ...,
                    "has_none": ...,
                    "has_other": ...,
                    "has_select_all": ...,
                    "height": ...,
                    "hide_if_choices_empty": ...,
                    "hide_number": ...,
                    "horizontal_scroll": ...,
                    "html": ...,
                    "image_fit": ...,
                    "image_height": ...,
                    "image_width": ...,
                    "indent": ...,
                    "inner_indent": ...,
                    "input_format": ...,
                    "input_mask": ...,
                    "input_type": ...,
                    "items": ...,
                    "item_size": ...,
                    "key_duplication_error": ...,
                    "key_name": ...,
                    "kind": ...,
                    "label_false": ...,
                    "label_true": ...,
                    "maximum_fraction_digits": ...,
                    "max_answers_count": ...,
                    "max_date": ...,
                    "max_length": ...,
                    "max_panel_count": ...,
                    "max_rate_description": ...,
                    "max_row_count": ...,
                    "max_size": ...,
                    "max_value": ...,
                    "max_width": ...,
                    "minimum_fraction_digits": ...,
                    "min_date": ...,
                    "min_panel_count": ...,
                    "min_rate_description": ...,
                    "min_row_count": ...,
                    "min_width": ...,
                    "min_value": ...,
                    "multi_select": ...,
                    "name": ...,
                    "need_confirm_remove_file": ...,
                    "none_text": ...,
                    "orientation": ...,
                    "options_caption": ...,
                    "other_text": ...,
                    "other_error_text": ...,
                    "other_place_holder": ...,
                    "panel_add_text": ...,
                    "panel_count": ...,
                    "panel_next_text": ...,
                    "panel_prev_text": ...,
                    "panel_remove_text": ...,
                    "panels_state": ...,
                    "pips_mode": ...,
                    "pips_density": ...,
                    "pips_text": ...,
                    "pips_values": ...,
                    "place_holder": ...,
                    "prefix": ...,
                    "question_start_index": ...,
                    "question_title_location": ...,
                    "range_max": ...,
                    "range_min": ...,
                    "rate_max": ...,
                    "rate_min": ...,
                    "rate_step": ...,
                    "rating_theme": ...,
                    "remove_row_text": ...,
                    "render_as": ...,
                    "render_mode": ...,
                    "required": ...,
                    "required_error_text": ...,
                    "required_if": ...,
                    "rows": ...,
                    "rows_order": ...,
                    "rows_visible_if": ...,
                    "row_count": ...,
                    "row_title_width": ...,
                    "select_all_text": ...,
                    "select2_config": ...,
                    "show_clear_button": ...,
                    "show_header": ...,
                    "show_label": ...,
                    "show_number": ...,
                    "show_options_caption": ...,
                    "show_preview": ...,
                    "show_question_numbers": ...,
                    "show_range_in_progress": ...,
                    "show_title": ...,
                    "show_values": ...,
                    "size": ...,
                    "start_date": ...,
                    "start_with_new_line": ...,
                    "state": ...,
                    "step": ...,
                    "store_data_as_text": ...,
                    "template_elements": ...,
                    "template_description": ...,
                    "template_title": ...,
                    "template_title_location": ...,
                    "text_update_mode": ...,
                    "title": ...,
                    "title_location": ...,
                    "today_highlight": ...,
                    "tooltips": ...,
                    "total_text": ...,
                    "use_display_values_in_title": ...,
                    "use_grouping": ...,
                    "validators": ...,
                    "value_false": ...,
                    "value_name": ...,
                    "value_true": ...,
                    "visible": ...,
                    "visible_if": ...,
                    "wait_for_upload": ...,
                    "week_start": ...,
                    "width": ...,
                }
            },
            "title": ...,
            "max_time_to_finish": ...,
            "navigation_buttons_visibility": ...,
            "question_title_location": ...,
            "questions_order": ...,
        }
    },
    "title": ...,
    "calculated_values": ...,
    "check_errors_mode": ...,
    "clear_invisible_values": ...,
    "completed_before_html": ...,
    "completed_html": ...,
    "completed_html_on_condition": ...,
    "complete_text": ...,
    "cookie_name": ...,
    "description": ...,
    "edit_text": ...,
    "first_page_is_started": ...,
    "focus_first_question_automatic": ...,
    "focus_on_first_error": ...,
    "go_next_page_automatic": ...,
    "loading_html": ...,
    "locale": ...,
    "logo": ...,
    "logo_fit": ...,
    "logo_height": ...,
    "logo_position": ...,
    "logo_width": ...,
    "max_others_length": ...,
    "max_text_length": ...,
    "max_time_to_finish": ...,
    "max_time_to_finish_page": ...,
    "mode": ...,
    "navigate_to_url": ...,
    "navigate_to_url_on_condition": ...,
    "page_next_text": ...,
    "page_prev_text": ...,
    "preview_text": ...,
    "progress_bar_type": ...,
    "questions_on_page_mode": ...,
    "questions_order": ...,
    "question_description_location": ...,
    "question_error_location": ...,
    "question_start_index": ...,
    "question_title_location": ...,
    "question_title_pattern": ...,
    "question_title_template": ...,
    "required_text": ...,
    "send_result_on_page_next": ...,
    "show_completed_page": ...,
    "show_navigation_buttons": ...,
    "show_page_numbers": ...,
    "show_page_titles": ...,
    "show_prev_button": ...,
    "show_preview_before_complete": ...,
    "show_progress_bar": ...,
    "show_question_numbers": ...,
    "show_timer_panel": ...,
    "show_timer_panel_mode": ...,
    "show_title": ...,
    "start_survey_text": ...,
    "store_others_as_comment": ...,
    "survey_id": ...,
    "survey_post_id": ...,
    "survey_show_data_saving": ...,
    "text_update_mode": ...,
    "triggers": ...,
}

TEXT_INPUT_TYPES = (
    "color",
    "date",
    "datetime",
    "datetime-local",
    "email",
    "month",
    "number",
    "password",
    "range",
    "tel",
    "text",
    "time",
    "url",
    "week",
)

LOCALES = (
    "ar",
    "bg",
    "ca",
    "cs",
    "da",
    "de",
    "en",
    "es",
    "et",
    "fa",
    "fi",
    "fr",
    "gr",
    "he",
    "hu",
    "id",
    "is",
    "it",
    "ja",
    "ka",
    "ko",
    "lt",
    "lv",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "ru",
    "sv",
    "sw",
    "tg",
    "th",
    "tr",
    "ua",
    "zh-cn",
    "zh-tw",
)

CHOICE_ORDER_VALUES = (
    "none",
    "asc",
    "desc",
    "random",
)

CHOICES_BY_URL_KEYS = (
    "path",
    "titleName",
    "url",
    "valueName",
)

IMAGE_FIT_VALUES = (
    "contain",
    "none",
    "cover",
    "fill",
)

IMAGE_CONTENT_MODE_VALUES = (
    "image",
    "video",
)

PANEL_RENDER_MODES = (
    "progressTop",
    "progressBottom",
)

DESCRIPTION_LOCATIONS = (
    "default",
    "underInput",
    "underTitle",
)

TITLE_LOCATIONS = (
    "default",
    "top",
    "bottom",
    "left",
    "hidden",
)

CHECK_ERRORS_MODES = (
    "onNextPage",
    "onValueCHanged",
    "onComplete",
)

TEXT_UPDATE_MODES = (
    "default",
    "onBlur",
    "onTyping",
)

EXPRESSION_DISPLAY_STYLES = (
    "none",
    "decimal",
    "currency",
    "percent",
    "date",
)

SHOW_QUESTION_NUMBERS_VALUES = (
    "default",
    "onpanel",
    "off",
)

PANEL_STATES = (
    "default",
    "collapsed",
    "expanded",
    "firstExpanded",
)

QUESTION_ORDER_VALUES = (
    "default",
    "initial",
    "random",
)

NAV_BUTTONS_VISIBILITY = (
    "inherit",
    "show",
    "hide",
)

NAV_BUTTONS_POSITIONS = (
    "none",
    "top",
    "bottom",
    "both",
)

CLEAR_INVISIBLE_VALUES = (
    "none",
    "onHidden",
    "onComplete",
)

LOGO_POSITIONS = (
    "none",
    "left",
    "right",
    "top",
    "bottom",
)

PROGRESS_BAR_TYPES = (
    "pages",
    "questions",
    "correctQuestions",
)

SURVEY_MODES = (
    "edit",
    "display",
)

QUESTION_DESCRIPTION_LOCATIONS = (
    "underTitle",
    "underInput",
)

QUESTION_ERROR_LOCATIONS = (
    "top",
    "bottom",
)

QUESTION_PAGE_MODES = (
    "standard",
    "singlePage",
    "questionPerPage",
)

PAGE_SHOW_QUESTION_NUMBERS_VALUES = (
    "on",
    "onpage",
    "off",
)

SHOW_PROGRESS_BAR_OPTIONS = (
    "off",
    "top",
    "bottom",
    "both",
)

SHOW_PREVIEW_VALUES = (
    "noPreview",
    "showAllQuestions",
    "showAnsweredQuestions",
)

SHOW_TIMER_VALUES = (
    "none",
    "top",
    "bottom",
)

SHOW_TIMER_MODES = (
    "page",
    "survey",
    "all",
)

SURVEY_TEXT_UPDATE_MODES = (
    "onBlur",
    "onTyping",
)

ROW_ORDER_VALUES = (
    "initial",
    "random",
)

MATRIX_CELL_TYPES = (
    "dropdown",
    "checkbox",
    "radiogroup",
    "text",
    "comment",
    "boolean",
    "expression",
    "rating",
)

MATRIX_COLUMN_LAYOUTS = (
    "horizontal",
    "vertical",
)

MATRIX_ROW_LOCATIONS = (
    "default",
    "top",
    "bottom",
    "topBottom",
)

SURVEY_JS_THEMES = (
    "default",
    "bootstrap",
    "orange",
    "darkblue",
    "darkrose",
    "stone",
    "winter",
    "winterstone",
    "modern",
)

BAR_RATING_THEMES = (
    "fontawesome-stars",
    "css-stars",
    "bars-pill",
    "bars-1to10",
    "bars-movie",
    "bars-reversed",
    "bars-horizontal",
    "fontawesome-stars-o",
)
